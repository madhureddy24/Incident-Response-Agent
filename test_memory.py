from hindsight_client import Hindsight

mem = Hindsight(
    base_url="https://api.hindsight.vectorize.io",  # check in docs
    api_key="hsk_7d1983aa11554d268a3c3f7e40efd463_26ba0e80d4bdce17",
)

BANK = "incident-agent"

mem.retain(
    bank_id=BANK,
    content="Incident INC-001 on payments-api: 500 errors, DB connection timeouts "
            "after deploy. Root cause: connection pool exhaustion. "
            "Fix: increased pool size and restarted service. Outcome: WORKED.",
)

print(mem.recall(bank_id=BANK, query="payments service timing out after deploy"))