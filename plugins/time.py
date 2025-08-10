from datetime import datetime


class TimeConverter():
    def __init__(self, CONFIG):
        self.config = CONFIG

        if not self.config.has_section(str(self.__class__.__name__)):
            self.config.add_section(str(self.__class__.__name__))
        if not self.config.has_option(str(self.__class__.__name__), "format"):
            self.config.set(str(self.__class__.__name__), "format", "24h")
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

        self.time_format = CONFIG.get(str(self.__class__.__name__), "format")
    
    def is_12h_format(self, text):
        try:
            datetime.strptime(text, "%I:%M %p")
            return True
        except ValueError:
            return False

    def is_24h_format(self, text):
        try:
            datetime.strptime(text, "%H:%M")
            return True
        except ValueError:
            return False

    def detect(self, text):
        if self.time_format.lower() == "12h":
            return self.is_24h_format(text)
        elif self.time_format.lower() == "24h":
            return self.is_12h_format(text)
        return False

    def convert(self, text):
        if self.time_format.lower() == "24h":
            try:
                t = datetime.strptime(text, "%I:%M %p")
                return t.strftime("%H:%M")
            except ValueError:
                return None
        elif self.time_format.lower() == "12h":
            try:
                t = datetime.strptime(text, "%H:%M")
                return t.strftime("%I:%M %p")
            except ValueError:
                return None
        return None