from langchain.schema.runnable import RunnableSerializable
from langchain.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import  Any, Tuple, Optional
from langchain_linkdin_search_agent.models.summary_model import summary, Summary
from langchain_linkdin_search_agent.agent_calling_function.agent_calling_function import (
    linkedin_profile_search_agent, scrape_linkedin_profile, GEMINI_API_KEY
)

def linkedin_search_agent(name: str) -> Optional[Tuple[Summary, str]]:
    # Step 1: Search for the LinkedIn profile URL
    linkedin_username: Optional[str] = linkedin_profile_search_agent(name = name)
    
    if not linkedin_username:
        print("Could not retrieve the LinkedIn profile URL.")
        return None

    # Step 2: Scrape the LinkedIn profile data
    linkdin_data: Optional[dict[str, Any]] = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    
    if not linkdin_data:
        print("Failed to retrieve profile data. Please check the URL or profile access.")
        return None

    # Step 3: Define the prompt template for summary and facts generation
    summary_template = """
    Given the following LinkedIn information:
    {information}
    
    Create the following:
    1. A short summary of the person's profile.
    2. Two interesting facts about the person.
    
    Use Information from LinkedIn
    
    \n{format_instructions}
    """

    summary_prompt_template: PromptTemplate = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={"format_instructions": summary.get_format_instructions()}
    )

    # Step 4: Initialize the LLM and run the prompt chain
    llm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
        temperature = 0,
        model = "gemini-2.0-flash-exp",
        api_key = GEMINI_API_KEY
    )

    chain: RunnableSerializable[dict[str, Any], Summary] = (
        summary_prompt_template | llm | summary
    )

    try:
        # Step 5: Generate the summary and interesting facts
        res: Summary = chain.invoke(input = {"information": linkdin_data})
        print(res)

        # Cast profile picture URL to str explicitly
        profile_pic_url: str = str(linkdin_data.get("profile_pic_url", "No profile picture found."))

        return res, profile_pic_url
    except Exception as e:
        print(f"An error occurred during summary generation: {e}")
        return None