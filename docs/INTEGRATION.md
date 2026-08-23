# Concord Integration Guide

## Consumer pattern: pin a constitution

A downstream contract can store:

```text
rulebook_id
expected_canon_hash
```

Before a sensitive transition, it calls Concord:

```python
concord = IConcord(concord_address)
valid = concord.view().is_consistent_for(rulebook_id, expected_canon_hash)
```

If `valid` is false, the consumer can fail closed because either the rulebook is inconsistent or active canonical state changed since the consumer pinned it.

## Consumer pattern: inspect current canon

`get_canon(rulebook_id)` returns active rules with normalized semantics and priority.

A consumer can use this as trusted shared context for a separate adjudication contract without repeating normalization work.

## Consumer pattern: inspect a conflict

`relation_between(left_rule_id, right_rule_id)` exposes semantic relation, conflict subtype, overlap description, deterministic resolution, and semantic hashes used by the edge.

This is useful for governance tooling or another Intelligent Contract deciding whether a candidate action enters a disputed part of the rule graph.

## Ownership composition

The rulebook owner is an address. It can be a normal account or another contract-controlled address depending on the governance architecture.

Concord itself does not implement voting. It is intentionally a primitive for semantic consistency and canon state.

## Recommended integration invariant

For high-stakes consumers, pin all of:

1. Concord contract address;
2. rulebook ID;
3. expected canon hash.

Do not trust only a human-readable rulebook name.

## Version handling

`revision` changes for any persisted rulebook governance change.

`canon_version` changes only when active canonical state changes.

Consumers interested only in operative rules should track `canon_version` and `canon_hash`. Audit systems interested in failed or blocked proposals may also track `revision`.
