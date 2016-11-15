# encoding=utf8
import sys
from nltk.tokenize import word_tokenize
from tqdm import *
import morfeusz
import os
import codecs

reload(sys)
sys.setdefaultencoding('utf8')


class XmlParser:

    @staticmethod
    def get_stopwords(self):
        with open(self.stopwords_path) as f:
            words_list = f.readlines()[0]
            return words_list.split(", ")

    def __init__(self):
        self.stopwords_path = os.path.abspath('..') + '\\resources\\stopwords.txt'
        self.stopwords = self.get_stopwords(self)
        self.special_char = "\'~*+§/\[](){}<>@=°„‚’\”&^|%_#-:;.!?,"
        self.xml_article_path = os.path.abspath('..') + '\\resources\\wiki.xml'
        self.articles_json_path = os.path.abspath('..') + '\\resources\\articles.json'
        self.mapping_json_path = os.path.abspath('..') + '\\resources\\mapping.json'

    @staticmethod
    def list_to_json_list(source_list):
        json_list = '['
        for word in source_list:
            json_list += '\"'
            json_list += word
            json_list += '\",'
        final = json_list[:-1]
        final += ']'
        return final

    @staticmethod
    def extract_title(line):
        title = line.split('title=\"')[1].split('\"')[0]
        return title

    @staticmethod
    def stemming(word):
        sword = morfeusz.analyse(word, expand_tags=False)
        return sword[0][0][1].lower()

    @staticmethod
    def num_there(s):
        return any(i.isdigit() for i in s)

    def filter_article(self, article):
        article_tokens = word_tokenize(article)
        filtered_article = []
        for w in article_tokens:
            if w not in self.stopwords and w not in self.special_char and not self.num_there(w) and not len(w) < 3:
                filtered_article.append(self.stemming(w).replace(':', ''))
        return filtered_article

    def parse_xml(self, path):
        element = {'text': '', 'title': ''}
        with codecs.open(path, "r", encoding='utf-8', errors='ignore') as f:
            no_of_lines = 11779569
            i = 1
            with open(self.articles_json_path, 'w') as articles_json:
                with open(self.mapping_json_path, 'w') as mapping_json:
                    articles_json.write('{')
                    mapping_json.write('{')
                    for line in tqdm(f, desc='Parsing XML File', total=no_of_lines):
                        if 'document' in line or line == '\n' or line == '':
                            pass
                        elif '</doc>' not in line:
                            if '<doc' in line:
                                element['title'] = self.extract_title(line)
                            else:
                                element['text'] += line
                        elif '</doc>' in line:
                            articles_json.write('\"'+str(i)+'\"')
                            articles_json.write(':')
                            articles_json.write(self.list_to_json_list(self.filter_article(element.get('text'))))
                            if not(i == no_of_lines-1):
                                articles_json.write(',')
                            mapping_json.write('\"'+str(i)+'\"')
                            mapping_json.write(':')
                            mapping_json.write(element.get('title'))
                            if not (i == no_of_lines-1):
                                mapping_json.write(',')
                            i += 1
                            element = {'text': '', 'title': ''}
                mapping_json.write('}')
                mapping_json.close()
            articles_json.write('}')
            articles_json.close()
        f.close()

if __name__ == "__main__":
    parser = XmlParser()
    if not(os.path.isfile(parser.articles_json_path) and os.path.isfile(parser.mapping_json_path)):
        parser.parse_xml(parser.xml_article_path)
