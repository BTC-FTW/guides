# PART 2: PASSPHRASE AND WALLET VERIFICATION

**Do PART 1 first.** Part 1 rebuilds the 24 word seed from the shares.
Part 2 turns that seed into the correct wallet and proves you got it right.

**This document contains no secrets and names no locations.**

---

## 0. WHY THERE IS A SECOND STEP

The 2-of-4 shares rebuild the **seed only**.

A seed on its own is not broken or incomplete. It opens a real, valid,
perfectly normal wallet. That wallet is simply **not the right one**, and it
is empty.

The **BIP-39 passphrase** is a separate piece of text, stored apart from the
shares on purpose. It is not contained in the shares and cannot be derived
from them. No amount of computation recovers it.

```
   seed  +  no passphrase   ->  a valid, empty wallet
   seed  +  wrong passphrase ->  a different valid, empty wallet
   seed  +  right passphrase ->  the funded wallet
```

**This is the single most important thing to understand:** a wrong passphrase
does **not** produce an error message. The device does not reject it. It
silently opens a different empty wallet and everything looks completely
normal.

An empty balance therefore tells you nothing on its own. It could mean the
passphrase is wrong, or that you mistyped one character. The **only**
reliable way to tell the difference is the fingerprint check in section 2.

Do not panic and do not assume the funds are gone if you see an empty wallet.
Work through section 2 first.

---

## 1. OBTAINING THE PASSPHRASE

The passphrase is **not in this document**, **not on the share cards**, and
**not in Part 1**. It is held separately, and deliberately so: anyone who
steals shares must still not be able to reach the funds.

Where it is kept is written on a separate **location sheet**. That sheet is
never stored with a share, and it is given to a different set of people.

**If you hold shares but have no location sheet, stop here.** You cannot
complete recovery alone. Contact the other holders. Two of four shares plus
the location sheet is the complete set.

### Transcribing it

The passphrase must be entered **exactly**. It is case sensitive and every
character counts:

- Upper and lower case are different
- Spaces count, including a trailing space at the end
- Punctuation counts
- A letter O and a digit 0 are different, as are letter l, capital I and digit 1
- Accented and non-English characters may encode differently on different
  devices. If the passphrase contains any, note that fact on the location sheet.

If the fingerprint in section 2 does not match, transcription is the most
likely cause by a wide margin.

---

## 2. THE FINGERPRINT CHECK

A **wallet fingerprint** is 8 hexadecimal characters, for example `a1b2c3d4`.
It is derived from the wallet's public key, so it reveals nothing about the
funds, but it is unique to one specific seed and passphrase combination.

Where to read it:

| Device | Where the fingerprint is shown |
|---|---|
| Jade / Jade Plus | Bottom right of the screen once a wallet is unlocked. The companion app (Green, Sparrow) shows it too |
| COLDCARD Q | `Advanced/Tools` → `View Identity` (Master Key Fingerprint). After a passphrase, also on its confirmation screen |

Two reference fingerprints are recorded, and comparing them **in order** tells
you exactly which step went wrong:

### Step 1: check the seed, without a passphrase

Load the seed with the passphrase feature switched **off**. Compare the
fingerprint to `Fingerprint A` on the reference card.

- **Jade:** before unlocking, open `Options` → `BIP39 Passphrase` and set it
  to `Disabled`. Then unlock with the PIN.
- **COLDCARD Q:** right after the import in Part 1, before using
  `Passphrase`, open `Advanced/Tools` → `View Identity`.

| Result | Meaning | Action |
|---|---|---|
| Matches `A` | The shares combined correctly and the 24 words are right | Go to step 2 |
| Does **not** match `A` | The seed itself is wrong | Go back to PART 1. Most likely the words within a share were entered out of order, or a word was misread |

**Do not go on to step 2 until fingerprint A matches.** Adding a passphrase to
a wrong seed makes the failure impossible to diagnose.

### Step 2: check the passphrase

Now load the wallet **with** the passphrase. Compare to `Fingerprint B`.

- **Jade:** switch the Jade off and on. Before unlocking, open `Options` →
  `BIP39 Passphrase` and set it to `Always Ask`. Unlock with the PIN and type
  the passphrase when asked. The Jade only asks if this setting is on.
- **COLDCARD Q:** main menu `Passphrase`, type it, press ENTER. The
  confirmation screen shows the new fingerprint. Confirm it only if it
  matches B.

| Result | Meaning | Action |
|---|---|---|
| Matches `B` | Correct seed and correct passphrase. This is the real wallet | Done. Funds should be visible |
| Does **not** match `B` | The seed is fine, the passphrase is wrong or mistyped | Re-read section 1 and try again. Check case, spaces and lookalike characters |

Because fingerprint A already proved the seed, a failure at step 2 can only be
the passphrase. That is the entire reason two values are recorded rather than
one.

---

## 3. IF NEITHER FINGERPRINT IS AVAILABLE

If the reference card is lost and you have no fingerprints to compare against,
recovery is still possible but you lose the ability to verify.

In that case, restore with the passphrase and check whether the wallet shows
the expected transaction history. Treat a zero balance as **unproven, not
final**, and try passphrase variations before concluding anything.

Never destroy or overwrite the shares while any doubt remains.

---

## 4. SAFETY RULES

- Do all of this on the hardware wallet itself. Never type the seed or the
  passphrase into a computer, phone, browser or password manager to "test" it.
- Never photograph the seed, the passphrase or a screen showing either.
- A wrong attempt is harmless and unlimited. There is no lockout and no
  penalty for retrying, because each attempt simply opens a different wallet.
- If the Tails computer is still running, follow the teardown steps in
  PART 1 section F.

---

## REFERENCE DATA

*(no secrets, fill in and keep with the share cards)*

```
Fingerprint A, seed with NO passphrase  : ________________
Fingerprint B, seed WITH passphrase     : ________________
Passphrase contains non-English chars   : yes / no
Jade menu path to the passphrase setting: Options > BIP39 Passphrase
Date these values were last verified    : ________________
```

> Fingerprints are safe to keep beside the shares. They prove a correct
> recovery but cannot be used to spend, and they reveal no balance.
> **Never write the passphrase itself, or where it is kept, on this card.**
