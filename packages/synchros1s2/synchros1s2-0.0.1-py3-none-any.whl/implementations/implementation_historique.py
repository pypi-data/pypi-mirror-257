from domains.historique import HistoriqueSynchronisation
import config_version2

class ImplementationHistorique(HistoriqueSynchronisation):

    def save_synchronisation(self):
        try:
            with open(config.history_file,"a") as history:
                history.write(self.date + "," + self.synchro_message + "\n")
                history.close()
                return True
        except Exception as e:
            print(e)
            return False
