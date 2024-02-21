#!/usr/bin/env python3
# -*- coding: latin-1 -*-

"""Make Terraform Cloud API calls for common platform administration tasks."""
import requests
import sys
from pprint import pprint


__version__ = '1.0.0'


class TFC_API:
    """Terraform Cloud API class."""

    def __init__(self, token, org, endpoint, json_obj):
        self.token = token
        self.org = org
        self.headers = {
            'Content-Type': 'application/vnd.api+json',
            'Authorization': f'Bearer {self.token}'
        }
        self.url = 'https://app.terraform.io/api/v2'
        self.endpoint = endpoint
        self.json_obj = json_obj

    def get(self):
        """Make a GET request."""
        response = requests.get(
            f'{self.url}/{self.endpoint}',
            headers=self.headers
        )
        return response.json()
    
    def post(self):
        """Make a POST request."""
        response = requests.post(
            f'{self.url}/{self.endpoint}',
            headers=self.headers,
            json=self.json_obj
        )
        return_data = response if response else response.json()
        return return_data


def get_organization(
    token: str,
    org: str
) -> dict:
    """Get an organization."""
    endpoint = f'organizations/{org}'
    tf = TFC_API(token, org, endpoint, None)
    return tf.get()


def get_projects(
    token: str,
    org: str
) -> dict:
    """Get all projects for an organization."""
    endpoint = f'organizations/{org}/projects'
    tf = TFC_API(token, org, endpoint, None)
    return tf.get()


def get_project_id(
    token: str,
    org: str,
    project_name: str
) -> str:
    """Get a project ID."""
    project_id = 'Exception: Project not found'
    for project in get_projects(token, org)['data']:
        if project['attributes']['name'] == project_name:
            project_id = project['id']
            break
    return project_id


def get_project_ws(
    token: str,
    org: str,
    project_id: str
) -> dict:
    """Get all workspaces for a project."""
    endpoint = f'organizations/{org}/workspaces?filter%5Bproject%5D%5Bid%5D={project_id}'
    tf = TFC_API(token, org, endpoint, None)
    return tf.get()


def get_workspace_id(
    token: str,
    org: str,
    workspace_name: str
) -> str:
    """Get a workspace ID."""
    endpoint = f'organizations/{org}/workspaces/{workspace_name}'
    tf = TFC_API(token, org, endpoint, None)
    return tf.get()['data']['id']


def post_ws_to_project(
    token: str,
    project_id: str,
    workspace_id: str
) -> dict:
    """Associate a workspace with a project."""
    endpoint = f'projects/{project_id}/relationships/workspaces'
    json_obj = {
        'data': [{
            'type': 'workspaces',
            'id': workspace_id
        }]
    }
    tf = TFC_API(token, None, endpoint, json_obj)
    return tf.post()


def main():
    """Main function."""
    # Get parameters.
    org = sys.argv[1]
    token = sys.argv[2]
    pprint(get_organization(token, org))


if __name__ == '__main__':
    main()
