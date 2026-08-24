# Sanitized live proof

These JSON files are sanitized extracts of observed GenLayer CLI receipts and
state reads. Files named `raw-*` contain raw public RPC responses; files named
`*-summary` contain accurately labeled sanitized CLI summaries.

They intentionally omit validator private keys, credentials, and machine-local
configuration. The authoritative on-chain identifiers are the transaction
hashes, contract address, rulebook/rule/relation IDs, and final state fields.
The older lifecycle JSON files are retained as historical evidence from the
superseded deployment and are marked accordingly.
