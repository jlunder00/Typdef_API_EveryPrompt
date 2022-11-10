from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.model import PostSchema

app = FastAPI()

# origins = [
#     "http://localhost",
#     "*"
# ]

posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content":"...."
    }
]

# app.add_middleware
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "welcome to your blog!"}
