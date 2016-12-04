# coding=utf-8
import os
import gensim
from dataloader import load_json_words


def train_gensim(path, num_topics=70, passes=50, num_words=10):
    save_dict_path = os.path.join(path, "dictionary.dict")
    save_model_path = os.path.join(path, "model.lda")
    art_words, mapp_titles = load_json_words(path, tolist=True)
    dictionary = gensim.corpora.Dictionary(art_words.values())
    dictionary.save(save_dict_path)
    corpus = [dictionary.doc2bow(text) for text in art_words.values()]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=passes)
    ldamodel.save(save_model_path)
    topic_words = ldamodel.print_topics(num_topics=num_topics, num_words=num_words)
    return ldamodel, topic_words, corpus

if __name__ == '__main__':
    lda, t_words, corp = train_gensim("../data/")
    print "Model trained"

