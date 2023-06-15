class User:
    def __init__(self, name):
        self.name = name
        self.formatted_name = str(self.name).split('#')[0]
        self.reading_list = []
        self.read_list = []
        
    def getUserReadingTitles(self):
        return None
        