import re
from app.vectorstore.client import get_vector_store

vector_store = get_vector_store()

def retrieve_context(state: dict):
    spec = state["job_spec"]
    plan_text = state["plan_steps"]
    x = spec["job_type"]
    print(f"Job type: {x}\n")

    if spec["job_type"] == "document_analysis":
        # Extract individual steps from the plan to search specifically for each
        queries = [line.strip() for line in plan_text.split('\n') if line.strip() and line[0].isdigit()]
        # Add the original objective as a primary query
        queries.append(spec["objective"])
        
        all_results = []
        for q in queries:
            docs = vector_store.similarity_search(q, k=2) # Get top 2 for each plan step
            all_results.extend([d.page_content for d in docs])
        
        # Deduplicate results
        return "\n---\n".join(list(set(all_results)))

    if spec["job_type"] == "log_analysis":
        raw_logs = spec["inputs"].get("logs", "")
        return preprocess_logs(raw_logs)

    return ""


def preprocess_logs(raw_logs: str, max_lines: int = 100) -> str:
    """Filters logs for high-signal patterns to avoid context window flooding."""
    # Normalize input
    if isinstance(raw_logs, list):
        # Convert list of logs to a single string
        raw_logs = "\n".join(map(str, raw_logs))
    elif not isinstance(raw_logs, str):
        raw_logs = str(raw_logs)
    lines = raw_logs.splitlines()
    
    # Pattern for errors, failures, or critical issues
    signal_pattern = re.compile(r"(error|fail|critical|exception|fatal|500|timeout|denied)", re.IGNORECASE)
    
    # Filter for signal
    important_lines = [l for l in lines if signal_pattern.search(l)]
    
    # If still too many, take the most recent (tail)
    if len(important_lines) > max_lines:
        important_lines = important_lines[-max_lines:]
        
    return "\n".join(important_lines) if important_lines else "\n".join(lines[-max_lines:])