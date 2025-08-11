import json

class JSONPrettyPrint:
    def __init__(self, config):
        self.config = config
        self.config.write("on_keypress", "false")
        self.config.write("hotkey", "ctrl+alt+j")

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
