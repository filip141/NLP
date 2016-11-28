import json
import numpy as np

N_TOPICS = 10


def gen_documents():
    with open('../data/documents.json', 'r') as json_file:
        corpus_docs = json.load(json_file)
    corpus_docs = dict([(int(x), y) for x, y in corpus_docs.items()])
    return corpus_docs


class LDAGibbsSampler(object):

    def __init__(self, n_topics, docs, alpha=0.1, beta=0.1):
        # Initialize matrixes by none
        self.ndz = None
        self.nzw = None
        self.nz = None
        self.nd = None

        # Define smoothing parameters
        self.alpha = alpha
        self.beta = beta

        self.n_words = 0
        self.idx2words = []
        self.topics_per_doc = {}
        self.n_topic = n_topics
        self.docs = docs
        self.words2idx()
        self.initialize_matrixes()

    def words2idx(self):
        word_list = []
        for doc in self.docs.values():
            word_list += doc
        word_set = set(word_list)

        # Define mapping
        words2idx = dict([(y, x) for x, y in enumerate(word_set)])
        self.idx2words = dict([(x, y) for x, y in enumerate(word_set)])
        self.n_words = len(self.idx2words)

        # change words to idx
        for doc_id, doc in self.docs.items():
            new_word_list = []
            for word in doc:
                new_word_list.append(words2idx[word])
                self.docs[doc_id] = new_word_list

    def initialize_matrixes(self):
        n_docs = len(docs)
        # Initialize topic per document list
        for doc in xrange(1, n_docs + 1):
            words_in_doc = len(self.docs[doc])
            topic_zeros_list = [0 for _ in range(0, words_in_doc)]
            self.topics_per_doc[doc] = topic_zeros_list

        # Define matrixes
        self.ndz = np.zeros((n_docs, self.n_topic))
        self.nzw = np.zeros((self.n_topic, self.n_words))
        self.nz = np.zeros((self.n_topic,))
        self.nd = np.zeros((n_docs,))

        # Random initialization
        for doc_id, doc in self.docs.items():
            for word_idx, word in enumerate(doc):
                z = np.random.randint(self.n_topic)

                self.topics_per_doc[doc_id][word_idx] = z
                self.ndz[doc_id - 1][z] += 1
                self.nzw[z][word] += 1
                self.nz[z] += 1
                self.nd[doc_id - 1] += 1

    # Compute probability P(z_i | z_-i, w)
    def conditional(self, doc_id, word):
        vocab_size = self.nzw.shape[1]
        per_words = (self.nzw[:, word] + self.beta) / \
                    (self.nz + self.beta * vocab_size)
        per_topics = (self.ndz[doc_id - 1, :] + self.alpha) / \
                     (self.nd[doc_id - 1] + self.alpha * self.n_topic)
        cond_proba = per_topics * per_words
        cond_proba /= sum(cond_proba)
        return cond_proba

    # Learn LDA from corpus
    def learn(self, num_iteration=50):
        for _ in xrange(num_iteration):
            for doc_id, doc in self.docs.items():
                for word_idx, word in enumerate(doc):
                    z = self.topics_per_doc[doc_id][word_idx]
                    # Decrement values
                    self.ndz[doc_id - 1][z] -= 1
                    self.nzw[z][word] -= 1
                    self.nz[z] -= 1
                    self.nd[doc_id - 1] -= 1

                    # Conditional probability
                    cond_proba = self.conditional(doc_id, word)
                    z = np.random.multinomial(1, cond_proba).argmax()
                    # Increment again
                    self.topics_per_doc[doc_id][word_idx] = z
                    self.ndz[doc_id - 1][z] += 1
                    self.nzw[z][word] += 1
                    self.nz[z] += 1
                    self.nd[doc_id - 1] += 1

    def measure_learning_phase(self):
        log_likelihood = 0.0
        # Random initialization
        for doc_id, doc in self.docs.items():
            for word_idx, word in enumerate(doc):
                joint_proba = (self.nzw[:, word] / self.nz) * (self.ndz[doc_id - 1, :] / self.nd[doc_id - 1])
                log_likelihood += np.log(joint_proba.sum())
        return log_likelihood

    def get_topic_words(self):
        words = {}
        for doc_id, doc in self.docs.items():
            topics_doc = self.topics_per_doc[doc_id]
            bag_of_words = self.docs[doc_id]
            for w_idx, topic_idx in enumerate(topics_doc):
                word_list = words.get(topic_idx)
                if word_list:
                    word_list.append(self.idx2words[bag_of_words[w_idx]])
                    words[topic_idx] = word_list
                else:
                    words[topic_idx] = [self.idx2words[bag_of_words[w_idx]]]
        return words


if __name__ == '__main__':
    docs = gen_documents()
    lda = LDAGibbsSampler(N_TOPICS, docs)
    lda.learn(num_iteration=100)
    doc_topic_words = lda.get_topic_words()
    print "aa"