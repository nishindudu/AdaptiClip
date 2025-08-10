import json

class JSONPrettyPrint:
    def __init__(self, config):
        self.config = config
        if not self.config.has_section(str(self.__class__.__name__)):
            self.config.add_section(str(self.__class__.__name__))
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

    def detect(self, text):
        try:
            json.loads(text)
            return True
        except json.JSONDecodeError:
            return False
        except Exception as e:
            return False

    def convert(self, text):
        parsed = json.loads(text)
        return json.dumps(parsed, indent=4)
