# JSON To TypeScript API
* API to interact with jtd-codegen to generate corresponding typescript from a json schema
* For use with EveryPrompt's JSON/TypeScript generation using GTP-3
* Hosted on fly.io
* Uses redis upstage server through fly.io for caching

## Usage:
* `curl -X POST https://json-ts-api.fly.dev/generate_typescript -H "Content-Type: application/json" -d '{"schema_title":"Item", api_key":"<api_key>", "json_schema":{}}'`
    - Responds with: `{"typescript":"export type Item = any;\n"}`
* Requires an API key in body or header

## To Build/Deploy on fly.io:
* Get an account on [fly.io](fly.io) and follow their instructions to setup cli tools
* Clone Repo
* in fly.toml, modify "app" with whatever name you want
* in root of repo: `fly launch`
    - Respond "Y" When asked to use existing fly.toml
    - Select name, region and organization
    - Accept when asked if you want a redis server.
    - Reject postgres server
    - Do not deploy
* If not asked if you want a redis server, run:
    - `flyctl redis create`
* Record the private address given, and enter it as a secret via `flyctl secrets set <name>=<value>`
    - Call this secret REDIS_URL
* Generate a list of chosen API keys, seperated by :, enter them as a secret
    - Call this secred EVERYPROMPT_API_KEYS, or change the name of the evironment variable referenced in main.py
* Once secrets are entered, run `flyctl deploy`

## To Build/Deploy Locally
* This repo is not setup for local builds, so this would require changes, including:
    - Install redis on the docker container by adding the commands to do so to the dockerfile:
        * RUN sudo apt-get install redis
    - In place of setting a secret through flyctl secrets, set env variables in the docker container. For example:
        * ENV REDIS_URL=https://localhost:6397
        * ENV EVERYPROMPT_API_KEYS=key1fe13251d212c:key22e213cfd323cdd21
    - Build with `docker build ./` from the root of the repo
    - Run with `docker run -p 8000:8000 <image name or id>`
    - Access with `curl -X POST https://localhost:8000/generate_typescript ...`
