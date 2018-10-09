import util

class TrieNode:
  def __init__(self, phrase):
    assert len(phrase) > 0
    self.my_char = phrase[0]
    self.my_children = {}
    self.length = 0
    self.end = False
    self.add(phrase)


  def add(self, phrase):
    if len(phrase) == 0:
      return False
    assert phrase[0] == self.my_char
    if self.__contains__(phrase, check_end=True):
      return False

    self.length += 1
    if len(phrase) == 1:
      self.end = True
      return True
    if phrase[1] not in self.my_children:
      self.my_children[phrase[1]] = TrieNode(phrase[1:])
    else:
      self.my_children[phrase[1]].add(phrase[1:])
    return True


  def __contains__(self, phrase, check_end=True):
    if len(phrase) == 0:
      return False
    if len(phrase) == 1:
      return phrase[0] == self.my_char and (not check_end or self.end)
    if phrase[1] not in self.my_children:
      return False
    return self.my_children[phrase[1]].__contains__(phrase[1:])


  def __len__(self):
    return self.length



class Trie:
  def __init__(self):
    self.my_children = {}
    self.length = 0


  def add(self, phrase):
    if len(phrase) == 0:
      return
    if phrase[0] not in self.my_children:
      self.my_children[phrase[0]] = TrieNode(phrase)
      self.length += 1
    else:
      success = self.my_children[phrase[0]].add(phrase)
      self.length += int(success)


  def __contains__(self, phrase):
    if len(phrase) == 0:
      return False
    if phrase[0] not in self.my_children:
      return False
    return self.my_children[phrase[0]].__contains__(phrase)


  def __len__(self):
    return self.length


  def clear(self):
    self.my_children = {}
    self.length = 0



class AutocompleteModel:
  def __init__(self, filename):
    self.data = util.read_input(filename)
    print(self.data["Issues"][0]["Messages"])

