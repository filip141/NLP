from dataloader import load_json_words
from LdaGibbsSampler import LDAGibbsSampler

N_TOPICS = 10


def gen_documents(corpus_docs):
    corpus_docs = dict([(int(x), y) for x, y in corpus_docs.iteritems()])
    return corpus_docs

if __name__ == '__main__':
    art_words, mapp_titles = load_json_words("../data/", tolist=True)
    art_words = gen_documents(art_words)
    print "Documents Loaded"
    lda = LDAGibbsSampler()
    lda.train(art_words, n_topics=N_TOPICS, num_iteration=30)
    lda.save("../data/gibs_model.npz")
    doc_topic_words = lda.get_topic_words()
    for key, value in doc_topic_words.items():
        print "{}: {}\n".format(key, value)