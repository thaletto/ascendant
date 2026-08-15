"""Public FastMCP behavior for hosted Ascendant records."""

from __future__ import annotations

import asyncio
import socket
import time
from contextlib import contextmanager
from threading import Thread
from typing import Any, Iterator, cast

from fastmcp import Client
import pytest
import uvicorn

from ascendant.mcp_service import (
    HostedRecordStore,
    HostedRecordError,
    _birth_input,
    create_mcp_server,
    create_vercel_app,
)


@contextmanager
def _serve_asgi(app: Any) -> Iterator[str]:
    """Run the same stateless FastMCP ASGI shape Vercel receives."""

    with socket.socket() as port_socket:
        port_socket.bind(("127.0.0.1", 0))
        _, port = port_socket.getsockname()
    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error")
    )
    thread = Thread(target=server.run, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 5
        while not server.started and time.monotonic() < deadline:
            time.sleep(0.01)
        if not server.started:
            raise RuntimeError("FastMCP ASGI server did not start")
        yield f"http://127.0.0.1:{port}"
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def test_birth_input_rejects_non_finite_coordinates() -> None:
    with pytest.raises(HostedRecordError, match="must be finite"):
        _birth_input("1990-01-01T12:00:00+05:30", float("nan"), 77.2090)


def test_data_tools_reject_a_request_without_an_account() -> None:
    async def exercise() -> None:
        server = create_mcp_server(store=HostedRecordStore.in_memory())
        async with Client(server) as client:
            result = await client.call_tool(
                "list_person_records", {}, raise_on_error=False
            )
            assert result.is_error

    asyncio.run(exercise())


def test_hosted_record_lifecycle_is_account_scoped() -> None:
    """An authenticated account can use only its own hosted evidence."""

    store = HostedRecordStore.in_memory()
    alice = create_mcp_server(store=store, account_id="alice")
    bob = create_mcp_server(store=store, account_id="bob")

    async def exercise(server_url: str) -> None:
        async with Client(f"{server_url}/api/mcp") as alice_client:
            resources = await alice_client.list_resources()
            assert any(
                str(resource.uri) == "skill://ascendant/career"
                for resource in resources
            )
            career_skill = await alice_client.read_resource(
                "skill://ascendant/career"
            )
            assert "Career" in cast(Any, career_skill[0]).text
            assert "## Reference: topic.md" in cast(Any, career_skill[0]).text
            init_skill = await alice_client.read_resource(
                "skill://ascendant/init-person"
            )
            init_text = cast(Any, init_skill[0]).text
            assert "create_person_record" in init_text
            assert "<path-to-init-person-skill>" not in init_text

            created = await alice_client.call_tool(
                "create_person_record",
                {
                    "display_label": "Me",
                    "dob": "1990-01-01T12:00:00+05:30",
                    "latitude": 28.6139,
                    "longitude": 77.2090,
                    "consent_attested": True,
                },
            )
            assert created.data is not None
            record_id = created.data["record_id"]
            revision_id = created.data["artifact_revision_id"]

            context = await alice_client.call_tool(
                "get_person_context", {"record_id": record_id}
            )
            assert context.data is not None
            assert context.data["record_id"] == record_id
            assert context.data["artifact_revision_id"] == revision_id
            assert (
                context.data["provenance"]["rule_pack"]
                == "parashari_raman_jaimini_v3"
            )

            recalculated = await alice_client.call_tool(
                "recalculate_person_record", {"record_id": record_id}
            )
            assert recalculated.data is not None
            assert recalculated.data["artifact_revision_id"] != revision_id
            original_context = await alice_client.call_tool(
                "get_person_context",
                {
                    "record_id": record_id,
                    "artifact_revision_id": revision_id,
                },
            )
            assert original_context.data is not None
            assert original_context.data["artifact_revision_id"] == revision_id

            partner = await alice_client.call_tool(
                "create_person_record",
                {
                    "display_label": "Partner",
                    "dob": "1991-02-01T12:00:00+05:30",
                    "latitude": 28.6139,
                    "longitude": 77.2090,
                    "consent_attested": True,
                },
            )
            assert partner.data is not None
            compatibility = await alice_client.call_tool(
                "get_relationship_context",
                {
                    "first_record_id": record_id,
                    "second_record_id": partner.data["record_id"],
                },
            )
            assert compatibility.data is not None
            assert compatibility.data["first"]["record_id"] == record_id
            assert (
                compatibility.data["second"]["record_id"]
                == partner.data["record_id"]
            )

            request = await alice_client.call_tool(
                "record_reading_request",
                {
                    "record_id": record_id,
                    "topic": "career",
                    "question": (
                        "What professional patterns should I reflect on?"
                    ),
                    "artifact_revision_id": revision_id,
                },
            )
            assert request.data is not None

            history = await alice_client.call_tool(
                "get_reading_history", {"record_id": record_id}
            )
            assert history.data is not None
            assert history.data["requests"][0]["question"] == (
                "What professional patterns should I reflect on?"
            )

        async with Client(bob) as bob_client:
            inaccessible = await bob_client.call_tool(
                "get_person_context",
                {"record_id": record_id},
                raise_on_error=False,
            )
            assert inaccessible.is_error

        async with Client(alice) as alice_client:
            deleted = await alice_client.call_tool(
                "delete_person_record", {"record_id": record_id}
            )
            assert deleted.data == {"record_id": record_id, "deleted": True}

            history = await alice_client.call_tool("get_reading_history", {})
            assert history.data == {"requests": []}

    with _serve_asgi(create_vercel_app(alice)) as server_url:
        asyncio.run(exercise(server_url))
