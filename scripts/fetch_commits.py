from github_client import get_repo

repo = get_repo()

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