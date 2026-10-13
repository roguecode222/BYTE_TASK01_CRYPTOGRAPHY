import base64
import itertools
import string
import sys

CHALLENGE = "QkFJTntiQTczX1E4Ul9BcmhIQ19YNHlHY0R9"
TARGET = "BYTE{"

# Layer 1: base64
layer1 = base64.b64decode(CHALLENGE).decode()
print("After base64:", layer1)


def idx(ch):
    return ord(ch.upper()) - 65


def decode(text, key, mode, counting):
    """mode: 'vig' (decrypt), 'enc' (vigenere encode), 'beau' (beaufort).
    counting: 'letters' (key advances on letters only) or 'all' (every character)."""
    out, k = "", 0
    for i, ch in enumerate(text):
        if ch.isalpha():
            pos = k if counting == "letters" else i
            kk = idx(key[pos % len(key)])
            x = idx(ch)
            r = {"vig": x - kk, "enc": x + kk, "beau": kk - x}[mode] % 26
            o = chr(r + 65)
            out += o.lower() if ch.islower() else o
            k += 1
        else:
            out += ch
            if counting == "letters":
                pass
    return out


def try_key(key, show_all=False):
    hits = []
    for mode in ("vig", "enc", "beau"):
        for counting in ("letters", "all"):
            res = decode(layer1, key, mode, counting)
            if show_all or res.startswith(TARGET):
                hits.append((mode, counting, res))
    return hits


# 1) Try some guessed keys (add your own: event name, club name, etc.)
guesses = ["BYTE", "BAIN", "CTF", "KEY", "CYBER", "FLAG", "SECRET", "CIPHER",
           "VIGENERE", "CRYPTO", "BYTECTF", "MAIT"]
extra = sys.argv[1:]  # python solve.py KEY1 KEY2 ...
for key in guesses + extra:
    for mode, counting, res in try_key(key):
        print(f"FOUND  key={key} mode={mode} counting={counting} -> {res}")

# 2) Optional wordlist: python solve.py --wordlist words.txt
if "--wordlist" in sys.argv:
    path = sys.argv[sys.argv.index("--wordlist") + 1]
    with open(path, errors="ignore") as f:
        for line in f:
            w = line.strip()
            if w.isalpha():
                for mode, counting, res in try_key(w):
                    print(f"FOUND  key={w} mode={mode} counting={counting} -> {res}")

# 3) Show what the first 4 letters imply about the key
print("\nKey must start with (decode mode):", end=" ")
print("".join(chr((idx(a) - idx(b)) % 26 + 65) for a, b in zip(layer1[:4], "BYTE")))
print("Key must start with (encode mode):", end=" ")
print("".join(chr((idx(b) - idx(a)) % 26 + 65) for a, b in zip(layer1[:4], "BYTE")))
