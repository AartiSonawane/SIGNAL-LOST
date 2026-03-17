"""
Detects suspicious patterns in submissions.
"""

from datetime import datetime
from typing import List, Tuple
import json
from pathlib import Path

class AntiCheat:
    def __init__(self):
        self.submission_log = Path('data/submission_log.json')
        self.load_log()
    
    def load_log(self):
        """Load submission history"""
        if self.submission_log.exists():
            with open(self.submission_log, 'r') as f:
                self.log = json.load(f)
        else:
            self.log = []
    
    def save_log(self):
        """Save submission log"""
        self.submission_log.parent.mkdir(exist_ok=True)
        with open(self.submission_log, 'w') as f:
            json.dump(self.log, f, indent=2)
    
    def check_submission(self, solver: str, day: int, solution: str) -> Tuple[bool, str]:
        """
        Check if submission seems suspicious.
        Returns: (is_suspicious, reason)
        """
        
        # Log this submission
        submission = {
            "solver": solver,
            "day": day,
            "timestamp": datetime.now().isoformat(),
            "solution_length": len(solution)
        }
        self.log.append(submission)
        self.save_log()
        
        # Check 1: Multiple rapid submissions
        recent_submissions = [
            s for s in self.log
            if s["solver"] == solver and s["day"] == day
        ]
        
        if len(recent_submissions) > 5:
            return True, "Too many rapid submissions for the same puzzle"
        
        # Check 2: Identical solutions from different solvers
        similar = [
            s for s in self.log
            if s["day"] == day and s["solution_length"] == len(solution)
        ]
        
        if len(similar) > 3:
            # Flag for manual review
            return False, "Similar solution pattern detected (flagged for review)"
        
        # Check 3: Unrealistic solve times (too fast)
        # (This would require puzzle release timestamps)
        
        return False, ""
    
    def generate_warning(self, reason: str) -> str:
        """Generate anti-cheat warning message"""
        return f"""
⚠️ **SUSPICIOUS ACTIVITY DETECTED**

The orbital relay's security systems have flagged this submission.

**Reason:** {reason}

> *The network values authenticity. Collaboration is encouraged, but direct copying undermines the mission.*

**Action:** This submission will be reviewed manually.

If you believe this is an error, please contact the relay operators.
"""

def main():
    ac = AntiCheat()
    is_sus, reason = ac.check_submission("TestSolver", 1, "THE ANSWER")
    
    if is_sus:
        print(ac.generate_warning(reason))
    else:
        print("✅ Submission appears legitimate")

if __name__ == "__main__":
    main()
