"""
CLI tool to generate PR responses.
Called by GitHub Actions.
"""

import argparse
from responder import SignalResponder
import json
from pathlib import Path

def load_hint(day: int, attempt_count: int = 1):
    """Load appropriate hint based on attempt"""
    answers_file = Path('data/answers.json')
    if answers_file.exists():
        with open(answers_file, 'r') as f:
            answers = json.load(f)
            day_data = answers.get(f"day_{day}", {})
            
            # Progressive hints
            hint_key = f"hint_{min(attempt_count, 3)}"
            return day_data.get(hint_key, "Review the puzzle description carefully.")
    return "The relay offers no additional guidance at this time."

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--solver', required=True)
    parser.add_argument('--day', type=int, required=True)
    parser.add_argument('--valid', required=True)
    parser.add_argument('--first', required=True)
    parser.add_argument('--streak', type=int, default=0)
    parser.add_argument('--feedback', required=True)
    
    args = parser.parse_args()
    
    responder = SignalResponder()
    
    if args.valid == '0':  # Exit code 0 means success
        # Correct solution
        response = responder.generate_correct_response(
            solver=args.solver,
            day=args.day,
            is_first=(args.first == 'true'),
            streak=args.streak
        )
    else:
        # Wrong solution
        hint = load_hint(args.day)
        response = responder.generate_wrong_response(
            solver=args.solver,
            hint=hint
        )
    
    # Add feedback from validator
    response += f"\n\n---\n**Validator Output:**\n{args.feedback}"
    
    print(response)

if __name__ == "__main__":
    main()
