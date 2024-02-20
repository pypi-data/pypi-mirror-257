import logging

import config_version2
from domains.issue import Issue
from implementations.S11 import S1
from implementations.implementation_issue_S1 import IssueImplementationS1
from implementations.implementation_issue_S2 import IssueImplementationS2

logging.basicConfig(filename=config.log_file, level=logging.INFO, format=config.log_format)


class Synchronisation:
    issue = S1.__new__(summary='', description='', updated=None, status='')

    @staticmethod
    def synchronisation_S2_S1():
        issues_in_S2 = IssueImplementationS2.all_filtre_id_et_updated()
        for issue_in_S2 in issues_in_S2:
            miror_S1_de_S2 = issue_in_S2.miror
            if miror_S1_de_S2 is None:
                issue_complet_S2 = issue_in_S2.get()
                issue_S2_convertie_en_S1 = IssueImplementationS1.convertirS_enS_(issue_complet_S2)
                issue_complet_S2.miror = issue_S2_convertie_en_S1.save()
                issue_complet_S2.update()
                logging.info(f"Ajout du ticket N°{issue_complet_S2.key} dans S1")

            # elif miror_S1_de_S2 and Issue.date_S1_entre_date_derniere_synchro_et_date_S2(miror_S1_de_S2.updated,
            #                                                                           issue_in_S2.updated):
            #     issue_complet_S2_convertie_en_S1.update()
            #     logging.info(f"Modification du ticket N°{issue_in_S2.key} dans S1")

            # issue_in_S1 = Issue.trouver(issue_in_S2, issues_in_S1)
            # issue_to_save_or_update = IssueImplementationS1.convertirS_enS_(issue_in_S2.get())
            # if issue_in_S1 is None:
            #     issue_to_save_or_update.save()
            #     logging.info(f"Ajout du ticket N°{issue_in_S2.key} dans S1")
            #     # Changer fonction date_S1_entre_date_derniere_synchro_et_date_S2 en utilisant mirror
            # elif issue_in_S1 and Issue.date_S1_entre_date_derniere_synchro_et_date_S2(issue_in_S1.updated,
            #                                                                           issue_in_S2.updated):
            #     issue_to_save_or_update.update()
            #     logging.info(f"Modification du ticket N°{issue_in_S2.key} dans S1")

    @staticmethod
    def synchronisation_S2_S1_modification_de_chaque_attribut():
        issues_in_S2 = IssueImplementationS2.all_filtre_id_et_updated()
        issues_in_S1 = issue.all_filtre_id_et_updated()
        for issue_in_S2 in issues_in_S2:
            issue_in_S1 = Issue.trouver(issue_in_S2, issues_in_S1)
            if issue_in_S1 is None:
                issue_to_save_or_update = IssueImplementationS1.convertirS_enS_(issue_in_S2.get())
                issue_to_save_or_update.save()
                logging.info(f"Ajout du ticket N°{issue_in_S2.key} dans S1")
                # Changer fonction date_S1_entre_date_derniere_synchro_et_date_S2 en utilisant mirror
            elif issue_in_S1 and Issue.date_S1_entre_date_derniere_synchro_et_date_S2(issue_in_S1.updated,
                                                                                      issue_in_S2.updated):
                Synchronisation.synchronisation_summary_S2_S1_Version2()
                Synchronisation.synchronisation_description_S2_S1_Version2()
                logging.info(f"Modification du ticket N°{issue_in_S2.key} dans S1")

    @staticmethod
    def synchronisation_S1_S2():
        try:
            issues_in_S2 = IssueImplementationS2.all_filtre_id_et_updated()
            issues_in_S1 = IssueImplementationS1.all_filtre_id_et_updated()
            for issue_in_S1 in issues_in_S1:
                issue_in_S2 = Issue.trouver(issue_in_S1, issues_in_S2)
                issue_to_save_or_update = IssueImplementationS2.convertirS_enS_(issue_in_S1.get())
                if issue_in_S2 is None:
                    issue_to_save_or_update.key = "KAN-12"
                    new_key = issue_to_save_or_update.save()  # Save in jira
                    issue_in_S1.key = new_key
                    issue_in_S1.update()
                    break
        except Exception as e:
            print(e)

    # @staticmethod
    # def synchonisation_status_S1_S2():  # synchro status entre S1 et S2
    #     issues_in_S1 = IssueImplementationS1.all_filtre_key_et_updated()
    #     for issue_in_S1 in issues_in_S1:
    #         correspondant_S2 = IssueImplementationS2.get(issue_in_S1)
    #         if correspondant_S2:
    #             print(correspondant_S2)
    #             correspondant_S2.change_issue_status(config.status_dict_S1_to_S2[issue_in_S1.status])
    #
    # @staticmethod
    # def synchonisation_status_S2_S1():
    #     issues_in_S2 = IssueImplementationS2.all_filtre_id_et_updated()
    #     for issue_in_S2 in issues_in_S2:
    #         correspondant_S1 = IssueImplementationS1.get(issue_in_S2)
    #         if correspondant_S1:
    #             print(correspondant_S1)
    #             correspondant_S1.change_issue_status(config.status_dict_S2_to_S1[issue_in_S2.status])


if __name__ == "__main__":
    Synchronisation.synchronisation_S2_S1()
