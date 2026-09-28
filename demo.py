import time
from agent import mem, BANK, recall_context, build_prompt, ask_llm


def show(title, text):
    print("\n" + "=" * 70 + "\n" + title + "\n" + "=" * 70 + "\n" + text)


alert1 = "payments-api: 500 errors and DB connection timeouts started 5 minutes after deploy v3.3"

# RUN 1: WITHOUT memory (generic agent)
show("RUN 1: NO MEMORY", ask_llm(
    f"You are an incident response agent. Alert: {alert1}. "
    "Suggest a fix and a confidence %. Keep it under 200 words."))

# RUN 2: WITH Hindsight memory
show("RUN 2: WITH MEMORY", ask_llm(build_prompt(alert1, recall_context(alert1))))

# Engineer resolves the incident and the agent learns from it
print("\nEngineer resolves the incident and gives feedback...")
mem.retain(bank_id=BANK, content=(
    "Incident INC-013 on payments-api: 500 errors and DB connection timeouts 5 minutes "
    "after deploy v3.3, same pattern as INC-010. Fix attempted: restarting payments-api pods. "
    "Outcome: FAILED. Root cause: connection leak in the new retry logic. Fix that worked: "
    "rolling back deploy v3.3. Outcome: WORKED."))
print("Saved to Hindsight memory. Waiting for it to process...")
time.sleep(30)

# RUN 3: a variant incident on a different service
alert2 = "orders-api: 500 errors and DB connection timeouts started 8 minutes after deploy v5.1"
show("RUN 3: VARIANT, AGENT HAS LEARNED", ask_llm(build_prompt(alert2, recall_context(alert2))))