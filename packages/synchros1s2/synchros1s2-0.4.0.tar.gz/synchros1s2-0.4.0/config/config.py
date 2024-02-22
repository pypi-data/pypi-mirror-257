import os
from requests.auth import HTTPBasicAuth


class config:
    main_directory = os.path.dirname(os.path.abspath(__file__))
    log_file = main_directory + "/log/file.log"
    table_correspondance_file = main_directory + "/files/correspondance_table.json"
    history_file = main_directory + "/files/history.txt"
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    database_file = "sqlite:///" + main_directory + "/database/issues_bd.db"
    last_synchronized_data_in_S2 = '2023-01-11T09:33:44.695+0100'
    status_dict_S1_to_S2 = {"status1": "To Do", "status2": "Pret", "status3": "In Progress",
                            "status4": "Done"}
    status_dict_S2_to_S1 = {"En attente": "status1", "Pret": "status2", "en cours": "status3",
                            "Qualifications": "status4"}
    s1_id_in_jira = "customfield_10034"
    s1_class = "S3"
    module_to_use = "implementations.implementation_issue_S3"
    class_to_use = "IssueImplementationS3"

    project_key = ""
    key_issue_type = ""
    username = ""
    api_token = ""
    jira_url_base = ""
    jira_url_ticket = jira_url_base + "rest/api/3/issue/"
    jira_url_all = jira_url_base + "rest/api/3/search"
    auth = HTTPBasicAuth(username, api_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    def __init__(self, project_key, key_issue_type, username, api_token, jira_url_base):
        self.project_key = project_key
        self.key_issue_type = key_issue_type
        self.username = username
        self.api_token = api_token
        self.jira_url_base = jira_url_base
        self.jira_url_ticket = self.jira_url_base + "rest/api/3/issue/"
        self.jira_url_all = self.jira_url_base + "rest/api/3/search"
        self.auth = HTTPBasicAuth(self.username, self.api_token)

