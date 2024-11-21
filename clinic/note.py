from datetime import datetime

# Note class stores notes which have a code, timestamp, and text associated with it
class Note:
    def __init__(self, code, text):
        self.code = code
        self.text = text
        self.timestamp = datetime.now()

    # Ensures that when two note objects are compared, their code and text are checked to see if they match
    def __eq__(self, other):
        if self.code == other.code and self.text == other.text:
            return True
        return False

    # change_text changes the text to a new text
    def change_text(self, text):
        self.text = text

    # change_code changes the code to a new code
    def change_code(self, code):
        self.code = code
