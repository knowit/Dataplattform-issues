from data_types.AbstractType import AbstractType

"""
Example of a Github doc in raw format:
{
    "data": {
        "ref": "refs/heads/master",
        "before": "afccc6cf3053d0efcfdcbe95441c16746c2026d8",
        "after": "605417583221e397e13d15b369a9cf6a3ffc9b2e",
        "created": false,
        "deleted": false,
        "forced": false,
        "base_ref": null,
        "compare": "https://github.com/Tinusf/Dataplattform/compare/afccc6cf3053...605417583221",
        "commits": [
            {
                "id": "605417583221e397e13d15b369a9cf6a3ffc9b2e",
                "tree_id": "8f303c87d203a139b02e29bd89b23abb1c46e6a1",
                "distinct": true,
                "message": "Document folder structure and AWS lambda setup. Rename lambda handlers.",
                "timestamp": "2019-06-21T13:29:31+02:00",
                "url": "https://github.com/Tinusf/Dataplattform/commit/605417583221e397e13d15b369a9cf6a3ffc9b2e",
                "author": {
                    "name": "Aksel Slettemark",
                    "email": "akselslettemark@gmail.com",
                    "username": "aslettemark"
                },
                "committer": {
                    "name": "Aksel Slettemark",
                    "email": "akselslettemark@gmail.com",
                    "username": "aslettemark"
                },
                "added": [
                    "lambda/README.md",
                    "lambda/fetchers/get_docs/lambda_function.py",
                    "lambda/ingest/lambda_function.py"
                ],
                "removed": [
                    "lambda/fetchers/get_docs/handler.py",
                    "lambda/ingest/handler.py"
                ],
                "modified": [
                    "README.md"
                ]
            }
        ],
        "head_commit": {
            "id": "605417583221e397e13d15b369a9cf6a3ffc9b2e",
            "tree_id": "8f303c87d203a139b02e29bd89b23abb1c46e6a1",
            "distinct": true,
            "message": "Document folder structure and AWS lambda setup. Rename lambda handlers.",
            "timestamp": "2019-06-21T13:29:31+02:00",
            "url": "https://github.com/Tinusf/Dataplattform/commit/605417583221e397e13d15b369a9cf6a3ffc9b2e",
            "author": {
                "name": "Aksel Slettemark",
                "email": "akselslettemark@gmail.com",
                "username": "aslettemark"
            },
            "committer": {
                "name": "Aksel Slettemark",
                "email": "akselslettemark@gmail.com",
                "username": "aslettemark"
            },
            "added": [
                "lambda/README.md",
                "lambda/fetchers/get_docs/lambda_function.py",
                "lambda/ingest/lambda_function.py"
            ],
            "removed": [
                "lambda/fetchers/get_docs/handler.py",
                "lambda/ingest/handler.py"
            ],
            "modified": [
                "README.md"
            ]
        },
        "repository": {
            "id": 192526607,
            "node_id": "MDEwOlJlcG9zaXRvcnkxOTI1MjY2MDc=",
            "name": "Dataplattform",
            "full_name": "Tinusf/Dataplattform",
            "private": true,
            "owner": {
                "name": "Tinusf",
                "email": "tinus@flagstad.as",
                "login": "Tinusf",
                "id": 10515239,
                "node_id": "MDQ6VXNlcjEwNTE1MjM5",
                "avatar_url": "https://avatars2.githubusercontent.com/u/10515239?v=4",
                "gravatar_id": "",
                "url": "https://api.github.com/users/Tinusf",
                "html_url": "https://github.com/Tinusf",
                "followers_url": "https://api.github.com/users/Tinusf/followers",
                "following_url": "https://api.github.com/users/Tinusf/following{/other_user}",
                "gists_url": "https://api.github.com/users/Tinusf/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/Tinusf/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/Tinusf/subscriptions",
                "organizations_url": "https://api.github.com/users/Tinusf/orgs",
                "repos_url": "https://api.github.com/users/Tinusf/repos",
                "events_url": "https://api.github.com/users/Tinusf/events{/privacy}",
                "received_events_url": "https://api.github.com/users/Tinusf/received_events",
                "type": "User",
                "site_admin": false
            },
            "html_url": "https://github.com/Tinusf/Dataplattform",
            "description": null,
            "fork": false,
            "url": "https://github.com/Tinusf/Dataplattform",
            "forks_url": "https://api.github.com/repos/Tinusf/Dataplattform/forks",
            "keys_url": "https://api.github.com/repos/Tinusf/Dataplattform/keys{/key_id}",
            "collaborators_url": "https://api.github.com/repos/Tinusf/Dataplattform/collaborators{/collaborator}",
            "teams_url": "https://api.github.com/repos/Tinusf/Dataplattform/teams",
            "hooks_url": "https://api.github.com/repos/Tinusf/Dataplattform/hooks",
            "issue_events_url": "https://api.github.com/repos/Tinusf/Dataplattform/issues/events{/number}",
            "events_url": "https://api.github.com/repos/Tinusf/Dataplattform/events",
            "assignees_url": "https://api.github.com/repos/Tinusf/Dataplattform/assignees{/user}",
            "branches_url": "https://api.github.com/repos/Tinusf/Dataplattform/branches{/branch}",
            "tags_url": "https://api.github.com/repos/Tinusf/Dataplattform/tags",
            "blobs_url": "https://api.github.com/repos/Tinusf/Dataplattform/git/blobs{/sha}",
            "git_tags_url": "https://api.github.com/repos/Tinusf/Dataplattform/git/tags{/sha}",
            "git_refs_url": "https://api.github.com/repos/Tinusf/Dataplattform/git/refs{/sha}",
            "trees_url": "https://api.github.com/repos/Tinusf/Dataplattform/git/trees{/sha}",
            "statuses_url": "https://api.github.com/repos/Tinusf/Dataplattform/statuses/{sha}",
            "languages_url": "https://api.github.com/repos/Tinusf/Dataplattform/languages",
            "stargazers_url": "https://api.github.com/repos/Tinusf/Dataplattform/stargazers",
            "contributors_url": "https://api.github.com/repos/Tinusf/Dataplattform/contributors",
            "subscribers_url": "https://api.github.com/repos/Tinusf/Dataplattform/subscribers",
            "subscription_url": "https://api.github.com/repos/Tinusf/Dataplattform/subscription",
            "commits_url": "https://api.github.com/repos/Tinusf/Dataplattform/commits{/sha}",
            "git_commits_url": "https://api.github.com/repos/Tinusf/Dataplattform/git/commits{/sha}",
            "comments_url": "https://api.github.com/repos/Tinusf/Dataplattform/comments{/number}",
            "issue_comment_url": "https://api.github.com/repos/Tinusf/Dataplattform/issues/comments{/number}",
            "contents_url": "https://api.github.com/repos/Tinusf/Dataplattform/contents/{+path}",
            "compare_url": "https://api.github.com/repos/Tinusf/Dataplattform/compare/{base}...{head}",
            "merges_url": "https://api.github.com/repos/Tinusf/Dataplattform/merges",
            "archive_url": "https://api.github.com/repos/Tinusf/Dataplattform/{archive_format}{/ref}",
            "downloads_url": "https://api.github.com/repos/Tinusf/Dataplattform/downloads",
            "issues_url": "https://api.github.com/repos/Tinusf/Dataplattform/issues{/number}",
            "pulls_url": "https://api.github.com/repos/Tinusf/Dataplattform/pulls{/number}",
            "milestones_url": "https://api.github.com/repos/Tinusf/Dataplattform/milestones{/number}",
            "notifications_url": "https://api.github.com/repos/Tinusf/Dataplattform/notifications{?since,all,participating}",
            "labels_url": "https://api.github.com/repos/Tinusf/Dataplattform/labels{/name}",
            "releases_url": "https://api.github.com/repos/Tinusf/Dataplattform/releases{/id}",
            "deployments_url": "https://api.github.com/repos/Tinusf/Dataplattform/deployments",
            "created_at": 1560857258,
            "updated_at": "2019-06-21T08:28:17Z",
            "pushed_at": 1561116650,
            "git_url": "git://github.com/Tinusf/Dataplattform.git",
            "ssh_url": "git@github.com:Tinusf/Dataplattform.git",
            "clone_url": "https://github.com/Tinusf/Dataplattform.git",
            "svn_url": "https://github.com/Tinusf/Dataplattform",
            "homepage": null,
            "size": 13,
            "stargazers_count": 0,
            "watchers_count": 0,
            "language": "Python",
            "has_issues": true,
            "has_projects": true,
            "has_downloads": true,
            "has_wiki": true,
            "has_pages": false,
            "forks_count": 0,
            "mirror_url": null,
            "archived": false,
            "disabled": false,
            "open_issues_count": 0,
            "license": null,
            "forks": 0,
            "open_issues": 0,
            "watchers": 0,
            "default_branch": "master",
            "stargazers": 0,
            "master_branch": "master"
        },
        "pusher": {
            "name": "aslettemark",
            "email": "akselslettemark@gmail.com"
        },
        "sender": {
            "login": "aslettemark",
            "id": 7214852,
            "node_id": "MDQ6VXNlcjcyMTQ4NTI=",
            "avatar_url": "https://avatars0.githubusercontent.com/u/7214852?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/aslettemark",
            "html_url": "https://github.com/aslettemark",
            "followers_url": "https://api.github.com/users/aslettemark/followers",
            "following_url": "https://api.github.com/users/aslettemark/following{/other_user}",
            "gists_url": "https://api.github.com/users/aslettemark/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/aslettemark/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/aslettemark/subscriptions",
            "organizations_url": "https://api.github.com/users/aslettemark/orgs",
            "repos_url": "https://api.github.com/users/aslettemark/repos",
            "events_url": "https://api.github.com/users/aslettemark/events{/privacy}",
            "received_events_url": "https://api.github.com/users/aslettemark/received_events",
            "type": "User",
            "site_admin": false
        }
    },
    "type": "GithubType",
    "timestamp": 1561372607,
    "id": "AAAAAF0Qp79lNx8dkdk1qQ=="
}

Example of how the SQL table should look like:

CREATE TABLE GithubType (
    id VARCHAR(24) NOT NULL,
    timestamp BIGINT NOT NULL,
    commit_id TEXT,
    PRIMARY KEY (id)
);

"""


class GithubType(AbstractType):
    """
    Example: if you want to keep ["data"]["commits"][0]["id"] and save it as commit_id
    You could use this configure the attributes_keep dictionary like this:
    attributes_keep = {
        "commit_id": ["data", "commits", 0, "id"]
    }
    """
    attributes_keep = {
        "commit_id": ["data", "commits", 0, "id"]
    }
