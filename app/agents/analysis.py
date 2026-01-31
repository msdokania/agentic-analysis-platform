from openai import OpenAI
from app.settings import OPENAI_MODEL
from app.prompts import AgentPrompts

client = OpenAI()

def analyze(state: dict):
    spec = state["job_spec"]
    constraints = spec.get("constraints") or "No specific constraints."
    
    user_content = f"""
    OBJECTIVE: {spec['objective']}
    JOB TYPE: {spec['job_type']}
    CONSTRAINTS: {constraints}
    CONTEXT: {state['context']}
    """
    
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": AgentPrompts.ANALYSIS_PROMPT},
            {"role": "user", "content": user_content}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content