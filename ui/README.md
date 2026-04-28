# @westeuropeco/__PLUGIN_SLUG__-ui

__PLUGIN_DISPLAY__ admin UI for the Martha plugin host. See
[`westeuropeco/martha` issue #104](https://github.com/westeuropeco/martha/issues/104)
and [`dev_docs/specs/plugin-author-guide.md`](https://github.com/westeuropeco/martha/blob/main/dev_docs/specs/plugin-author-guide.md)
for the full plugin contract.

## Local install

This package depends on `@westeuropeco/martha-sdk` and `@westeuropeco/admin-chrome` from GitHub Packages npm. **GHCR npm requires `read:packages` auth even on public packages** — that's GitHub's policy, not ours.

One-time setup:

```bash
gh auth refresh --hostname github.com --scopes read:packages
export GITHUB_TOKEN=$(gh auth token)
```

Add the `export` to your `~/.zshrc` / `~/.bashrc` to persist.

Then:

```bash
cd ui
npm install --legacy-peer-deps
```

The committed `ui/.npmrc` already points the `@westeuropeco` scope at `https://npm.pkg.github.com` and reads the auth from your `GITHUB_TOKEN` env var.

## Iterating

Once mounted in `martha-admin-svelte` via a registry semver dep, host Vite picks up your changes when you `npm version <patch> && git tag __PLUGIN_SLUG__-ui-v<version> && git push --tags` — the GHA at `.github/workflows/publish-ui.yml` publishes the new version to GHCR.

For day-to-day dev without re-publishing, ask the host maintainer to switch the host's `package.json` entry to `file:../../<your-plugin>/ui` while you iterate. Switch back to a registry semver before merging anything to `main`.
