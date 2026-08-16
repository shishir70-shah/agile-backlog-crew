# Agile Backlog Generator (CrewAI POC)

Turns a one-line business idea into a Jira-ready backlog: Epics → Stories → Tasks.

## Agents

1. **Business & Market Researcher** — web-searches the idea (via Serper) and writes a research brief.
2. **Business Analyst** — turns the idea + research into a problem statement and a set of Epics.
3. **Technical SME / Certified Scrum Master / Jira Expert** — breaks each Epic into User Stories (acceptance criteria, story points, priority) and each Story into engineering Tasks.

## Setup

Uses the `venv` and `.env` already at the repo root (`OPENROUTER_API_KEY`, `SERPER_API_KEY`) — nothing extra to configure.

```
..\venv\Scripts\pip install -r requirements.txt
```

## Run

```
..\venv\Scripts\python main.py "A subscription box service for artisanal coffee roasters"
```

(Or run with no argument to be prompted interactively.)

Output lands in `output/backlog_<timestamp>.csv`, formatted for Jira's bulk CSV importer:
`Issue Type, Epic Name, Epic Link, Parent, Summary, Description, Acceptance Criteria, Story Points, Priority`.

- Epic rows carry `Epic Name`.
- Story rows link to their epic via `Epic Link`.
- Task rows link to their parent story via `Parent`.
