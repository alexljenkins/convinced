import logging
from fastapi import FastAPI, Request, Response, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import APIKey

from review.review_and_voting import vote
from scenario.character_ai import ask_character_ai
from database.database_calls import get_entries_for_voting, delete_entry_from_vote, get_specific_voted_on_entries, report_response_id, admin_entry_switch, get_table_contents
from api import auth

from globals import DATABASE

tags_metadata = [
    {"name": "Testing Method", "description": "Useful for running things from fastapi/docs for testing."},
    {"name": "Production Method", "description": "Main functionality and endpoint used by frontend - expecting full json."},
    {"name": "Inspection Method", "description": "Used by frontend to know what and how it can use it's corresponding API endpoint."},
    {"name": "Admin Method", "description": "Used by developers to interact with admin only endpoints."},
]
app = FastAPI(openapi_tags=tags_metadata)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Configure CORS
origins = [
    "http://localhost:3000",  # Update with the origin of your frontend
    "http://0.0.0.0:3000",
    "https://0.0.0.0:3000",
    "https://3.25.105.171:3000",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.options("/api/vote")
@app.options("/api/get_responses")
@app.options("/api/ask_character_ai")
async def handle_options(request: Request, response: Response):
    logger.warning("Handling OPTIONS request")
    response.headers["Allow"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Origin"] = ", ".join(origins)
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"

    return response


@app.post("/api/ask_character_ai", tags=["Production Method"])
async def post_character_response(request: Request, auth: APIKey = Depends(auth.get_api_key)):
    data = await request.json()
    try:
        answer, success = ask_character_ai(str(data.get("user_input")))
        logger.info('Sending response with keys: response, success!')
    except Exception as e:
        logger.error(e)
        return {'response':"Sorry, something went wrong.", 'success':False}
    return {'response':answer, 'success':success}


@app.get("/api/ask_character_ai", tags=["Testing Method"])
async def get_character_response(response: str, auth: APIKey = Depends(auth.get_api_key)):
    response, success = ask_character_ai(response)
    return {'response':response, 'success':success}


@app.post("/api/vote", tags=["Production Method"])
async def post_vote(request: Request, auth: APIKey = Depends(auth.get_api_key)):
    data = await request.json()
    try:
        voted_on_entries = get_specific_voted_on_entries(DATABASE, data.get("winner_id"), data.get("loser_id"))
    except Exception as e:
        logger.error(e)
        return {'response':"Sorry, it looks like the input data couldn't be parsed.", 'success':False}
    
    try:
        vote(voted_on_entries)
    except Exception as e:
        logger.error(e)
        return {'response':"Sorry, it looks like the vote was not cast.", 'success':False}

    return {'success':True}


@app.post("/api/collect_responses", tags=["Production Method"])
async def post_responses(request: Request, auth: APIKey = Depends(auth.get_api_key)):
    data = await request.json()
    logger.info(f"At least you got into the api with {data}")
    try:
        entries = get_entries_for_voting(DATABASE)
        logger.info(f"Returning entries: {entries.response_a.response_id} AND {entries.response_b.response_id}")
    except Exception as e:
        logger.error(e)
        return {'response':"Sorry, something went wrong.", 'success':False}
    
    return {'response':entries.get_voting_data(), 'success':True}


@app.get("/api/collect_responses", tags=["Testing Method"])
async def get_responses(auth: APIKey = Depends(auth.get_api_key)):
    entries = get_entries_for_voting(DATABASE)
    logger.info(f"Returning entries: {entries.response_a.response_id} AND {entries.response_b.response_id}")
    
    return entries.get_voting_data()


@app.post("/api/report", tags=["Production Method"])
async def post_report(request: Request, auth: APIKey = Depends(auth.get_api_key)):
    data = await request.json()
    reported_id = data.get("response_id")
    try:
        report_response_id(DATABASE, reported_id)
    except Exception as e:
        logger.error(e)
        return {'response':"Sorry, something went wrong.", 'success':False}
    logger.info(f"Report content with id {reported_id}, successful.")
    return {'success':True}


@app.get("/api/report", tags=["Testing Method"])
async def get_report(response_id: int, auth: APIKey = Depends(auth.get_api_key)):
    try:
        report_response_id(DATABASE, response_id)
    except Exception as e:
        logger.error(e)
        return {'response':"Sorry, something went wrong.", 'success':False}
    logger.info(f"Report content with id {response_id}, successful.")
    
    return {'success': True}


# @app.get("/admin/delete_response", tags=["Admin Method"])
# async def delete_response(id: int, auth: APIKey = Depends(auth.get_api_key)):
#     delete_entry_from_vote(DATABASE, id)
#     logger.info(f'Deleted entry with id: {id}.')
    
#     return {'success':True, 'id':id}


@app.get("/admin/list_responses", tags=["Admin Method"])
async def list_responses(enabled: int = 0, report:int = 0, auth: APIKey = Depends(auth.get_api_key)):
    logger.info(f'Getting records from db.')
    return get_table_contents(DATABASE, enabled, report)

@app.get("/admin/whitelist_response", tags=["Admin Method"])
async def whitelist_blacklist_response(id: int, enable: int, auth: APIKey = Depends(auth.get_api_key)):
    admin_entry_switch(DATABASE, id, enable)
    logger.info(f'Entry perminantly updated: {id}.')
    return {'success':True, 'id':id, 'enabled':enable}

if __name__ == "__main__":
    # print_table_contents(DATABASE)
    import uvicorn
    uvicorn.run("api:app", port=8000, reload=True, access_log=False)
