"""Hosted Ascendant records exposed through a compact FastMCP data layer."""

from __future__ import annotations

import json
from math import isfinite
import os
import sqlite3
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from functools import wraps
from pathlib import Path
from threading import RLock
from typing import Any, Literal, Protocol, cast
from uuid import uuid4

from fastapi import FastAPI
from fastmcp import FastMCP
from fastmcp.server.auth.providers.supabase import SupabaseProvider
from fastmcp.server.dependencies import get_access_token
from fastmcp.resources.types import TextResource
from mcp.types import ToolAnnotations

from ascendant import Ascendant
from ascendant.person_record import PersonRecordInput, PersonRecordStore


_SKILLS_ROOT = (
    Path(__file__).resolve().parents[1]
    / "plugins"
    / "agent"
    / "ascendant"
    / "skills"
)
_MAX_DISPLAY_LABEL_LENGTH = 120
_MAX_TOPIC_LENGTH = 80
_MAX_QUESTION_LENGTH = 4_000


class HostedRecordError(ValueError):
    """A hosted record request cannot be completed for the current account."""


class RecordStore(Protocol):
    """Persistence operations used by the MCP data tools."""

    def create_record(
        self,
        *,
        account_id: str,
        display_label: str,
        birth_input: dict[str, object],
        attested_at: str,
        artifacts: dict[str, object],
        provenance: dict[str, object],
    ) -> dict[str, object]: ...

    def list_records(self, *, account_id: str) -> list[dict[str, object]]: ...

    def get_context(
        self,
        *,
        account_id: str,
        record_id: str,
        artifact_revision_id: str | None = None,
    ) -> dict[str, object]: ...

    def add_revision(
        self,
        *,
        account_id: str,
        record_id: str,
        artifacts: dict[str, object],
        provenance: dict[str, object],
    ) -> dict[str, object]: ...

    def record_request(
        self,
        *,
        account_id: str,
        record_id: str,
        artifact_revision_id: str,
        topic: str,
        question: str,
        requested_moment: str | None,
    ) -> dict[str, object]: ...

    def history(
        self, *, account_id: str, record_id: str | None
    ) -> list[dict[str, object]]: ...

    def delete_record(self, *, account_id: str, record_id: str) -> bool: ...


@dataclass(frozen=True)
class _SqlDialect:
    placeholder: str

    def placeholders(self, count: int) -> str:
        return ", ".join([self.placeholder] * count)


def _serialized(operation: Callable[..., Any]) -> Callable[..., Any]:
    """Serialize use of the synchronous per-instance database connection."""

    @wraps(operation)
    def wrapped(store: Any, *args: object, **kwargs: object) -> Any:
        with store._lock:
            return operation(store, *args, **kwargs)

    return wrapped


class HostedRecordStore:
    """SQL persistence shared by test SQLite and production Neon Postgres."""

    _dialect: _SqlDialect

    def __init__(self, connection: Any, *, placeholder: str) -> None:
        self._connection = connection
        self._lock = RLock()
        self._dialect = _SqlDialect(placeholder=placeholder)
        self._initialize_schema()

    @classmethod
    def in_memory(cls) -> HostedRecordStore:
        """Create an isolated SQL store for the public MCP integration seam."""

        # FastMCP invokes synchronous tools in a worker thread. The test store
        # is deliberately configured for that transport boundary.
        connection = sqlite3.connect(":memory:", check_same_thread=False)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return cls(connection, placeholder="?")

    def _initialize_schema(self) -> None:
        statements = (
            """
            CREATE TABLE IF NOT EXISTS hosted_person_records (
                record_id TEXT PRIMARY KEY,
                account_id TEXT NOT NULL,
                display_label TEXT NOT NULL,
                birth_input TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS consent_attestations (
                record_id TEXT PRIMARY KEY
                    REFERENCES hosted_person_records(record_id)
                    ON DELETE CASCADE,
                account_id TEXT NOT NULL,
                attested_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS artifact_revisions (
                artifact_revision_id TEXT PRIMARY KEY,
                record_id TEXT NOT NULL
                    REFERENCES hosted_person_records(record_id)
                    ON DELETE CASCADE,
                rule_pack TEXT NOT NULL,
                schema_version INTEGER NOT NULL,
                provenance TEXT NOT NULL,
                artifacts TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS reading_requests (
                reading_request_id TEXT PRIMARY KEY,
                record_id TEXT NOT NULL
                    REFERENCES hosted_person_records(record_id)
                    ON DELETE CASCADE,
                artifact_revision_id TEXT NOT NULL
                    REFERENCES artifact_revisions(artifact_revision_id)
                    ON DELETE CASCADE,
                account_id TEXT NOT NULL,
                topic TEXT NOT NULL,
                question TEXT NOT NULL,
                requested_moment TEXT,
                created_at TEXT NOT NULL
            )
            """,
        )
        cursor = self._connection.cursor()
        try:
            for statement in statements:
                cursor.execute(statement)
            self._connection.commit()
        finally:
            cursor.close()

    def _execute(
        self, statement: str, values: tuple[object, ...] = ()
    ) -> Any:
        cursor = self._connection.cursor()
        cursor.execute(statement, values)
        return cursor

    @_serialized
    def create_record(
        self,
        *,
        account_id: str,
        display_label: str,
        birth_input: dict[str, object],
        attested_at: str,
        artifacts: dict[str, object],
        provenance: dict[str, object],
    ) -> dict[str, object]:
        record_id = str(uuid4())
        revision_id = str(uuid4())
        created_at = _now()
        try:
            cursor = self._execute(
                "INSERT INTO hosted_person_records "
                "(record_id, account_id, display_label, birth_input, "
                "created_at) "
                f"VALUES ({self._dialect.placeholders(5)})",
                (
                    record_id,
                    account_id,
                    display_label,
                    _json(birth_input),
                    created_at,
                ),
            )
            cursor.close()
            cursor = self._execute(
                "INSERT INTO consent_attestations "
                "(record_id, account_id, attested_at) "
                f"VALUES ({self._dialect.placeholders(3)})",
                (record_id, account_id, attested_at),
            )
            cursor.close()
            cursor = self._execute(
                "INSERT INTO artifact_revisions "
                "(artifact_revision_id, record_id, rule_pack, schema_version, "
                "provenance, artifacts, created_at) "
                f"VALUES ({self._dialect.placeholders(7)})",
                (
                    revision_id,
                    record_id,
                    _string(provenance, "rule_pack"),
                    _integer(provenance, "schema_version"),
                    _json(provenance),
                    _json(artifacts),
                    created_at,
                ),
            )
            cursor.close()
            self._connection.commit()
        except Exception:
            self._connection.rollback()
            raise
        return {
            "record_id": record_id,
            "display_label": display_label,
            "artifact_revision_id": revision_id,
        }

    @_serialized
    def list_records(self, *, account_id: str) -> list[dict[str, object]]:
        cursor = self._execute(
            "SELECT record_id, display_label, created_at "
            "FROM hosted_person_records WHERE account_id = "
            f"{self._dialect.placeholder} ORDER BY created_at",
            (account_id,),
        )
        try:
            return [_row(record) for record in cursor.fetchall()]
        finally:
            cursor.close()

    @_serialized
    def get_context(
        self,
        *,
        account_id: str,
        record_id: str,
        artifact_revision_id: str | None = None,
    ) -> dict[str, object]:
        revision_filter = ""
        parameters: tuple[object, ...] = (record_id, account_id)
        if artifact_revision_id is not None:
            revision_filter = (
                " AND r.artifact_revision_id = " + self._dialect.placeholder
            )
            parameters += (artifact_revision_id,)
        statement = (
            "SELECT p.record_id, p.display_label, p.birth_input, "
            "r.artifact_revision_id, r.provenance, r.artifacts "
            "FROM hosted_person_records p "
            "JOIN artifact_revisions r ON r.record_id = p.record_id "
            "WHERE p.record_id = "
            f"{self._dialect.placeholder} AND p.account_id = "
            f"{self._dialect.placeholder} "
            + revision_filter
            + " ORDER BY r.created_at DESC LIMIT 1"
        )
        cursor = self._execute(statement, parameters)
        try:
            record = cursor.fetchone()
        finally:
            cursor.close()
        if record is None:
            raise HostedRecordError("Hosted person record was not found")
        values = _row(record)
        return {
            "record_id": values["record_id"],
            "display_label": values["display_label"],
            "birth_input": _parse_json(values["birth_input"]),
            "artifact_revision_id": values["artifact_revision_id"],
            "provenance": _parse_json(values["provenance"]),
            "artifacts": _parse_json(values["artifacts"]),
        }

    @_serialized
    def add_revision(
        self,
        *,
        account_id: str,
        record_id: str,
        artifacts: dict[str, object],
        provenance: dict[str, object],
    ) -> dict[str, object]:
        self.get_context(account_id=account_id, record_id=record_id)
        revision_id = str(uuid4())
        created_at = _now()
        cursor = self._execute(
            "INSERT INTO artifact_revisions "
            "(artifact_revision_id, record_id, rule_pack, schema_version, "
            "provenance, artifacts, created_at) "
            f"VALUES ({self._dialect.placeholders(7)})",
            (
                revision_id,
                record_id,
                _string(provenance, "rule_pack"),
                _integer(provenance, "schema_version"),
                _json(provenance),
                _json(artifacts),
                created_at,
            ),
        )
        cursor.close()
        self._connection.commit()
        return {"record_id": record_id, "artifact_revision_id": revision_id}

    @_serialized
    def record_request(
        self,
        *,
        account_id: str,
        record_id: str,
        artifact_revision_id: str,
        topic: str,
        question: str,
        requested_moment: str | None,
    ) -> dict[str, object]:
        self._require_revision(
            account_id=account_id,
            record_id=record_id,
            artifact_revision_id=artifact_revision_id,
        )
        request_id = str(uuid4())
        created_at = _now()
        cursor = self._execute(
            "INSERT INTO reading_requests "
            "(reading_request_id, record_id, artifact_revision_id, "
            "account_id, "
            "topic, question, requested_moment, created_at) "
            f"VALUES ({self._dialect.placeholders(8)})",
            (
                request_id,
                record_id,
                artifact_revision_id,
                account_id,
                topic,
                question,
                requested_moment,
                created_at,
            ),
        )
        cursor.close()
        self._connection.commit()
        return {"reading_request_id": request_id, "created_at": created_at}

    @_serialized
    def history(
        self, *, account_id: str, record_id: str | None
    ) -> list[dict[str, object]]:
        filters = ["account_id = " + self._dialect.placeholder]
        values: list[object] = [account_id]
        if record_id is not None:
            filters.append("record_id = " + self._dialect.placeholder)
            values.append(record_id)
        cursor = self._execute(
            "SELECT reading_request_id, record_id, artifact_revision_id, "
            "topic, question, requested_moment, created_at "
            "FROM reading_requests WHERE "
            + " AND ".join(filters)
            + " ORDER BY created_at DESC",
            tuple(values),
        )
        try:
            return [_row(request) for request in cursor.fetchall()]
        finally:
            cursor.close()

    @_serialized
    def delete_record(self, *, account_id: str, record_id: str) -> bool:
        cursor = self._execute(
            "DELETE FROM hosted_person_records WHERE record_id = "
            f"{self._dialect.placeholder} AND account_id = "
            f"{self._dialect.placeholder}",
            (record_id, account_id),
        )
        try:
            deleted = cursor.rowcount == 1
        finally:
            cursor.close()
        self._connection.commit()
        if not deleted:
            raise HostedRecordError("Hosted person record was not found")
        return True

    def _require_revision(
        self,
        *,
        account_id: str,
        record_id: str,
        artifact_revision_id: str,
    ) -> None:
        cursor = self._execute(
            "SELECT 1 FROM hosted_person_records p "
            "JOIN artifact_revisions r ON r.record_id = p.record_id "
            "WHERE p.record_id = "
            f"{self._dialect.placeholder} AND p.account_id = "
            f"{self._dialect.placeholder} AND r.artifact_revision_id = "
            f"{self._dialect.placeholder}",
            (record_id, account_id, artifact_revision_id),
        )
        try:
            exists = cursor.fetchone() is not None
        finally:
            cursor.close()
        if not exists:
            raise HostedRecordError(
                "Evidence bundle was not found for this account"
            )


class NeonHostedRecordStore(HostedRecordStore):
    """Neon PostgreSQL implementation for the deployed service."""

    def __init__(self, connection_string: str) -> None:
        import psycopg
        from psycopg.rows import dict_row

        connection = cast(
            Any,
            psycopg.connect(
                connection_string, row_factory=cast(Any, dict_row)
            ),
        )
        super().__init__(connection, placeholder="%s")


def create_mcp_server(
    *,
    store: RecordStore,
    account_id: str | None = None,
    auth: object | None = None,
) -> FastMCP:
    """Create the compact account-scoped MCP server.

    ``account_id`` is intentionally available only for isolated tests.
    Production resolves the account from a FastMCP-validated OAuth token.
    """

    mcp = FastMCP("Ascendant", auth=cast(Any, auth))

    def current_account() -> str:
        if account_id is not None:
            return account_id
        token = get_access_token()
        subject = token.claims.get("sub") if token is not None else None
        if not isinstance(subject, str) or not subject:
            raise HostedRecordError(
                "An authenticated Ascendant account is required"
            )
        return subject

    @mcp.tool(
        annotations=ToolAnnotations(
            destructiveHint=False,
            idempotentHint=False,
            openWorldHint=False,
        )
    )
    def create_person_record(
        display_label: str,
        dob: str,
        latitude: float,
        longitude: float,
        consent_attested: bool,
    ) -> dict[str, object]:
        """Create a consent-attested hosted record and evidence bundle."""

        if not display_label.strip():
            raise HostedRecordError("display_label must not be empty")
        if len(display_label) > _MAX_DISPLAY_LABEL_LENGTH:
            raise HostedRecordError("display_label is too long")
        if not consent_attested:
            raise HostedRecordError("consent_attested must be true")
        birth_input = _birth_input(dob, latitude, longitude)
        artifacts, provenance = _calculate_artifacts(birth_input)
        return store.create_record(
            account_id=current_account(),
            display_label=display_label.strip(),
            birth_input=birth_input,
            attested_at=_now(),
            artifacts=artifacts,
            provenance=provenance,
        )

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def list_person_records() -> dict[str, object]:
        """List the authenticated account's hosted person records."""

        return {"records": store.list_records(account_id=current_account())}

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def get_person_context(
        record_id: str,
        artifact_revision_id: str | None = None,
        moment: str | None = None,
    ) -> dict[str, object]:
        """Retrieve a selected record's versioned natal/transit evidence."""

        context = store.get_context(
            account_id=current_account(),
            record_id=record_id,
            artifact_revision_id=artifact_revision_id,
        )
        birth_input = cast(dict[str, object], context.pop("birth_input"))
        if moment is not None:
            context["transit"] = _calculate_transit(birth_input, moment)
        return context

    @mcp.tool(
        annotations=ToolAnnotations(
            destructiveHint=False,
            idempotentHint=False,
            openWorldHint=False,
        )
    )
    def recalculate_person_record(record_id: str) -> dict[str, object]:
        """Recalculate a record and retain its previous evidence revisions."""

        account = current_account()
        context = store.get_context(account_id=account, record_id=record_id)
        birth_input = cast(dict[str, object], context["birth_input"])
        artifacts, provenance = _calculate_artifacts(birth_input)
        return store.add_revision(
            account_id=account,
            record_id=record_id,
            artifacts=artifacts,
            provenance=provenance,
        )

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def get_relationship_context(
        first_record_id: str, second_record_id: str
    ) -> dict[str, object]:
        """Retrieve two authorized evidence bundles for a relationship skill.

        This is intentionally a data-only tool: the relationship-compatibility
        skill supplies the reading methodology and consent-aware instructions.
        """

        account = current_account()
        first = store.get_context(
            account_id=account, record_id=first_record_id
        )
        second = store.get_context(
            account_id=account, record_id=second_record_id
        )
        first.pop("birth_input")
        second.pop("birth_input")
        return {"first": first, "second": second}

    @mcp.tool(
        annotations=ToolAnnotations(
            destructiveHint=False,
            idempotentHint=False,
            openWorldHint=False,
        )
    )
    def record_reading_request(
        record_id: str,
        artifact_revision_id: str,
        topic: str,
        question: str,
        requested_moment: str | None = None,
    ) -> dict[str, object]:
        """Save a tool-level question and its exact Reading evidence bundle."""

        if not topic.strip() or not question.strip():
            raise HostedRecordError("topic and question must not be empty")
        if (
            len(topic) > _MAX_TOPIC_LENGTH
            or len(question) > _MAX_QUESTION_LENGTH
        ):
            raise HostedRecordError("topic or question is too long")
        if requested_moment is not None:
            _ = _parse_moment(requested_moment)
        return store.record_request(
            account_id=current_account(),
            record_id=record_id,
            artifact_revision_id=artifact_revision_id,
            topic=topic.strip(),
            question=question.strip(),
            requested_moment=requested_moment,
        )

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def get_reading_history(
        record_id: str | None = None,
    ) -> dict[str, object]:
        """Retrieve tool-level Reading requests, not a ChatGPT transcript."""

        return {
            "requests": store.history(
                account_id=current_account(), record_id=record_id
            )
        }

    @mcp.tool(
        annotations=ToolAnnotations(
            destructiveHint=True,
            idempotentHint=False,
            openWorldHint=False,
        )
    )
    def delete_person_record(record_id: str) -> dict[str, object]:
        """Delete a record and cascade evidence, attestation, and history."""

        _ = store.delete_record(
            account_id=current_account(), record_id=record_id
        )
        return {"record_id": record_id, "deleted": True}

    _register_skill_resources(mcp)
    return mcp


def create_production_mcp_server() -> FastMCP:
    """Build the Vercel server from the required Neon and Supabase settings."""

    database_url = os.environ.get("NEON_DATABASE_URL") or os.environ.get(
        "POSTGRES_URL"
    )
    if not database_url:
        raise RuntimeError("NEON_DATABASE_URL or POSTGRES_URL is required")
    project_url = os.environ.get("SUPABASE_PROJECT_URL")
    base_url = os.environ.get("BASE_URL")
    if not project_url or not base_url:
        raise RuntimeError("SUPABASE_PROJECT_URL and BASE_URL are required")
    auth = SupabaseProvider(
        project_url=project_url,
        base_url=base_url,
        algorithm=cast(
            Literal["RS256", "ES256"],
            os.environ.get("SUPABASE_JWT_ALGORITHM", "ES256"),
        ),
    )
    return create_mcp_server(
        store=NeonHostedRecordStore(database_url), auth=auth
    )


def create_vercel_app(mcp: FastMCP) -> FastAPI:
    """Wrap the MCP ASGI app with Vercel's `/api` path and lifespan."""

    mcp_app = mcp.http_app(stateless_http=True)
    app = FastAPI(title="Ascendant MCP", lifespan=mcp_app.lifespan)
    app.mount("/api", mcp_app)
    return app


def _register_skill_resources(mcp: FastMCP) -> None:
    for skill_path in sorted(_SKILLS_ROOT.glob("*/SKILL.md")):
        skill_name = skill_path.parent.name
        mcp.add_resource(
            TextResource(
                uri=cast(Any, f"skill://ascendant/{skill_name}"),
                name=f"Ascendant {skill_name} skill",
                description=(
                    "Read-only self-contained Ascendant topic instruction."
                ),
                text=_skill_resource_text(skill_path),
            )
        )


def _skill_resource_text(skill_path: Path) -> str:
    """Publish a skill with the references its relative links require."""

    skill_root = skill_path.parent
    plugin_agent = _SKILLS_ROOT.parent / "AGENTS.md"
    sections = [
        "# Hosted MCP data workflow\n\n"
        "The instruction files below are self-contained in this resource. "
        "Do not use relative filesystem paths, local `persons/` records, or "
        "local scripts. Retrieve owned evidence with Ascendant data tools, "
        "and use `get_relationship_context` only when both owned records are "
        "required.\n",
        "# Skill\n\n" + _hosted_skill_text(skill_path),
    ]
    if plugin_agent.exists():
        sections.append(
            "# Plugin instructions\n\n"
            + plugin_agent.read_text(encoding="utf-8")
        )
    for reference in sorted((skill_root / "references").glob("*.md")):
        sections.append(
            f"## Reference: {reference.name}\n\n"
            + reference.read_text(encoding="utf-8")
        )
    return "\n\n".join(sections)


def _hosted_skill_text(skill_path: Path) -> str:
    """Replace local-record commands in the two data skills for MCP clients."""

    name = skill_path.parent.name
    if name == "init-person":
        return """# Save birth details

Use `create_person_record` to create a consent-attested hosted record. Pass a
human-readable `display_label`, timezone-aware ISO 8601 `dob`, latitude,
longitude, and `consent_attested=true`. The result contains a record ID and
immutable evidence revision ID. Use `get_person_context` for the resulting
evidence; use `list_person_records` to select another record. All records are
scoped to the authenticated account and no local `persons/` directory exists.
"""
    if name == "get-transit":
        return """# Current planetary positions

Use `list_person_records` to select an owned record, then call
`get_person_context` with its `record_id` and an optional timezone-aware
`moment`. The returned `transit` is dated D1 evidence alongside the stored
natal evidence. This data tool supplies positions only; apply the matching
specialist skill to interpret them.
"""
    return skill_path.read_text(encoding="utf-8")


def _birth_input(
    dob: str, latitude: float, longitude: float
) -> dict[str, object]:
    birth_moment = _parse_moment(dob)
    if not isfinite(latitude) or not isfinite(longitude):
        raise HostedRecordError("latitude and longitude must be finite")
    if not -90 <= latitude <= 90:
        raise HostedRecordError("latitude must be between -90 and 90")
    if not -180 <= longitude <= 180:
        raise HostedRecordError("longitude must be between -180 and 180")
    return {
        "dob": birth_moment.isoformat(),
        "latitude": latitude,
        "longitude": longitude,
    }


def _calculate_artifacts(
    birth_input: dict[str, object],
) -> tuple[dict[str, object], dict[str, object]]:
    with tempfile.TemporaryDirectory(prefix="ascendant-mcp-") as directory:
        person = PersonRecordInput(
            name="person",
            dob=_parse_moment(_string(birth_input, "dob")),
            latitude=_number(birth_input, "latitude"),
            longitude=_number(birth_input, "longitude"),
        )
        record_store = PersonRecordStore(Path(directory) / "persons")
        record = record_store.initialize(person)
        artifacts = {
            str(path.relative_to(record.directory)): json.loads(
                path.read_text(encoding="utf-8")
            )
            for path in sorted(record.directory.rglob("*.json"))
        }
        provenance = cast(
            dict[str, object], artifacts["provenance.json"]
        )
        return artifacts, provenance


def _calculate_transit(
    birth_input: dict[str, object], moment: str
) -> dict[str, object]:
    target = _parse_moment(moment)
    offset = target.utcoffset()
    if offset is None:
        raise HostedRecordError("moment must be timezone-aware")
    total_minutes = int(offset.total_seconds() // 60)
    hours, minutes = divmod(abs(total_minutes), 60)
    utc = f"{'+' if total_minutes >= 0 else '-'}{hours:02}:{minutes:02}"
    chart = Ascendant(
        year=target.year,
        month=target.month,
        day=target.day,
        hour=target.hour,
        minute=target.minute,
        second=target.second,
        latitude=_number(birth_input, "latitude"),
        longitude=_number(birth_input, "longitude"),
        utc=utc,
    ).get_chart(1)
    return {"moment": target.isoformat(), "chart": chart}


def _parse_moment(value: str) -> datetime:
    try:
        moment = datetime.fromisoformat(value)
    except ValueError as error:
        raise HostedRecordError(f"Invalid ISO 8601 moment: {value}") from error
    if moment.tzinfo is None or moment.utcoffset() is None:
        raise HostedRecordError("moment must be timezone-aware")
    return moment


def _row(value: object) -> dict[str, object]:
    return dict(cast(Any, value))


def _json(value: object) -> str:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


def _parse_json(value: object) -> object:
    if not isinstance(value, str):
        raise HostedRecordError("Stored JSON value is invalid")
    return json.loads(value)


def _string(value: dict[str, object], key: str) -> str:
    result = value.get(key)
    if not isinstance(result, str):
        raise HostedRecordError(f"Missing string field: {key}")
    return result


def _integer(value: dict[str, object], key: str) -> int:
    result = value.get(key)
    if not isinstance(result, int):
        raise HostedRecordError(f"Missing integer field: {key}")
    return result


def _number(value: dict[str, object], key: str) -> float:
    result = value.get(key)
    if not isinstance(result, (int, float)):
        raise HostedRecordError(f"Missing numeric field: {key}")
    return float(result)


def _now() -> str:
    return datetime.now(UTC).isoformat()
