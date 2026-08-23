# Concord Deployment

## Current repository status

The source, tests, documentation, and offline preflight are complete. The
repository has no claimed live deployment: an address and transaction hash are
intentionally omitted until a real CLI account can deploy and finalize the
exact source commit.

A live address must only be recorded after a deployment has actually finalized. Do not fabricate an address or transaction hash.

## Requirements

- Node.js and npm
- GenLayer CLI
- a funded active account for the selected network

Current official CLI documentation lists direct deployment as:

```bash
genlayer deploy --contract <contractPath>
```

Concord has no constructor arguments.

## Install CLI

```bash
npm install -g genlayer
genlayer --version
```

## Select StudioNet

```bash
genlayer network studionet
genlayer config get network
genlayer account show
```

Use an existing active account if one is already configured. Do not commit private keys or passwords to this repository.

## Deploy

```bash
genlayer deploy --contract contracts/concord.py
```

Record only real output:

```text
Network: studionet
Contract address: <finalized address>
Deployment transaction: <transaction hash>
Deployment status: <accepted/finalized>
CLI version: <version>
```

## Runtime smoke sequence

After deployment, use the Studio or CLI to execute the lifecycle in `examples/treasury_rulebook.md`.

Minimum proof should include:

1. rulebook creation;
2. first active rule;
3. equal-priority conflicting rule blocked in strict mode;
4. relation edge showing `CONFLICT` + `UNRESOLVED`;
5. blocked-rule priority update;
6. same relation edge showing deterministic precedence;
7. blocked rule activation;
8. new canon hash;
9. successful `is_consistent_for` call using that exact hash.

## Test before/after deployment

Local Direct Mode:

```bash
python -m pip install -r requirements-dev.txt
gltest tests/test_concord.py -v -s
```

Offline repository preflight:

```bash
python scripts/preflight.py
```

Hosted network integration can then be added using GenLayer Test once the finalized contract address is known.
