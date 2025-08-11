import dateutil.parser

class DateConverter():
    def __init__(self, CONFIG):
        self.config = CONFIG
        
        self.config.write("format", "%%d-%%m-%%Y")
        self.date_format = self.config.read("format")

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