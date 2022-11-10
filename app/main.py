from fastapi import HTTPException, status, Security, FastAPI
from fastapi.security import APIKeyHeader, APIKeyQuery
from pydantic import BaseModel
import subprocess
import json
import datetime, time


# Define a list of valid API keys
API_KEYS = [
    "9d207bf0-10f5-4d8f-a479-22ff5aeff8d1",
    "f47d4a2c-24cf-4745-937e-620a5963c0b8",
    "b7061546-75e8-444b-a2c4-f19655d07eb8",
]

# Define the name of query param to retrieve an API key from
api_key_query = APIKeyQuery(name="api-key", auto_error=False)
# Define the name of HTTP header to retrieve an API key from
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


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
app = FastAPI(title="Example API")


@app.get("/public")
def public():
    """A Public endpoint that does not require any authentication"""
    return "Public Endpoint"


@app.post("/generate_typescript")
def generate_typescript(json_input: JSONInput):
    #TODO: run jtd-codegen on inputted data, get inputted data
     
    json_string = json.dumps(json_input.json_schema)
    with open ('./tmp/in/in.json', 'w') as fin:
        fin.write(json_string)
    # folder = str(time.time()) #TODO: make better tmp folder creation/deletion
    with subprocess.Popen(["./lib/bin/jtd-codegen", "./tmp/in/in.json", "--root-name", "Item", "--typescript-out", "./tmp/"], stdout=subprocess.PIPE) as proc:
        print(proc.stdout.read())
    generated_typescript = ''
    with open("./tmp/index.ts") as fin:
         generated_typescript = '\n'.join(fin.readlines()[2:])
    return {'typescript':generated_typescript} 


