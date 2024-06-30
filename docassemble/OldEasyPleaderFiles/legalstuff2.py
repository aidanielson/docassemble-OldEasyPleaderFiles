from docassemble.base.util import Individual, DAList, DAObject

__all__ = ['Attorney', 'AttorneyList', 'Party', 'PartyList', 'Case', 'load_test_parties']

def load_test_parties():
  case.parties.auto.gather = False
  case.parties.gathered = True
  case.parties[0].name.first = 'Michael'
  case.parties[0].name.last = 'Anderson'
  case.parties[0].attorneys.there_are_any = True
  case.parties[0].attorneys[0].name.first = 'Samuel'
  case.parties[0].attorneys[0].name.last = 'Clemens'
  case.parties[0].attorneys[0].law_firm = 'Clemens & Associates'
  case.parties[0].attorneys[0].address.address = '1234 Main Street, Suite 125'
  case.parties[0].attorneys[0].address.city = 'Sacramento'
  case.parties[0].attorneys[0].address.state = 'California'
  case.parties[0].attorneys[0].address.zip = '95432'
  case.parties[0].attorneys[0].phone_number = '9165673456'
  case.parties[0].attorneys[0].email = 'Sam@Clemens.com'
  case.parties[0].attorneys[0].there_is_another = False
  
class Attorney(Individual):
    @property
    def complete(self):
        self.name.first
        self.address.address
        self.phone_number
        self.email
        return True

class AttorneyList(DAList):
    def init(self, *pargs, **kwargs):
        if 'object_type' not in kwargs:
            kwargs['object_type'] = Attorney
        kwargs['complete_attribute'] = 'complete'
        super().init(*pargs, **kwargs)

class Party(Individual):
    complete_attribute = 'complete'

    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)
        self.initializeAttribute('attorneys', AttorneyList)
        
    def is_represented(self):
        return len(self.attorneys.complete_elements()) > 0

    @property
    def complete(self):
        self.name.first
        self.attorneys.gather()
        if self.attorneys.there_are_any == False:
          self.address.address
          self.phone_number
          self.email
        return True

class PartyList(DAList):
    def init(self, *pargs, **kwargs):
        if 'object_type' not in kwargs:
            kwargs['object_type'] = Party
        kwargs['complete_attribute'] = 'complete'
        super().init(*pargs, **kwargs)

class Case(DAObject):
    def attorneys_in(self, exclude=None):
        attorneys = set()
        if exclude is None:
            to_exclude = []
        else:
            to_exclude = exclude.complete_elements()   
        for party in self.parties.complete_elements():
            for attorney in party.attorneys.complete_elements():
                if attorney not in to_exclude:
                    attorneys.add(attorney)
        return list(sorted(attorneys, key=lambda y: y.name.last))