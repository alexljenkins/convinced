import uvicorn
import logging

if __name__ == "__main__":
    logger = logging.getLogger("uvicorn")
    uvicorn.run("api.api:app", host="0.0.0.0", port=8000, reload=True, access_log=False)
