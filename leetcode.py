import requests
from datetime import datetime

GRAPHQL_URL = "https://leetcode.com/graphql"

HEADERS = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com",
    "User-Agent": "Mozilla/5.0"
}

def fetch_recent_submissions(username):
    payload = {
        "query": """
        query recentSubmissions($username: String!) {
          recentSubmissionList(username: $username) {
            titleSlug
            statusDisplay
            timestamp
          }
        }
        """,
        "variables": {"username": username}
    }

    r = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()["data"]["recentSubmissionList"]

def fetch_problem_difficulty(slug):
    payload = {
        "query": """
        query getQuestion($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            difficulty
          }
        }
        """,
        "variables": {"titleSlug": slug}
    }

    r = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()["data"]["question"]["difficulty"]

def solved_today(username, slug):
    today = datetime.now().date()
    submissions = fetch_recent_submissions(username)

    for s in submissions:
        if s["titleSlug"] == slug and s["statusDisplay"] == "Accepted":
            sub_date = datetime.fromtimestamp(int(s["timestamp"])).date()
            if sub_date == today:
                return True
    return False
