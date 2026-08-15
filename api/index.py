"""Vercel entrypoint for Ascendant's authenticated FastMCP service."""

from ascendant.mcp_service import create_production_mcp_server, create_vercel_app


app = create_vercel_app(create_production_mcp_server())
