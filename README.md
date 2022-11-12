# JSON To TypeScript API
* API to interact with jtd-codegen to generate corresponding typescript from a json schema
* For use with EveryPrompt's JSON/TypeScript generation using GTP-3
* Hosted on fly.io
* Uses redis upstage server through fly.io for caching

## Usage:
* `curl -X POST https://json-ts-api.fly.dev/generate_typescript -H "Content-Type: application/json" -d '{"schema_title":"Item", api_key":"<api_key>", "json_schema":{}}'`
    - Responds with: `{"typescript":"export type Item = any;\n"}`
* Requires an API key in body or header

