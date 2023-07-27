import pickle
from sklearn.pipeline import Pipeline
import re
import os
from nltk.corpus import stopwords
from string import punctuation

from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, NewsNERTagger, PER, NamesExtractor, Doc
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
names_extractor = NamesExtractor(morph_vocab)

russian_stopwords = stopwords.words("russian")

def text_preprocessor(text):
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    lemmas = []
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
        if token.pos != 'PUNCT':
            lemmas.append(token.lemma)
    tokens = [token for token in lemmas if token not in russian_stopwords\
      and token != " " \
      and token.strip() not in punctuation]   

    text = " ".join(tokens)
    text = re.sub('\d+', '', text)
    text =  re.sub('\\t|\\n|\+', '', text)
    text =  re.sub('[^ЁёА-я\s]', '', text)
    text =  re.sub('\s+', ' ', text)    
    return text

with open(f'./models/naive_bayes/MultinominalNB + NATASHA + BOW + full texts.bin', 'rb') as input_stream:
    topic_pipeline = pickle.load(input_stream)

with open(f'./models/naive_bayes/MultinominalNB(grade) + NATASHA+ N-GRAMS + BOW + paragraphs.bin', 'rb') as input_stream_2:
    grade_pipeline = pickle.load(input_stream_2)

def classify_topic(text):
    return topic_pipeline.predict([(text_preprocessor(text))])

def classify_grade(text):
    return grade_pipeline.predict([(text_preprocessor(text))])
