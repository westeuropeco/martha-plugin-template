/**
 * Plugin-owned wuchale loader.
 *
 * Registers the plugin's compiled `.po` catalogues under the plugin's
 * slug as the wuchale namespace. The host's locale switch calls
 * `loadLocale(code, '__PLUGIN_SLUG__')` → wuchale's runtime invokes this
 * loader → catalog applies.
 *
 * The `'__PLUGIN_SLUG__'` namespace MUST match the slug the host mounts under
 * (`/plugins/__PLUGIN_SLUG__`) — that's how the host's `routes/+layout.svelte`
 * fans out per-plugin locale switches. Plugin authors who copy this file
 * from another plugin must remember to update the slug.
 */

/// <reference types="wuchale/virtual" />

import { loadCatalog, loadIDs } from "virtual:wuchale/loader";
import { registerLoaders } from "wuchale/run-client";

const catalogs = $state({});

export default registerLoaders(
  "__PLUGIN_SLUG__",
  loadCatalog,
  loadIDs,
  catalogs,
);
