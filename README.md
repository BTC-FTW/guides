# Guides

Plain-text reference procedures, published openly so they stay reachable
without depending on any single machine, disk, account or service.

Everything in this repository is public by design. It contains no secrets,
no keys, no credentials and no personal information. The procedures here are
useless on their own: they describe *how* to do something, never *what* to
do it with.

## Contents

### Bitcoin seed recovery

Read these in order. Part 1 rebuilds the seed, Part 2 turns it into the
correct wallet and proves the result is right.

| | Guide | What it covers |
|---|---|---|
| 1 | [Seed reconstruction, 2-of-4 SLIP-39](bitcoin-seed-recovery/SLIP39-Recovery-Card.md) | Rebuilding a BIP-39 seed from SLIP-39 shares on an air-gapped machine, and restoring it to a hardware wallet. Includes rebuilding the required toolchain from scratch if the original media are lost. |
| 2 | [Passphrase and verification](bitcoin-seed-recovery/Passphrase-And-Verification.md) | Why the shares alone open an empty wallet, how the BIP-39 passphrase fits in, and how to use the two wallet fingerprints to prove whether a failure is a bad seed or a bad passphrase. |

> If you are following these with shares in hand: the passphrase is not in
> this repository and never will be. It is held separately, and Part 2
> explains where to look for that.

### Print version

[`print/seed-recovery-procedure.pdf`](print/seed-recovery-procedure.pdf)
holds Parts 1 and 2 as one A4 document. It is built from the two Markdown
files above by `print/build_pdf.py`, so the paper copy always matches the
text here. Rebuild it after any change to either guide.

## Why this is public

A recovery procedure is only useful if it can still be found years later,
by someone who may have none of the original equipment and no help. Anything
stored in one place eventually stops existing. Publishing the procedure costs
nothing, because the procedure is not the secret.

Mirroring and forking is encouraged. Redundancy is the entire point.

## License

[CC0 1.0 Universal](LICENSE). Public domain. Copy it, fork it, mirror it,
republish it, no attribution required.
