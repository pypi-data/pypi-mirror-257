import logging
import os
from requests.auth import HTTPBasicAuth

main_directory = os.path.dirname(os.path.abspath(__file__))

log_file = main_directory + "/log/file.log"

table_correspondance_file = main_directory + "/files/correspondance_table.json"

history_file = main_directory + "/files/history.txt"

log_format = '%(asctime)s - %(levelname)s - %(message)s'

database_file = "sqlite:///" + main_directory + "/database/issues_bd.db"

#Username du compte jira
username = ""

#Token du compte jira
api_token = ""

#Jira url de base
jira_url_base = ""
#Jira url pour récupérer un ticket
jira_url_ticket = jira_url_base + "rest/api/3/issue/"
#Jira url pour récupérer tout les ticket
jira_url_all = jira_url_base + "rest/api/3/search"

auth = HTTPBasicAuth(username, api_token)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

#La clé - attribut Key du projet
project_key = ""
#La clé des tickets - attribut Key du issue
key_issue_type = ""

last_synchronized_data_in_S2 = '2023-01-11T09:33:44.695+0100'

status_dict_S1_to_S2 = {"status1": "To Do", "status2": "Pret", "status3": "In Progress", "status4": "Done"}
status_dict_S2_to_S1 = {"En attente": "status1", "Pret": "status2", "en cours": "status3", "Qualifications": "status4"}

#L'attribut de l'id de S1 dans jira
s1_id_in_jira = "customfield_10034"
s1_class = "S3"

module_to_use = "implementations.implementation_issue_S3"
class_to_use = "IssueImplementationS3"