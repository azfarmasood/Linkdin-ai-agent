from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.runnable import Runnable
from langchain.tools import Tool
from dotenv import load_dotenv
from langchain import hub
from requests import Response, get
from typing import Literal, Any
from pydantic import SecretStr
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import (create_react_agent, AgentExecutor)
import os

load_dotenv()

GEMINI_API_KEY = SecretStr(os.environ["GEMINI_API_KEY"])
PROXY_CURL_API_KEY = os.environ["PROXY_API_KEY"]

def search_profile_with_tavily(name: str):
    """Searches for Linkedin"""
    search: TavilySearchResults = TavilySearchResults()
    res: Any = search.run(f"{name}")
    return res
    
def linkedin_profile_search_agent(name: str) -> str:
    llm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
        temperature = 0,
        model='gemini-2.0-flash-exp',
        api_key = GEMINI_API_KEY,
    )
    template = """
    Given the full name "{name_of_person}", find and provide only the URL to their LinkedIn profile page. Do not include any other information or URLs.
    """
    prompt_template: PromptTemplate = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent: list[Tool] = [
        Tool(
            name = "Crawl linkedin Search profile page",
            func = search_profile_with_tavily,
            description = "useful for when you need get the Linkedin Page URL",
        )
    ]

    react_prompt: Any = hub.pull("hwchase17/react")
    agent: Runnable = create_react_agent(llm = llm, tools = tools_for_agent, prompt = react_prompt)
    agent_executor = AgentExecutor(agent = agent, tools = tools_for_agent, verbose = True)

    result: dict[str, Any] = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person = name)}
    )

    linked_profile_url: Any = result["output"]
    return linked_profile_url



def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    Creating API Endpoint for linkdin profile that search users linkdin profile dynamically. and not even only profiles it searches its whole profile description, skills and many more.
    """

    if mock:
        linkdin_profile_url: Literal["https://gist.githubusercontent.com/azfarmasood/0e346101ec0558f87e66a537c162d8f2/raw/04a2fbf0cf2627dc8f45cc933503ec8b1122e090/azfar-masood-json"] = "hhttps://gist.githubusercontent.com/azfarmasood/0e346101ec0558f87e66a537c162d8f2/raw/04a2fbf0cf2627dc8f45cc933503ec8b1122e090/azfar-masood-json"
        response: Response = get(linkdin_profile_url, timeout = 10)
    else:
        api_endpoint: Literal["https://nubela.co/proxycurl/api/v2/linkedin"] = (
            "https://nubela.co/proxycurl/api/v2/linkedin"
        )
        header_dic: dict[str, str] = {"Authorization": f'Bearer {PROXY_CURL_API_KEY}'}
        response = get(
            api_endpoint,
            params = {"url": linkedin_profile_url},
            headers = header_dic,
            timeout = 10,
        )

    data: dict = response.json()
    data = {
        key: value
        for key, value in data.items()
        if value not in ([], "", "", None)
        and key not in ["people_also_viewed", "certifications"]
    }
    groups = data.get("groups", [])
    if isinstance(groups, list):
        for group_dict in groups:
            group_dict.pop("profile_pic_url", None)

    return data