import os
import shutil

class StoragePaths:
    """ Classe para interagir com as pastas do storage local.
    """

    def __init__(self):
        self.storage = "/opt/airflow/storage"

    def get_path_in_layer(self, layer_name: str,
                            file_name: str = None) -> str:
        """ Generates a path string for a given layer and timestamp"""

        return f"{self.storage}/{layer_name}/" + (file_name or "")

    def get_file_list_in_layer(self, layer_name: str) -> list:

        path = f"{self.storage}/{layer_name}"

        file_list = [f for f in os.listdir(path)]

        return file_list

    def get_file_list_paths_in_layer(self, layer_name: str) -> list:

        path = f"{self.storage}/{layer_name}"

        file_list = [os.path.join(path, f) for f in os.listdir(path)]

        return file_list

    def clear_layer(self, layer_name: str) -> None:

        path = self.storage + layer_name

        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
