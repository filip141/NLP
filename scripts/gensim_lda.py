# coding=utf-8
import gensim
from main import XmlParser
from dataloader import load_json_words


def get_topics_doc(question):
    xml = XmlParser()
    tokenized_list = xml.filter_article(question)
    dictionary = gensim.corpora.Dictionary.load('questions.dict')

    ques_vec = []
    ques_vec = dictionary.doc2bow(tokenized_list)

    topic_vec = []
    topic_vec = lda[ques_vec]

    # word_count_array = numpy.empty((len(topic_vec), 2), dtype = numpy.object)
    # for i in range(len(topic_vec)):
    #     word_count_array[i, 0] = topic_vec[i][0]
    #     word_count_array[i, 1] = topic_vec[i][1]
    #
    # idx = numpy.argsort(word_count_array[:, 1])
    # idx = idx[::-1]
    # word_count_array = word_count_array[idx]
    #
    # final = []
    # final = lda.print_topic(word_count_array[0, 0], 1)
    #
    # question_topic = final.split('*') ## as format is like "probability * topic"
    #
    # return question_topic[1]
    #

if __name__ == '__main__':
    aa = get_topics_doc("jadę sobię do mojego znajomego pomagać mu w przprowadzce")
    print aa
    # art_words, mapp_titles = load_json_words("../data/", tolist=True)
    # dictionary = gensim.corpora.Dictionary(art_words.values())
    # corpus = [dictionary.doc2bow(text) for text in art_words.values()[:3]]
    # ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=5)
    # print ldamodel.print_topics(num_topics=3, num_words=3)
