from fastapi import HTTPException, status, Security, FastAPI
from fastapi.security import APIKeyHeader, APIKeyQuery
from pydantic import BaseModel
import subprocess
import json
import time
import redis
from pathlib import Path
import os, shutil

API_KEYS = os.environ['EVERYPROMPT_API_KEYS'].split(':')
# redis_url = "redis://default:"+REDIS_PASS+"@fly-json-ts-api-redis.upstash.io"
r = redis.Redis.from_url(os.environ['REDIS_URL'])

# Define the name of query param to retrieve an API key from
api_key_query = APIKeyQuery(name="api-key", auto_error=False)
# Define the name of HTTP header to retrieve an API key from
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

infolder = Path('./tmp/in')
outfolder = Path('./tmp/out')
if not infolder.exists():
    infolder.mkdir(parents=True)
if not outfolder.exists():
    outfolder.mkdir(parents=True)


def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
):
    """Retrieve & validate an API key from the query parameters or HTTP header"""
    # If the API Key is present as a query param & is valid, return it
    if api_key_query in API_KEYS:
        return api_key_query

    # If the API Key is present in the header of the request & is valid, return it
    if api_key_header in API_KEYS:
        return api_key_header

    # Otherwise, we can raise a 401
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )

class JSONInput(BaseModel):
    schema_title: str = 'Item'
    json_schema: dict
    api_key: str = Security(get_api_key)

# Define the application
app = FastAPI(title="JSON To TypeScript Converter")



@app.post("/generate_typescript")
async def generate_typescript(json_input: JSONInput):
    #Generate typescript from json input
    try:
        get_api_key(json_input.api_key)
        json_string = json.dumps(json_input.json_schema)
        title = json_input.schema_title
        cached_result = r.get(json_string)
        if cached_result is not None:
            return {'typescript':cached_result}
        t = str(time.time())
        infile = Path('/app/src/tmp/in/'+title+'-'+t+'.json')
        with open(str(infile), 'w') as fin:
            fin.write(json_string)
        outdir = Path('/app/src/tmp/out/'+title+'-'+t+'/')
        if not outdir.exists():
            outdir.mkdir(parents=True)
        cmd = ["./lib/bin/jtd-codegen", str(infile), "--root-name", str(json_input.schema_title), "--typescript-out", str(outdir)]
        process = subprocess.Popen(cmd)
        process.wait()
        outfile = outdir/'index.ts'
        generated_typescript = ''
        with open(str(outfile), 'r') as fin:
            generated_typescript = '\n'.join(fin.readlines()[2:])
            r.set(json_string, generated_typescript)
        shutil.rmtree(outdir)
        return {'typescript':generated_typescript}
    except Exception:
        raise Exception
        


