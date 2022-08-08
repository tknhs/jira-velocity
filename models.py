from pydantic import BaseModel, Field


class JiraBoard(BaseModel):
    board_id: int
    board_name: str
    project_id: str


class JiraSprint(BaseModel):
    id: int
    name: str


class JiraSprintCompletionStatus(BaseModel):
    task_count: int
    completed_task_count: int
    story_points: int
    completed_story_points: int
