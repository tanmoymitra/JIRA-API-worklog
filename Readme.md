✅ Gets all JIRA worklogs across all projects <br/>
✅ Filters to the last N days <br/>
✅ Displays each worklog entry <br/>
✅ Computes and prints total time spent per user <br/>
✅ Uses a thread pool to fetch worklogs for each issue concurrently. <br/>
✅ Thread-safe aggregation of user time. <br/>
✅ Maintains output + totals per user. <br/>
 <br/> <br/>
⚠️ Notes: <br/>
✅ Adjust MAX_WORKERS based on your API rate limit and system capacity (safe: 5–10). <br/>
✅ JIRA Cloud has rate limiting. Handle 429 Too Many Requests if needed. <br/>
