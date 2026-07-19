from github import Github, Auth
from dotenv import load_dotenv
import os

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load .env
load_dotenv(os.path.join(BASE_DIR, ".env"))

TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = os.getenv("OWNER")
REPO = os.getenv("REPO")


def get_repo():
    """
    Returns the authenticated GitHub repository object.
    """
    auth = Auth.Token(TOKEN)
    g = Github(auth=auth)

    return g.get_repo(f"{OWNER}/{REPO}")