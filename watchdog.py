#!/usr/bin/env python3
"""
Watchdog process for the Personal AI Employee System.
Monitors the main orchestrator process and restarts it if it crashes.
"""

import os
import sys
import time
import subprocess
import signal
from datetime import datetime

# Add project root to path
from pathlib import Path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.logger import log_action

class SystemWatchdog:
    """Monitors the AI Employee main process and restarts it upon failure."""
    
    def __init__(self, command: list):
        self.command = command
        self.process = None
        self.running = False
        self.restart_delay = 5  # Seconds to wait before restarting
        self.max_restarts = 10
        self.restart_count = 0
        
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)
        
    def _handle_signal(self, signum, frame):
        """Handle termination signals gracefully."""
        print(f"\nWatchdog received signal {signum}. Shutting down supervised process...")
        self.running = False
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
        sys.exit(0)

    def start(self):
        """Start the watchdog loop."""
        self.running = True
        log_action("Watchdog started", actor="system", result="success", details={"command": self.command})
        print(f"[{datetime.now().strftime('%H:%M:%S')}] SystemWatchdog: Starting supervised process...")
        
        while self.running and self.restart_count < self.max_restarts:
            try:
                self.process = subprocess.Popen(self.command)
                self.process.wait()
                
                # If process exits normally (code 0) and we didn't stop it, we can break or restart
                if not self.running:
                    break
                    
                exit_code = self.process.returncode
                if exit_code == 0:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] SystemWatchdog: Process exited normally.")
                    break
                
                self.restart_count += 1
                log_action(
                    "Supervised process crashed", 
                    actor="system", 
                    result="warning", 
                    details={"exit_code": exit_code, "restart_count": self.restart_count}
                )
                print(f"[{datetime.now().strftime('%H:%M:%S')}] SystemWatchdog: Process crashed (code {exit_code}). Restarting in {self.restart_delay}s... ({self.restart_count}/{self.max_restarts})")
                time.sleep(self.restart_delay)
                
            except Exception as e:
                log_action("Error in Watchdog loop", actor="system", result="error", details={"error": str(e)})
                time.sleep(self.restart_delay)
                
        if self.restart_count >= self.max_restarts:
            log_action("Watchdog max restarts reached", actor="system", result="critical")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] SystemWatchdog: Max restarts reached. Giving up.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Employee Supervisor')
    parser.add_argument('--role', type=str, choices=['Cloud', 'Local'], default='Local', help='Role to supervise')
    parser.add_argument('--name', type=str, help='Name of the agent instance')
    
    args = parser.parse_args()
    
    # Construct the command for main.py
    cmd = [sys.executable, "main.py", "--loop", "--agent-role", args.role]
    if args.name:
        cmd.extend(["--agent-name", args.name])
    elif args.role == 'Cloud':
        cmd.extend(["--agent-name", "CloudAgent"])
    else:
        cmd.extend(["--agent-name", "LocalAgent"])
        
    print(f"Supervisor initializing for {args.role} role...")
    watchdog = SystemWatchdog(cmd)
    watchdog.start()
