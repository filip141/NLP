# coding=utf-8
import os
import gensim
import numpy as np
from main import XmlParser
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


def get_topics_doc(question, data_path):
    xml = XmlParser()
    load_dict_path = os.path.join(data_path, "dictionary.dict")
    load_model_path = os.path.join(data_path, "model.lda")
    tokenized_list = xml.filter_article(question)
    dictionary = gensim.corpora.Dictionary.load(load_dict_path)
    lda = gensim.models.ldamodel.LdaModel.load(load_model_path)
    ques_vec = dictionary.doc2bow(tokenized_list)
    topic_vec = np.array(lda[ques_vec])

    idx = np.argsort(-topic_vec[:, 1])
    word_count_array = topic_vec[idx]
    final = []
    for topic in word_count_array:
        final.append(lda.print_topic(topic[0], 1))
    return final

if __name__ == '__main__':
    new_doc = 'Western narodził się II połowie XIX wieku, jako rodzaj literatury przygodowej nawiązującej ' \
              'do twórczość Jamesa Coopera. Akcja tych utworów toczyła się na Dzikim Zachodzie. ' \
              'Pierwsze westerny, były przeważnie tanimi powieściami rozrywkowymi przeznaczonymi ' \
              'dla masowego czytelnika i rzadko odznaczały się większymi walorami literackimi. Tematem' \
              ' były przygody traperów, banitów, rewolwerowców, kowbojów, stróżów prawa, którzy zamieszkiwali' \
              ' te niespokojne regiony. Charakterystyczne było to, że wiele z tych powieści opisywały ' \
              'fikcyjne perypetie autentycznych ludzi, żyjących w tych czasach, takich jak Buffalo Bill,' \
              ' Jesse James, Wyatt Earp, czy Calamity Jane. Popularność wśród czytelników sprawiła, że ' \
              'western stał się w literaturze amerykańskiej odrebnym gatunkiem literackim. Gatunek ten ' \
              'uprawiać zaczęli twórcy spoza Ameryki.'
    # lda, t_words, corp = train_gensim("../data/")
    print get_topics_doc(new_doc, "../data/")
    # print "Model trained"

