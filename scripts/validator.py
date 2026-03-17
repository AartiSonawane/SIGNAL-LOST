"""
Validates solution submissions against correct answers.
Supports multiple puzzle types: cipher, code, logic, crypto.
"""

import json
import re
from pathlib import Path
from typing import Dict, Tuple, Optional

class SolutionValidator:
    def __init__(self):
        self.answers = self.load_answers()
    
    def load_answers(self) -> Dict:
        """Load correct answers from data/answers.json"""
        answers_file = Path('data/answers.json')
        if answers_file.exists():
            with open(answers_file, 'r') as f:
                return json.load(f)
        return {}
    
    def validate_cipher(self, day: int, solution: str) -> Tuple[bool, str]:
        """Validate cipher puzzle solutions"""
        correct_answer = self.answers.get(f"day_{day}", {}).get("answer", "")
        
        # Normalize both strings (remove spaces, lowercase, punctuation)
        def normalize(s):
            return re.sub(r'[^a-z0-9]', '', s.lower())
        
        solution_clean = normalize(solution)
        answer_clean = normalize(correct_answer)
        
        if solution_clean == answer_clean:
            return True, "🎯 SIGNAL ACQUIRED. The relay acknowledges your decryption."
        
        # Check if partially correct (Levenshtein distance)
        similarity = self.calculate_similarity(solution_clean, answer_clean)
        
        if similarity > 0.8:
            return False, "⚡ SIGNAL DETECTED but corrupted. You're close. Recalibrate."
        elif similarity > 0.5:
            return False, "📡 WEAK SIGNAL. The pattern is emerging. Continue analysis."
        else:
            return False, "❌ NO SIGNAL. Your decryption key is incompatible."
    
    def validate_code(self, day: int, code: str) -> Tuple[bool, str]:
        """Validate coding challenge solutions"""
        # Extract function from solution
        test_cases = self.answers.get(f"day_{day}", {}).get("test_cases", [])
        
        try:
            # Execute the code safely
            namespace = {}
            exec(code, namespace)
            
            # Get the function name from answers
            func_name = self.answers.get(f"day_{day}", {}).get("function_name")
            if func_name not in namespace:
                return False, "⚠️ FUNCTION NOT FOUND. The relay cannot locate your decoder."
            
            func = namespace[func_name]
            
            # Run test cases
            all_passed = True
            for test in test_cases:
                input_val = test["input"]
                expected = test["expected"]
                try:
                    result = func(input_val)
                    if result != expected:
                        all_passed = False
                        break
                except Exception as e:
                    return False, f"⚠️ RUNTIME ERROR. The relay encountered: {str(e)[:50]}"
            
            if all_passed:
                return True, "✅ ALL TESTS PASSED. The relay accepts your algorithm."
            else:
                return False, "❌ TEST FAILED. Your decoder produces incorrect output."
        
        except Exception as e:
            return False, f"🔥 COMPILATION ERROR. Syntax invalid: {str(e)[:100]}"
    
    def validate_logic(self, day: int, solution: str) -> Tuple[bool, str]:
        """Validate logic puzzle solutions"""
        correct = self.answers.get(f"day_{day}", {}).get("answer", "")
        
        if solution.strip().lower() == correct.lower():
            return True, "🧠 LOGIC VERIFIED. The relay confirms your reasoning."
        else:
            return False, "🤔 LOGIC FLAW DETECTED. Review your premises."
    
    def calculate_similarity(self, s1: str, s2: str) -> float:
        """Calculate string similarity (0.0 to 1.0)"""
        if not s1 or not s2:
            return 0.0
        
        # Simple ratio of matching characters
        matches = sum(c1 == c2 for c1, c2 in zip(s1, s2))
        return matches / max(len(s1), len(s2))
    
    def validate_solution_file(self, filepath: str) -> Tuple[bool, str, Dict]:
        """
        Validate a solution file from a PR.
        Returns: (is_valid, feedback_message, solver_info)
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter-like metadata from the template
            # Look for GitHub Username line
            solver_match = re.search(r'\*\*GitHub Username\*\*:\s*`([^`]+)`', content)
            # Look for Day line
            day_match = re.search(r'\*\*Day / Puzzle Reference\*\*:\s*`Day (\d+)', content)
            # Look for puzzle type
            type_match = re.search(r'\*\*Puzzle Type\*\*:\s*`(cipher|code|riddle|logic)`', content, re.IGNORECASE)
            
            if not all([solver_match, day_match]):
                return False, "❌ INVALID FORMAT. Solution must include GitHub Username and Day in the metadata section.", {}
            
            solver = solver_match.group(1).strip()
            day = int(day_match.group(1))
            puzzle_type = type_match.group(1).lower() if type_match else "cipher"
            
            # Extract the final answer
            answer_match = re.search(r'## Solution\s*\n.*?The decoded message is: \*\*(.+?)\*\*', content, re.DOTALL)
            if not answer_match:
                answer_match = re.search(r'## Solution\s*\n.*?The answer is: \*\*(.+?)\*\*', content, re.DOTALL)
            if not answer_match:
                return False, "❌ NO ANSWER FOUND. Please provide your final answer in the Solution section.", {}
            
            solution = answer_match.group(1).strip()
            
            # Validate based on type
            if puzzle_type == "cipher":
                is_correct, feedback = self.validate_cipher(day, solution)
            elif puzzle_type == "code":
                # Extract code from the solution file
                code_match = re.search(r'```python\n(.*?)\n```', content, re.DOTALL)
                if code_match:
                    code = code_match.group(1)
                    is_correct, feedback = self.validate_code(day, code)
                else:
                    return False, "❌ NO CODE FOUND. Coding challenges require code blocks.", {}
            elif puzzle_type in ["logic", "riddle"]:
                is_correct, feedback = self.validate_logic(day, solution)
            else:
                return False, "⚠️ UNKNOWN PUZZLE TYPE. The relay cannot process this format.", {}
            
            solver_info = {
                "day": day,
                "solver": solver,
                "timestamp": None,  # Will be added by GitHub Actions
                "puzzle_type": puzzle_type
            }
            
            return is_correct, feedback, solver_info
        
        except Exception as e:
            return False, f"🔥 PROCESSING ERROR: {str(e)}", {}

def main():
    """CLI for testing validator"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python validator.py <solution_file>")
        sys.exit(1)
    
    validator = SolutionValidator()
    is_valid, feedback, info = validator.validate_solution_file(sys.argv[1])
    
    print(f"Valid: {is_valid}")
    print(f"Feedback: {feedback}")
    print(f"Info: {info}")
    
    # Exit code for GitHub Actions
    sys.exit(0 if is_valid else 1)

if __name__ == "__main__":
    main()
