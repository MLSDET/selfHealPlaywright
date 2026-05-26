
import yaml
class Settings:
    def __init__(self, path="config/configTest.yaml"):
        with open(path, "r") as f:
            self.config = yaml.safe_load(f)
    @property
    def base_url(self):
        return self.config["base_url"]

    @property
    def browser(self):
        return self.config["browser"]

    @property
    def headless(self):
        return self.config["headless"]

    @property
    def username(self):
        return self.config["username"]

    @property
    def password(self):
        return self.config["password"]
settings=Settings()


