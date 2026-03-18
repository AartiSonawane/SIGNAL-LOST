# Orbital Signal Relay Network
## Day 3 of ∞
The silence is deafening. The orbital signal relay network stirs, its intentions unclear. The decoded message from yesterday remains elusive, a constant reminder of the uncertainty that lies ahead.

### Update from the Front Lines
We acknowledge the efforts of **vedh-sonawane**, who dared to venture into the unknown. Though the solution to the cipher remains a mystery, their bravery will not be forgotten.

## How to Play
To unravel the mysteries of the orbital signal relay network, follow these steps:
1. Read the README carefully, for it holds the clues to the next challenge.
2. Solve the daily puzzle, and submit your solution as a Pull Request, adding a file under `solutions/` based on `solutions/TEMPLATE.md`.
3. To suggest new lore twists or theories, open an Issue, and share your thoughts with the community.

### Day 3 Puzzle — Coding Challenge
A fragment of code has been intercepted from the network. It appears to be a Python function, but it's incomplete. Fill in the blanks to unlock the next layer of the network.
```python
def decode_signal(signal):
    # Initialize an empty string to store the decoded message
    decoded_message = ""
    # Iterate over each character in the signal
    for char in signal:
        # Apply a Caesar cipher with a shift of 3
        decoded_char = chr((ord(char) - 65 + 3) % 26 + 65)
        # Append the decoded character to the decoded message
        decoded_message += decoded_char
    return decoded_message

# Test the function with a sample signal
sample_signal = "KHOOR"
print(decode_signal(sample_signal))
```
However, this code only works for uppercase letters. Modify it to handle both uppercase and lowercase letters, as well as non-alphabetic characters.

## Hall of Fame
The following individuals have made significant contributions to our understanding of the orbital signal relay network:
* None (yet)

## Credits
Thanks to **vedh-sonawane** for their contributions to the solution space.
