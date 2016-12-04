import os
import json
from main import XmlParser
from lda_gibbs import predict_doc
from gensim_lda import get_topics_doc
from flask import Flask, render_template, request

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')
app = Flask('app', template_folder=template_dir, static_folder=static_dir)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/purelda', methods=['POST'])
def pure_lda():
    doc = request.json.get("text")
    xml = XmlParser()
    doc_splitted = xml.filter_article(doc, stemming=False)
    result = predict_doc(doc)
    new_res = []
    for id_t, topic in enumerate(result[0]):
        new_topic = []
        for id_w, word in enumerate(topic):
            for s_word in doc_splitted:
                if word == XmlParser.stemming(s_word):
                    new_topic.append(s_word)
        new_res.append(list(set(new_topic)))
    return json.dumps({'status': 'OK', "keywords": new_res, "topic_words": result[1]})


@app.route('/gensimlda', methods=['POST'])
def gensim_lda():
    doc = request.json.get("text")
    xml = XmlParser()
    doc_splitted = xml.filter_article(doc, stemming=False)
    result = get_topics_doc(doc, "../data/")
    new_res = []
    for id_t, topic in enumerate(result[0]):
        new_topic = []
        for id_w, word in enumerate(topic):
            for s_word in doc_splitted:
                if word == XmlParser.stemming(s_word):
                    new_topic.append(s_word)
        new_res.append(list(set(new_topic)))
    return json.dumps({'status': 'OK', "keywords": new_res, "topic_words": result[1]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)