#!/usr/bin/python3
import re
from collections import Counter

from api_key import api
from markov_chain import MarkovChain


def get_all_tweets(analyzed_user):
    """Gather all tweets from a user's timeline subject to API limitations

    #Arguments
        analyzed_user: twitter handle

    #Returns
        A list of unfiltered tweets from the user
    """
    tweet_list = list()
    timeline = api.GetUserTimeline(
        screen_name=analyzed_user, count=200, include_rts=False)
    while True:
        tweet_list.extend([i.full_text for i in timeline])
        if len(timeline) == 0:
            break
        timeline = api.GetUserTimeline(
            screen_name=analyzed_user,
            count=200,
            max_id=timeline[-1].id - 1,
            include_rts=False)
    return tweet_list


def tweets_to_list(tweet_list):
    """Convert a list of sentences to a list of word tokens"""

    tweet_string = ' <eof> '.join(tweet_list).replace("&amp", "&").lower()
    tweet_string = re.sub(r'https:.* ', '', tweet_string)

    # Remove unwanted characters from the string
    filters = '!"#$%&()*+,-./:;=?[\\]^_`{|}~\t\n”“'
    translate_dict = {c: " " for c in filters}
    tweet_string = tweet_string.translate(str.maketrans(translate_dict))

    seq = tweet_string.split(" ")
    return [i for i in seq if i]


def draw_frequency_graph(word_list, word_count=20):
    """Draw a graph representing relative frequency of words in the list
    #Arguments
        word_list: list of tokens
        word_count: number of words to represent, starting from the most common
    """
    counts = Counter(word_list).most_common(int(word_count))

    # Don't show count for eof marker
    if (counts[0][0]) == "<eof>":
        del counts[0]
    max_freq = counts[0][1]
    for word, freq in sorted(counts, key=lambda p: (-p[1], p[0])):
        number_of_asterisks = (50 * freq) // max_freq  # (50 * N) / M
        asterisks = '*' * number_of_asterisks  # the (50*N)/M asterisks
        print('{:<15} {}'.format(word, asterisks))


def main():
    user = input("User handle to analyze?\n")
    word_list = tweets_to_list(get_all_tweets(user))
    sentences = 0
    chain = MarkovChain(word_list)
    while True:
        try:
            sentences = int(input("How many sentences to generate?\n"))
            break
        except ValueError:
            print("Please input a number\n")
    for _ in range(sentences):
        chain.generate_sentence()


if __name__ == "__main__":
    main()
