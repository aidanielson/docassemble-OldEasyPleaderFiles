from docassemble.base.util import DAList, Individual, DAObject

class MyParty(Individual):
  pass

class MyCase(DAObject):
  def init(self, *pargs, **kwargs):
    super().init(*pargs, **kwargs)
    self.initializeAttribute('parties', DAList.using(object_type=MyParty))

  def unique_states(self):
    states = set()
    for party in self.parties:
      states.add(party.address.state)
    return list(states)
  
  def add_person_to_parties(self):
    all_parties = set()
    xxxxxxxxxxx
    