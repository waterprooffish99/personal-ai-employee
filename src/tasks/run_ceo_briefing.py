#!/usr/bin/env python3
"""
Weekly scheduled task to generate the CEO Briefing.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.skills.agent_skills import get_skill_registry
from src.utils.logger import log_action

def run_ceo_briefing():
    """Execute the CEO Briefing skill."""
    print("Starting CEO Briefing Generation...")
    registry = get_skill_registry()
    ceo_skill = registry.get_skill("ceo_briefing")
    
    if ceo_skill:
        result = ceo_skill.execute()
        if result.get("success"):
            print(f"Success: {result.get('result')}")
            log_action("Weekly CEO Briefing generated successfully", actor="system", result="success")
        else:
            print(f"Failed to generate CEO Briefing: {result.get('result')}")
            log_action("Weekly CEO Briefing failed", actor="system", result="error", details={"error": result.get("result")})
    else:
        print("Error: CEO Briefing skill not found in registry.")

if __name__ == "__main__":
    run_ceo_briefing()
