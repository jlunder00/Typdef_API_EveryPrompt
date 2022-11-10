from fastapi import HTTPException, status, Security, FastAPI
from fastapi.security import APIKeyHeader, APIKeyQuery
from pydantic import BaseModel


class JSON_Input(BaseModel):
    json:Dict
    api_key:str

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


# Define the application
app = FastAPI(title="Example API")


@app.get("/public")
def public():
    """A Public endpoint that does not require any authentication"""
    return "Public Endpoint"


@app.post("/generate_typescript")
def generate_typescript(api_key: str = Security(get_api_key)):

    return f"Private Endpoint. API Key is: {api_key}"


