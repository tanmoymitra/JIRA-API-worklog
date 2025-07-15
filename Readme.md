✅ Gets all JIRA worklogs across all projects
✅ Filters to the last N days
✅ Displays each worklog entry
✅ Computes and prints total time spent per user
✅ Uses a thread pool to fetch worklogs for each issue concurrently.
✅ Thread-safe aggregation of user time.
✅ Maintains output + totals per user.

⚠️ Notes:
✅ Adjust MAX_WORKERS based on your API rate limit and system capacity (safe: 5–10).
✅ JIRA Cloud has rate limiting. Handle 429 Too Many Requests if needed.
