import twitter, re
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
api = twitter.Api(consumer_key='KF4pQ48FM5TkdLs6j1zrsDvES',
                  consumer_secret='iJ3uNswOYnU5E6jIdEywCBRNRylpVtnA7lnniK4MYJRJnbCUUr',
                  access_token_key='2356120214-zfgyIzY61qRQmP01LyMFbo60yqUijJIToGUreRN',
                  access_token_secret='hVi69tP76dRyUTCPenD1pCdGO0F74CIJFOC6gmGqW6xiW',
                  tweet_mode = 'extended')

tweet_list = list()
analyzed_user = input("Who should we analyze today?\n")
bumbum = api.GetUserTimeline(screen_name=analyzed_user, count=200, include_rts=False)
while True:
    tweet_list.extend([i.full_text for i in bumbum])
    if len(bumbum) == 0:
        break
    bumbum = api.GetUserTimeline(screen_name=analyzed_user, count=200, max_id=bumbum[-1].id-1, include_rts=False)

re_list = [re.compile('(https.+? )|(?!\w)[\W_\d]+?(?!\w)'), re.compile('[,()/\n—]| \''), re.compile('  +')]
tweet_string = ' '.join(tweet_list)

analyzed = tweet_string
for i in re_list:
    analyzed = i.sub(' ', analyzed)

word_list = analyzed.split(' ')
word_count = input("How many words should the histogram show?\n")
counts = Counter(word_list).most_common(int(word_count))

max_freq = counts[0][1]
for word, freq in sorted(counts, key=lambda p: (-p[1], p[0])):
    number_of_asterisks = (50 * freq ) // max_freq     # (50 * N) / M
    asterisks = '*' * number_of_asterisks        # the (50*N)/M asterisks
    print('{:<15} {}'.format(word, asterisks))

labels, values = zip(*dict(counts).items())
indSort = np.argsort(values)[::-1]

labels = np.array(labels)[indSort]
values = np.array(values)[indSort]

indices = np.arange(len(labels))

bar_width = 0.05

plt.bar(indices, values)

plt.xticks(indices + bar_width, labels)
plt.show()
