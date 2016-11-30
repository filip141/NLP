import os
import json
import scipy
import textrank
import dataloader
from summa import keywords

if __name__ == "__main__":
    art_words, mapp_titles = dataloader.load_json_words("../data/", tolist=True)
    keywords = keywords.keywords(' '.join(art_words['1152']))
    print "a"