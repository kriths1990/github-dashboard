from github import Github
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Read values from .env
TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = os.getenv("OWNER")
REPO = os.getenv("REPO")

# Check if token exists
if not TOKEN:
    raise Exception("GitHub token not found! Check your .env file.")

# Connect to GitHub
g = Github(TOKEN)

# Access the repository
repo = g.get_repo(f"{OWNER}/{REPO}")

print("=" * 50)
print("✅ Connected to GitHub Successfully")
print("=" * 50)

print(f"Repository Name : {repo.name}")
print(f"Owner           : {repo.owner.login}")
print(f"Default Branch  : {repo.default_branch}")
print(f"Stars           : {repo.stargazers_count}")
print(f"Forks           : {repo.forks_count}")
print(f"Open Issues     : {repo.open_issues_count}")