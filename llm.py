from langchain_core.tools import tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import requests

#API_KEY
load_dotenv()

#langchain tool for patient lookup
@tool
def lookup_patients(first_name: str, last_name: str, dob: str) -> dict:
    """call this tool to check if a patient exists in the EMR database.  always use this first when a user provides their name and date of birth."""
    response = requests.post( "http://127.0.0.1:8000/patients/lookup",  json={"first_name": first_name, "last_name": last_name, "dob": dob} ) 
    return response.json()

#setting up LLM

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
llm_with_tools = llm.bind_tools([lookup_patients])

system_prompt= '''
You are a Medical Records Extraction assistant. Your purpose is to gather required inputs to help the system look up patient EMR records.

You have access to the `lookup_patients` tool schema.

Mandatory Procedure to Follow:
1. IF ALL DETAILS ARE PRESENT: If the user provides a first name, a last name, and a date of birth, you MUST call the `lookup_patients` tool. Do not ask for confirmation or write a conversational response. Simply return the tool call payload.
2. IF ANY DATA IS MISSING: Do NOT generate a tool call. Ask the user to enter the missing data.
3. DATA FORMATTING CONSTRAINTS:
- Capitalize the first letter of the first and last name.
- You must parse and normalize any mentioned date of birth into 'MM/DD/YYYY' format before generating the tool argument payload. 
'''


messages = [("system", system_prompt)] #stores message history for current chat

print("Enter your name and DOB(Date of Birth): ")

while(True):
    #we use this loop to keep the chat running until user enters all details
    user_input = input("\nUser: ")
    
    messages.append(("user", user_input))
    
    response = llm_with_tools.invoke(messages)
    
    messages.append(response)
    
    
    if(response.tool_calls): #if all details present then tool call will be triggered
        for tool_call in response.tool_calls:
            if tool_call["name"] == "lookup_patients":
                query = tool_call["args"]
                print(f"\nSearching DB for: {query}")
                result = lookup_patients.invoke(query)
                print(f"\nEMR Database Result: {result}")
                break
        break
    else: #missing data case
        print(f"\nAssistant: {response.content}")
    



