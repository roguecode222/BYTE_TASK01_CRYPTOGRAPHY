# BYTE Task 01 – Cryptography

## Challenge
A simple cipher challenge. The flag is in the format `BYTE{...}`.

Challenge text:

```
QkFJTntiQTczX1E4Ul9BcmhIQ19YNHlHY0R9
```

## Tools used
- **CyberChef** – From Base64, Vigenère Decode, Magic
- **Python 3** – scripts in this repo (`solve.py`)
- **dcode.fr** – cipher identification and Vigenère/other solvers
- **claude** - help with analysis and script

## Approach

### Step 1 – Identify the encoding
The text looks like Base64 (letters, digits, no spaces). Decoding it in CyberChef From Base64 gives:

```
BAIN{bA73_Q8R_ArhHC_X4yGcD}
```

This looks like a flag with a wrong prefix, so there is a second layer of encryption.

### Step 2 – Compare with the known flag format
The flag must start with `BYTE{`, so I compared the first four letters:

| Cipher | B | A | I | N |
|---|---|---|---|---|
| Plain  | B | Y | T | E |
| Shift  | 0 | 2 | 15 | 9 |

The shifts are not constant, so this is not a Caesar/ROT cipher. Different letters get different shifts, which points to a polyalphabetic cipher such as Vigenère or Beaufort.

### Step 3 – Derive the start of the key
From the shifts, the key must start with:
- `ACPJ` (Vigenère decode)
- `CYBR` (Beaufort)

Applying a repeating 4-letter key gives `BYTE{bY73_...`. The start matches, and `bY73` is leetspeak for "byte", which suggests the approach is on the right track. The rest of the text is not yet readable.

### Step 4 – Other things tested
- Caesar/ROT shifts and Atbash on the text before and after Base64 decoding
- Vigenère, Vigenère encode, Beaufort, variant Beaufort and autokey
- Different alphabets (26, 36, 62 and 95 characters) and different ways of advancing the key (letters only, or every character)
- Guessed keys from the event context (`BYTE`, `CTF`, `CYBER`, …) and a dictionary of English words as keys
- Affine cipher and single-byte XOR

None of these produced a readable full flag.

## Result
The first layer (Base64) is solved, and the second layer is a keyed polyalphabetic-style cipher whose key starts with `ACPJ`. The full key is still unknown

## Files
| File | Purpose |
|---|---|
| `solve.py` | Decodes Base64 and tests Vigenère/Beaufort keys (guessed keys, command-line keys, optional wordlist) |
| `screenshots/` | CyberChef recipe and output screenshots |

## How to run
```bash
python solve.py                      # built-in guessed keys
python solve.py MYKEY                # also try MYKEY
python solve.py --wordlist words.txt # try every word in a wordlist
```
