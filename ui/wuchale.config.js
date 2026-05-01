/**
 * Plugin-owned wuchale extraction. Mirrors the host's
 * `martha-admin-svelte/wuchale.config.js` shape so plugin strings live
 * in the same three locales with the same fallback behaviour.
 *
 * `wuchale extract` reads `src/**` and writes
 * `src/locales/{en,pt,es}.po`. The `.po` files are committed and
 * shipped in the published tarball. The host's wuchale Vite plugin
 * compiles them in-tree at host build time under the plugin's slug
 * as the wuchale namespace; `src/locales/loader.svelte.js` registers
 * the catalogue at runtime.
 */
import { adapter as svelte } from "@wuchale/svelte";
import { defineConfig } from "wuchale";

export default defineConfig({
  locales: {
    en: { name: "English" },
    pt: { name: "Portuguese" },
    es: { name: "Spanish" },
  },
  fallback: true,
  adapters: {
    main: svelte(),
  },
});
