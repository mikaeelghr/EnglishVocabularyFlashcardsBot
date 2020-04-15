class WordOccur:
    def __init__(self, book_name, lesson_name, reading_name, line_number):
        self.book_name = book_name
        self.lesson_name = lesson_name
        self.reading_name = reading_name
        self.line_number = line_number

    def get_tuple(self):
        return self.book_name, self.lesson_name, self.reading_name, "Line " + str(self.line_number)
