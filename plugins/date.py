import dateutil.parser

class DateConverter():
    def __init__(self, CONFIG):
        self.config = CONFIG

        if not self.config.has_section(str(self.__class__.__name__)):
            self.config.add_section(str(self.__class__.__name__))
        if not self.config.has_option(str(self.__class__.__name__), "format"):
            self.config.set(str(self.__class__.__name__), "format", "%%d-%%m-%%Y")
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

        self.date_format = CONFIG.get(str(self.__class__.__name__), "format")

    def detect(self, text):
        try:
            date = dateutil.parser.parse(text, dayfirst=True, default=None)
            if str(date.time()) != "00:00:00":
                return False
        except ValueError:
            return False
        except Exception:
            return False
        return True
    
    def convert(self, text):
        date = dateutil.parser.parse(text, dayfirst=True)
        return date.strftime(self.date_format)