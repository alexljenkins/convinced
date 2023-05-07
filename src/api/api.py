from random import Random
from typing import Optional

from fastapi import FastAPI


# could look into https://github.com/pandera-dev/pandera/releases/tag/v0.9.0 for dataframe returns

tags_metadata = [
    {"name": "UAT Method", "description": "Test functionality and endpoint using UAT credentials"},
    {"name": "Production Method", "description": "Test functionality and endpoint using Production credentials"},
]
app = FastAPI(openapi_tags=tags_metadata)


@app.get("/marker_ai", tags=["Production Method"])
async def api_marker_ai(response: str):
    # st.title("convince.me")
    # st.markdown("You've approached me at my bridge! But nothing I've seen has made me want to let you past.\nWrite a short message that would convince me to let you through...")
    return marker_ai(response)

@app.get("/character_ai", tags=["Production Method"])
async def api_character_ai(response: str):
    # st.title("convince.me")
    # st.markdown("You've approached me at my bridge! But nothing I've seen has made me want to let you past.\nWrite a short message that would convince me to let you through...")
    return character_ai(response)


@app.get("/vote", tags=["Production Method"])
async def api_vote(response: str):
    return vote(response)

@app.get("/see_responses", tags=["Production Method"])
async def api_see_responses(number_of_resonses: int):
    return see_responses(number_of_resonses)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", port=8000, reload=True, access_log=False)
