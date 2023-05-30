import logging
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from src.review.review_and_voting import vote
from src.scenario.character_ai import ask_character_ai
from src.database.database_calls import get_entries_for_voting, print_table_contents, delete_entry_from_vote
from src.globals import DATABASE

tags_metadata = [
    {"name": "Testing Method", "description": "Test functionality and endpoint using UAT credentials"},
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
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["Content-Type"],
)

@app.options("/api/vote")
@app.options("/api/get_responses")
@app.options("/api/ask_character_ai")
async def handle_options(request: Request, response: Response):
    response.headers["Allow"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"  # Replace with the origin of your frontend
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"

    return response


@app.post("/api/ask_character_ai")
async def post_character_response(request: Request):
    data = await request.json()
    if data.get("key") != 'alexisthebestchuckouttherest':
        return {'response':"Sorry, you don't have permission to talk to me.", 'success':False}
    try:
        answer, success = ask_character_ai(data.get("response"))
        logger.info('Sending response with keys: response, success!')
    except Exception as e:
        logger.error(e)
        return {'response':"Sorry, something went wrong.", 'success':False}
    return {'response':answer, 'success':success}


@app.get("/api/ask_character_ai", tags=["Testing Method"])
async def get_character_response(response: str, key: str):
    if key != 'alexisthebestchuckouttherest':
        return {'response':"Sorry, you don't have permission to talk to me.", 'success':False}

    response, success = ask_character_ai(response)
    return {'response':response, 'success':success}


@app.post("/api/vote", tags=["Production Method"])
async def post_vote(request: Request):
    data = await request.json()
    if data.get("key") != 'alexisthebestchuckouttherest':
        return {'response':"Sorry, you don't have permission to talk to me.", 'success':False}
    try:
        vote(DATABASE, data)
    except Exception as e:
        logger.error(e)
        return {'response':"Sorry, something went wrong.", 'success':False}
    return 


@app.post("/api/collect_responses", tags=["Production Method"])
async def post_responses(request: Request):
    data = await request.json()
    if data.get("key") != 'alexisthebestchuckouttherest':
        return {'response':"Sorry, you don't have permission to talk to me.", 'success':False}
    try:
        entries = get_entries_for_voting(DATABASE)
        logger.info('Got entries:\n{entries}')
    except Exception as e:
        logger.error(e)
        return {'response':"Sorry, something went wrong.", 'success':False}
    
    return {'response':entries.get_voting_data(), 'success':True}


@app.get("/api/collect_responses", tags=["Testing Method"])
async def get_responses(key: str):
    if key != 'alexisthebestchuckouttherest':
        return {'response':"Sorry, you don't have permission to talk to me.", 'success':False}

    entries = get_entries_for_voting(DATABASE)
    
    logger.info('Got entries:\n{entries}')
    
    return entries


@app.get("/api/set_disable", tags=["Testing Method"])
async def set_disable(id: int, key: str):
    if key != 'alexisthebestchuckouttherest':
        return {'response':"Sorry, you don't have permission to talk to me.", 'success':False}

    delete_entry_from_vote(DATABASE, id)
    logger.info(f'Deleted entry with id: {id}.')
    
    return {'success':True}

if __name__ == "__main__":
    # print_table_contents(DATABASE)
    import uvicorn
    uvicorn.run("api:app", port=8000, reload=True, access_log=False)
