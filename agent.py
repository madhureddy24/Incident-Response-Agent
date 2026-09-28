from hindsight_client import Hindsight
from groq import Groq
import time

mem = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key="HINDSIGHT_API_KEY",
)
llm = Groq(api_key="GROQ_API_KEY")

BANK = "incident-demo-2"


def recall_context(alert):
    for _ in range(3):
        res = mem.recall(bank_id=BANK, query=alert)
        facts = [r.text for r in res.results[:25]]
        if facts:
            break
        time.sleep(3)
    print(f"[memory] recalled {len(facts)} facts")
    return "\n".join("- " + f for f in facts)


def build_prompt(alert, context):
    return f"""You are an incident response agent. A new alert just fired:

{alert}

Memory of past incidents:
{context}

RULES:
- Only use facts stated in the memory above. Never invent incidents or outcomes.
- A fix counts as FAILED only if the memory explicitly says it failed, and you must name the incident.
- If past incidents with the same pattern were fixed by a rollback, put the rollback as step 1.
- Recommend only fixes recorded as WORKED. Never recommend a fix that was recorded as FAILED anywhere.
- Keep the answer under 200 words.

Reply in this format:
1. Similar past incidents: cite EVERY relevant incident ID that appears in the memory, one line each
2. Likely root cause
3. Recommended fix (max 4 steps), based on what WORKED before
4. Fixes to AVOID (only ones recorded as FAILED, with the incident ID)
5. Confidence: X%"""


def ask_llm(prompt):
    for _ in range(3):  # retry on errors
        try:
            r = llm.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
            )
            return r.choices[0].message.content
        except Exception as e:
            print("LLM error, retrying:", e)
    return "LLM failed"