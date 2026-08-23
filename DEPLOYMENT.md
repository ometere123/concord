# Concord Deployment

## Current repository status

The exact source commit below is deployed and finalized on GenLayer StudioNet.
The live lifecycle evidence was collected from the active CLI account and is
recorded here so the deployment can be independently audited.

| Field | Value |
|---|---|
| Source commit | `faee334f046fded76a6dd2b79d268d6495d285cf` |
| Network | GenLayer StudioNet |
| CLI | `genlayer@0.39.1` |
| Deployer | `0xB5EcD6dDa36B370aca4af5E2005d8E2Ae89c6db2` |
| Deployment transaction | `0x0be1d2477393f618193ee01d10b019eb7056608d3b2b0b89183eaadbe4a3aa1b` |
| Contract address | `0xf529EDf5291B7fB78f0ba3922b9162A593972020` |
| Deployment receipt | `FINALIZED`, `MAJORITY_AGREE`; execution `SUCCESS` |

The deployment schema was verified through the CLI and exposes 15 methods.

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
    genlayer network set studionet
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

## Verified live lifecycle

The following transactions were finalized or observed committed against the
deployed address above:

| Operation | Transaction | Observed result |
|---|---|---|
| Create rulebook | `0xa421b31af1a96b3faf5f5fd8090975cd6b4bbd120ae3688148c887821d1a2fe7` | Rulebook `1`, strict, canon v0, consistent |
| Propose rule 1 | `0xdf5e1f0b390ad986f4902b3b140bcd68f998da14a7add0604c5e87022d0d6b8a` | Active; canon v1 `86a4e0d1b951554f38a3c397c6378c934024a912022e11e3c61aab1d592a7462` |
| Propose rule 2 | `0x116755b375df715e4699b5cbb4541064c3a14fe685616cad824343a04f5e3407` | Finalized; blocked; relation `CONFLICT` / `UNRESOLVED` |
| Set rule 2 priority | `0xb8971c375143486b4bfb5aeedc2eadb0f975e7a6a17bcdcf2ebd7a8ab8127478` | Priority changed to `200` |
| Activate rule 2 | `0x416ab079d2477e42eac76b203fcdc597b5957bee55e1cc6aa5d3fb43ac1759ed` | Two active rules; consistent; canon v2 `058c677f64bc7fcc80b5a4af1d5b7c98b01df35528deef84a7ecc45a976dc750` |

Final relation readback: relation `1`, rule `1 -> 2`, kind `CONFLICT`, reason
`EMERGENCY_OVERRIDE`, resolution `RIGHT_PREVAILS`. Final rulebook readback:
`active_count=2`, `blocked_count=0`, `relation_count=1`,
`unresolved_conflicts=0`, `consistent=true`.

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
