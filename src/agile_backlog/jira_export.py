import csv
from pathlib import Path

from agile_backlog.models import Backlog

CSV_FIELDS = [
    "Issue Type",
    "Epic Name",
    "Epic Link",
    "Parent",
    "Summary",
    "Description",
    "Acceptance Criteria",
    "Story Points",
    "Priority",
]


def backlog_to_csv(backlog: Backlog, output_path: Path) -> Path:
    """Write a Backlog as a Jira bulk-CSV-import file (Epic -> Story -> Task rows)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    for epic in backlog.epics:
        rows.append(
            {
                "Issue Type": "Epic",
                "Epic Name": epic.name,
                "Summary": epic.name,
                "Description": epic.description,
            }
        )
        for story in epic.stories:
            rows.append(
                {
                    "Issue Type": "Story",
                    "Epic Link": epic.name,
                    "Summary": story.summary,
                    "Description": story.description,
                    "Acceptance Criteria": "\n".join(
                        f"- {criterion}" for criterion in story.acceptance_criteria
                    ),
                    "Story Points": str(story.story_points),
                    "Priority": story.priority,
                }
            )
            for task in story.tasks:
                rows.append(
                    {
                        "Issue Type": "Task",
                        "Parent": story.summary,
                        "Summary": task.summary,
                        "Description": task.description,
                    }
                )

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    return output_path
