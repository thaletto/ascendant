# Deploy the Ascendant MCP server

The remote MCP endpoint is the FastMCP ASGI application at `/api/mcp`. It is
stateless: Neon PostgreSQL holds all hosted records, evidence revisions,
consent attestations, and tool-level reading requests.

## Vercel

1. Import this repository into Vercel with the repository root as the project
   root. Vercel detects the FastAPI `app` exported by `api/index.py`.
2. Set these Production and Preview environment variables:

   ```text
   NEON_DATABASE_URL=postgresql://...
   SUPABASE_PROJECT_URL=https://<project-ref>.supabase.co
   BASE_URL=https://<your-vercel-domain>/api
   SUPABASE_JWT_ALGORITHM=ES256
   ```

   `POSTGRES_URL` is accepted as an alternative to `NEON_DATABASE_URL`.
   `BASE_URL` must include `/api`, because that is the public base path of the
   FastMCP application on Vercel.
3. Deploy a preview with `vercel deploy`, then use its endpoint at
   `https://<preview-domain>/api/mcp`. Promote only after the authenticated
   checks below pass.

The server dependencies are production dependencies in `pyproject.toml`, so
Vercel installs them directly from that file.

## Supabase Auth

Enable the Supabase OAuth Server and Dynamic Client Registration. Configure its
site URL for the production domain and its authorization path as
`/oauth/consent`, then use the same public `/api` URL in `BASE_URL`. The
committed Vercel rewrites expose the root OAuth discovery URLs while the MCP
ASGI application remains at `/api/mcp`.

Supabase delegates the OAuth consent callback to the application. ChatGPT
provides the conversation UI, but it cannot replace this protocol-mandated
browser approval step. Before inviting pilot users, host a minimal consent
callback that completes Supabase's `approveAuthorization()` or
`denyAuthorization()` flow; FastMCP's `SupabaseProvider` validates the returned
tokens and maps their `sub` claim to the account scope used by every data tool.

## ChatGPT connector

In ChatGPT Developer Mode, create a connector with:

```text
Server URL: https://<production-domain>/api/mcp
Authentication: OAuth
```

Use the native ChatGPT conversation interface. The server exposes read-only
Ascendant skills as resources and keeps writes limited to consent-attested
record creation, recalculation, tool-level Reading history, and deletion.

## Production smoke test

With a pilot account, verify that the connector can list and read a skill,
create a record, retrieve its current and prior evidence revisions, save a
Reading request, retrieve history, and delete the record. Then repeat an
evidence request from a different account and confirm it is rejected.
