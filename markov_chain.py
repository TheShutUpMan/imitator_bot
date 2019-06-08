from collections import Counter, defaultdict
from random import choices


class MarkovChain:
    """
    Class for generating a markov chain from a list of words 
    which can then be used to generate sentences
    """

    def __init__(self, word_list):
        """Encode words into a set of states and transitions
        Each transition is represented in a dictionary as a mapping
        from a word to a list of word-probability tuples

        #Arguments
            word_list: list of tokens
        """
        word_pairs = list()
        for i in range(1, len(word_list)):
            word_pairs.append((word_list[i - 1], word_list[i]))
        pair_counter = Counter(word_pairs)
        self.transition_dict = defaultdict(list)
        for pair, count in pair_counter.items():
            self.transition_dict[pair[0]].append([pair[1], count])
        for elem in self.transition_dict.values():
            total_count = sum(i[1] for i in elem)
            for transition in elem:
                transition[1] /= total_count

    def generate_sentence(self, terminator="<eof>"):
        """Generate a sentence using the transition dictionary by choosing
        transitions according to probability until terminator is reached

        #Arguments
            terminator: terminate sentence when this word is reached, begin
            transitions from this word

        #Returns
            A sentence resulting from simulation of the markov chain
        """
        sentence = list()
        word = terminator
        while True:
            next_transition = self.transition_dict[word]
            try:
                word = choices(
                    next_transition,
                    weights=(i[1] for i in next_transition))[0][0]
            except IndexError:
                break
            if word == terminator:
                break
            sentence.append(word)

        return sentence
