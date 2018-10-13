import autocomplete
import util
import sys
sys.setrecursionlimit(2000)


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
    assert "Hello World aaaaaaaaaaaaaa" not in tt
    tt.add("Hello World")
    assert len(tt) == 2
    assert "Hello World" in tt
    assert "Hello world" in tt
    assert "hello world" not in tt
    assert "" not in tt
    assert "H" not in tt
    assert "" not in tt
    assert tt.__contains__("Hello", check_end=False)
    tt.clear()
    assert len(tt) == 0
    print("basic tests cleared")

    # set equivalence and memory constraints
    data = util.read_input("data/sample_conversations.json")
    all_convos_set = set()
    for line, count in util.get_customer_service_phrases(data).items():
        for i in range(count):
            # test duplication
            all_convos_set.add(line)
            tt.add(line)

    for line in all_convos_set:
        assert line in tt

    assert len(tt) == len(all_convos_set)
    print("I have %d phrases saved now" % len(tt))
    print("large tests cleared")
    util.save_object(tt, "test_autocomplete_state.pkl")


def test_autocomplete():
    ac = autocomplete.Autocomplete()

    # let's just test that the phrases we get as output actually exist in the trie
    results = ac.generate_completions("When w")
    assert len(results) > 0
    for r in results:
        stupid_results = ac.generate_completions(r)
        assert r in stupid_results

    degenerate_results = ac.generate_completions("")
    assert len(degenerate_results) == 0

    degenerate_results = ac.generate_completions(
        "asdkljf;alsdkjfa;lsdkjfdl;akjfakl;j")
    assert len(degenerate_results) == 0


if __name__ == "__main__":
    test_trie()
    test_autocomplete()
    print("trie tests passed!")