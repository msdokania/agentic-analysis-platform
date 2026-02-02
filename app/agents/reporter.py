from openai import OpenAI
from app.settings import OPENAI_MODEL
from app.prompts import AgentPrompts

client = OpenAI()

def build_report(state: dict):
    spec = state["job_spec"]
    
    user_content = f"""
    ### PRIMARY OBJECTIVE
    {spec['objective']}

    ### JOB TYPE
    {spec['job_type']}

    ### DRAFT ANALYSIS (TO BE FILTERED)
    {state['analysis']}

    ### QUALITY AUDIT / CRITIQUE (TRUTH SOURCE)
    {state['critique']}
    """

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": AgentPrompts.REPORT_PROMPT},
            {"role": "user", "content": user_content}
        ],
        temperature=0
    )
    result = response.choices[0].message.content
    report = result.strip()
    if report.startswith("```"): # Clean up LLM-added markdown blocks
        report = "\n".join(report.split("\n")[1:-1])
    return report