import numpy as np


class LDAGibbsSampler(object):

    def __init__(self, alpha=0.1, beta=0.1):
        # Initialize matrixes by none
        self.ndz = None
        self.nzw = None
        self.nz = None
        self.nd = None

        # Define smoothing parameters
        self.alpha = alpha
        self.beta = beta

        # Assign base
        self.n_topic = 0
        self.docs = None
        self.n_words = 0
        self.min_key = 0
        self.w2idx = {}
        self.idx2words = {}
        self.topics_per_doc = {}

    def words2idx(self, docs, append=True):
        # If mapping not defined
        if not self.idx2words:
            word_list = []
            for doc in docs.values():
                word_list += doc
            word_set = set(word_list)

            # Define mapping
            self.w2idx = dict([(y, x) for x, y in enumerate(word_set)])
            self.idx2words = dict([(x, y) for x, y in enumerate(word_set)])

        self.n_words = len(self.idx2words)
        # change words to idx
        for doc_id, doc in docs.iteritems():
            print "Doc Converted to indexes: {}".format(doc_id)
            new_word_list = []
            for word in doc:
                if append:
                    if word in self.w2idx.keys():
                        translated_item = self.w2idx[word]
                    else:
                        self.w2idx[word] = self.n_words
                        self.idx2words[self.n_words] = word
                        translated_item = self.n_words
                        self.n_words += 1
                else:
                    translated_item = self.w2idx[word]
                new_word_list.append(translated_item)
                docs[doc_id] = new_word_list
        return docs

    def initialize_matrixes(self, docs):
        n_docs = len(docs)
        # Initialize topic per document list
        for doc in docs.keys():
            words_in_doc = len(list(docs[doc]))
            topic_zeros_list = [0 for _ in range(0, words_in_doc)]
            self.topics_per_doc[doc] = topic_zeros_list

        # Define matrixes
        self.ndz = np.zeros((n_docs, self.n_topic))
        self.nd = np.zeros((n_docs,))
        if self.nzw is None:
            self.nzw = np.zeros((self.n_topic, self.n_words))
            self.nz = np.zeros((self.n_topic,))
        else:
            old_cols = self.nzw.shape[1]
            tmp_nzw = np.zeros((self.n_topic, self.n_words))
            tmp_nzw[:, :(old_cols - self.n_words)] = self.nzw
            self.nzw = tmp_nzw

        # Random initialization
        for doc_id, doc in docs.items():
            for word_idx, word in enumerate(doc):
                z = np.random.randint(self.n_topic)

                self.topics_per_doc[doc_id][word_idx] = z
                self.ndz[doc_id - self.min_key][z] += 1
                self.nzw[z][word] += 1
                self.nz[z] += 1
                self.nd[doc_id - self.min_key] += 1

    # Compute probability P(z_i | z_-i, w)
    def conditional(self, doc_id, word):
        vocab_size = self.nzw.shape[1]
        per_words = (self.nzw[:, word] + self.beta) / \
                    (self.nz + self.beta * vocab_size)
        per_topics = (self.ndz[doc_id - self.min_key, :] + self.alpha) / \
                     (self.nd[doc_id - self.min_key] + self.alpha * self.n_topic)
        cond_proba = per_topics * per_words
        cond_proba /= sum(cond_proba)
        return cond_proba

    def gibbs_sampling(self, docs, num_iteration):
        for iter_num in xrange(num_iteration):
            for doc_id, doc in docs.items():
                for word_idx, word in enumerate(doc):
                    z = self.topics_per_doc[doc_id][word_idx]
                    # Decrement values
                    self.ndz[doc_id - self.min_key][z] -= 1
                    self.nzw[z][word] -= 1
                    self.nz[z] -= 1
                    self.nd[doc_id - self.min_key] -= 1

                    # Conditional probability
                    cond_proba = self.conditional(doc_id, word)
                    z = np.random.multinomial(1, cond_proba).argmax()
                    # Increment again
                    self.topics_per_doc[doc_id][word_idx] = z
                    self.ndz[doc_id - self.min_key][z] += 1
                    self.nzw[z][word] += 1
                    self.nz[z] += 1
                    self.nd[doc_id - self.min_key] += 1
            print "Learning status, percent: {}".format(100 * (iter_num / float(num_iteration)))
            print "Log likelihood: {}".format(self.measure_learning_phase(docs))

    # Learn LDA from corpus
    def train(self, docs, num_iteration=50, n_topics=10):
        self.n_topic = n_topics
        self.docs = self.words2idx(docs, append=False)
        # Assign database
        self.min_key = min(self.docs.keys())
        print "Initializing matrices"
        self.initialize_matrixes(self.docs)
        print "Starting Gibbs Sampler"
        self.gibbs_sampling(self.docs, num_iteration)

    def save(self, path):
        np.savez(path, nzw=self.nzw, nz=self.nz, w2idx=self.w2idx.items(),
                 idx2words=self.idx2words.items(), n_topic=self.n_topic,
                 alpha=self.alpha, beta=self.beta)

    def load(self, path):
        with np.load(path) as X:
            self.nzw = X["nzw"]
            self.nz = X["nz"]
            # Convert dicts
            w2idx = {}
            tmp_w2idx = dict(X["w2idx"])
            for key, value in tmp_w2idx.iteritems():
                w2idx[key] = int(value)
            idx2words = {}
            tmp_idx2words = dict(X["idx2words"])
            for key, value in tmp_idx2words.iteritems():
                idx2words[int(key)] = value
            self.w2idx = w2idx
            self.idx2words = idx2words
            self.n_topic = X["n_topic"]
            self.alpha = X["alpha"]
            self.beta = X["beta"]

    # Predict
    def predict(self, document, num_iteration=50, s_words=50, s_topics=3):
        words = []
        doc_dict = {1: document}
        self.min_key = 1
        self.words2idx(doc_dict, append=True)
        self.initialize_matrixes(doc_dict)
        self.gibbs_sampling(doc_dict, num_iteration)
        idx = np.argsort(-self.ndz[0])
        topics = self.nzw[idx]
        sorted_args = (-topics).argsort()
        for topic_idx in xrange(self.n_topic):
            word_list = []
            for t_word in sorted_args[topic_idx]:
                word_list.append(self.idx2words[t_word])
            words.append(word_list[0: min(s_words, len(word_list))])
        # Convert to local context
        print ""
        main_topics = words[:s_topics]
        local_all_topics = []
        for topic in main_topics:
            local_topic = []
            for word in topic:
                if word in document:
                    local_topic.append(word)
            local_all_topics.append(local_topic)
        return local_all_topics, words

    # Measure Learning phase
    def measure_learning_phase(self, docs):
        log_likelihood = 0.0
        # Calculate learning status
        for doc_id, doc in docs.items():
            for word_idx, word in enumerate(doc):
                joint_proba = (self.nzw[:, word] / self.nz) * \
                              (self.ndz[doc_id - self.min_key, :] / self.nd[doc_id - self.min_key])
                log_likelihood += np.log(joint_proba.sum())
        return log_likelihood

    # Get ten words
    def get_topic_words(self, s_words=10):
        words = {}
        sorted_args = (-self.nzw).argsort()
        for topic_idx in xrange(self.n_topic):
            word_list = []
            for t_word in sorted_args[topic_idx]:
                word_list.append(self.idx2words[t_word])
            words[topic_idx] = word_list[0: min(s_words, len(word_list))]
        return words


if __name__ == '__main__':
    pass
