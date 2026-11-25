"""Save one fixed submission line into /output/entry.txt.

The script never touches the network, never reads the clock and never
rolls any dice, so repeated runs always land on identical bytes.
"""

import os
import string
import sys

# A single line: a vending machine chatting up someone walking past.
SUBMISSION = "Hey, beautiful, I have been holding your favourite snack at eye level for three weeks. Press B4 and let's make it official."
MAX_LENGTH = 200


def give_up(message):
    """Print the problem to stderr and stop with a non-zero status."""
    sys.stderr.write("failure: %s\n" % message)
    raise SystemExit(1)


def check_submission(candidate):
    """Inspect the candidate against every rule before writing anything."""
    trimmed = candidate.strip()
    if trimmed == "":
        give_up("submission cannot be blank")
    if any(ord(char) < 32 or ord(char) == 127 for char in candidate):
        give_up("submission must not contain control characters")
    if trimmed.isdigit():
        give_up("submission cannot be only digits")
    if all(char in string.punctuation for char in trimmed):
        give_up("submission cannot be only punctuation")
    if not any(char.isalpha() for char in trimmed):
        give_up("submission needs at least one letter")
    if len(candidate) > MAX_LENGTH:
        give_up("submission has %d characters, over the %d limit" % (len(candidate), MAX_LENGTH))
    try:
        candidate.encode("utf-8")
    except UnicodeEncodeError as problem:
        give_up("submission is not valid UTF-8: %s" % problem)


def run():
    check_submission(SUBMISSION)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(SUBMISSION)


if __name__ == "__main__":
    run()
