from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from langchain_linkdin_search_agent.linkdin_agent import linkedin_search_agent
from langchain_linkdin_search_agent.models.summary_model import Agent_Response

app: FastAPI = FastAPI()

chat_history: list[Agent_Response] = []


@app.get("/")
def checking_route():
    return {"message": "Hello Linkedin AI Agent."}

@app.get("/get-linkdin-data/", response_model=list[Agent_Response])
async def get_linkdin_profile_data():
    return JSONResponse(content=chat_history)

@app.post("/search-profile/", response_model=Agent_Response)
async def linkedin_profile_agent(name: str):
    result = linkedin_search_agent(name)

    if result is None:
        raise HTTPException(status_code=404, detail="Profile not found.")

    summary, profile_pic_url = result
    
    agent_response = Agent_Response(summary=summary.to_dict(), profile_pic_url=profile_pic_url)
    
    chat_history.append(agent_response.model_dump())

    return JSONResponse(
        content=[agent_response.model_dump()]
    )