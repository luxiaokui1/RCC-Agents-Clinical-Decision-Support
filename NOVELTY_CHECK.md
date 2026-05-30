# Novelty Check

## Working Title

Role-Conditioned Communication for Auditable Heterogeneous LLM Agents in Clinician-in-the-Loop Decision Support: A Modular Framework and Ablation Study

## Preliminary Verdict

The broad area has been studied: multi-agent LLM systems for clinical decision support, medical QA, diagnosis, triage, oncology MDT consultation, order-set optimization, and clinical prediction already exist.

The current title is therefore not novel enough if framed only as "multi-agent LLMs for clinical decision support."

The stronger and more defensible gap is:

> A modular, role-conditioned, heterogeneous-agent communication framework that studies how agent role, model family, routing policy, and evidence-verification modules interact under add/remove ablations for auditable clinician-in-the-loop decision support.

## Closest Prior Work Categories

1. Clinical multi-agent LLM systems
   - Existing work uses specialist agents, orchestrators, debate, or panel-style reasoning for clinical tasks.

2. Role-specialized clinical agents
   - Existing systems assign roles such as doctor, specialist, safety critic, or MDT member.

3. Heterogeneous or mixed-vendor LLM agents
   - Existing work studies whether diverse model families outperform homogeneous teams in clinical diagnosis.

4. Adaptive clinical agent workflows
   - Existing work adapts agent routing or workflow state to case complexity.

5. Evidence-grounded and auditable CDS
   - Existing work emphasizes citations, clinical guideline grounding, expert alignment, and traceability.

## Proposed Differentiation

The paper should not claim that role-specialized clinical agents are new.

Instead, position the contribution as:

1. Role-conditioned communication protocol
   - Each message is conditioned by sender role, receiver role, evidence requirement, permitted action, and escalation rule.

2. Heterogeneous model-family collaboration
   - Compare single-model, homogeneous multi-agent, and heterogeneous multi-agent settings.

3. Modular add/remove architecture
   - Treat retrieval, guideline verification, safety critic, uncertainty estimation, and synthesis as modules that can be ablated.

4. Adaptive routing
   - Activate expensive or critical agents only when uncertainty, disagreement, or evidence insufficiency is detected.

5. Clinician-in-the-loop framing
   - The system supports decision review and documentation, not autonomous diagnosis or treatment.

## Recommended Revised Claim

We propose a modular role-conditioned communication framework for heterogeneous LLM agents in clinical decision support. Instead of treating multi-agent collaboration as fixed debate or simple voting, the framework controls who can communicate, what evidence must be attached, when additional agents are activated, and how final decisions are escalated or abstained. We evaluate the system through module-level ablations and compare heterogeneous collaboration against single-agent, homogeneous multi-agent, RAG-only, and majority-vote baselines.
