from dotenv import load_dotenv

from config import JiraConfig
from jira_data import Jira


load_dotenv()

config = JiraConfig()
jira = Jira(config)
b = jira.board()

sprints = jira.sprints(b.board_id)
for s in sprints:
    status = jira.sprint_completion_status(config.project_id, s.id)
    print(s, status)
