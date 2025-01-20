from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from langchain_linkdin_search_agent.linkdin_agent import linkedin_search_agent

app: FastAPI = FastAPI()

@app.get("/")
def checking_route():
    return {"message": "Hello Linkedin AI Agent."}

@app.post("/search-profile/")
async def linkedin_profile_agent(name: str):
    result = linkedin_search_agent(name)

    if result is None:
        raise HTTPException(status_code=404, detail="Profile not found.")

    summary, profile_pic_url = result

    return JSONResponse(
        content={
            "summary_and_facts": summary.to_dict(),
            "profile_pic_url": profile_pic_url,
        }
    )