import autocomplete
import util

def test_trie():
  # some basic functions
  tt = autocomplete.Trie()
  tt.add("Hello world")
  assert len(tt) == 1
  assert "Hello world" in tt
  tt.add("Hello World")
  assert len(tt) == 2
  assert "Hello World" in tt
  assert "Hello world" in tt
  assert "hello world - i'm not supposed to be in the trie" not in tt
  tt.add("Hello World")
  assert len(tt) == 2
  assert "Hello World" in tt
  assert "Hello world" in tt
  assert "hello world" not in tt
  assert "" not in tt
  assert "H" not in tt
  assert "" not in tt
  tt.clear()
  assert len(tt) == 0

  # set equivalence and memory constraints
  data = util.read_input("data/sample_conversations.json")
  all_convos_set = set()
  for line, _ in util.get_customer_service_phrases(data).items():
    all_convos_set.add(line)
    tt.add(line)

  for line in all_convos_set:
    assert line in tt

if __name__ == "__main__":
  test_trie()
  print("trie tests passed!")
  # print(AutocompleteModel("data/sample_conversations.json"))