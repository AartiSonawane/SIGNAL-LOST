"""
Manages the solver leaderboard and statistics.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class Leaderboard:
    def __init__(self):
        self.data_file = Path('data/leaderboard.json')
        self.solvers = self.load_solvers()
    
    def load_solvers(self) -> Dict:
        """Load solver data"""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_solvers(self):
        """Save solver data"""
        self.data_file.parent.mkdir(exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.solvers, f, indent=2)
    
    def add_solve(self, solver: str, day: int, is_first: bool = False):
        """Record a successful solve"""
        if solver not in self.solvers:
            self.solvers[solver] = {
                "total_solves": 0,
                "first_solves": 0,
                "days_solved": [],
                "streak": 0,
                "max_streak": 0,
                "points": 0,
                "rank": "Novice Operator",
                "joined": datetime.now().isoformat()
            }
        
        solver_data = self.solvers[solver]
        
        # Update stats
        solver_data["total_solves"] += 1
        if day not in solver_data["days_solved"]:
            solver_data["days_solved"].append(day)
        
        if is_first:
            solver_data["first_solves"] += 1
            solver_data["points"] += 100  # Bonus for first solve
        
        # Base points
        solver_data["points"] += 10
        
        # Update streak
        solver_data["days_solved"].sort()
        streak = self.calculate_streak(solver_data["days_solved"])
        solver_data["streak"] = streak
        solver_data["max_streak"] = max(solver_data["max_streak"], streak)
        
        # Update rank
        solver_data["rank"] = self.calculate_rank(solver_data["points"])
        
        self.save_solvers()
    
    def calculate_streak(self, days: List[int]) -> int:
        """Calculate current consecutive day streak"""
        if not days:
            return 0
        
        streak = 1
        for i in range(len(days) - 1, 0, -1):
            if days[i] - days[i-1] == 1:
                streak += 1
            else:
                break
        
        return streak
    
    def calculate_rank(self, points: int) -> str:
        """Determine rank based on points"""
        if points < 50:
            return "🌑 Novice Operator"
        elif points < 150:
            return "🌘 Signal Apprentice"
        elif points < 300:
            return "🌗 Relay Technician"
        elif points < 500:
            return "🌖 Satellite Engineer"
        elif points < 800:
            return "🌕 Master Decoder"
        elif points < 1200:
            return "⭐ Network Architect"
        elif points < 2000:
            return "✨ Orbital Legend"
        else:
            return "👑 Signal Sovereign"
    
    def get_top_solvers(self, limit: int = 10) -> List[Dict]:
        """Get top solvers by points"""
        sorted_solvers = sorted(
            self.solvers.items(),
            key=lambda x: x[1]["points"],
            reverse=True
        )
        
        return [
            {
                "solver": name,
                **data
            }
            for name, data in sorted_solvers[:limit]
        ]
    
    def generate_leaderboard_markdown(self) -> str:
        """Generate markdown leaderboard for README"""
        top_solvers = self.get_top_solvers(10)
        
        if not top_solvers:
            return "## 🏆 Leaderboard\n\nNo solvers yet. Be the first to crack the code!"
        
        md = "## 🏆 Leaderboard - Top Signal Operators\n\n"
        md += "| Rank | Operator | Points | Solves | Streak | First Solves | Title |\n"
        md += "|------|----------|--------|--------|--------|--------------|-------|\n"
        
        medals = ["🥇", "🥈", "🥉"]
        
        for i, solver in enumerate(top_solvers, 1):
            rank_display = medals[i-1] if i <= 3 else f"#{i}"
            md += f"| {rank_display} | **{solver['solver']}** | {solver['points']} | {solver['total_solves']} | {solver['streak']}🔥 | {solver['first_solves']} | {solver['rank']} |\n"
        
        return md

def main():
    """Test the leaderboard"""
    lb = Leaderboard()
    
    # Simulate some solves
    lb.add_solve("Alice", 1, is_first=True)
    lb.add_solve("Alice", 2, is_first=False)
    lb.add_solve("Alice", 3, is_first=True)
    lb.add_solve("Bob", 1, is_first=False)
    lb.add_solve("Bob", 3, is_first=False)
    
    print(lb.generate_leaderboard_markdown())

if __name__ == "__main__":
    main()
