import re
class Incident:
    def __init__(self, time, number, location, nature, ori):
        self.time = time
        self.number = number
        if re.search(r'HWY', location): 
            self.location = location.rsplit(' ', 1)[0]
        else:
            self.location = location
        if re.search(r'HWY', location) and nature=='Traffic Stop':
            self.nature = f'HWY {nature}'
        elif nature!='':
            self.nature = nature
        else:
            self.nature = 'blank'
        self.ori = ori
    
    def __str__(self):
        return f'{self.time} | {self.number} | {self.location} | {self.nature} | {self.ori}'
