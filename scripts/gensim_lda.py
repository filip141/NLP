import gensim
from dataloader import load_json_words

if __name__ == '__main__':
    art_words, mapp_titles = load_json_words("../data/", tolist=True)
    dictionary = gensim.corpora.Dictionary(art_words.values())
    corpus = [dictionary.doc2bow(art_words['5630'])]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word=dictionary, passes=20)
    print ldamodel.print_topics(num_topics=2, num_words=2)