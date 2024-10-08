class Floor:
    def __init__(self, floor_num):
        self.floor_num = floor_num
        self.requests = []
    
    def add_request(self, passenger):
        self.requests.append(passenger)
