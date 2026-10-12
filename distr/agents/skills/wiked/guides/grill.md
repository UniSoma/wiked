# Mandatory Grill

Load this guide before creating or changing governed operational content in a consumer instance. Methodology evolution belongs to Wiked's source repository and authoring authority. A read-only query or review needs no grill unless the user asks to qualify its objective.

## Prepare

1. Confirm the session is operational and have the participating human state explicitly that they are qualified to govern the current objective. Never infer qualification from identity, organizational role, ticket assignment, or instance configuration; renew it for a new session or substantive objective.
2. State one coherent objective and its initial file scope.
3. Load the applicable instance context, rules, affected content, and read-only checks.

## Interview

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Each question should be formatted like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree — settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it — don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report — ask the rest of the frontier now. The _decisions_ are the user's — put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

Before closure, keep resolved terms and definitions in the conversation or in Knot tickets and notes. These records may preserve decisions or lateral discoveries without expanding scope; they do not authorize governed-content changes. Unresolved decisions remain open.

Resolving a term during the interview does not authorize writing it to the instance context file. Like any governed-content change, that write requires explicit confirmation of the final summary first. There is no in-session exception for terms or incidental edits to other governed content.

## Close

When no in-scope decision remains:

1. Summarize the objective, scope, decisions (including agreed terms and definitions), exceptions, affected content, and lateral pending issues. Distinguish unresolved decisions from agreed terms; records made during the interview do not substitute for confirmation.
2. Have the confirmed qualified operator explicitly confirm that the summary represents mutual understanding.
3. Continue the interview after any correction, qualification, or rejection.
4. Consolidate only after confirmation and within the confirmed scope.

If implementation exposes a new substantive decision, stop and resume the grill.
