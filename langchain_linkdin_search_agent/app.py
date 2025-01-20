from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from langchain_linkdin_search_agent.linkdin_agent import linkedin_search_agent

app: FastAPI = FastAPI()

# In-memory storage for profile data
profile_storage = {}

@app.get("/")
def checking_route():
    return {"message": "Hello Linkedin AI Agent."}

@app.get("/get-data")
def get_data():
    if not profile_storage:
        raise HTTPException(status_code=404, detail="No profiles available.")
    return profile_storage

@app.post("/search-profile/")
async def linkedin_profile_agent(name: str):
    result = linkedin_search_agent(name)

    if result is None:
        raise HTTPException(status_code=404, detail="Profile not found.")

    summary, profile_pic_url = result

    # Store the data in the in-memory storage
    profile_storage[name] = {
        "summary_and_facts": summary.to_dict(),
        "profile_pic_url": profile_pic_url,
    }

    return JSONResponse(
        content={
            "summary_and_facts": summary.to_dict(),
            "profile_pic_url": profile_pic_url,
        }
    )
