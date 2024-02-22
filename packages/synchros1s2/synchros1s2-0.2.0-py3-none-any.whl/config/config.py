import os
from requests.auth import HTTPBasicAuth


class config:
    def __init__(self, project_key, key_issue_type, username, api_token, jira_url_base):
        main_directory = os.path.dirname(os.path.abspath(__file__))
        self.log_file = main_directory + "/log/file.log"
        self.table_correspondance_file = main_directory + "/files/correspondance_table.json"
        self.history_file = main_directory + "/files/history.txt"
        self.log_format = '%(asctime)s - %(levelname)s - %(message)s'
        self.database_file = "sqlite:///" + main_directory + "/database/issues_bd.db"
        self.last_synchronized_data_in_S2 = '2023-01-11T09:33:44.695+0100'
        self.status_dict_S1_to_S2 = {"status1": "To Do", "status2": "Pret", "status3": "In Progress",
                                     "status4": "Done"}
        self.status_dict_S2_to_S1 = {"En attente": "status1", "Pret": "status2", "en cours": "status3",
                                     "Qualifications": "status4"}
        self.s1_id_in_jira = "customfield_10034"
        self.s1_class = "S3"
        self.module_to_use = "implementations.implementation_issue_S3"
        self.class_to_use = "IssueImplementationS3"

        # Initialisez les variables passées en paramètres
        self.project_key = project_key
        self.key_issue_type = key_issue_type
        self.username = username
        self.api_token = api_token
        self.jira_url_base = jira_url_base
        self.jira_url_ticket = self.jira_url_base + "rest/api/3/issue/"
        self.jira_url_all = self.jira_url_base + "rest/api/3/search"
        self.auth = HTTPBasicAuth(self.username, self.api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
