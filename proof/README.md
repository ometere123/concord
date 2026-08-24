# Sanitized live proof

These JSON files are sanitized extracts of observed GenLayer CLI receipts and
state reads. Files named `raw-*` contain raw public RPC responses; files named
`*-summary` contain accurately labeled sanitized CLI summaries.

They intentionally omit validator private keys, credentials, and machine-local
configuration. The authoritative on-chain identifiers are the transaction
hashes, contract address, rulebook/rule/relation IDs, and final state fields.
The `final-*` files are the final-source lifecycle evidence for commit
`bd6682d81afa7063d6b595dcdab04d220aed8bbb` at
`0x67a027446838296FcB3022B376c8ff3873a4566C`.
The older lifecycle JSON files are retained as historical evidence from the
superseded deployment and are marked accordingly.
