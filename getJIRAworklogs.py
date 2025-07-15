import requests
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth
from collections import defaultdict
import re

# ---------------------- CONFIG -----------------------
JIRA_DOMAIN = "your-domain.atlassian.net"
EMAIL = "your-email@example.com"
API_TOKEN = "your-api-token"
N_DAYS = 5  # Change as needed

# ---------------------- INIT -----------------------
BASE_URL = f"https://{JIRA_DOMAIN}/rest/api/3"
auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = {
    "Accept": "application/json"
}

def get_recent_issues(n_days):
    date_from = (datetime.utcnow() - timedelta(days=n_days)).strftime('%Y-%m-%d')
    jql = f'worklogDate >= "{date_from}" ORDER BY updated DESC'
    search_url = f"{BASE_URL}/search"
    issues = []

    start_at = 0
    max_results = 50
    while True:
        params = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results,
            "fields": "summary"
        }
        response = requests.get(search_url, headers=headers, auth=auth, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching issues: {response.text}")

        data = response.json()
        issues.extend(data.get("issues", []))

        if start_at + max_results >= data.get("total", 0):
            break
        start_at += max_results

    return issues

def get_worklogs_for_issue(issue_key, date_from):
    url = f"{BASE_URL}/issue/{issue_key}/worklog"
    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code != 200:
        raise Exception(f"Error fetching worklogs for {issue_key}: {response.text}")
        
    worklogs = response.json().get("worklogs", [])
    
    recent_logs = []
    for log in worklogs:
        started = datetime.strptime(log["started"][:10], "%Y-%m-%d")
        if started >= date_from:
            recent_logs.append({
                "issue": issue_key,
                "author": log["author"]["displayName"],
                "timeSpent": log["timeSpent"],
                "started": log["started"]
            })
    return recent_logs

def parse_time_spent(timespent_str):
    """Convert JIRA-style time string (e.g., '3h 45m') to minutes"""
    hours = minutes = 0
    match = re.findall(r'(\d+)([hm])', timespent_str)
    for value, unit in match:
        if unit == 'h':
            hours += int(value)
        elif unit == 'm':
            minutes += int(value)
    return hours * 60 + minutes

def format_minutes_to_hours_minutes(minutes):
    h = minutes // 60
    m = minutes % 60
    return f"{h}h {m}m" if h else f"{m}m"

def main():
    date_from = datetime.utcnow() - timedelta(days=N_DAYS)
    print(f"\n🔍 Fetching JIRA worklogs from last {N_DAYS} days...\n")
    issues = get_recent_issues(N_DAYS)
    
    all_worklogs = []
    user_time = defaultdict(int)

    for issue in issues:
        issue_key = issue["key"]
        logs = get_worklogs_for_issue(issue_key, date_from)
        for log in logs:
            minutes = parse_time_spent(log['timeSpent'])
            user_time[log["author"]] += minutes
            all_worklogs.append({
                **log,
                "minutes": minutes
            })

    if not all_worklogs:
        print("No worklogs found in the specified time range.")
        return

    print(f"{'Issue':10} | {'User':20} | {'Time Spent':10} | {'Started'}")
    print("-" * 65)
    for log in all_worklogs:
        print(f"{log['issue']:10} | {log['author']:20} | {log['timeSpent']:10} | {log['started']}")

    print("\n🧾 Total Time Spent per User:")
    print("-" * 35)
    for user, total_minutes in sorted(user_time.items(), key=lambda x: -x[1]):
        print(f"{user:20} : {format_minutes_to_hours_minutes(total_minutes)}")

if __name__ == "__main__":
    main()
