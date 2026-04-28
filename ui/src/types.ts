/**
 * Domain types for __PLUGIN_DISPLAY__.
 *
 * Mirror the FastAPI BFF's response shapes. The plugin's `api.ts` is the
 * single place you cross from `unknown` HTTP responses to typed data, so
 * keep these definitions accurate.
 */

export interface Thing {
  id: string;
  name: string;
  description: string;
}

export interface ThingCreate {
  name: string;
  description?: string;
}
