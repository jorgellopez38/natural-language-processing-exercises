import unicodedata
import re
import json
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
import pandas as pd


################################################ Prepare Basic Clean Function ################################################


def basic_clean(string):
    '''
    This function takes in a string and lowers the case, normalizes unicode characters, 
    and uses regex to replace anything that is not a letter, number, whitespace or a single quote.
    '''
    # lower it
    string = string.lower()
    # normalize it
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8')
    # regex it 
    string = re.sub(r'[^a-z0-9\s]', '', string)
    
    return string


################################################ Prepare Tokenize Function ################################################


def tokenize(string):
    '''
    This function takes in a string and tokenizes all the words in the string.
    '''
    # create object
    tokenize = nltk.tokenize.ToktokTokenizer()
    # spit out tokenize
    string = tokenize.tokenize(string)
    
    return string


############################################### Prepare Stem Function ################################################


def stem(string):
    '''
    This function takes in a string and
    returns a string with words stemmed.
    '''
    # create our stemming object
    ps = nltk.porter.PorterStemmer()
    # use a list comprehension => stem each word for each word inside of the entire document,
    # split by the default, which are single spaces
    stems = [ps.stem(word) for word in string.split()]
    # glue it back together with spaces, as it was before
    string = ' '.join(stems)
    
    return string


############################################### Prepare Lemmatize Function ################################################


def lemmatize(string):
    '''
    This function takes in string for and
    returns a string with words lemmatized.
    '''
    # create our lemmatizer object
    wnl = nltk.stem.WordNetLemmatizer()
    # use a list comprehension to lemmatize each word
    # string.split() => output a list of every token inside of the document
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    # glue the lemmas back together by the strings we split on
    string = ' '.join(lemmas)
    #return the altered document
    return string


############################################### Prepare Remove Stopwords Function ################################################


def remove_stopwords(string, extra_words = [], exclude_words = []):
    '''
    This function takes in a string, optional extra_words and exclude_words parameters
    with default empty lists and returns a string.
    '''
    # assign our stopwords from nltk into stopword_list
    stopword_list = stopwords.words('english')
    # utilizing set casting, i will remove any excluded stopwords
    stopword_list = set(stopword_list) - set(exclude_words)
    # add in any extra words to my stopwords set using a union
    stopword_list = stopword_list.union(set(extra_words))
    # split our document by spaces
    words = string.split()
    # every word in our document, as long as that word is not in our stopwords
    filtered_words = [word for word in words if word not in stopword_list]
    # glue it back together with spaces, as it was so it shall be
    string_without_stopwords = ' '.join(filtered_words)
    # return the document back
    return string_without_stopwords


############################################### Prepare Article Function ################################################


def prep_article_data(df, column, extra_words=[], exclude_words=[]):
    '''
    This function take in a df and the string name for a text column with 
    option to pass lists for extra_words and exclude_words and
    returns a df with the text article title, original text, stemmed text,
    lemmatized text, cleaned, tokenized, & lemmatized text with stopwords removed.
    '''
    #original text from content column
    df['original'] = df['content']
    
    #chain together clean, tokenize, remove stopwords
    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    #chain clean, tokenize, stem, remove stopwords
    df['stemmed'] = df['clean'].apply(stem)
    
    #clean clean, tokenize, lemmatize, remove stopwords
    df['lemmatized'] = df['clean'].apply(lemmatize)
    
    return df[['title', 'original', 'clean', 'stemmed', 'lemmatized']]