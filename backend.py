from typing import TypedDict,Annotated
import operator
import uuid
import psycopg
from psycopg.rows import dict_row
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver

import os 
import certifi
from dotenv import load_dotenv 
load_dotenv() 

from langchain_core.messages import (
    AnyMessage, 
    HumanMessage,
    AIMessage, 
    SystemMessage
)

from langchain_groq import ChatGroq
from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights


# Conect to the Postgre data base server 
def get_database_url():
    database_url=os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set.")

    if "sslmode" not in database_url:
        separator = '&' if '?' in database_url else '?'
        database_url = f"{database_url}{separator}sslmode=require"

    return database_url



# get api key 
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

# LLM
llm = ChatGroq(api_key=GROQ_API_KEY, model="openai/gpt-oss-20b", temperature=0.6, max_tokens=2000)


# langraph 
# 1st step Stare Graph Define State
class TrvelState(TypedDict):
    message: Annotated[list[AnyMessage],operator.add]
    user_query: str
    flight_results:str
    hotel_results:str
    itinerary:str
    llm_calls:int

# 2nd step
#  Flight Agent Create Nodes
def flight_agent(state:TrvelState):
    query=state["user_query"]
    flight_results = search_flights(query)

    return {
        "flight_results": flight_results,
        "message":[
            AIMessage(content="Flight results fetched successfully.")
        ],
        "llm_calls":state.get("llm_calls",0) + 1
    }


# Hotel Agent Create Nodes
def hotel_agent(state:TrvelState):
    query=f"Best Hotels in {state['user_query']}"
    hotel_results = tavily_search(query)

    return {
        "hotel_results": hotel_results,
        "message":[
            AIMessage(content="Hotel results fetched successfully.")
        ],
        "llm_calls":state.get("llm_calls",0) + 1
    }


# Itinerary Agent Create Nodes
def itinerary_agent(state:TrvelState):
    prompt=f"""
    Create a complete travel itineray.
    User query: {state['user_query']}
    Flight Results: {state['flight_results']}
    Hotel Results: {state['hotel_results']}
    Make  the itinerary practical ,budget friendly and enjoyable. Provide a day-wise breakdown of activities, including sightseeing, dining, and any other relevant information. Ensure that the itinerary is well-structured and easy to follow.
    """
    response = llm.invoke([
        SystemMessage(content="You are an expert travel planner ."),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
         "message":[response],
        "llm_calls":state.get("llm_calls",0) + 1
    }

# Final Agent Create Nodes
def final_agent(state:TrvelState):
    final_prompt = f"""
    Generate the final travel response for the user.
    User Request: {state['user_query']}
    Flight Results: {state['flight_results']}
    Hotel Results: {state['hotel_results']}
    Itinerary: {state['itinerary']}

    Format the final answer beautifully using these sections:
    1.trip summary
    2.flight information
    3.hotel suggestions
    4.day-by-day itinerary
    5.estimate budget
    6.final recommendations

    Important:
    -Be clear and practical
    -mention that live flight API may not provide ticket prices if pricing is unavaiable from the API, clearly mention "Live ticket prices are currently unavailable. Please check the airline or booking website for the latest fares." Do not invent or estimate actual ticket prices.
    -Keep the response  useful for real travel planning.""" 

    response = llm.invoke([
        SystemMessage(content="You are Professional AI travel AI booking assistant "),
        HumanMessage(content=final_prompt)
    ])

    return{
        "message":[response],
        "llm_calls":state.get("llm_calls",0)+1    
        }


# 3rd step 
# Bulid grpah 
graph= StateGraph(TrvelState)


# 4th step 
# Add node 
graph.add_node("flight_agent",flight_agent)
graph.add_node("hotel_agent",hotel_agent)
graph.add_node("itinerary_agent",itinerary_agent)
graph.add_node("final_agent",final_agent)

# 5th step
# Add edge
graph.add_edge(START,"flight_agent")
graph.add_edge("flight_agent","hotel_agent")
graph.add_edge("hotel_agent","itinerary_agent")
graph.add_edge("itinerary_agent","final_agent")
graph.add_edge("final_agent",END)

# Postgres CheckPointer

DATABASE_URl=get_database_url()
_conn = psycopg.connect(
    DATABASE_URl,
    autocommit=True,
    row_factory=dict_row
)

checkpointer = PostgresSaver(_conn)
checkpointer.setup()

# 6th step
# compile Graph  
travel_graph = graph.compile(checkpointer=checkpointer)


# Function For FastAPI
def run_travel_agent(user_input:str,thread_id:str |None=None):
    if not thread_id:
        thread_id = f"user_{uuid.uuid4().hex}" 

    config ={
        "configurable":{
            "thread_id":thread_id
        }
    }    

    result = travel_graph.invoke(
    {
        "message":[
            HumanMessage(content=user_input)
        ],
        "user_query":user_input,
        "flight_results":"",
        "hotel_results":"",
        "itinerary":"",
        "llm_calls":0
    },
    config=config
    )  
    
    final_answer = result["message"][-1].content

    return{
        "thread_id":thread_id,
        "answer":final_answer,
        "flight_results":result.get("flight_results",""),
        "hotel_results":result.get("hotel_results",""),
        "itinerary":result.get("itinerary",""),
        "llm_calls":result.get("llm_calls",0),
    }