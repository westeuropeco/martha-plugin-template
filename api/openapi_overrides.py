"""OpenAPI schema customization with Martha plugin manifest extensions.

The Martha host reads two top-level OpenAPI extensions from the plugin BFF
to register the integration in its sidebar and route URLs to the plugin UI:

- `x-martha-integration` — display metadata (name, icon, color)
- `x-martha-plugin` — runtime metadata (resource paths)

`integration.name` is what users see in the integrations list. `plugin.name`
(set implicitly by the host's manifest sync via the OpenAPI title slug-mapping
on its end, OR explicitly here if you need it) is the BFF segment in
`/api/admin/plugins/<plugin.name>/...`. Keep them aligned with the
package.json name `@westeuropeco/__PLUGIN_SLUG__-ui` and the host's
`discover.ts` registry key (`__PLUGIN_SLUG__`).
"""

from fastapi import FastAPI


def apply_openapi_overrides(app: FastAPI) -> None:
    """Attach Martha plugin metadata to the OpenAPI schema."""
    original_openapi = app.openapi

    def custom_openapi() -> dict:
        if app.openapi_schema:
            return app.openapi_schema

        schema = original_openapi()

        schema["x-martha-integration"] = {
            "type": "plugin",
            "name": "__PLUGIN_DISPLAY__",
            "icon": "__PLUGIN_ICON__",
            "color": "__PLUGIN_COLOR__",
        }
        schema["x-martha-plugin"] = {
            "name": "__PLUGIN_NAME__",
            "resources": [
                {
                    "name": "things",
                    "path": "/things",
                },
            ],
        }

        app.openapi_schema = schema
        return schema

    app.openapi = custom_openapi
