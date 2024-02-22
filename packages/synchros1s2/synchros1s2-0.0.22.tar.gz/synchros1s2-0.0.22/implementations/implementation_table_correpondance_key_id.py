import json
import config


def save_correspondence(correspondence):
    try:

        table = get_correspondence_table()
    except FileNotFoundError:
        table = {}
    table.update(correspondence)

    with open(config.table_correspondance_file, 'w') as f:
        json.dump(table, f)


def get_correspondence_table():
    try:
        with open(config.table_correspondance_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def get_correspondance(id):
    table = get_correspondence_table()
    return table[id]


def save_correspondance_table(key, id):
    if not verifier_existence_key(key) and not verifier_existence_id(id):
        data = get_correspondence_table()
        nouvelle_entree = {"key": key, "id": id}
        data.append(nouvelle_entree)
        with open(config.table_correspondance_file, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    return False


def verifier_existence_key(key):
    data = get_correspondence_table()
    for entry in data:
        if entry.get("key") == key:
            return True
    return False


def verifier_existence_id(id):
    data = get_correspondence_table()
    for entry in data:
        if entry.get("id") == id:
            return True
    return False


def supprimer_key_id(key=None, id=None):
    data = get_correspondence_table()
    if key is not None or id is not None:
        for entry in data:
            if entry.get("key") == key or entry.get("id") == id:
                data.remove(entry)
                with open(config.table_correspondance_file, 'w') as f:
                    json.dump(data, f, indent=4)
                return True
    return False

