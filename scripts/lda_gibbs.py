# coding=utf-8
from main import XmlParser
from LdaGibbsSampler import LDAGibbsSampler

N_TOPICS = 10


def gen_documents(corpus_docs):
    corpus_docs = dict([(int(x), y) for x, y in corpus_docs.iteritems()])
    return corpus_docs


def predict_doc(question):
    question = question.decode('utf-8')
    xml = XmlParser()
    lda = LDAGibbsSampler()
    lda.load("../data/gibs_model.npz")
    tokenized_list = xml.filter_article(question)
    doc_topic_words = lda.predict(tokenized_list)
    return doc_topic_words

if __name__ == '__main__':
    print "Predicting new document"
    new_doc = 'Termin chemia organiczna oznaczał pierwotnie dział chemii zajmujący się systematyką oraz ' \
              'badaniem własności związków organicznych, które, jak wierzono, nie mogą być otrzymane na drodze' \
              ' syntezy laboratoryjnej, a jedynie przez żywe organizmy.Później okazało się jednak, że niemal ' \
              'wszystkie związki chemiczne produkowane przez organizmy żywe da się też sztucznie zsyntezować. ' \
              'Udało się następnie otrzymać wiele związków, które w naturze nie występują, ale których własności ' \
              'są zbliżone do tych produkowanych przez organizmy żywe. Ponadto samo życie zależy w znacznym stopniu' \
              ' od związków nieorganicznych. Bardzo wiele enzymów i innych białek takich jak hemoglobina wymaga do' \
              ' swojej aktywności obecności metali przejściowych.Obecnie nauką, która zajmuje się badaniem ' \
              'związków chemicznych występujących w żywych organizmach oraz ich przemianami jest biochemia, ' \
              'która jest powiązana zarówno z chemią organiczną jak i wieloma dyscyplinami biologii.Z drugiej ' \
              'strony okazało się, że wszystkie związki organiczne zawierają węgiel czterowartościowy (pomijając' \
              ' dwutlenek węgla i cyjanki, będące zw. nieorganicznymi), stąd obecnie definicja chemii organicznej ' \
              'to chemia wszystkich tych związków węgla, którymi nie zajmowała się wcześniej tradycyjna chemia' \
              ' nieorganiczna. Z powodu ogromnej liczby możliwych do otrzymania związków zawierających złożony ' \
              'szkielet węglowy mogą one posiadać bardzo różnorodne właściwości oraz zastosowania. Przykładowo' \
              ' praktycznie wszystkie stosowane obecnie barwniki, tworzywa sztuczne oraz leki to związki organiczne.'

    local_all_topics, words = predict_doc(new_doc)
    print "Topic words"
    for key, value in enumerate(words):
        print "{}: {}\n".format(key, value)

    print "Document keywords"
    for value in local_all_topics:
        print value