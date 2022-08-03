class Politician:
    def __init__(self, first_name, last_name, party, state, residence, date_born):
        self.first_name = first_name
        self.last_name = last_name
        self.party = party
        self.state = state
        self.residence = residence
        self.date_born = date_born

    def getPoliticianType(self):
        raise NotImplementedError()

