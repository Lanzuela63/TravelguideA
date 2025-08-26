import os
import subprocess
from datetime import datetime

# Change this to your project path
project_path = r"C:\Users\Achi\Capstone_Project\TravelGuide"

# Commit message with timestamp
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
commit_message = f"Auto backup on {now}"

# Git commands
commands = [
    "git add .",
    f'git commit -m "{commit_message}"',
    "git push origin main"
]

def run_backup():
    try:
        os.chdir(project_path)
        for cmd in commands:
            print(f"Running: {cmd}")
            subprocess.check_call(cmd, shell=True)
        print("✅ Auto backup completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    run_backup()
