from dataclasses import dataclass


@dataclass
class HistoriqueSynchronisation:
    date: str
    synchro_message: str

    def save_synchronisation(self):
        pass
