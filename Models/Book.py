all_books = {}


def get_books():
    return list(all_books.keys())


class Book:
    def __init__(self, name, lessons=None):
        if lessons is None:
            lessons = []
        self.name = name
        self.lessons = lessons
        all_books[name] = self
