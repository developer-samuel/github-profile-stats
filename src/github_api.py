import subprocess, json, sys
from datetime import date


def get_start_year(username: str) -> int:
    result = subprocess.run(
        ["gh", "api", f"users/{username}", "--jq", ".created_at[:4]"],
        capture_output=True, text=True
    )
    return int(result.stdout.strip()) if result.returncode == 0 else date.today().year


def fetch_contributions(username: str, start_year: int) -> dict[str, int]:
    """Returns dict of {date_str: commit_count} for all years since start_year."""
    today = date.today()
    all_days: dict[str, int] = {}

    for year in range(start_year, today.year + 1):
        query = (
            f'query {{ user(login: "{username}") {{'
            f' contributionsCollection(from: "{year}-01-01T00:00:00Z", to: "{year}-12-31T23:59:59Z") {{'
            ' contributionCalendar { weeks { contributionDays { date contributionCount } } }'
            ' } } }'
        )
        result = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={query}"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Warning: failed for {year}: {result.stderr}", file=sys.stderr)
            continue
        data = json.loads(result.stdout)
        weeks = (data.get("data", {}).get("user", {})
                     .get("contributionsCollection", {})
                     .get("contributionCalendar", {})
                     .get("weeks", []))
        for week in weeks:
            for day in week.get("contributionDays", []):
                all_days[day["date"]] = day["contributionCount"]

    return all_days


def fetch_total_commits(username: str, start_year: int) -> int:
    """Returns total commit count across all years since start_year."""
    today = date.today()
    total = 0

    for year in range(start_year, today.year + 1):
        query = (
            f'query {{ user(login: "{username}") {{'
            f' contributionsCollection(from: "{year}-01-01T00:00:00Z", to: "{year}-12-31T23:59:59Z") {{'
            ' totalCommitContributions'
            ' } } }'
        )
        result = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={query}"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            total += (data.get("data", {}).get("user", {})
                          .get("contributionsCollection", {})
                          .get("totalCommitContributions", 0))
        else:
            print(f"Warning: GraphQL failed for {year}: {result.stderr}", file=sys.stderr)

    return total


def fetch_total_stars(username: str) -> int:
    result = subprocess.run(
        ["gh", "api", f"users/{username}/repos", "--paginate",
         "--jq", "[.[].stargazers_count] | add // 0"],
        capture_output=True, text=True
    )
    return int(result.stdout.strip() or 0) if result.returncode == 0 else 0
