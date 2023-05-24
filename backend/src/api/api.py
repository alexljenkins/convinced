import logging
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from src.scenario.character_ai import ask_character_ai


tags_metadata = [
    {"name": "UAT Method", "description": "Test functionality and endpoint using UAT credentials"},
    {"name": "Production Method", "description": "Test functionality and endpoint using Production credentials"},
]
app = FastAPI(openapi_tags=tags_metadata)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Configure CORS
origins = [
    "http://localhost:3000",  # Update with the origin of your frontend
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

@app.options("/api/ask_character_ai")
async def handle_options(request: Request, response: Response):
    response.headers["Allow"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"  # Replace with the origin of your frontend
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"

    return response

@app.post("/api/ask_character_ai")
async def api_character(request: Request):
    data = await request.json()
    if data.get("key") != 'alexisthebestchuckouttherest':
        return {'response':"Sorry, you don't have permission to talk to me.", 'success':False}
    
    answer, success = ask_character_ai(data.get("response"))
    logger.info('Sending response with keys: response, success!')
    return {'response':answer, 'success':success}


@app.get("/ask_character_ai", tags=["Production Method"])
async def api_character_ai(response: str, key: str):
    if key != 'alexisthebestchuckouttherest':
        return {'response':"Sorry, you don't have permission to talk to me.", 'success':False}

    response, success = ask_character_ai(response)
    return {'response':response, 'success':success}


# @app.get("/vote", tags=["Production Method"])
# async def api_vote(response: str):
#     return vote(response)

# @app.get("/get_responses", tags=["Production Method"])
# async def api_get_responses(number_of_resonses: int):
#     return get_responses(number_of_resonses)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", port=8000, reload=True, access_log=False)
