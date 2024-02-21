import logging
import config
from implementations.implementation_issue_S1 import IssueImplementationS1
from implementations.implementation_issue_S2 import IssueImplementationS2
from implementations.implementation_table_correpondance_key_id import verifier_existence_id, save_correspondance_table

logging.basicConfig(filename=config.log_file, level=logging.INFO, format=config.log_format)


class Synchronisation:
    # issue = S1.__new__(summary='', description='', updated=None, status='')

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
    def synchronisation_S1_S2():  # Créer a partir de S1 tout les S2
        issues_in_S1 = IssueImplementationS1.all_filtre_id_et_updated()
        for issue_in_S1 in issues_in_S1:
            if not verifier_existence_id(issue_in_S1.id):
                issue_complet_S1 = IssueImplementationS1.find_by_id(issue_in_S1.id)
                correspondance_S2 = IssueImplementationS2.convertirS_enS_(issue_complet_S1)
                correspondance_S2.miror = issue_in_S1
                key = correspondance_S2.save()
                save_correspondance_table(key, issue_in_S1.id)


if __name__ == "__main__":
    # issue = IssueImplementationS1(summary="test1", description="", updated=None, status="None").save()
    # print(issue)
    # print(IssueImplementationS1.all())
    # print(IssueImplementationS2.all())
    Synchronisation.synchronisation_S1_S2()
