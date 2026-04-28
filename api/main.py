"""FastAPI application for __PLUGIN_NAME__.

The plugin BFF exposes resources at `/resources/...` paths. The Martha host's
plugin proxy forwards `/api/admin/plugins/__PLUGIN_NAME__/<path>` to this BFF
at `<path>` (with the prefix stripped). The plugin UI calls relative paths
via the host-provided `ctx.api` client.

Replace the demo `things` resource with your own. Then surface it in
`api/openapi_overrides.py` under `x-martha-plugin.resources` so the host's
manifest sync picks it up.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.openapi_overrides import apply_openapi_overrides
from api.routes.things import router as things_router

app = FastAPI(
    title="__PLUGIN_DISPLAY__",
    description="__PLUGIN_DESCRIPTION__",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(things_router)

apply_openapi_overrides(app)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
