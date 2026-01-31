Agentic Analysis Platform

A Multi-Agent Approach to Technical Intelligence

⸻

Why This Project Exists (The Problem Statement)

In typical LLM use-cases, users often find themselves in a “prompting loop” — tweaking a question repeatedly to get a useful answer. As the conversation grows, the LLM begins to lose the thread, forgetting initial constraints or, worse, hallucinating technical details to fill the gaps in its memory.

So instead of asking the LLM to “answer better”, this project asks the system to think better.

⸻

Project Objective

This project replaces the "Linear Chat" with an "Agentic Workflow."

Instead of relying on a single, fragile conversation, the platform initiates a specialized Chain of Command. By decoupling thinking from doing, it ensures every answer is:
	•	Strategically planned
	•	Grounded in multi-source data
	•	Critically audited before reaching the user

This approach directly addresses the twin problems of Information Overload and Context Drift.

⸻

Key Capabilities
	•	📄 Document Analysis
Semantic deep-dives into complex PDFs to answer user queries with evidence-backed reasoning.
	•	🪵 Log Diagnostics
Root-cause analysis by filtering noise and identifying temporal failure patterns in large log streams.

⸻

Tech Stack & Framework

This project uses a custom-built Multi-Agent System (MAS).

While libraries like LangChain are used selectively (for document ingestion and vector retrieval), all agent logic, orchestration, and state transitions are fully custom.
This design makes the system easier to understand, modify, and extend for anyone forking the repository.

Core Stack
	•	Language: Python 3.10+
	•	API Layer: FastAPI (async endpoint management)
	•	Task Queue: Redis + RQ (background task processing)
	•	Vector Store: Qdrant (high-performance semantic retrieval)
	•	LLM: OpenAI (GPT-4o-mini)

⸻

Core Concepts: What Makes It “Agentic”?

Agentic AI refers to systems where the AI is given the agency to follow a process, rather than just completing a sentence.
This project implements three foundational agentic concepts:

1. Decomposition (The Planner): Instead of answering immediately, the system first asks: “What steps do I need to take to answer this accurately?”

2. Specialization: Different personas (Planner, Analyst, Critic) are used to create a checks-and-balances system, similar to a professional engineering team.

3. State Accumulation: As the process moves from planning to reporting, a central State Object grows. Later agents can see the reasoning and decisions of earlier agents, enabling traceability and introspection.

⸻

High-Level Logic & Architecture

When a job is submitted, the system follows this execution flow:
	1.	FastAPI accepts the job and immediately returns a job_id, pushing the task to Redis
	2.	A background Worker picks up the job and initializes a Shared State (persistent job memory)
	3.	The Planner maps out the investigation strategy
	4.	The Retriever executes the plan, fetching data from Qdrant or raw logs
	5.	The Analyst synthesizes findings under strict user-defined constraints
	6.	The Critic performs a Zero-Hallucination check against raw context
	7.	The Reporter delivers a structured final output

⸻

Deep Dive: Component Implementation

1. The Planning Phase (planner.py)

The Planner acts as the Architect.
It converts a high-level objective into a numbered list of execution steps.
	•	temperature=0 is used to ensure logical, deterministic plans.

⸻

2. Multi-Query Retrieval (retrieval.py)

To prevent information gaps, the retriever uses the Planner’s steps to perform multiple targeted searches.
	•	Document Analysis: Uses Qdrant to retrieve semantic matches for each plan step.
	•	Log Analysis: Applies a signal filter to strip away INFO heartbeats and surface high-signal ERROR / FATAL patterns.

⸻

3. The Analyst (analysis.py)

The Analyst is the Subject Matter Expert.
It synthesizes the filtered context into a technical breakdown while strictly adhering to user constraints (e.g., “Max 500 words”).

⸻

4. The Critic (critic.py)

The Gatekeeper of Truth.
The Critic compares the Analyst’s claims against the raw context. If a claim is not explicitly supported by the data, it is flagged — preventing hallucinations from reaching the final report.

⸻

Observations & Results

Live Diagnostic Demos

Document Analysis Flow: Step by result of agents parsing the EKS PDF and planning retrieval
![Analyze Video 1 at assets/doc-analysis.mov](assets/doc-analysis.mov)

Log Diagnostic Flow: Step by result of agents filtering log noise and identifying root cause
![Analyze Video 1 at assets/log-analysis.mov](assets/log-analysis.mov)

Final Report Sample:
Below is a sample final report generated after a complex log analysis, showcasing structured findings and confidence scoring:
![Analyze Output at assets/sample_output_log_analysis.gif](assets/sample_output_log_analysis.gif)

If you run these locally, you’ll see each agent’s execution printed step-by-step in the worker console, exactly as shown above.

⸻

Getting Started

1. Prerequisites
	•	Python 3.10+
	•	Docker & Docker Compose
	•	OpenAI API Key

⸻

2. Infrastructure Setup (Redis & Qdrant)

Docker is used to spin up all required infrastructure.
```bash
# Start Redis and Qdrant
docker-compose up -d
```
	•	Redis powers the background task queue
	•	Qdrant stores vector embeddings
	•	Qdrant UI is available at: http://localhost:6333

⸻

3. Application Setup

```bash
git clone https://github.com/msdokania/agentic-analysis-platform.git
cd agentic-analysis-platform

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

⸻

4. Configuration

Create a .env file in the project root:
```text
OPENAI_API_KEY=your_openai_api_key
REDIS_HOST=localhost
REDIS_PORT=6379
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=your-collection-name
```

⸻

5. Execution

Run two separate terminals:

Terminal 1 — API Server
```bash
python main.py
```

Terminal 2 — Worker
```bash
rq worker agent-jobs
```

MacOS fork-safety workaround:
```bash
OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES rq worker agent-jobs
```

⸻

First-Time Setup Note

On first run:
	1.	Place your PDF document in the data/ directory
	2.	Uncomment bootstrap_docs() in main.py
	3.	Update the filename passed to ingest_pdf()

This will ingest the document as vector embeddings into Qdrant for future retrieval.

⸻

Future Roadmap
	•	Self-Correction Loop — Critic can reject low-confidence analysis and trigger a re-run
	•	Human-in-the-Loop — Allow users to edit the plan before execution
	•	Hybrid Model Routing — GPT-4o for planning, Claude 3.5 Sonnet for analysis

⸻

🤝 Contributing

Contributions are welcome!

If you have ideas for:
	•	New agent personas
	•	Retrieval strategies
	•	Evaluation or verification techniques

Feel free to open an issue or submit a PR.
