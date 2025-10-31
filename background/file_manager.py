# background/file_manager.py
import os
import sys
import json
def resource_base_dir():
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "data")
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
class FileManager:
    DEFAULT_FILES = ["users.json", "doctors.json", "patients.json", "appointments.json"]
    @staticmethod
    def ensure_data_folder():
        folder = resource_base_dir()
        os.makedirs(folder, exist_ok=True)
        for fname in FileManager.DEFAULT_FILES:
            fpath = os.path.join(folder, fname)
            if not os.path.exists(fpath):
                with open(fpath, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4, ensure_ascii=False)
        return folder
    @staticmethod
    def filepath(filename):
        folder = FileManager.ensure_data_folder()
        return os.path.join(folder, f"{filename}.json")
    @staticmethod
    def load_data(filename):
        path = FileManager.filepath(filename)
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"[FileManager] JSON decode error in {path} — returning [].")
            return []
    @staticmethod
    def save_data(filename, data):
        path = FileManager.filepath(filename)
        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[FileManager] Error saving {path}: {e}")
            return False
    @staticmethod
    def delete_by_key(filename, key_name, key_value):
        items = FileManager.load_data(filename)
        new_items = [it for it in items if str(it.get(key_name)) != str(key_value)]
        return FileManager.save_data(filename, new_items)
    @staticmethod
    def fetch(data_list, compare_value, wanted_item=None):
        for item in data_list:
            for key, val in item.items():
                if key == "password":
                    continue
                if str(val) == str(compare_value):
                    return item.get(wanted_item) if wanted_item else item
        return None