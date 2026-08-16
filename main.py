import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

if sys.platform == "win32":
    # Avoid UnicodeEncodeError/charmap noise from crewai's emoji logging on
    # the default Windows console codepage.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parent

load_dotenv(REPO_ROOT / ".env")
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from agile_backlog.crew import AgileBacklogCrew  # noqa: E402
from agile_backlog.jira_export import backlog_to_csv  # noqa: E402


def main() -> None:
    if len(sys.argv) > 1:
        business_idea = " ".join(sys.argv[1:])
    else:
        business_idea = input("Describe your business idea: ").strip()

    if not business_idea:
        print("A business idea is required.")
        sys.exit(1)

    result = AgileBacklogCrew().crew().kickoff(inputs={"business_idea": business_idea})

    if result.pydantic is None:
        print("Crew did not return structured output. Raw result:")
        print(result.raw)
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = PROJECT_ROOT / "output" / f"backlog_{timestamp}.csv"
    backlog_to_csv(result.pydantic, output_path)

    print(f"\nBacklog written to: {output_path}")


if __name__ == "__main__":
    main()
