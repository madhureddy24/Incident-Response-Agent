from hindsight_client import Hindsight
import time

mem = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key="hsk_7d1983aa11554d268a3c3f7e40efd463_26ba0e80d4bdce17",
)
BANK = "incident-demo-2"

incidents = [
 "Incident INC-002 on checkout-service: p99 latency spiked to 8s and DB connection timeouts began 10 minutes after deploy v2.14. Fix attempted: increased connection pool size. Outcome: FAILED, timeouts returned within 20 minutes. Actual root cause: new ORM code leaked connections. Fix that worked: rolled back deploy v2.14. Outcome: WORKED, recovery in 4 minutes.",
 "Incident INC-003 on orders-db: read replica lag reached 90 seconds and order pages showed stale data. Fix attempted: failed over to replica. Outcome: FAILED, replica was too far behind and caused data inconsistency. Root cause: long-running analytics query blocking replication. Fix that worked: killed the analytics query and throttled the reporting job. Outcome: WORKED.",
 "Incident INC-004 on auth-service: pods repeatedly OOMKilled, users could not log in. Fix attempted: raised memory limit from 512Mi to 1Gi. Outcome: FAILED, pods crashed again after 2 hours. Root cause: token cache memory leak. Fix that worked: patched cache TTL and restarted pods. Outcome: WORKED.",
 "Incident INC-005 on search-api: Elasticsearch cluster turned read-only, searches returned 503. Root cause: disk usage passed the 95% flood-stage watermark. Fix: deleted old log indices and removed the read-only block. Outcome: WORKED.",
 "Incident INC-006 on payments-api: 502 errors from the load balancer, TLS handshake failures. Root cause: expired TLS certificate. Fix: renewed the certificate and reloaded nginx. Outcome: WORKED. Follow-up: added a cert expiry alert.",
 "Incident INC-007 on notification-service: RabbitMQ queue backlog of 400k messages, emails delayed by hours. Fix attempted: purged the queue. Outcome: FAILED, customers lost order confirmation emails. Root cause: consumer crash loop after bad message. Fix that worked: scaled consumers to 6 and moved the poison message to a dead-letter queue. Outcome: WORKED.",
 "Incident INC-008 on cart-service: carts randomly emptied. Root cause: Redis hit maxmemory and evicted keys. Fix: increased Redis maxmemory and set eviction policy to volatile-lru. Outcome: WORKED.",
 "Incident INC-009 on api-gateway: sudden 429 Too Many Requests for all clients after deploy. Root cause: rate limit config changed from 1000 to 100 requests per minute by mistake. Fix: rolled back gateway config. Outcome: WORKED.",
 "Incident INC-010 on payments-api: DB connection timeouts and 500 errors after deploy v3.2, similar to INC-001. Fix attempted: restarted the service only. Outcome: FAILED, timeouts came back in 15 minutes. Root cause: connection leak in new code. Fix that worked: rolled back deploy v3.2. Outcome: WORKED.",
 "Incident INC-011 on inventory-service: CPU at 100% and slow responses during a flash sale. Root cause: missing index on the stock table causing full table scans. Fix: added a composite index concurrently. Outcome: WORKED.",
 "Incident INC-012 on user-profile-service: image uploads failing with 403 errors. Root cause: S3 bucket policy changed by a Terraform apply. Fix: reverted the Terraform change. Outcome: WORKED.",
]

for text in incidents:
    mem.retain(bank_id=BANK, content=text)
    print("retained:", text[:50])

print("Waiting for Hindsight to process...")
time.sleep(30)

res = mem.recall(bank_id=BANK,
    query="checkout service latency and DB connection timeouts after deploy")
for r in res.results:
    print("-", r.text)