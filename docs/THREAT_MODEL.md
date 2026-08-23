# Concord Threat Model

## Protected assets

Concord protects the integrity of immutable rule text, normalized semantic meaning, the pairwise conflict graph, explicit precedence, lifecycle history, canonical consistency state, and downstream `canon_hash` pins.

## Threat: malicious leader changes rule meaning

Example: source text prohibits an action but the leader returns `PERMIT`.

Mitigation: validators receive the original immutable text and independently verify leader normalization. Direct Mode tests include a malicious-leader case.

## Threat: leader hides a real conflict

Example: two rules cannot jointly be satisfied but the leader returns `COMPATIBLE`.

Mitigation: pairwise relation edges have their own independent validator prompt. Validators must confirm that both rules really can be obeyed together.

## Threat: model invents hierarchy

Mitigation: relation prompts are explicitly forbidden from using priority. Precedence is computed deterministically from stored priority and declared supersession.

## Threat: ambiguous prose enters strict canon

Mitigation: non-atomic or semantically incomplete rules fail closed to `AMBIGUOUS`, which blocks activation. Ambiguous pairwise relations also block admission in strict mode.

## Threat: governance rewrites history

Mitigation: active rule text and semantic interpretation are immutable. Priority can change only while a rule is blocked. Amendments create new rule nodes and explicit supersession lineage.

## Threat: later activation skips newer rules

Mitigation: every newly proposed live node is compared not only with active nodes but also with blocked nodes. A blocked rule therefore accumulates relations with rules created after it.

## Threat: unrelated rule falsely declared a replacement

Mitigation: supersession is not accepted blindly. Concord checks the semantic edge between replacement and target. `UNRELATED` or `AMBIGUOUS` replacement relations block activation.

## Threat: unresolved canon consumed as authoritative

Mitigation: consumers can call `is_consistent` or `is_consistent_for`. The latter requires both current consistency and an exact expected canon hash.

## Threat: state explosion / denial of service

Pairwise comparison is bounded by `MAX_RULES_PER_BOOK = 24`. The owner controls proposals, preventing arbitrary third-party graph spam.

## Threat: hidden mutation through priority

Priority changes are allowed only while a rule is blocked. Once active, priority is immutable. A different authority level must be represented as a new node or explicit governance transition.

## Threat: stale relation after semantic mutation

There is no semantic mutation path. Relation edges store both endpoint semantic hashes. New semantics require a new node and new edges.

## Non-goals

Concord does not decide whether a real-world action complied with a rule, move funds, execute governance proposals, infer external legal authority, prove submitted text is legally authoritative, or replace legal review. Those concerns belong to consuming applications or other primitives.
