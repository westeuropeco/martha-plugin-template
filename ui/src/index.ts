/**
 * `@westeuropeco/__PLUGIN_SLUG__-ui` — entry point consumed by the Martha
 * admin host's plugin discovery (`src/lib/plugins/discover.ts`). The host
 * imports this module dynamically, reads the `routes` export, and runs
 * `matchRoute` against incoming `/plugins/__PLUGIN_SLUG__/...` URLs.
 *
 * Layout:
 *   - `pages/Home.svelte`   — `/plugins/__PLUGIN_SLUG__`
 *   - `pages/Detail.svelte` — `/plugins/__PLUGIN_SLUG__/:id`
 *
 * Add routes by appending to the array. Path syntax:
 *   - `""` matches the plugin root
 *   - `"items"` matches `/plugins/__PLUGIN_SLUG__/items`
 *   - `":id"` is a single-segment param, surfaced as `params.id`
 *   - `"items/:id/edit"` mixes literals and params
 */
import "./locales/loader.svelte.js";
import { defineRoutes } from "@westeuropeco/martha-sdk/client";
import Home from "./pages/Home.svelte";
import Detail from "./pages/Detail.svelte";

export const routes = defineRoutes([
  { path: "", component: Home, title: "__PLUGIN_DISPLAY__" },
  { path: ":id", component: Detail, title: "__PLUGIN_DISPLAY__ detail" },
]);
