# Capstone Architecture Note — Support Agent with Redis, Vector Recall, Async Queue, and Human Approval

## Goal
Extend the Lab 2 chaining notebook into a small support agent that can answer support questions, look up orders, trigger operational follow-ups asynchronously, and require human approval for sensitive actions.

## Core design
a tool-using support agent with Redis + an event queue — and adds:
1. Redis short-term memory for per-session conversation state.
2. Vector store long-term recall for knowledge-base / FAQ retrieval.
3. At least 3 tools, including one async queue-backed tool.
4. Routing + chaining so the agent can decide which tools to call and in what order.
5. Human approval gate for risky actions (refunds, cancellations, address changes).
6. Tracing, retries, and prompt caching for reliability and observability.

## Components
- Support agent orchestrator
- Redis short-term memory
- Vector store KB retrieval
- SQLite operational store for orders / refund requests
- Redis Stream async tool + worker + job status
- Human approval gate before sensitive actions

## Tools
- search_kb(query)
- lookup_order(order_id)
- create_refund_request(order_id, reason)
- send_followup_email(to, subject, body)  # async queue-backed
- check_job(job_id)

## Routing examples
- FAQ / policy question -> KB search
- Order status -> order lookup (+ optional KB note)
- Refund / cancellation -> lookup -> approval gate -> action -> async confirmation
- Follow-up / notify -> async email job

It demonstrates all required capabilities in one compact notebook:
- Redis short-term memory
- vector-store long-term recall
- 3+ tools with one async queue-backed tool
- routing + chaining + human approval
- tracing + retries + prompt caching
