import yaml
import json

__all__ = [
    "RepoConfig"
]

class RepoConfig():
    """
    This class represents the configuration of a repository.
    It is initialized with a path to the configuration file.
    """

def __init__(self, path: str):
        """
        Initializes the RepoConfig object.
        
        Parameters:
        path (str): The path to the configuration file.
        """
        with open(path + "/ai.yaml", 'r') as file:
            config = yaml.safe_load(file)
            self.name = config.get("name")
            self.description = config.get("description")
            self.exclude_list = config.get("exclude")

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)