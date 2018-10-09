import util


class TrieNode:
    def __init__(self, phrase):
        assert len(phrase) > 0
        self.my_char = phrase[0]
        self.my_children = {}
        self.stems = {}
        self.sorted_stems = []
        self.length = 0
        self.end = False
        self.add(phrase)

    def _preprocess_phrase_counts(self, phrase_long):
        phrase = phrase_long
        if phrase in self.stems:
            self.stems[phrase] += 1
        else:
            self.stems[phrase] = 1
        self.sorted_stems = [(k, self.stems[k]) for k in sorted(
            self.stems, key=self.stems.__getitem__, reverse=True)]
        if len(phrase) > 1:
            self.my_children[phrase[1]]._preprocess_phrase_counts(phrase[1:])

    def add(self, phrase, update_phrase_counts=True):
        if len(phrase) == 0:
            return False

        assert phrase[0] == self.my_char

        rval = True

        if self.__contains__(phrase, check_end=True):
            rval = False

        self.length += 1
        if len(phrase) == 1:
            self.end = True
        elif phrase[1] not in self.my_children:
            self.my_children[phrase[1]] = TrieNode(phrase[1:])
        else:
            self.my_children[phrase[1]].add(
                phrase[1:], update_phrase_counts=False)
        if update_phrase_counts:
            self._preprocess_phrase_counts(phrase)
        return rval

    def get_top_k_subphrases(self, k):
        return self.sorted_stems[:min(k, len(self.sorted_stems))]

    def __contains__(self, phrase, check_end=True):
        if len(phrase) == 0:
            return False
        if len(phrase) == 1:
            return phrase[0] == self.my_char and (not check_end or self.end)
        if phrase[1] not in self.my_children:
            return False
        return self.my_children[phrase[1]].__contains__(phrase[1:], check_end)

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

    def get_top_k_subphrases(self, phrase, k=10):
        if not self.__contains__(phrase, check_end=False):
            return []
        current_node = self.my_children[phrase[0]]
        for i in range(1, len(phrase)):
            current_node = current_node.my_children[phrase[i]]
        return current_node.get_top_k_subphrases(k)

    def __contains__(self, phrase, check_end=True):
        if len(phrase) == 0:
            return False
        if phrase[0] not in self.my_children:
            return False
        return self.my_children[phrase[0]].__contains__(phrase, check_end)

    def __len__(self):
        return self.length

    def clear(self):
        self.my_children = {}
        self.length = 0


class Autocomplete:
    def __init__(self, filename_data="data/sample_conversations.json", filename_pkl="autocomplete_state.pkl", load=False):
        if load:
            self.load_from_file(filename_pkl)
            return
        self.tt = Trie()
        data = util.read_input(filename_data)
        all_convos_set = set()
        for line, count in util.get_customer_service_phrases(data).items():
            for i in range(count):
                all_convos_set.add(line)
                self.tt.add(line)
        util.save_object(self.tt, filename_pkl)

    def load_from_file(self, filename):
        self.tt = util.load_object(filename)
        assert isinstance(self.tt, Trie)

    def generate_completions(self, phrase):
        results_from_trie = self.tt.get_top_k_subphrases(phrase)
        results = [phrase + r[0][1:] for r in results_from_trie]
        return results