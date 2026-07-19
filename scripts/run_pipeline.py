import os
import json
from datetime import datetime

from github_client import get_repo
from parse_diff import parse_patch

# =====================================================
# Paths
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)

CHANGES_FILE = os.path.join(REPORTS_DIR, "changes.json")
HISTORY_FILE = os.path.join(REPORTS_DIR, "history.json")

# =====================================================
# Connect to GitHub
# =====================================================

repo = get_repo()

# =====================================================
# Fetch Latest Commits
# =====================================================

commits = list(repo.get_commits())

if len(commits) < 2:
    raise Exception("Repository must have at least 2 commits.")

latest = commits[0]
previous = commits[1]

print("=" * 80)
print("GitHub Change Dashboard Pipeline")
print("=" * 80)

print("Repository :", repo.full_name)
print("Branch     :", repo.default_branch)
print("Latest     :", latest.sha)
print("Previous   :", previous.sha)

# =====================================================
# Compare
# =====================================================

comparison = repo.compare(previous.sha, latest.sha)

# =====================================================
# Build Report
# =====================================================

report = {
    "repository": repo.full_name,
    "branch": repo.default_branch,

    "latest_commit": latest.sha,
    "previous_commit": previous.sha,

    "author": latest.commit.author.name if latest.commit.author else "Unknown",
    "author_email": latest.commit.author.email if latest.commit.author else "",

    "message": latest.commit.message,

    "commit_time": str(latest.commit.author.date),

    "pipeline_time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),

    "files": [],

    "line_changes": []
}

# =====================================================
# Changed Files
# =====================================================

print("\nChanged Files")
print("-" * 80)

for file in comparison.files:

    print(file.filename)

    report["files"].append({

        "filename": file.filename,

        "status": file.status,

        "additions": file.additions,

        "deletions": file.deletions,

        "changes": file.changes,

        "patch": file.patch

    })

    if file.patch:

        parsed = parse_patch(file.filename, file.patch)

        report["line_changes"].extend(parsed)

# =====================================================
# Save Latest Report
# =====================================================

with open(CHANGES_FILE, "w") as f:

    json.dump(report, f, indent=4)

# =====================================================
# Save History
# =====================================================

history = []

if os.path.exists(HISTORY_FILE):

    try:

        with open(HISTORY_FILE, "r") as f:

            history = json.load(f)

    except:

        history = []

history.append(report)

with open(HISTORY_FILE, "w") as f:

    json.dump(history, f, indent=4)

# =====================================================
# Finish
# =====================================================

print("\n")

print("=" * 80)
print("Pipeline Completed Successfully")
print("=" * 80)

print("Repository      :", report["repository"])
print("Branch          :", report["branch"])
print("Author          :", report["author"])
print("Commit Message  :", report["message"])
print("Files Changed   :", len(report["files"]))
print("Line Changes    :", len(report["line_changes"]))
print("Changes File    :", CHANGES_FILE)
print("History File    :", HISTORY_FILE)