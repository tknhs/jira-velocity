from functools import cached_property
from typing import Optional

from jira import JIRA

from config import JiraConfig
from models import JiraBoard, JiraSprint, JiraSprintCompletionStatus


class Jira:
    def __init__(self, config: JiraConfig):
        self.__config = config

    @cached_property
    def _client(self) -> JIRA:
        jira = JIRA(
            server=self.__config.server_uri,
            basic_auth=(self.__config.user, self.__config.api_token),
        )
        return jira

    def board(self, project_id: Optional[str] = None) -> Optional[JiraBoard]:
        if project_id is None:
            project_id = self.__config.project_id

        boards = self._client.boards(projectKeyOrID=project_id)
        for b in boards:
            if b.raw["location"]["projectKey"] == project_id:
                board = {
                    "board_id": b.id,
                    "board_name": b.name,
                    "project_id": project_id,
                }
                return JiraBoard(**board)
        return None

    def sprints(self, board_id: int) -> list[JiraSprint]:
        results = self._client.sprints(board_id)
        data = [JiraSprint(**{"id": s.id, "name": s.name}) for s in results if s.state == "closed"]
        data.reverse()
        return data

    def sprint_completion_status(self, project_id: str, sprint_id: int) -> JiraSprintCompletionStatus:
        issues = self._client.search_issues(
            f"project = {project_id} AND issuetype = ストーリー AND Sprint = {sprint_id} order by created DESC",
            maxResults=1000,
        )
        task_count = len(issues)
        completed_task_count = 0
        story_points = 0
        completed_story_points = 0
        for issue in issues:
            max_sprint_id = max([i.id for i in issue.fields.customfield_10021])
            story_point = 0 if issue.fields.customfield_10016 is None else issue.fields.customfield_10016
            if sprint_id == max_sprint_id and issue.fields.status.name == "完了":
                completed_task_count += 1
                completed_story_points += story_point
                #print(issue.fields.customfield_10016, issue.fields.status, issue, issue.fields.summary, issue.fields.resolutiondate)
                #print(i.name, i.state, i.startDate, i.endDate, i.id)
            story_points += story_point
        status = {
            "task_count": task_count,
            "completed_task_count": completed_task_count,
            "story_points": story_points,
            "completed_story_points": completed_story_points,
        }
        return JiraSprintCompletionStatus(**status)
