from github import Github
from dotenv import load_dotenv
import os

# Load .env
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = os.getenv("OWNER")
REPO = os.getenv("REPO")

# Connect to GitHub
g = Github(TOKEN)
repo = g.get_repo(f"{OWNER}/{REPO}")

# Fetch latest commits
commits = repo.get_commits()

print("=" * 80)
print("LATEST COMMITS")
print("=" * 80)

for commit in commits[:10]:
    print(f"Commit SHA : {commit.sha}")
    print(f"Author     : {commit.commit.author.name}")
    print(f"Date       : {commit.commit.author.date}")
    print(f"Message    : {commit.commit.message}")
    print("-" * 80)