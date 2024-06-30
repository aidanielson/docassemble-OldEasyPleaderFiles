from docassemble.base.util import Individual, DAList, DAObject

__all__ = ['Attorney', 'AttorneyList', 'Party', 'PartyList', 'Case']


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