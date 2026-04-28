# martha-plugin-template

Reference template for [Martha](https://github.com/westeuropeco/martha) plugins. Combines a FastAPI BFF (mounted by the host's plugin proxy at `/api/admin/plugins/<plugin-name>/...`) with a Svelte component library (mounted by the host's catch-all router at `/plugins/<slug>/...`).

This is the repo behind [`@westeuropeco/create-martha-plugin`](https://github.com/westeuropeco/create-martha-plugin). Most authors will scaffold via the wrapper rather than cloning this directly:

```bash
npm create @westeuropeco/martha-plugin my-plugin
```

If you want to clone manually, see "Manual scaffold" below.

## What you get

```
my-plugin/
├── README.md
├── Dockerfile                       # Python 3.13 image, runs uvicorn
├── docker-compose.yml               # one-service stack on port 8099
├── requirements.txt                 # fastapi + uvicorn + pydantic + pytest
├── pytest.ini
├── api/
│   ├── main.py                      # FastAPI app, /health + /things
│   ├── openapi_overrides.py         # x-martha-integration + x-martha-plugin
│   └── routes/
│       └── things.py                # demo CRUD resource (in-memory)
├── tests/
│   └── test_health.py
├── .github/workflows/
│   └── publish-ui.yml               # tag {slug}-ui-v* → GHCR npm
└── ui/
    ├── .npmrc                       # @westeuropeco scope → GHCR
    ├── package.json                 # @westeuropeco/{slug}-ui
    ├── tsconfig.json
    └── src/
        ├── index.ts                 # defineRoutes([Home, Detail])
        ├── api.ts                   # plugin-scoped API client (ctx.api wrapper)
        ├── types.ts
        └── pages/
            ├── Home.svelte          # path: ""
            └── Detail.svelte        # path: ":id"
```

The BFF is intentionally minimal — no DB, no Alembic, no auth. Add what you need; `martha-scoring` is a good DB-backed reference if you want SQLAlchemy + Alembic + version history.

## Manual scaffold (no npm-create)

The template uses placeholder tokens that the wrapper substitutes. To scaffold by hand, clone and run a single sed pass:

```bash
git clone --depth=1 https://github.com/westeuropeco/martha-plugin-template.git my-plugin
cd my-plugin
rm -rf .git && git init

# Pick values for your plugin
SLUG="inventory"                    # URL segment, package suffix
NAME="martha-${SLUG}"               # manifest name, BFF prefix
DISPLAY="Inventory Sync"            # display name in integrations list
ICON="package"                      # Phosphor icon name
COLOR="#10b981"                     # brand color hex
DESCRIPTION="Sync inventory to upstream system"

# Replace tokens across all files (skip node_modules / .git)
find . -type f \
  ! -path './.git/*' \
  ! -path './node_modules/*' \
  ! -path './ui/node_modules/*' \
  -exec sed -i.bak \
    -e "s|__PLUGIN_SLUG__|${SLUG}|g" \
    -e "s|__PLUGIN_NAME__|${NAME}|g" \
    -e "s|__PLUGIN_DISPLAY__|${DISPLAY}|g" \
    -e "s|__PLUGIN_ICON__|${ICON}|g" \
    -e "s|__PLUGIN_COLOR__|${COLOR}|g" \
    -e "s|__PLUGIN_DESCRIPTION__|${DESCRIPTION}|g" \
    {} +
find . -name '*.bak' -delete
```

Token reference:

| Token | Example | Used in |
|---|---|---|
| `__PLUGIN_SLUG__` | `inventory` | URL segment, package name (`@westeuropeco/{slug}-ui`), GHA tag pattern |
| `__PLUGIN_NAME__` | `martha-inventory` | Manifest `plugin.name`, BFF prefix `/api/admin/plugins/{name}/...` |
| `__PLUGIN_DISPLAY__` | `Inventory Sync` | `x-martha-integration.name`, page headers |
| `__PLUGIN_ICON__` | `package` | Phosphor icon name in manifest |
| `__PLUGIN_COLOR__` | `#10b981` | Brand color in `x-martha-integration.color` |
| `__PLUGIN_DESCRIPTION__` | `Sync inventory…` | Manifest description, BFF metadata |

## Local development

### One-time auth (per dev machine)

GHCR npm requires `read:packages` for ALL reads, even on public packages. Configure once:

```bash
gh auth refresh --hostname github.com --scopes read:packages
export GITHUB_TOKEN=$(gh auth token)
```

Add the `export` to `~/.zshrc` / `~/.bashrc` to persist.

### Install + run

```bash
# UI deps
cd my-plugin/ui && npm install --legacy-peer-deps && cd ..

# BFF
docker compose up -d
curl http://localhost:8099/health
# → {"status":"ok"}

# Tests
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest
```

## Wiring into the host

Until dynamic plugin discovery lands ([issue #104](https://github.com/westeuropeco/martha/issues/104)), mounting requires a PR to `westeuropeco/martha` with three entries:

1. **`martha-admin-svelte/package.json`** — registry dep:
   ```json
   "@westeuropeco/{slug}-ui": "^0.0.1"
   ```

2. **`martha-admin-svelte/src/lib/plugins/discover.ts`** — registry entry:
   ```ts
   REGISTRY["{slug}"] = () => import("@westeuropeco/{slug}-ui");
   ```

3. **`martha-admin-svelte/vite.config.ts`** — append to `ssr.noExternal`:
   ```ts
   "@westeuropeco/{slug}-ui",
   ```

The host also needs to know about your BFF spec via `seed_plugins.py` — see [`dev_docs/specs/plugin-author-guide.md`](https://github.com/westeuropeco/martha/blob/main/dev_docs/specs/plugin-author-guide.md) for the full host-wiring procedure.

## Releasing

```bash
cd ui
npm version patch        # bumps ui/package.json
git tag {slug}-ui-v$(node -p "require('./package.json').version")
git push origin --tags
# GHA workflow publishes to https://npm.pkg.github.com
```

## Architecture pointers

- **Plugin contract spec**: [`plugin-host-contract.md`](https://github.com/westeuropeco/martha/blob/main/dev_docs/specs/plugin-host-contract.md)
- **Author guide**: [`plugin-author-guide.md`](https://github.com/westeuropeco/martha/blob/main/dev_docs/specs/plugin-author-guide.md)
- **Reference plugins**: [`martha-scoring`](https://github.com/westeuropeco/martha-scoring), [`martha-signatures`](https://github.com/westeuropeco/martha-signatures), [`martha-sku`](https://github.com/westeuropeco/martha-sku)

## Locked decisions you should know

- Plugin server loaders (`+page.server.ts`) are **banned**. Fetch on `onMount` via `ctx.api`.
- DS is **live-at-head** — no version pin. Plugin's `package.json` declares DS as a regular dep so Vite SSR can resolve it from the plugin's filesystem path.
- i18n is **plugin-owned** — locale extraction pipeline ships separately when needed; the template currently uses host-namespace strings.
- Sidebar `PLUGINS` section is deferred — entry stays under `/integrations`.

## What's NOT in this template

- DB / Alembic — add when you need persistence; mirror `martha-scoring`.
- Authentication on BFF endpoints — host's plugin proxy injects auth context; surface plugin-side authorization checks if needed.
- Per-plugin wuchale extraction wiring — falls back to host namespace until plugin-owned i18n pipeline is wired.
- CI for the BFF (lint, typecheck, deploy) — copy from `martha-scoring/.github/workflows/` if you want it.
