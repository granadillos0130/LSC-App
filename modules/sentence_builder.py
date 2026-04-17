import time

class SentenceBuilder:
    def __init__(self, letter_delay=1.5, confidence_threshold=0.7):
        self.current_sentence = []
        self.last_letter = None
        self.last_time = time.time()
        self.letter_delay = letter_delay
        self.confidence_threshold = confidence_threshold

    def add_letter(self, letter, confidence):
        if confidence < self.confidence_threshold:
            return None

        current_time = time.time()
        time_passed = current_time - self.last_time

        if letter == self.last_letter and time_passed < self.letter_delay:
            return None

        if letter == 'SPACE':
            self.current_sentence.append(' ')
        elif letter == 'DELETE':
            if self.current_sentence:
                self.current_sentence.pop()
        else:
            self.current_sentence.append(letter)

        self.last_letter = letter
        self.last_time = current_time
        return letter

    def get_sentence(self):
        return ''.join(self.current_sentence)

    def clear(self):
        self.current_sentence = []
        self.last_letter = None
        self.last_time = time.time()