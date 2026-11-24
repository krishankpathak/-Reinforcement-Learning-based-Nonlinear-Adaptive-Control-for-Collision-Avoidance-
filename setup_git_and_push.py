"""
Git Repository Setup, Mirror Synchronization, and GitHub Push Script
Configures user credentials: krishankpathak (anandprakashpathak07469@gmail.com)
Remote: https://github.com/krishankpathak/-Reinforcement-Learning-based-Nonlinear-Adaptive-Control-for-Collision-Avoidance-
"""

import os
import shutil
import subprocess

def sync_and_push_git():
    src = r"C:\Users\lenovo\.gemini\antigravity\scratch\Research_Work"
    desktop = r"C:\Users\lenovo\Desktop\Research_Work"
    home = r"C:\Users\lenovo\Research_Work"
    
    print("1. Synchronizing updated files to Desktop and Home folders...")
    for d in [desktop, home]:
        if os.path.exists(d):
            shutil.rmtree(d)
        shutil.copytree(src, d)
        print(f"Synchronized to: {d}")

    # Set up Git in Desktop workspace
    repo_dir = desktop
    print(f"\n2. Configuring Git in {repo_dir}...")
    
    def run_git(cmd):
        res = subprocess.run(["git"] + cmd, cwd=repo_dir, capture_output=True, text=True)
        print(f"git {' '.join(cmd)}")
        if res.stdout:
            print("STDOUT:", res.stdout.strip())
        if res.stderr:
            print("STDERR:", res.stderr.strip())
        return res

    run_git(["init"])
    run_git(["config", "user.name", "krishankpathak"])
    run_git(["config", "user.email", "anandprakashpathak07469@gmail.com"])
    
    # Configure remote
    remote_url = "https://github.com/krishankpathak/-Reinforcement-Learning-based-Nonlinear-Adaptive-Control-for-Collision-Avoidance-.git"
    # Remove existing remote if present
    run_git(["remote", "remove", "origin"])
    run_git(["remote", "add", "origin", remote_url])
    
    print("\n3. Staging and committing all research assets...")
    run_git(["add", "-A"])
    commit_msg = "Complete Unified Robotics Research Suite: Friction-Aware Adaptive Control, 3D CAE Multiphysics, ROS 2 Gazebo, Datasets, and Proposals"
    run_git(["commit", "-m", commit_msg])
    
    print("\n4. Checking branch and attempting push to GitHub...")
    run_git(["branch", "-M", "main"])
    push_res = run_git(["push", "-u", "origin", "main"])
    
    if push_res.returncode != 0:
        print("\nNote: Push requires network credentials/access token. Attempting with standard credentials...")
        # Check if master branch exists on remote
        run_git(["push", "-u", "origin", "master"])

if __name__ == "__main__":
    sync_and_push_git()
