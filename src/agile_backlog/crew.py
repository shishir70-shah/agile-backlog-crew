import os

from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

from agile_backlog.models import Backlog


@CrewBase
class AgileBacklogCrew:
    """Business idea -> Epics -> Stories -> Tasks crew."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self) -> None:
        self.llm = LLM(
            model="openrouter/openai/gpt-4.1-mini",
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )
        self.search_tool = SerperDevTool()

    @agent
    def business_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["business_researcher"],
            llm=self.llm,
            tools=[self.search_tool],
            verbose=True,
        )

    @agent
    def business_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["business_analyst"],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def tech_scrum_jira_expert(self) -> Agent:
        return Agent(
            config=self.agents_config["tech_scrum_jira_expert"],
            llm=self.llm,
            verbose=True,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            agent=self.business_researcher(),
        )

    @task
    def epic_definition_task(self) -> Task:
        return Task(
            config=self.tasks_config["epic_definition_task"],
            agent=self.business_analyst(),
            context=[self.research_task()],
        )

    @task
    def backlog_breakdown_task(self) -> Task:
        return Task(
            config=self.tasks_config["backlog_breakdown_task"],
            agent=self.tech_scrum_jira_expert(),
            context=[self.epic_definition_task()],
            output_pydantic=Backlog,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
