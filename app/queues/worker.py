from app.console_renderer import render_report

def run_agent_job(job_spec: dict):
    # Initialize State to pass between agents instead of raw strings
    state = {
        "job_spec": job_spec,
        "plan_steps": "",
        "context": "",
        "analysis": "",
        "critique": "",
        "report": ""
    }

    try:
        from app.agents.planner import plan
        from app.agents.retrieval import retrieve_context
        from app.agents.analysis import analyze
        from app.agents.critic import critique
        from app.agents.reporter import build_report

        print("\n🔥 Step 1: Planning\n")
        state["plan_steps"] = plan(state)
        print(f"\Result: {state['plan_steps']}\n")

        print("\n🔥 Step 2: Multi-Query Retrieval\n")
        state["context"] = retrieve_context(state)
        print(f"\Result: {state['context']}\n")

        print("\n🔥 Step 3: Analysis (Applying Constraints)\n")
        state["analysis"] = analyze(state)
        print(f"\Result: {state['analysis']}\n")

        print("\n🔥 Step 4: Critique\n")
        state["critique"] = critique(state)
        print(f"\Result: {state['critique']}\n")

        print("\n🔥 Step 5: Final Reporting\n")
        state["report"] = build_report(state)
        # 🔥 PRINT HUMAN-READABLE REPORT
        render_report(state["report"])
        # print(f"\Result: {state['report']}\n")

        return state["report"]

    except Exception as e:
        print(f"Job failed: {e}")
        raise