all_lessons = {}


def get_lessons(book_names):
    return [x[1] for x in list(filter(lambda lesson_key: lesson_key[0] in book_names, all_lessons.keys()))]


class Lesson:
    def __init__(self, book_name, name, readings=None):
        if readings is None:
            readings = []
        self.book_name = book_name
        self.name = name
        self.readings = readings
        all_lessons[(book_name, name)] = self
