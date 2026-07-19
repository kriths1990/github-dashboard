from github_client import get_repo
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

repo = get_repo()

last_commit_file = os.path.join(BASE_DIR, "reports", "last_commit.txt")

with open(last_commit_file, "r") as f:
    previous_commit = f.read().strip()

latest_commit = repo.get_commits()[0].sha

print("Repository      :", repo.full_name)
print("Previous Commit :", previous_commit)
print("Latest Commit   :", latest_commit)

# Stop here
exit()