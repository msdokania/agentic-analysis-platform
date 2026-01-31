from openai import OpenAI
from app.settings import OPENAI_MODEL
from app.prompts import AgentPrompts


client = OpenAI()

def critique(state: dict):
    spec = state["job_spec"]
    constraints = spec.get("constraints") or "No specific constraints."
    
    user_content = f"""
    OBJECTIVE: {spec['objective']}
    JOB TYPE: {spec['job_type']}
    CONSTRAINTS: {constraints}
    RAW_CONTEXT: {state['context']}
    PROPOSED_ANALYSIS: {state['analysis']}
    """

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": AgentPrompts.CRITIC_PROMPT},
            {"role": "user", "content": user_content}
        ],
        temperature=0
    )
    return response.choices[0].message.content