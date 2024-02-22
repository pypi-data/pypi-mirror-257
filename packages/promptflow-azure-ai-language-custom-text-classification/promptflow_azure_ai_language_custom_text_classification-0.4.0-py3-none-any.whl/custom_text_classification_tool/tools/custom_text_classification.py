from promptflow import tool
from promptflow.connections import CustomConnection
from custom_text_classification_tool.language_utils.language_skill import LanguageSkill
from custom_text_classification_tool.language_utils.language_tool_utils import run_language_skill

API_VERSION = "2022-10-01-preview"
SKILL = LanguageSkill.CUSTOM_TEXT_CLASSIFICATION


@tool
def classify_text(connection: CustomConnection,
                  document: dict,
                  project_name: str,
                  deployment_name: str,
                  max_retries: int = 5,
                  max_wait: int = 60,
                  parse_response: bool = False):
    query_parameters = {
        "api-version": API_VERSION,
    }

    # Create task parameters:
    task_parameters = {
        "projectName": project_name,
        "deploymentName": deployment_name
    }

    # Create skill config:
    skill_config = {
        "connection": connection,
        "query_parameters": query_parameters,
        "input": document,
        "task_parameters": task_parameters,
        "skill": SKILL,
        "max_retries": max_retries,
        "max_wait": max_wait,
        "parse_response": parse_response
    }

    # Run skill:
    return run_language_skill(skill_config=skill_config)
