import yaml
import json

__all__ = [
    "RepoConfig"
]

# This class is used to handle the configuration of the repository
class RepoConfig():
# This function initializes the RepoConfig class and loads the configuration from the ai.yaml file

    def __init__(self, path: str):
        with open(path + "/ai.yaml", 'r') as file:
            config = yaml.safe_load(file)
            self.name = config.get("name")
            self.description = config.get("description")
# This function returns a string representation of the RepoConfig object
            self.exclude_list = config.get("exclude")

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)