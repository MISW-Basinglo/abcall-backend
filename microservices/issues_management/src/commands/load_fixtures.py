import json

from flask import current_app  # noqa
from src.common.logger import logger
from src.repositories.issues_repository import IssuesManagementRepository
from src.serializers.serializers import IssueCreateSerializer

FIXTURES_FILE_PATH = "src/fixtures/fixtures.json"


def register_commands(app):
    @app.cli.command("load-fixtures")
    def load_fixtures():
        """Command to load test data (fixtures) from a JSON file."""
        logger.info(f"Loading test data from {FIXTURES_FILE_PATH}...")
        with open(FIXTURES_FILE_PATH, "r") as f:
            data = json.load(f)

        issue_repository = IssuesManagementRepository()

        data_to_create = []
        issues_ids = {issue["id"] for issue in data["issues"]}
        issues_instances = issue_repository.get_all()
        issues_instances_ids = {issue.id for issue in issues_instances}

        not_populated_issues = issues_ids - issues_instances_ids

        for issue in data["issues"]:
            if issue["id"] in not_populated_issues:
                del issue["id"]
                data_to_create.append(IssueCreateSerializer().load(issue))

        for issue in data_to_create:
            issue_repository.create(issue)

        logger.info(f"Test data loaded successfully from {FIXTURES_FILE_PATH}.")
