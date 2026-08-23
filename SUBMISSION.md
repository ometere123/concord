# Concord Submission Notes

## Category

Standalone GenLayer Intelligent Contract.

No frontend. No backend. No off-chain database. The Intelligent Contract is the source of truth.

## Primitive

Concord is a reusable semantic consistency and precedence graph for natural-language rule systems.

It is intended for builders who need a constitution, policy stack, mandate set, operating agreement, or other natural-language rulebook to become shared machine-consumable state without allowing one AI response to silently decide authority.

## What consensus does

Concord has two independent non-deterministic consensus boundaries:

1. **Rule normalization**: a leader proposes a bounded semantic representation of one atomic norm. Validators independently verify that the proposal is faithful and materially complete against the immutable source rule.
2. **Rule relation analysis**: a leader proposes whether two rules are unrelated, compatible, redundant, specializing, conflicting, or ambiguous. Validators independently verify that relation against both source rules and both semantic records.

Both use `gl.vm.run_nondet_unsafe` with custom validators.

## What consensus does not do

Consensus does not choose which conflicting rule wins.

Precedence is deterministic:

- higher stored priority wins;
- equal priority remains unresolved;
- explicit valid supersession gives the replacement precedence over its target.

This keeps constitutional authority in protocol state rather than model preference.

## Meaningful persistent state

Concord stores more than one-shot receipts:

- immutable rule nodes;
- semantic hashes;
- complete live pairwise relation graph;
- conflict resolutions;
- blocked proposals;
- supersession lineage;
- repeal/restoration history;
- revision and canon versions;
- active canon hash;
- consistency status.

Later rules are compared with blocked as well as active live nodes so a blocked node can never be activated later without relation coverage against rules added after it.

## Reuse surface

Other contracts can call:

- `is_consistent(rulebook_id)`
- `is_consistent_for(rulebook_id, expected_canon_hash)`
- `current_canon_hash(rulebook_id)`
- `get_canon(rulebook_id)`
- `relation_between(left_rule_id, right_rule_id)`

The repository includes `IConcord` as a typed contract interface.

## State safety

- Individual ambiguity fails closed.
- Strict mode blocks unresolved conflicts and ambiguous relations.
- Permissive mode can intentionally expose an inconsistent active draft canon.
- Rule semantics are immutable after consensus.
- Active priority is immutable.
- Pairwise edges are pinned to semantic hashes.
- The graph is bounded to 24 nodes per rulebook to cap pairwise consensus cost.

## Tests and documentation

The repository contains:

- 26 GenLayer Direct Mode tests;
- malicious-leader normalization rejection;
- malicious relation rejection;
- deterministic priority and canon tests;
- an offline 14-check preflight;
- architecture documentation;
- consensus documentation;
- threat model;
- integration guide;
- lifecycle example;
- deployment procedure.

## Reviewer demo

A concise live demo should show:

1. create a strict treasury rulebook;
2. add a prohibition at priority 100 -> `ACTIVE`;
3. add an emergency permission at priority 100 -> `BLOCKED` with `UNRESOLVED_CONFLICT`;
4. inspect the stored `CONFLICT` edge;
5. change only the blocked rule priority to 200;
6. observe the existing edge change deterministically to `RIGHT_PREVAILS`;
7. activate the blocked rule without any new semantic LLM call;
8. pin the new `canon_hash` with `is_consistent_for`;
9. submit a superseding amendment and show immutable lineage.

That sequence demonstrates consensus, state design, deterministic mechanics, reuse, and graph compounding in one lifecycle.
