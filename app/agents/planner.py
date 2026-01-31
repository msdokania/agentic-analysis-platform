from openai import OpenAI
from app.settings import OPENAI_MODEL
from app.prompts import AgentPrompts

client = OpenAI()

def plan(state: dict):
    spec = state["job_spec"]
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": AgentPrompts.PLANNER_PROMPT},
            {"role": "user", "content": str(spec)}
        ],
        temperature=0
    )
    return response.choices[0].message.content