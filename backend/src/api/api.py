from fastapi import FastAPI

from scenario.character_ai import ask_character_ai


# could look into https://github.com/pandera-dev/pandera/releases/tag/v0.9.0 for dataframe returns

tags_metadata = [
    {"name": "UAT Method", "description": "Test functionality and endpoint using UAT credentials"},
    {"name": "Production Method", "description": "Test functionality and endpoint using Production credentials"},
]
app = FastAPI(openapi_tags=tags_metadata)


@app.get("/ask_character_ai", tags=["Production Method"])
async def api_character_ai(response: str):
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
