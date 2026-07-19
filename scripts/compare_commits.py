from github import Github
from dotenv import load_dotenv
import os

# -----------------------------
# Load Environment Variables
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = os.getenv("OWNER")
REPO = os.getenv("REPO")

# -----------------------------
# Connect to GitHub
# -----------------------------
g = Github(TOKEN)
repo = g.get_repo(f"{OWNER}/{REPO}")

# -----------------------------
# Read Previous Commit
# -----------------------------
last_commit_file = os.path.join(BASE_DIR, "reports", "last_commit.txt")

with open(last_commit_file, "r") as f:
    previous_commit = f.read().strip()

# -----------------------------
# Get Latest Commit
# -----------------------------
latest_commit = repo.get_commits()[0].sha

print(f"Previous Commit : {previous_commit}")
print(f"Latest Commit   : {latest_commit}")

# -----------------------------
# Compare
# -----------------------------
if previous_commit == latest_commit:
    print("\nNo new commits found.")
else:
    print("\nNew commit detected!")