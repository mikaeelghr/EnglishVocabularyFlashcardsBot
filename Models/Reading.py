from Models.WordOccur import WordOccur

all_readings = {}


class Reading:
    def __init__(self, lesson, reading_name, words=None):
        if words is None:
            words = []
        self.lesson = lesson
        self.reading_name = reading_name
        self.words = words
        all_readings[(lesson.book_name, lesson.name, reading_name)] = self
