import os
from datetime import datetime, timedelta
import pytz

# Define the pattern (7 rows for days, add as many columns as there are weeks in the image)
heart_pattern = [
    [0, 1, 1, 0, 1, 1, 0],  # Sunday
    [1, 1, 1, 1, 1, 1, 1],  # Monday
    [1, 1, 1, 1, 1, 1, 1],  # Tuesday
    [1, 1, 1, 1, 1, 1, 1],  # Wednesday
    [0, 1, 1, 1, 1, 1, 0],  # Thursday
    [0, 0, 1, 1, 1, 0, 0],  # Friday
    [0, 0, 0, 1, 0, 0, 0],  # Saturday
]

# Set the timezone
timezone = pytz.timezone("America/New_York")

# Start date for the heart: September 1st (Sunday)
start_date = datetime(2024, 9, 1)

# Verify Git repository
if not os.path.exists(".git"):
    print("Error: This directory is not a Git repository.")
    exit(1)

# Loop through the period and create commits based on the pattern
for week in range(7):
    for day in range(7):
        try:
            commit_date = start_date + timedelta(weeks=week, days=day)

            # Ensure index is valid
            if 0 <= day < len(heart_pattern) and 0 <= week < len(heart_pattern[day]):
                # Number of commits for the day
                commit_count = heart_pattern[day][week]

                for commit_num in range(commit_count):
                    # Localize the datetime to the specified timezone
                    commit_time = commit_date + timedelta(
                        hours=commit_num
                    )  # Spread commits over the day
                    commit_time = timezone.localize(commit_time)

                    # Git date format
                    formatted_date = commit_time.strftime("%a %b %d %H:%M:%S %Y %z")

                    # Create a dummy file and make a commit with backdated time
                    with open("pixel.txt", "w") as file:
                        file.write(
                            f"Commit on {commit_time.strftime('%Y-%m-%d %H:%M:%S')} (Commit {commit_num + 1})\n"
                        )

                    os.system("git add pixel.txt")

                    commit_cmd = (
                        f'GIT_COMMITTER_DATE="{formatted_date}" '
                        f'git commit --date="{formatted_date}" '
                        f'-m "Commit on {commit_time.strftime("%Y-%m-%d %H:%M:%S")}"'
                    )

                    if os.system(commit_cmd) != 0:
                        print(
                            f"Error committing on {commit_time.strftime('%Y-%m-%d %H:%M:%S')}"
                        )

        except IndexError:
            print(f"Skipping invalid index at week {week}, day {day}")

# Push the commits to GitHub once all are created
if os.system("git push origin main") != 0:
    print("Error: Git push failed. Check authentication and branch name.")
