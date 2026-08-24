# Concord Deployment

## Current repository status

The exact source commit below is deployed and finalized on GenLayer StudioNet.
The live lifecycle evidence was collected from the active CLI account and is
recorded here so the deployment can be independently audited.

| Field | Value |
|---|---|
| Source commit | `bd6682d81afa7063d6b595dcdab04d220aed8bbb` (`Harden semantic convergence and conflict metadata policy`) |
| Network | GenLayer StudioNet |
| CLI | `genlayer@0.39.1` |
| Deployer | `0xA7EeAE0E93793e3146Cb14b0700251B8b0EBADFB` |
| Deployment transaction | `0xacfed35041fae0ca9224ab07034838145f51c2f112809e8b968814be5584a2f2` |
| Contract address | `0x67a027446838296FcB3022B376c8ff3873a4566C` |
| Deployment receipt | `FINALIZED`, `MAJORITY_AGREE`; execution `SUCCESS` |

The deployment schema was verified through the CLI and exposes 17 methods. Direct StudioNet RPC independently returned status `0x1` for the deployment transaction; its GenLayer receipt format returned `contractAddress: null`, while the CLI returned the contract address above.
The previous deployment at `0xf529EDf5291B7fB78f0ba3922b9162A593972020`
is historical because the contract source changed after that deployment.

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

## Current live evidence

The final-source deployment has a complete clean lifecycle on rulebook `1`: two CLEAR rules, a stored CONFLICT edge, equal-priority blocking, deterministic priority resolution on the same edge, activation without semantic re-analysis, and final `RESOLVED_CONFLICTS` canon state.

| Operation | Transaction | Observed result |
|---|---|---|
| Create final proof rulebook 1 | `0x9a7f171de158b3096b70b224ee70369e68740bc606bcfb7806a70d67bc2852e4` | Finalized; strict; rulebook 1 |
| Propose Rule A | `0x5925745612a28ebea221145467437dded0d8de736907a4b3398b7b2aa13b848f` | Finalized; CLEAR; ACTIVE; canon v1 |
| Propose equal-priority Rule B | `0x79ffc24bc6f70a2ca1b271851e245c5571586395d8b0e402a369de010b930340` | Finalized; CLEAR; `CONFLICT` / `UNRESOLVED`; BLOCKED |
| Set Rule B priority to 200 | `0x7b60cbeb65805a5c8a4a5c7820d672bb5bef222bb70af0633efdc5d1d9e71525` | Finalized; same relation `RIGHT_PREVAILS`; blocking reason empty |
| Activate Rule B | `0x8becc751189a7074526264ef92f770be35c9cd7e03e52fa518e4f9468701477d` | Finalized; Rule B ACTIVE; canon v2 |

## Historical live lifecycle

The following sequential transactions were finalized or observed committed
against the previous deployment. Rulebook `2` was the clean historical proof
rulebook; rulebook `1` also contains live exploratory writes but is not used for
the final proof state.

| Operation | Transaction | Observed result |
|---|---|---|
| Create proof rulebook | `0xbc95c28953b85e00447979bd0aa1b6a105f9c997c62b8a01988382bd0bb9d5e0` | Rulebook `2`, strict, canon v0, consistent |
| Propose rule 3 | `0xa4c252f40b98ead5a6bae2af60cf0493960f6ae2ae56094777f15fc8a6918c06` | Active; canon v1 `5202f13875fc753031ad2951be91637908a165ae537ddf391878f335aa968745` |
| Propose rule 4 | `0x83e4ce10d9e8c48c44305f974a61abff576767cd2e043b501cef2cdf4f299802` | Finalized; blocked; relation `CONFLICT` / `UNRESOLVED` |
| Set rule 4 priority | `0x4429817be6d9c0c348f8674e7dc395f17e65ec7f50636ae2242198450a268252` | Priority changed to `200`; same edge became `RIGHT_PREVAILS` |
| Activate rule 4 | `0xa99c6b7fbd4d251d755f067114a0a789bd8df56287a81b3d11b803ccdbdbb054` | Two active rules; `RESOLVED_CONFLICTS`; canon v2 `db9debd7e8fa063f9c824f6343263b40fedf12fa32dba1d0bda6881626aa9e30` |

Final relation readback: relation `2`, rule `3 -> 4`, kind `CONFLICT`, reason
`REQUIRE_VS_PERMIT_APPROVAL_BYPASS`, resolution `RIGHT_PREVAILS`. Final rulebook readback:
`active_count=2`, `blocked_count=0`, `relation_count=1`,
`resolved_conflicts=1`, `unresolved_conflicts=0`, `canon_status=RESOLVED_CONFLICTS`,
`consistent=true`. Exact `is_consistent_for` returned `true`; a zero hash returned
`false`.

Sanitized machine-readable artifacts are in [`proof/`](proof/): deployment,
rulebook, semantic rule, conflict, priority-update, activation, and final-state
records. They contain no private keys or credentials.

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
