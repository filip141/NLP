import os
import json
import gensim
import itertools

dir_name = os.path.dirname(os.path.realpath(__file__))


def get_ids_list(json_file):
    for key in json_file.iterkeys():
        yield key


def get_words(json_file, key):
    json_values = json_file.get(key)
    if json_values:
        for value in json_values:
            yield value
    else:
        raise ValueError("Wrong value in json dictionary!")


def json_list(json_fp_list):
    for json_file in json_fp_list:
        json_loaded = json.load(json_file)
        json_file.close()
        yield json_loaded


def load_json_words(files_directory):
    # Loads words from json
    art_file_name = 'articles'
    map_file_name = 'mapping'
    art_files_list = []
    files_in_dir = os.listdir(files_directory)
    dir_witho_scripts = os.path.split(dir_name)[0]

    # Article file list
    for jfile in files_in_dir:
        if art_file_name in jfile:
            art_files_list.append(jfile)

    # load jsons
    json_fp_list = []
    for art_file in art_files_list:
        full_art_path = os.path.join(dir_witho_scripts, 'data', art_file)
        fp = open(full_art_path, "r")
        json_fp_list.append(fp)

    json_list_gen = json_list(json_fp_list)
    words_dict = {}
    for json_loaded in json_list_gen:
        for art_id in get_ids_list(json_loaded):
            words_gen = get_words(json_loaded, art_id)
            words_dict[art_id] = words_gen

    full_map_path = os.path.join(dir_witho_scripts, 'data', map_file_name + ".json")
    with open(full_map_path, "r") as json_title:
        titles = json.load(json_title)
    return words_dict, titles


if __name__ == '__main__':
    art_words, mapp_titles = load_json_words("../data/")
    concat_art = [(key, itertools.tee(doc)) for key, doc in art_words.iteritems()]
    art_words = dict([(con_art[0], con_art[1][0]) for con_art in concat_art])
    art_copy = dict([(con_art[0], con_art[1][1]) for con_art in concat_art])
    dictionary = gensim.corpora.Dictionary(art_words.values())
    corpus = [dictionary.doc2bow(art_copy['8'])]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=4, id2word=dictionary, passes=20)
    print ldamodel.print_topics(num_topics=3, num_words=3)