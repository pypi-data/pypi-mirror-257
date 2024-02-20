import json
import requests
import config
from domains.issue import Issue
from implementations.implementation_issue_S1 import IssueImplementationS1


class IssueImplementationS2(Issue):
    key: str

    def __init__(self, key, summary, description, updated, status):
        Issue.__init__(self, summary, description, updated, status)
        self.key = key
        self.miror = self.get_miror_()
        if self.miror is not None:
            self.miror.miror = self

    def format_issue_into_json(self):
        issue = {
            "fields": {
                "description": {
                    "content": [
                        {
                            "content": [
                                {
                                    "text": self.description,
                                    "type": "text"
                                }
                            ],
                            "type": "paragraph"
                        }
                    ],
                    "type": "doc",
                    "version": 1
                },
                "issuetype": {
                    "id": config.key_issue_type
                },
                "project": {
                    "id": config.project_key
                },
                "summary": self.summary
            },
            "update": {},
        }
        if self.miror is not None:
            issue['fields'][config.s1_id_in_jira] = str(self.miror.id)
        return json.dumps(issue)

    @staticmethod
    def convertir_json_en_issue(issue_json):
        try:
            issue_key = issue_json.get('key', None)
            issue_summary = issue_json['fields'].get('summary', None)
            description_data = issue_json['fields'].get('description', None)

            description_text = None
            if description_data is not None and 'content' in description_data:
                content_list = description_data['content']

                if content_list and content_list[0].get('content'):
                    description_text = content_list[0]['content'][0].get('text', None)

            issue_updated = issue_json['fields'].get('updated', None)
            status = issue_json['fields']['status']['name']
            return IssueImplementationS2(key=issue_key, summary=issue_summary, description=description_text,
                                         updated=issue_updated,
                                         status=status)
        except Exception as e:
            print(e)
            return None

    def get(self):
        try:
            response = requests.request("GET", config.jira_url + self.key, headers=config.headers, auth=config.auth)
            json_data = response.json()
            issue = IssueImplementationS2.convertir_json_en_issue(json_data)
            if issue is not None:
                return IssueImplementationS2(key=issue.key, summary=issue.summary, description=issue.description,
                                             updated=issue.updated, status=issue.status)
        except Exception as e:
            return e

    @staticmethod
    def find_by_id(key):
        try:
            response = requests.request("GET", config.jira_url + key, headers=config.headers, auth=config.auth)
            json_data = response.json()
            issue = IssueImplementationS2.convertir_json_en_issue(json_data)
            if issue is not None:
                return IssueImplementationS2(key=issue.key, summary=issue.summary, description=issue.description,
                                             updated=issue.updated, status=issue.status)
        except Exception as e:
            return e

    @staticmethod
    def find_by(jql_query):
        payload = {"jql": jql_query}
        response = requests.get(config.jira_url_all, params=payload, headers=config.headers, auth=config.auth)
        if response.status_code == 200:
            return response.json().get("issues", [])
        else:
            print(f"Failed to execute search query. Status code: {response.status_code}")
            return []

    @staticmethod
    def delete_all(jql_query):
        payload = {"jql": jql_query}
        response = requests.get(config.jira_url_all, params=payload, headers=config.headers, auth=config.auth)
        if response.status_code == 200:
            issues = response.json().get("issues", [])
            for issue in issues:
                IssueImplementationS2.delete(issue["key"])
        else:
            return f"Failed to execute search query. Status code: {response.status_code}"

    def get_miror(self):
        response = requests.request("GET", config.jira_url + self.key, headers=config.headers, auth=config.auth)
        if response.status_code == 200:
            mirror_id = response.json()['fields'].get(config.s1_id_in_jira, None)
            miror = IssueImplementationS1.find_by_id(mirror_id)
            return miror

    # def get_miror_(self):
    #     print("trying to get mirror ")
    #     issue = S1.__new__(summary='', description='', updated=None, status='')
    #     response = requests.request("GET", config.jira_url + self.key, headers=config.headers, auth=config.auth)
    #     if response.status_code == 200:
    #          mirror_id = response.json()['fields'].get(config.s1_id_in_jira, None)
    #          miror = issue.find_by_id(mirror_id)
    #          return miror

    def change_status_name(self):
        data = {"status":
                    {"name": "En cours"}}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(config.jira_url + self.key, json=data, headers=headers, auth=config.auth)
        print(response)

    @staticmethod
    def all():
        response = requests.get(config.jira_url_all, headers=config.headers, auth=config.auth)
        issues = response.json()["issues"]
        issues_list = []
        for issue in issues:
            issues_list.append(IssueImplementationS2.convertir_json_en_issue(issue))

        return issues_list

    @staticmethod
    def all_filtre_id_et_updated():
        response = requests.get(config.jira_url_all, headers=config.headers, auth=config.auth)
        issues = response.json()["issues"]
        issues_list = []
        for issue in issues:
            issue_key = issue.get('key', None)
            issue_updated = issue['fields'].get('updated', None)
            issues_list.append(
                IssueImplementationS2(key=issue_key, summary="", description="", updated=issue_updated, status=""))
        return issues_list

    def save(self):
        response = requests.request("POST", config.jira_url, data=self.format_issue_into_json(), headers=config.headers,
                                    auth=config.auth)
        if response.status_code == 201:
            return (json.loads(response.text)).get("key")
        else:
            return f"Erreur lors de la création du ticket. Code d'erreur : {response.status_code}"

    def delete(self):
        response = requests.request("DELETE", config.jira_url + self.key, auth=config.auth)

        if response.status_code == 204:
            print(f"Suppression effectuée avec succées")
        else:
            print(f"Erreur lors de la suppression du ticket. Code d'erreur : {response.status_code}")

    def update(self):
        response = requests.request("PUT", config.jira_url + self.key, data=self.format_issue_into_json(),
                                    headers=config.headers, auth=config.auth)
        return response.text

    def change_issue_status(self, new_status):
        transition_url = config.jira_url + self.key + "/transitions"
        response = requests.get(transition_url, auth=config.auth)
        transitions = response.json()['transitions']
        transition_id = None
        for transition in transitions:
            if transition['name'] == new_status:
                transition_id = transition['id']
                break
        if not transition_id:
            return None

        data = {
            "transition": {"id": transition_id}
        }
        headers = {'Content-Type': 'application/json'}

        response = requests.post(transition_url, json=data, headers=headers, auth=config.auth)

        if response.status_code == 204:
            return transition_id
        else:
            print("Erreur lors du changement de statut:", response.text)
            return None

    @staticmethod
    def supprimer_tickets_entre_a_and_b(a, b):
        for i in range(a, b):
            key = "KAN-" + str(i)
            issue_to_delete = IssueImplementationS2(key=key, summary="", description="", updated="", status="")
            issue_to_delete.delete()


if __name__ == '__main__':
    IssueImplementationS2.supprimer_tickets_entre_a_and_b(1045, 1190)
