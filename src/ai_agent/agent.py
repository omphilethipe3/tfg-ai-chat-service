import os
from openai import OpenAI
import fastmcp
if not hasattr(fastmcp, "Agent"):
    fastmcp.Agent = None
from src.ai_agent.tools import get_person_address, check_credit_customer

# 1) Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("AGENT_API_KEY"))

def chat_with_openai(user_msg: str) -> str:
    # 2) Call the Chat Completion API with Function-Calling enabled
    resp = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":user_msg}],
        functions=[
            {
                "name": "get_person_address",
                "parameters": {
                    "type":"object",
                    "properties": {"person_id": {"type":"string"}},
                    "required": ["person_id"]
                }
            },
            {
                "name": "check_credit_customer",
                "parameters": {
                    "type":"object",
                    "properties": {"person_id": {"type":"string"}},
                    "required": ["person_id"]
                }
            }
        ],
        function_call="auto"
    )
    # 3) Detect & dispatch any function call
    msg = resp.choices[0].message
    if msg.function_call:
        fname = msg.function_call.name
        args = msg.function_call.arguments
        if fname == "get_person_address":
            result = get_person_address(**args)
        elif fname == "check_credit_customer":
            result = check_credit_customer(**args)
        # 4) Send the function result back for a final assistant reply
        followup = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"user","content":user_msg},
                msg.model_dump(),  # the function call
                {"role":"function","name": fname, "content": result}
            ]
        )
        return followup.choices[0].message.content
    return msg.content



def chat_with_fastmcp(user_msg: str) -> str:
    agent = fastmcp.Agent(
        api_key=os.getenv("AGENT_API_KEY"),
        tools={
            "get_person_address": get_person_address,
            "check_credit_customer": check_credit_customer,
        },
        local=True
    )
    return agent.chat(user_msg)