# PART 1: SEED RECOVERY, 2-of-4 SLIP-39

**This part rebuilds the seed. It is not enough on its own.** The seed alone
opens a valid but **empty** wallet. After this part, continue with
[PART 2: Passphrase and verification](Passphrase-And-Verification.md), which
explains the BIP-39 passphrase and how to prove you have the right wallet.

**This document contains no secrets. Keep one copy with each share.**
Without it, the shares are very hard to use.

> **HOW TO READ THIS CARD**
>
> Every grey box under a numbered step (A1, C3, D1 and so on) holds
> **exactly one command**. Type it, press Enter, then go to the next box.
>
> A box marked `[ONE LINE]` is a single line, even where the paper wraps it.
> Do not press Enter until you have typed all of it.
>
> Replace anything written in `<angle brackets>` with the real value, and
> leave out the brackets themselves.

---

## 0. WHAT YOU NEED

| Item | Notes |
|---|---|
| Any **2 of 4** shares | 33 words each. Any pair works. |
| **BIP-39 passphrase** | Kept separately. NOT contained in the shares. See Part 2. |
| **Tails USB** | Can be re-created, see section B |
| **WHEELS USB** | Can be re-created, see section A |
| A laptop or PC with an Intel or AMD processor | Tails does not start on Macs with Apple chips (M1 and later) |
| Blockstream Jade, Coinkite COLDCARD Q, or any BIP-39 wallet | A Jade Plus was used at creation |

**Scheme:** 2-of-4 SLIP-39 over the 256-bit BIP-39 entropy of a 24-word seed.

---

## A. RE-CREATE THE WHEELS USB (only if lost)

Needs a Windows computer with internet access and Python 3.10 or newer.
Install Python from `python.org` with the default options, then open a new
**Command Prompt**. **Do this before going offline.**

**A1.** Download the packages `[ONE LINE]`

```
py -m pip download "shamir-mnemonic[cli]==0.3.0" "mnemonic==0.21" "click==8.4.2" -d wheels
```

> If Windows says `py` is not recognized, type `python` instead of `py` at
> the start of A1. A notice that a new pip release is available is harmless.

**A2.** Format a USB stick as FAT32 and name it `WHEELS`. If Windows only
offers exFAT (sticks over 32 GB), exFAT works too. Copy the files to it. Here
the stick is drive `E:`, use the letter your stick has.

```
xcopy wheels E: /s /e
```

The stick must now hold exactly these four files:

| File | Role |
|---|---|
| `shamir_mnemonic-0.3.0-py3-none-any.whl` | SatoshiLabs SLIP-39 reference implementation |
| `mnemonic-0.21-py3-none-any.whl` | SatoshiLabs BIP-39 reference implementation |
| `click-8.4.2-py3-none-any.whl` | Command line helper, needed by the first one |
| `colorama-0.4.6-py2.py3-none-any.whl` | Windows only, unused on Tails |

All are `py3-none-any` (pure Python), so a file downloaded on Windows runs on
Tails. The versions are pinned on purpose: a re-created stick then holds the
same code that made the shares.

**If PyPI is unavailable**, build the same versions from source:
`github.com/trezor/python-shamir-mnemonic` (version 0.3.0) and
`github.com/trezor/python-mnemonic` (version 0.21).

**If the tools are gone entirely:** SLIP-39 is a published open standard
(`github.com/satoshilabs/slips/blob/master/slip-0039.md`), and so is BIP-39.
Use an implementation of the **2024 revision** of SLIP-39. These shares carry
the "extendable backup" flag introduced in that revision, and an
implementation from before 2024 will not decode them correctly.

---

## B. GET AND VERIFY TAILS (only if lost)

Needs a computer with internet access and GnuPG. On Windows, install
Gpg4win from `gpg4win.org` and type the commands below in Command Prompt.

**B1.** Open `https://tails.net/install/download/` and save these three
links into one folder (about 1.8 GB in total):

| Link on the page | File you get |
|---|---|
| **Download Tails** `<version>` **USB image** | `tails-amd64-<version>.img` |
| **OpenPGP signature** | `tails-amd64-<version>.img.sig` |
| **OpenPGP signing key** | `tails-signing.key` |

Then open the terminal in that folder. On Windows: open the folder in File
Explorer, click the address bar, type `cmd` and press Enter.

**B2.** Import the signing key

```
gpg --import tails-signing.key
```

It ends with `imported: 1`. Lines saying that folders were created, that
signatures were not checked, or that no ultimately trusted keys were found,
are normal.

**B3.** Show its fingerprint `[ONE LINE]`

```
gpg --fingerprint A490D0F4D311A4153E2BB7CADBB802B258ACD84F
```

The first fingerprint, on the line below `pub`, must be exactly this (gpg
leaves a wider gap in the middle). Newer gpg versions list more fingerprints
below it, for the subkeys. Those are normal.
**`A490 D0F4 D311 A415 3E2B B7CA DBB8 02B2 58AC D84F`**

> **Check this fingerprint against tails.net itself AND one independent
> source.** A signature check is only as good as the key it was checked
> against.

**B4.** Verify the image. Replace `<version>` with the number in the file
name you downloaded. `[ONE LINE]`

```
gpg --verify tails-amd64-<version>.img.sig tails-amd64-<version>.img
```

| Output | Meaning |
|---|---|
| `Good signature from "Tails developers"` | Proceed |
| `WARNING: This key is not certified with a trusted signature` | Normal, not tampering |
| `BAD signature` | **STOP** |

**B5.** Write the `.img` file to a USB stick of 8 GB or more with
balenaEtcher or Rufus. Everything already on that stick is erased.

---

## C. AIR-GAPPED ENVIRONMENT SETUP

1. **Physically disconnect the network.** Unplug the network cable. Switch
   Wi-Fi off, with the hardware switch if the laptop has one.
2. Plug in the Tails USB and switch the computer on. Straight away, press
   the boot menu key (often F12, F9, F11 or Esc, it depends on the brand) and
   choose the USB stick. If Tails will not start, switch off Secure Boot in
   the computer's setup screen and try again.
3. On the Tails **Welcome Screen**:
   - Set **Keyboard Layout** to match the keyboard in front of you
     (for example AZERTY or QWERTY). **A wrong layout garbles every command
     and every share word.**
   - Under **Additional Settings**, add **Offline Mode** and switch it on.
   - Do **not** create or unlock Persistent Storage.
   - Click **Start Tails**.
4. Open a Terminal: press the Windows key, type `Terminal`, press Enter.
5. Plug in the WHEELS USB.

> **Copy and paste in the Terminal:** select text with the mouse, then press
> **Ctrl+Shift+C** to copy and **Ctrl+Shift+V** to paste. Right-click also
> offers Copy and Paste. Plain Ctrl+C does **not** copy: it cancels the
> running command.

**C1.** Create the tools folder

```
mkdir -p /home/amnesia/slip39lib
```

**C2.** Go to the WHEELS stick

```
cd /media/amnesia/WHEELS
```

> If that fails, open the **Files** app and click the WHEELS stick once, then
> try again. To see the names of the mounted sticks, type `ls /media/amnesia/`

**C3.** Unpack all four files onto the tools folder `[ONE LINE]`

```
for w in *.whl; do python3 -m zipfile -e "$w" /home/amnesia/slip39lib/; done
```

**C4.** Tell Python where the tools are. Every later command relies on this.

```
export PYTHONPATH=/home/amnesia/slip39lib
```

> This lasts only for THIS terminal window. If you open a new one, run C4
> again.

**C5.** Go back to the home folder

```
cd /home/amnesia
```

**C6.** Confirm the tools load from the USB copy, not from Tails' own Python
`[ONE LINE]`

```
python3 -c "import mnemonic, click, shamir_mnemonic; print(mnemonic.__file__); print(click.__file__); print(shamir_mnemonic.__file__)"
```

All three printed lines **must** begin `/home/amnesia/slip39lib/`.
If any line shows `/usr/lib/python3/`, or you see `ModuleNotFoundError`,
redo C1 to C4.

**C7.** Test the BIP-39 tool against a known test value `[ONE LINE]`

```
python3 -c "from mnemonic import Mnemonic; print(Mnemonic('english').to_entropy('abandon '*23+'art').hex())"
```

Note the space after `abandon`, inside the quotes. It must print **64 zeros**.
If it does not, the tools are wrong: stop.

---

## D. RECOVER THE SEED

**D1.** Combine two shares into the master secret

```
python3 -m shamir_mnemonic.cli recover
```

- At `Enter a recovery share`, type **all 33 words of one share on a single
  line**, separated by spaces, in the exact written order. Then press Enter.
- It then asks for a second share. Any of the other three works.
- If it prints `ERROR: Invalid mnemonic checksum`, a word is mistyped or
  out of order. Check that share and type it again. `ERROR: Share already
  entered` means you typed the same share twice. It keeps asking until it
  has two good shares.
- When it has two, it prints `SUCCESS!` and then
  `Your master secret is:` followed by 64 characters. That is the hex.

**D2.** Turn the hex into the 24 BIP-39 words `[ONE LINE]`

```
python3 -c "from mnemonic import Mnemonic; print(Mnemonic('english').to_mnemonic(bytes.fromhex(input('Paste hex: '))))"
```

At `Paste hex:` paste the 64 characters from D1 and press Enter. It prints
the 24 words.

> ⚠️ **The hex from D1 and the 24 words are your complete seed.**
> Never write the hex down, save it to a file, or photograph it or the
> screen. It exists only in this computer's memory.

---

## E. RESTORE TO A WALLET

**Do not enter the passphrase yet.** First load the seed alone, so that
PART 2 can check the seed and the passphrase one at a time.

**Blockstream Jade / Jade Plus**

1. On the Jade: `Set up Jade` → `Restore Wallet` → `24 words`.
2. Type the 24 words from D2 on the Jade.
3. Now shut Tails down (section F). The seed is on the Jade, the computer no
   longer needs it.
4. The Jade finishes setup by asking you to choose a PIN through a companion
   app on an ordinary computer or phone, such as Blockstream Green or
   Sparrow (by USB cable or QR code, the noradio model has no Bluetooth).
   This is normal use and does not expose the seed.

**Coinkite COLDCARD Q**

1. On a blank COLDCARD, after it has asked you to choose a PIN:
   `Import Existing` → `24 Words`. Type the 24 words and press ENTER after
   the last one.
2. Shut Tails down (section F).

Then go to **PART 2, section 2**, the fingerprint check.

> **Do not judge a fingerprint mismatch on its own.** One value cannot tell
> you whether the seed or the passphrase is at fault. Part 2 checks the seed
> first with no passphrase, then adds the passphrase. Only then does a
> mismatch show which step failed.

---

## F. TEARDOWN

1. **Shut down Tails completely, do not restart.** Its memory is wiped on
   shutdown.
2. Reconnect the computer to the internet only after the full shutdown.
3. Destroy any scratch paper used during recovery.

---

## PRACTICE RUN (safe at any time)

To test the tools and your typing without the real shares, do section C,
then make a throwaway set:

```
python3 -m shamir_mnemonic.cli create 2of4 -s 256
```

It prints four new random test shares. Recover any two with D1 and D2.
Never practise with the real shares.

---

## REFERENCE DATA

*(no secrets, fill in by hand and keep with this card)*

```
Firmware at creation       : Jade Plus 1.0.40 noradio
Derivation path            : m/84'/0'/0'   (Native SegWit)
Scheme                     : 2-of-4 SLIP-39, single group, extendable
Tools at creation          : shamir-mnemonic 0.3.0, mnemonic 0.21
Date created               : ________________
```

The two wallet fingerprints are recorded in PART 2.

> **Never write on this card where the other shares or the passphrase are
> kept.** This card sits beside a share. If it says where the rest is, then
> anyone who gets two envelopes has everything. That information belongs on
> the separate location sheet only.

---

## HOW THIS WAS CREATED (reference only, do not re-run)

**X1.** 24 words to entropy hex `[ONE LINE]`

```
python3 -c "from mnemonic import Mnemonic; print(Mnemonic('english').to_entropy('<24 words>').hex())"
```

**X2.** Split into 2-of-4 `[ONE LINE]`

```
python3 -m shamir_mnemonic.cli create 2of4 -S <hex>
```

The SLIP-39 `-p` / `--passphrase` option was **NOT** used. SLIP-39 and BIP-39
mix passphrases differently, so using it would not reproduce this wallet.
Version 0.3.0 makes extendable shares by default, and no `-X` was given.

---

## CRITICAL NOTES

- **The shares rebuild the SEED ONLY.** The seed without the correct BIP-39
  passphrase opens a different, empty wallet. Both are required.
- **Any 1 share alone reveals nothing.** Any 2 of the 4 rebuild it fully.
- **Word order within a share is critical.** The order of the shares is not.
- **Never enter the shares or the seed on any internet-connected device.**
- Check the shares every year: humidity indicators, damage, readability.
- Rewrite the paper every 5 to 10 years.
- Re-test recovery from time to time with the practice run. A backup that
  was never tested is not proven.
