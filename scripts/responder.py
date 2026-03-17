"""
Generates immersive, lore-rich responses to PRs.
Maintains the SIGNAL-LOST atmosphere.
"""

import json
import random
from pathlib import Path
from datetime import datetime

class SignalResponder:
    def __init__(self):
        self.correct_messages = [
            "🎯 **SIGNAL ACQUIRED**\n\nThe orbital relay has accepted your transmission, {solver}. Your decryption was flawless.\n\n> *The network hums with approval. Another node awakens.*\n\n**Status:** AUTHENTICATED ✅\n**Timestamp:** {timestamp}\n**Next Challenge:** STANDBY...",
            
            "✨ **RELAY SYNCHRONIZED**\n\nImpressive work, {solver}. The signal is clear and strong.\n\n> *Distant satellites align. The network expands its reach.*\n\n**Verification:** COMPLETE ✅\n**Your Rank:** Updating...\n**The network remembers.**",
            
            "⚡ **TRANSMISSION CONFIRMED**\n\nYour solution resonates through the void, {solver}. The relay network acknowledges.\n\n> *Static clears. A new frequency emerges.*\n\n**Authentication:** SUCCESS ✅\n**Contribution:** RECORDED\n**Standing by for next signal...**"
        ]
        
        self.wrong_messages = [
            "❌ **SIGNAL LOST**\n\nYour decryption attempt failed, {solver}. The relay rejects your transmission.\n\n> *The network remains silent. Your key is incorrect.*\n\n**Status:** AUTHENTICATION FAILED\n**Hint:** {hint}\n**Retry:** PERMITTED\n\n*The satellites watch. They wait for your next attempt.*",
            
            "⚠️ **CORRUPTED TRANSMISSION**\n\nThe relay cannot parse your solution, {solver}. Signal integrity compromised.\n\n> *Static overwhelms the channel. Recalibrate your approach.*\n\n**Error:** DECRYPTION MISMATCH\n**Guidance:** {hint}\n**Next Attempt:** AUTHORIZED\n\n*The network does not give up easily on potential operators.*",
            
            "📡 **NO SIGNAL DETECTED**\n\nYour attempt did not resonate, {solver}. The orbital array remains locked.\n\n> *The void echoes with silence. Your pattern does not match.*\n\n**Validation:** FAILED\n**Clue:** {hint}\n**Persistence:** ENCOURAGED\n\n*True operators never stop transmitting.*"
        ]
        
        self.first_solve_bonus = "\n\n🏆 **FIRST SOLVER BONUS**\n\nYou are the FIRST to crack Day {day}! The relay grants you priority status.\n\n**Achievement Unlocked:** 🥇 *Pioneer Signal*\n**Bonus Points:** +100\n**Network Status:** LEGEND"
        
        self.streak_messages = {
            3: "🔥 **3-DAY STREAK**\n\nYour consistency impresses the network. Keep transmitting.",
            5: "⚡ **5-DAY STREAK**\n\nThe relay has marked you as a dedicated operator.",
            7: "🌟 **WEEK STREAK**\n\nYour persistence is unmatched. The network bows to your dedication.",
            10: "👑 **LEGENDARY STREAK**\n\nYou have become one with the relay. The satellites sing your name."
        }
    
    def generate_correct_response(self, solver: str, day: int, is_first: bool = False, streak: int = 0) -> str:
        """Generate response for correct solution"""
        message = random.choice(self.correct_messages)
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        response = message.format(solver=solver, timestamp=timestamp)
        
        # Add first solve bonus
        if is_first:
            response += self.first_solve_bonus.format(day=day)
        
        # Add streak bonus
        if streak in self.streak_messages:
            response += f"\n\n{self.streak_messages[streak]}"
        
        return response
    
    def generate_wrong_response(self, solver: str, hint: str) -> str:
        """Generate response for incorrect solution"""
        message = random.choice(self.wrong_messages)
        return message.format(solver=solver, hint=hint)
    
    def generate_welcome_message(self, solver: str, is_new: bool = True) -> str:
        """Generate welcome message for new solvers"""
        if is_new:
            return f"""👋 **WELCOME TO THE RELAY, {solver}**

The orbital signal network has detected your presence. You are now an authorized operator.

> *The satellites adjust their orbit. A new voice joins the transmission.*

**Your Mission:** Solve daily puzzles to unlock the network's secrets.
**Your Tools:** Logic, code, and cryptography.
**Your Reward:** Knowledge, achievement, and glory.

**Pro Tips:**
- Solutions go in `solutions/` using the template
- Check `data/answers.json` structure (but don't peek!)
- The network rewards consistency and creativity

*The relay awaits your first transmission. Good luck, operator.*

---
**Status:** OPERATOR REGISTERED ✅
**Clearance Level:** 1
**Next Challenge:** LOADED
"""
        else:
            return f"""👋 **WELCOME BACK, {solver}**

The relay recognizes your signal. Resuming operations.

> *The network remembers your previous transmissions.*

**Ready for the next challenge?**
"""

def main():
    """Test the responder"""
    responder = SignalResponder()
    
    print("=== CORRECT RESPONSE ===")
    print(responder.generate_correct_response("TestSolver", 1, is_first=True, streak=3))
    
    print("\n=== WRONG RESPONSE ===")
    print(responder.generate_wrong_response("TestSolver", "The alphabet has been shifted..."))
    
    print("\n=== WELCOME MESSAGE ===")
    print(responder.generate_welcome_message("NewSolver", is_new=True))

if __name__ == "__main__":
    main()
