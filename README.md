# Incident-Response-Agent

An incident-response agent that uses **Hindsight persistent memory** to recall previous incidents, learn from successful and failed fixes, and apply that experience to new incidents.

## Overview

Incident response often involves recognizing patterns from previous failures. An engineer may already know that a particular deployment caused a similar issue before, but that knowledge is not always available to an AI agent when it needs to make a recommendation.

This project explores how persistent memory can change that behavior.

The agent receives an incident alert, retrieves relevant historical incidents from Hindsight, and provides a response using both the current alert and the recalled context. After an engineer resolves the incident, the outcome is stored back into memory so it can be useful for future incidents.

The demonstration compares the agent's response **without memory**, **with memory**, and then tests the learned information on a **new variant of the incident**.

## How It Works

```text
Incident Alert
      ↓
Incident Response Agent
      ↓
Recall relevant history from Hindsight
      ↓
LLM analyzes the incident with historical context
      ↓
Recommended action
      ↓
Engineer provides feedback
      ↓
Store the outcome in Hindsight
      ↓
Future incidents can recall the experience
```

The core feedback loop is:

```text
Recall → Respond → Resolve → Retain → Recall Again
```

## Demonstration

The project uses a database connection failure following a deployment to demonstrate the effect of persistent memory.

### Run 1 — No Memory

The agent receives the current alert without historical context:

```text
payments-api: 500 errors and DB connection timeouts
started 5 minutes after deploy v3.3
```

The agent provides a general incident-response recommendation based only on the information in the alert.

### Run 2 — With Memory

The same type of incident is processed with relevant information recalled from Hindsight.

Historical incidents include information such as:

```text
Incident: INC-013
Service: payments-api

Problem:
500 errors and database connection timeouts
after deployment v3.3

Attempted fix:
Restarting payments-api pods

Outcome:
FAILED

Root cause:
Connection leak in the new retry logic

Successful fix:
Rolling back deployment v3.3

Outcome:
WORKED
```

This gives the agent access to previous operational experience before it generates its recommendation.

### Engineer Feedback

After the incident is resolved, the engineer's experience is retained in Hindsight.

The stored information includes:

* What happened
* What fix was attempted
* Whether the fix worked
* The identified root cause
* Which action successfully resolved the incident

### Run 3 — Learned Variant

A different incident is then introduced:

```text
orders-api: 500 errors and DB connection timeouts
started 8 minutes after deploy v5.1
```

Although the service and deployment version are different, the failure pattern is similar.

The agent recalls relevant historical incidents and uses that experience when responding to the new alert.

This demonstrates the main idea of the project: **persistent memory allows an agent to reuse experience instead of treating every incident as completely new.**

## Hindsight Integration

Hindsight acts as the persistent memory layer for the agent.

### Recall

Before generating a response, the agent retrieves relevant memories:

```python
context = recall_context(alert)
response = ask_llm(build_prompt(alert, context))
```

The recalled information is added to the prompt so the LLM can consider previous incidents and their outcomes.

### Retain

After an incident is resolved, the engineer's feedback is stored:

```python
mem.retain(
    bank_id=BANK,
    content="Incident INC-013 ... rollback v3.3 WORKED ..."
)
```

This creates a feedback loop where future incidents can benefit from previously stored experience.

## Before vs After Memory

### Without Persistent Memory

```text
Current Alert
     ↓
LLM
     ↓
General Recommendation
```

### With Hindsight Memory

```text
Current Alert
     ↓
Hindsight Recall
     ↓
Previous Incidents + Outcomes
     ↓
LLM
     ↓
Context-Aware Recommendation
```

## Project Structure

```text
Incident-Response-Agent/
│
├── agent.py
├── demo.py
├── seed.py
├── test_memory.py
├── requirements.txt
├── .gitignore
└── README.md
```

### File Description

| File               | Purpose                                                         |
| ------------------ | --------------------------------------------------------------- |
| `agent.py`         | Agent logic, LLM interaction and Hindsight memory integration   |
| `demo.py`          | Runs the complete three-stage demonstration                     |
| `seed.py`          | Adds historical incident information to memory                  |
| `test_memory.py`   | Tests memory retrieval and related functionality                |
| `requirements.txt` | Python dependencies required by the project                     |
| `.gitignore`       | Prevents secrets and local/generated files from being committed |

## Technology Stack

* **Python**
* **Hindsight** — persistent memory for the agent
* **Groq** — LLM inference
* **python-dotenv** — environment variable management

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/madhureddy24/Incident-Response-Agent.git
cd Incident-Response-Agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

On Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a local `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
HINDSIGHT_API_KEY=your_hindsight_api_key
```

**Never upload `.env` or API keys to the repository.**

The `.gitignore` file is configured to keep environment files out of Git.

### 5. Seed historical memories

```bash
python seed.py
```

### 6. Run the demonstration

```bash
python demo.py
```

The demonstration runs through:

```text
RUN 1: NO MEMORY
        ↓
RUN 2: WITH MEMORY
        ↓
Engineer feedback is retained
        ↓
RUN 3: VARIANT, AGENT HAS LEARNED
```

## What This Demonstrates

The project focuses on a specific behavior change:

**Without memory:** the agent reasons primarily from the current incident.

**With memory:** the agent can also use relevant previous incidents, including failed attempts and successful resolutions.

The third run tests whether that stored experience remains useful when the incident changes to another service and deployment version.

## Limitations

This is a focused prototype rather than a production incident-management system.

The demonstration uses a controlled set of incident examples and does not establish production-level reliability or response accuracy. Recommendations should still be reviewed by an engineer before any operational action is taken.

The usefulness of the system also depends on the quality, relevance and accuracy of the information stored in memory.

## Key Takeaway

The goal of this project is not simply to make an LLM generate incident-response suggestions.

It is to explore what changes when an agent can **remember previous incidents, including what failed, what worked, and why**.

Hindsight provides the persistent memory layer that makes this feedback loop possible.

## Resources

* [Hindsight GitHub Repository](https://github.com/vectorize-io/hindsight)
* [Hindsight Documentation](https://hindsight.vectorize.io/)
* [What is Agent Memory? — Vectorize](https://vectorize.io/what-is-agent-memory)

## Author

**Madhulatha Reddy**

GitHub: https://github.com/madhureddy24
