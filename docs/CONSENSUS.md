# Concord Consensus Model

## Why custom validation is necessary

Two validators can faithfully interpret the same prose with slightly different wording. Exact string equality over actor/action summaries would reject many substantively equivalent interpretations.

Concord therefore uses non-comparative validation with `gl.vm.run_nondet_unsafe`.

The leader proposes a bounded result. A validator independently checks whether the leader result is substantively faithful to the immutable source material.

## Boundary 1: normalization

### Leader task

The leader receives immutable rulebook purpose and immutable candidate rule text, then proposes one canonical semantic object:

```json
{
  "modality": "REQUIRE | PERMIT | PROHIBIT",
  "actor": "...",
  "action": "...",
  "object": "...",
  "condition": "...",
  "exception": "...",
  "scope": "...",
  "semantic_state": "CLEAR | AMBIGUOUS"
}
```

### Deterministic canonicalization

Before storage, the result is converted to bounded enums and strings.

A missing actor/action, unknown modality, or non-atomic rule fails closed to `AMBIGUOUS`.

### Validator task

The validator receives the original rule and leader candidate and checks whether the candidate:

- uses the correct modality;
- preserves material conditions;
- preserves explicit exceptions;
- does not invent authority or scope;
- does not collapse multiple independent norms;
- does not claim a distorted interpretation is clear.

The validator returns a boolean acceptance decision.

## Boundary 2: relation analysis

### Leader task

The leader receives two immutable rule texts and their accepted semantic records and proposes one relation enum:

- `UNRELATED`
- `COMPATIBLE`
- `REDUNDANT`
- `SPECIALIZES`
- `CONFLICT`
- `AMBIGUOUS`

A conflict requires a plausible shared case in which both rules apply but cannot both be satisfied.

### Validator task

The validator independently checks the proposed edge against both source rules.

It is specifically instructed to reject:

- `UNRELATED` when material overlap exists;
- `COMPATIBLE` when both norms cannot jointly be satisfied;
- `CONFLICT` when no plausible shared case exists;
- confident classification when the relation is genuinely ambiguous.

## Precedence is not consensus output

Priority is intentionally excluded from relation prompts.

After a `CONFLICT` edge is accepted, deterministic code resolves it using explicit stored priority or declared supersession.

This prevents validators or an LLM from becoming an implicit constitutional authority.

## Prompt-injection boundary

Rulebook purpose, rule text, and candidates are wrapped as untrusted data and prompts explicitly instruct the model not to obey instructions inside those blocks.

The same source material is re-presented to independent validators, so a leader cannot unilaterally exploit injected instructions to determine accepted state.

Concord still treats prompt injection as a model-layer risk, which is why outputs are bounded, validator-reviewed, and unable to choose priority.

## Consensus failure behavior

If validators reject a leader result, the transaction does not safely finalize with that semantic state.

The contract does not silently coerce rejected or malformed outputs into active canon.
