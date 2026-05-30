# Research Brief

## Topic
Role-Conditioned Communication for Auditable Heterogeneous LLM Agents in Clinician-in-the-Loop Decision Support: A Modular Framework and Ablation Study

## Target Venue
Primary: AMIA / IEEE JBHI / ACM CHIL workshop / NeurIPS Datasets and Benchmarks or ML4H workshop.
Fallback: healthcare AI workshop paper, systems paper, or applied AI conference paper.

## Core Question
How can heterogeneous LLM agents collaborate through role-conditioned communication to provide more reliable, evidence-grounded, and auditable clinical decision support than a single-agent or homogeneous multi-agent baseline?

The work should be framed as a research prototype for clinician-in-the-loop assistance, not an autonomous diagnosis or treatment system.

## Starting Point
- Core title: "Role-Conditioned Communication for Auditable Heterogeneous LLM Agents in Clinician-in-the-Loop Decision Support: A Modular Framework and Ablation Study"
- Candidate datasets/tasks:
  - medical QA: MedQA, PubMedQA, MedMCQA, MIMIC-derived note QA if accessible
  - clinical summarization or guideline-grounded recommendation tasks
  - synthetic case vignettes with evidence references
- Candidate baselines:
  - single LLM agent
  - homogeneous multi-agent debate
  - RAG-only agent
  - majority-vote ensemble
  - role-conditioned heterogeneous agent collaboration
- Candidate agent roles:
  - clinician reasoning agent
  - evidence retrieval agent
  - guideline verification agent
  - risk/safety critic
  - patient-context summarizer
  - final synthesis agent
- Main mechanism:
  - role-conditioned communication protocol
  - modular agent registry
  - evidence-grounded message passing
  - confidence/uncertainty and escalation logic
  - traceable final answer with cited evidence

## Constraints
- Compute budget: start with small-scale local CUDA experiments; scale later if results are promising.
- Deadline: TBD.
- Must-use methods or datasets: use public, de-identified, non-sensitive datasets only.
- Things to avoid:
  - no autonomous clinical diagnosis claims
  - no real patient data unless properly de-identified and authorized
  - no unsupported treatment recommendation claims
  - no fabricated citations or clinical guidelines
  - no claim that the system replaces clinicians

## Desired Output
First stage:
- literature review
- novelty check
- related work map
- system architecture
- experiment plan
- ablation plan for adding/removing modules

Second stage:
- runnable prototype
- evaluation scripts
- preliminary result tables
- paper outline and draft
