# coding: utf-8

# inspired by https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/readers/llama-index-readers-jira
# we do some customization for our case

from typing import List, Optional, TypedDict

from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document


class BasicAuth(TypedDict):
    email: str
    api_token: str
    server_url: str


class Oauth2(TypedDict):
    cloud_id: str
    api_token: str


class PATauth(TypedDict):
    server_url: str
    api_token: str


class JiraReader(BaseReader):
    """Jira reader. Reads data from Jira issues from passed query.

    Args:
        Optional basic_auth:{
            "email": "email",
            "api_token": "token",
            "server_url": "server_url"
        }
        Optional oauth:{
            "cloud_id": "cloud_id",
            "api_token": "token"
        }
        Optional patauth:{
            "server_url": "server_url",
            "api_token": "token"
        }
    """

    def __init__(
        self,
        email: Optional[str] = None,
        api_token: Optional[str] = None,
        server_url: Optional[str] = None,
        BasicAuth: Optional[BasicAuth] = None,
        Oauth2: Optional[Oauth2] = None,
        PATauth: Optional[PATauth] = None,
    ) -> None:
        from jira import JIRA

        if email and api_token and server_url:
            if BasicAuth is None:
                BasicAuth = {}
            BasicAuth["email"] = email
            BasicAuth["api_token"] = api_token
            BasicAuth["server_url"] = server_url

        if Oauth2:
            options = {
                "server": f"https://api.atlassian.com/ex/jira/{Oauth2['cloud_id']}",
                "headers": {"Authorization": f"Bearer {Oauth2['api_token']}"},
            }
            self.jira = JIRA(options=options)
        elif PATauth:
            options = {
                "server": PATauth["server_url"],
                "headers": {"Authorization": f"Bearer {PATauth['api_token']}"},
            }
            self.jira = JIRA(options=options)
        else:
            self.jira = JIRA(
                basic_auth=(BasicAuth["email"], BasicAuth["api_token"]),
                server=f"https://{BasicAuth['server_url']}",
            )

    def load_data(self, query: str) -> List[Document]:
        relevant_issues = self.jira.search_issues(query)

        issues = []

        assignee = ""
        reporter = ""
        affects_versions = []
        fix_versions = []
        components = []
        comments = []
        all_comments = ""
        for issue in relevant_issues:
            if issue.fields.versions:
                for version in issue.fields.versions:
                    affects_versions.append(version.name)
            print(affects_versions)

            if issue.raw["fields"]["fixVersions"]:
                for fixVersion in issue.raw["fields"]["fixVersions"]:
                    fix_versions.append(fixVersion["name"])
            print(fix_versions)

            if issue.raw["fields"]["components"]:
                for component in issue.raw["fields"]["components"]:
                    components.append(component["name"])
            print(components)

            if issue.fields.assignee:
                assignee = issue.fields.assignee.emailAddress
                print(assignee)
            
            if issue.fields.reporter:
                reporter = issue.fields.reporter.emailAddress
                print(reporter)
            
            if issue.fields.comment.comments:
                for comment in issue.fields.comment.comments:
                    comments.append(comment.body)
                all_comments = "\n".join(comments)

            issues.append(
                Document(
                    text=f"{issue.fields.summary} \n {issue.fields.description} \n {all_comments}",
                    extra_info={
                        "key": issue.key,
                        "title": issue.fields.summary,
                        "url": issue.permalink(),
                        "created_at": issue.fields.created,
                        "updated_at": issue.fields.updated,
                        "labels": issue.fields.labels,
                        "status": issue.fields.status.name,
                        "assignee": assignee,
                        "reporter": reporter,
                        "project": issue.fields.project.name,
                        "issue_type": issue.fields.issuetype.name,
                        "priority": issue.fields.priority.name,
                        "fix_versions": fix_versions,
                    },
                )
            )

        return issues
