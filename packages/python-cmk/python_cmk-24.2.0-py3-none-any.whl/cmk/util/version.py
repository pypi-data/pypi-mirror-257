import re

class Version:
    def __init__(self, *numbers):
       self.numbers = numbers
       if len(numbers) == 1 and isinstance(numbers[0], str):
         self.numbers = [int(x) for x in re.findall('\d+', numbers[0])]

