import argparse
import random
import string
import sys

#!/usr/bin/env python3
"""
random_char_generator.py

Generate random characters or strings from common character sets.
"""

CHARSETS = {
    "lower": string.ascii_lowercase,
    "upper": string.ascii_uppercase,
    "letters": string.ascii_letters,
    "digits": string.digits,
    "hex": string.hexdigits.lower(),
    "punct": string.punctuation,
    "printable": ''.join(ch for ch in string.printable if ch not in '\t\n\r\x0b\x0c'),
    "alnum": string.ascii_letters + string.digits,
    "all": string.ascii_letters + string.digits + string.punctuation,
}

AMBIGUOUS = "Il1O0"

def build_charset(name: str, custom: str, exclude: str = "") -> str:
    if custom is not None:
        base = ''.join(dict.fromkeys(custom))  # preserve order, remove duplicates
    else:
        base = CHARSETS.get(name, "")
    if exclude:
        base = ''.join(ch for ch in base if ch not in exclude)
    return base

def random_string(length: int, charset: str, allow_repeat: bool = True) -> str:
    if length < 0:
        raise ValueError("length must be non-negative")
    if not charset:
        raise ValueError("charset is empty")
    if not allow_repeat and length > len(charset):
        raise ValueError("length > unique charset size when repeats disallowed")
    if allow_repeat:
        return ''.join(random.choice(charset) for _ in range(length))
    else:
        return ''.join(random.sample(charset, length))

def parse_args():
    p = argparse.ArgumentParser(description="Random character/string generator")
    p.add_argument("-s", "--set", choices=sorted(CHARSETS.keys()), default="alnum",
                   help="predefined character set (default: alnum)")
    p.add_argument("-c", "--count", type=int, default=1, help="number of items to generate (default: 1)")
    p.add_argument("--custom", type=str, help="use a custom charset (overrides --set)")
    p.add_argument("--exclude", type=str, default="", help="characters to exclude from the charset")
    p.add_argument("--no-ambiguous", action="store_true", help=f"exclude ambiguous characters: {AMBIGUOUS}")
    p.add_argument("--no-repeat", action="store_true", help="do not repeat characters within each generated item")
    p.add_argument("--seed", type=int, help="set random seed for reproducibility")
    return p.parse_args()

def main():
    # Ask for length first (interactive)
    try:
        raw = input("Enter length (non-negative integer): ").strip()
        length = int(raw)
        if length < 0:
            raise ValueError("negative")
    except Exception:
        print("Invalid length entered. Please provide a non-negative integer.", file=sys.stderr)
        sys.exit(2)

    args = parse_args()
    args.length = length

    if args.seed is not None:
        random.seed(args.seed)

    exclude = args.exclude
    if args.no_ambiguous:
        exclude += AMBIGUOUS

    try:
        charset = build_charset(args.set, custom=args.custom, exclude=exclude)
    except Exception as e:
        print(f"Error building charset: {e}", file=sys.stderr)
        sys.exit(2)

    try:
        outputs = [random_string(args.length, charset, allow_repeat=not args.no_repeat)
                   for _ in range(args.count)]
    except Exception as e:
        print(f"Error generating string: {e}", file=sys.stderr)
        sys.exit(3)

    # Print each item on its own line.
    sys.stdout.write("\n".join(outputs))
    if outputs:
        sys.stdout.write("\n")

if __name__ == "__main__":
    main()