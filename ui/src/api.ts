/**
 * Plugin-scoped API client for __PLUGIN_DISPLAY__.
 *
 * The host injects a `PluginApiClient` into the plugin context that
 * auto-prefixes `/api/admin/plugins/__PLUGIN_NAME__`. Plugin code calls
 * relative paths like `/things` — the prefix is the host's job.
 *
 * Replace `things` with your own resource shape. Keep one factory per
 * resource so call sites read like `thingsApi(ctx.api).list()`.
 */
import type { PluginApiClient } from "@westeuropeco/martha-sdk/client";
import type { Thing, ThingCreate } from "./types.js";

export interface ThingsApi {
  list(): Promise<Thing[]>;
  get(id: string): Promise<Thing>;
  create(body: ThingCreate): Promise<Thing>;
  remove(id: string): Promise<void>;
}

export function thingsApi(api: PluginApiClient): ThingsApi {
  return {
    list: () => api.get<Thing[]>("/things"),
    get: (id) => api.get<Thing>(`/things/${encodeURIComponent(id)}`),
    create: (body) => api.post<Thing>("/things", body),
    remove: (id) => api.del<void>(`/things/${encodeURIComponent(id)}`),
  };
}
