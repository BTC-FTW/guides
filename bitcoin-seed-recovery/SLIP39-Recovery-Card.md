# SEED RECOVERY PROCEDURE — 2-of-4 SLIP-39

**PART 1 of 2.** This part rebuilds the seed. It is not sufficient on its own:
the seed alone opens a valid but **empty** wallet. Continue with
[PART 2: Passphrase and verification](Passphrase-And-Verification.md), which
explains the BIP-39 passphrase and how to confirm you have the right wallet.

**This document contains no secrets. Store one copy with each share.**
Without it, the shares are unusable.

---

## 0. WHAT YOU NEED

| Item | Notes |
|---|---|
| Any **2 of 4** shares | 33 words each. Any pair works. |
| **BIP-39 passphrase** | Stored separately. NOT contained in the shares. |
| **Tails USB** | Re-creatable — see Part B |
| **WHEELS USB** | Re-creatable — see Part A |
| Blockstream Jade (or any BIP-39 wallet) | |

**Scheme:** 2-of-4 SLIP-39 over the 256-bit BIP-39 entropy of a 24-word seed.

---

## A. RE-CREATE THE WHEELS USB (only if lost)

Requires an internet-connected Windows machine. **Do this before going offline.**

```
python -m pip download "shamir-mnemonic[cli]" mnemonic -d wheels
xcopy wheels E: /s /e
```

Expected files (versions used at creation):

```
shamir_mnemonic-0.3.0-py3-none-any.whl     SatoshiLabs SLIP-39 reference impl.
mnemonic-0.21-py3-none-any.whl             SatoshiLabs BIP-39 reference impl.
click-8.4.2-py3-none-any.whl               CLI dependency (must be >=7 <9)
colorama-0.4.6-py2.py3-none-any.whl        Windows-only, unused on Linux
```

All are `py3-none-any` (pure Python) — a wheel downloaded on Windows runs on Linux.

**If PyPI is unavailable**, build from source:
- `github.com/trezor/python-shamir-mnemonic`
- `github.com/trezor/python-mnemonic`

**If the tools are gone entirely:** SLIP-39 is a published open standard
(`github.com/satoshilabs/slips/blob/master/slip-0039.md`) and BIP-39 likewise.
Any conforming implementation will reconstruct these shares.

Format the USB as **FAT32**. Label it `WHEELS`.

---

## B. GET AND VERIFY TAILS (only if lost)

1. From `https://tails.net/install/` download:
   - `tails-amd64-<version>.img`
   - `tails-amd64-<version>.img.sig`
   - `https://tails.net/tails-signing.key`

2. Import and check the key:

```
gpg --import tails-signing.key
gpg --fingerprint A490D0F4D311A4153E2BB7CADBB802B258ACD84F
```

   Tails signing key fingerprint:
   `A490 D0F4 D311 A415 3E2B B7CA DBB8 02B2 58AC D84F`

   **Verify this fingerprint against tails.net itself and one independent source.**
   A signature check is only as good as the key it was checked against.

3. Verify the image:

```
gpg --verify tails-amd64-<version>.img.sig tails-amd64-<version>.img
```

   - `Good signature from "Tails developers"` → proceed
   - `WARNING: This key is not certified with a trusted signature` → **normal**, not tampering
   - `BAD signature` → **STOP**

4. Write to USB with Rufus or balenaEtcher. Disable Secure Boot if it won't boot.

---

## C. AIR-GAPPED ENVIRONMENT SETUP

1. **Physically disconnect the network.** Unplug ethernet. Remove or hardware-disable Wi-Fi.
2. Boot Tails. **Do not enable Persistent Storage.**
3. Open Terminal.

**Extract the tools** (must be one continuous line):

```
mkdir -p /home/amnesia/slip39lib
for w in /media/amnesia/WHEELS/*.whl; do python3 -m zipfile -e "$w" /home/amnesia/slip39lib/; done
```

> If the mount path differs, find it with `ls /media/amnesia/`

**Verify the tools load from the USB, not from Tails' own Python:**

```
cd /home/amnesia
PYTHONPATH=/home/amnesia/slip39lib python3 -c "import mnemonic, click, shamir_mnemonic; print(mnemonic.__file__); print(click.__file__)"
```

Both paths **must** begin `/home/amnesia/slip39lib/`.
Run from `/home/amnesia`, not from inside `slip39lib`.

**Sanity-check the BIP-39 conversion against a known test vector:**

```
PYTHONPATH=/home/amnesia/slip39lib python3 -c "
from mnemonic import Mnemonic
m='abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art'
print(Mnemonic('english').to_entropy(m).hex())
"
```

Must print **64 zeros**. If not, the toolchain is wrong — stop.

---

## D. RECOVER THE SEED

**Step 1 — Combine 2 shares into the master secret:**

```
PYTHONPATH=/home/amnesia/slip39lib python3 -m shamir_mnemonic.cli recover
```

- Enter each share's 33 words **in exact written order**. Word order within a share is critical.
- The order in which you enter the two shares does not matter.
- It stops prompting after the second share and prints a hex string.

**Step 2 — Convert the hex to 24 BIP-39 words:**

```
PYTHONPATH=/home/amnesia/slip39lib python3 -c "
from mnemonic import Mnemonic
print(Mnemonic('english').to_mnemonic(bytes.fromhex('PASTE_HEX_HERE')))
"
```

⚠️ **The hex is your complete seed. Never write it down, save it, or photograph it.**
It exists only in RAM.

---

## E. RESTORE TO JADE

1. `Setup Jade` → `Advanced Setup` → `Restore Wallet` → `24 Words`
2. Enter the 24 words from Step D2.
3. Enter the **BIP-39 passphrase** when prompted (stored separately from these shares).
4. Set a new PIN.
5. **Confirm the wallet fingerprint** (bottom right of Jade's screen).

**Do not interpret a fingerprint mismatch here on its own.** A single value
cannot tell you whether the seed or the passphrase is at fault. Follow the
two-stage check in
[PART 2, section 2](Passphrase-And-Verification.md#2-the-fingerprint-check):
verify the seed first with no passphrase, then add the passphrase. Only then
does a mismatch identify which step failed.

---

## F. TEARDOWN

1. **Shut down Tails completely** — not reboot. RAM is wiped on shutdown.
2. Reconnect to the internet only after full shutdown.
3. Destroy any scratch paper used during recovery.

---

## REFERENCE DATA

*(no secrets — fill in and keep with this card)*

```
Wallet fingerprint, no passphrase    : ________________
Wallet fingerprint, WITH passphrase  : ________________
Firmware at creation                 : Jade Plus 1.0.40 noradio
Derivation path                      : m/84'/0'/0'   (Native SegWit)
Scheme                               : 2-of-4 SLIP-39, single group
Date created                         : ________________
Share 1 location                     : ________________
Share 2 location                     : ________________
Share 3 location                     : ________________
Share 4 location                     : ________________
Passphrase location(s)               : ________________
```

---

## HOW THIS WAS CREATED (reference only)

```
# 24 words -> entropy hex
PYTHONPATH=/home/amnesia/slip39lib python3 -c "
from mnemonic import Mnemonic
print(Mnemonic('english').to_entropy('<24 words>').hex())
"

# split into 2-of-4
PYTHONPATH=/home/amnesia/slip39lib python3 -m shamir_mnemonic.cli create 2of4 -S <hex>
```

The SLIP-39 `-p/--passphrase` option was **NOT** used.
SLIP-39 and BIP-39 mix passphrases differently; using it would not reproduce this wallet.

---

## CRITICAL NOTES

- **The shares reconstruct the SEED ONLY.** Seed without the correct BIP-39 passphrase
  opens a different, empty wallet. Both are required.
- **Any 1 share alone reveals nothing.** Any 2 of the 4 reconstruct fully.
- **Word order within a share is critical.** Share-to-share order is irrelevant.
- **Never enter these shares or the seed into any internet-connected device.**
- Verify shares annually: check humidity indicators, inspect for damage.
- Rewrite paper every 5–10 years.
- Re-test recovery periodically — a backup untested is a backup unproven.
