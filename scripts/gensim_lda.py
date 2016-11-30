import gensim
from dataloader import load_json_words

if __name__ == '__main__':
    art_words, mapp_titles = load_json_words("../data/", tolist=True)
    dictionary = gensim.corpora.Dictionary(art_words.values())
    corpus = [dictionary.doc2bow(text) for text in art_words.values()[:3]]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=5)
    print ldamodel.print_topics(num_topics=3, num_words=3)
