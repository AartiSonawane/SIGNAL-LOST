"""
Manages solver achievements and badges.
"""

import json
from pathlib import Path
from typing import Dict, List, Set

class AchievementSystem:
    def __init__(self):
        self.achievements_file = Path('data/achievements.json')
        self.solver_achievements_file = Path('data/solver_achievements.json')
        
        self.achievements = self.load_achievements()
        self.solver_achievements = self.load_solver_achievements()
    
    def load_achievements(self) -> Dict:
        """Load achievement definitions"""
        if self.achievements_file.exists():
            with open(self.achievements_file, 'r') as f:
                return json.load(f)
        
        # Default achievements
        return {
            "first_blood": {
                "name": "🥇 First Blood",
                "description": "Be the first to solve any puzzle",
                "points": 100,
                "secret": False
            },
            "speed_demon": {
                "name": "⚡ Speed Demon",
                "description": "Solve a puzzle within 1 hour of release",
                "points": 50,
                "secret": False
            },
            "perfectionist": {
                "name": "✨ Perfectionist",
                "description": "Solve 10 puzzles without a single wrong submission",
                "points": 200,
                "secret": True
            },
            "marathon_runner": {
                "name": "🏃 Marathon Runner",
                "description": "Maintain a 7-day solve streak",
                "points": 150,
                "secret": False
            },
            "night_owl": {
                "name": "🦉 Night Owl",
                "description": "Submit a solution between 2 AM and 5 AM",
                "points": 25,
                "secret": True
            },
            "code_master": {
                "name": "💻 Code Master",
                "description": "Solve 5 coding challenges",
                "points": 75,
                "secret": False
            },
            "cipher_sage": {
                "name": "🔐 Cipher Sage",
                "description": "Solve 5 cipher puzzles",
                "points": 75,
                "secret": False
            },
            "triple_threat": {
                "name": "🎯 Triple Threat",
                "description": "Solve one of each puzzle type in a week",
                "points": 100,
                "secret": False
            },
            "comeback_kid": {
                "name": "🔄 Comeback Kid",
                "description": "Solve a puzzle after 3 failed attempts",
                "points": 50,
                "secret": True
            },
            "the_collector": {
                "name": "📚 The Collector",
                "description": "Unlock all non-secret achievements",
                "points": 500,
                "secret": True
            }
        }
    
    def load_solver_achievements(self) -> Dict:
        """Load solver achievement progress"""
        if self.solver_achievements_file.exists():
            with open(self.solver_achievements_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_solver_achievements(self):
        """Save solver achievements"""
        self.solver_achievements_file.parent.mkdir(exist_ok=True)
        with open(self.solver_achievements_file, 'w') as f:
            json.dump(self.solver_achievements, f, indent=2)
    
    def check_achievements(self, solver: str, solve_data: Dict) -> List[str]:
        """Check if any achievements were unlocked"""
        if solver not in self.solver_achievements:
            self.solver_achievements[solver] = {
                "unlocked": [],
                "progress": {}
            }
        
        solver_data = self.solver_achievements[solver]
        newly_unlocked = []
        
        # Check each achievement
        for achievement_id, achievement in self.achievements.items():
            if achievement_id in solver_data["unlocked"]:
                continue  # Already unlocked
            
            # Check conditions
            unlocked = False
            
            if achievement_id == "first_blood" and solve_data.get("is_first"):
                unlocked = True
            
            elif achievement_id == "speed_demon":
                # Check if solved within 1 hour (implement timing logic)
                pass
            
            elif achievement_id == "marathon_runner":
                if solve_data.get("streak", 0) >= 7:
                    unlocked = True
            
            # ... (implement other achievement checks)
            
            if unlocked:
                solver_data["unlocked"].append(achievement_id)
                newly_unlocked.append(achievement)
        
        self.save_solver_achievements()
        return newly_unlocked
    
    def format_achievement_unlock(self, achievements: List[Dict]) -> str:
        """Format achievement unlock message"""
        if not achievements:
            return ""
        
        msg = "\n\n## 🎊 ACHIEVEMENTS UNLOCKED!\n\n"
        
        for ach in achievements:
            msg += f"### {ach['name']}\n"
            msg += f"> {ach['description']}\n"
            msg += f"**Bonus:** +{ach['points']} points\n\n"
        
        return msg

def main():
    """Test achievements"""
    system = AchievementSystem()
    
    solve_data = {
        "is_first": True,
        "streak": 3
    }
    
    unlocked = system.check_achievements("TestSolver", solve_data)
    print(system.format_achievement_unlock(unlocked))

if __name__ == "__main__":
    main()
