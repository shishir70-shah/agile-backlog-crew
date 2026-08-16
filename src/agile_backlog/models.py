from pydantic import BaseModel, Field


class Task(BaseModel):
    summary: str = Field(..., description="Short, action-oriented title for the technical task")
    description: str = Field(..., description="What needs to be built/done and why")


class Story(BaseModel):
    summary: str = Field(..., description="Short title for the user story")
    description: str = Field(..., description="Full story in 'As a <role>, I want <goal>, so that <benefit>' form")
    acceptance_criteria: list[str] = Field(..., description="Bullet-point, testable acceptance criteria")
    story_points: int = Field(..., description="Fibonacci-scale estimate: 1, 2, 3, 5, 8, or 13")
    priority: str = Field(..., description="One of: Highest, High, Medium, Low")
    tasks: list[Task] = Field(default_factory=list, description="Technical sub-tasks under this story")


class Epic(BaseModel):
    name: str = Field(..., description="Short, unique epic name (used as the Jira Epic Name)")
    description: str = Field(..., description="What this epic covers and the business value it delivers")
    stories: list[Story] = Field(default_factory=list, description="User stories that belong to this epic")


class Backlog(BaseModel):
    epics: list[Epic] = Field(..., description="Full set of epics covering the business idea")
