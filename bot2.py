# Meet Pybot: your friend
import nltk
import warnings
from flask import session
from pymongo import MongoClient


warnings.filterwarnings("ignore")
# nltk.download() # for downloading packages
# import tensorflow as tf
import numpy as np
import random
import string  # to process standard python strings

client = MongoClient('mongodb+srv://infobee:InfoBee123@diseaseprediction.e1ihw.mongodb.net/myFirstDatabase'
                     '?retryWrites=true&w=majority')



f = open('symptom.txt', 'r', errors='ignore')
m = open('pincodes.txt', 'r', errors='ignore')
checkpoint = "./chatbot_weights.ckpt"
# session = tf.InteractiveSession()
# session.run(tf.global_variables_initializer())
# saver = tf.train.Saver()
# saver.restore(session, checkpoint)

raw = f.read()
rawone = m.read()
nltk.download('punkt')  # first-time use only
nltk.download('wordnet')  # first-time use only
sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of words
sent_tokensone = nltk.sent_tokenize(rawone)  # converts to list of sentences
word_tokensone = nltk.word_tokenize(rawone)  # converts to list of words

sent_tokens[:2]
sent_tokensone[:2]

word_tokens[:5]
word_tokensone[:5]

lemmer = nltk.stem.WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


Introduce_Ans = [" "]
GREETING_INPUTS = (
    "hello", "hi", "hiii", "hii", "hiiii", "hiiii", "greetings", "sup", "what's up", "hey", "salam", "salaam", "aoa",
    "assalamoalikum", "asslam o alikum", "asalam o alikum", "janab", "aslamalikum", "salamalikum", "slam", "jnab",
    "suna",
    "sunao")
GREETING_RESPONSES = ["Hi! Are you suffering from any health issues? Please respond with (Y/N)",
                      "Hey! Are you having any health issues? Please respond with (Y/N)",
                      "Hii There! Are you suffering from any health issues? Please respond with (Y/N)",
                      "Hi There! Are you suffering from any health issues? Please respond with (Y/N)",
                      "Hello! Are you suffering from any health issues? Please respond with (Y/N)",
                      "I am glad! You are talking to me. Are you having any health issues? Please respond with (Y/N)"]
GREETING_RESPONSES = [
    "Hi! Are you suffering from any health issues? Please respond with (Y/N)(سلام! کیا آپ کسی صحت کے مسائل کا شکار ہیں؟ براہ کرم جواب دیں)"]
Basic_Q = (
    "yes", "y", "g", "jee", "han g", "han jee", "jee han", "han g", "g han mein bemar hu", "han jee m bemar hu", "gg",
    "jee jee")
Basic_Ans = "Okay! Tell me about your symptoms(مجھے اپنی علامات کے بارے میں بتائیں)"
Basic_Om = (
    "no", "n", "ni", "nahi", "nai", "nae", "nai g", "ni g", "ni jee", "koi nahi", "koi ni", "ni to", "nahi to", "naa",
    "nah", "nah g")
Basic_AnsM = "Thank you! Visit again (شکریہ! دوبارہ تشریف لائیے گا)"
fev = ("i am suffering from fever", "i affected with fever", "i have fever", "fever", "bukhar", "mujhay bukhar ha",
       "bukhar hai", "bukhaar", "bukhar ha",)
feve_r = (
    "Which type of fever you have? Please mention your symptoms then we will try to calculate your disease.(پ کو کس قسم کا بخار ہے؟ براہ کرم اپنی علامات لکھیں پھر میں آپ کی بیماری کا اندازہ لگانے کی کوشش کروں گا۔)")


# Checking for greetings
def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Checking for Basic_Q
def basic(sentence):
    for word in Basic_Q:
        if sentence.lower() == word:
            return Basic_Ans


def fever(sentence):
    for word in fev:
        if sentence.lower() == word:
            return feve_r


# Checking for Basic_QM
def basicM(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in Basic_Om:
        if sentence.lower() == word:
            return Basic_AnsM


# Checking for Introduce
def IntroduceMe(sentence):
    return random.choice(Introduce_Ans)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Generating response
def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)

    vals = cosine_similarity(tfidf[-1], tfidf)

    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if (req_tfidf == 0):
        robo_response = robo_response + "I am sorry! I don't understand you (میں معافی چاہتا ہوں ! مجھےآپ کی بات سمجھ نہیں آئی)"
        return robo_response
    else:
        robo_response = robo_response + sent_tokens[idx]
        return robo_response


# Generating response 

# Generating response
def responseone(user_response):
    robo_response = ''
    sent_tokensone.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokensone)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if req_tfidf == 0:
        robo_response = robo_response + "I am sorry! I don't understand you (میں معافی چاہتا ہوں ! مجھےآپ کی بات سمجھ نہیں آئی)"
        return robo_response
    else:
        robo_response = robo_response + sent_tokensone[idx]
        return robo_response


def chat(user_response):
    user_response = user_response.lower()
    keyword = " module "
    keywordone = " module"
    keywordsecond = "module "

    if user_response != 'bye':

        if user_response == 'thanks' or user_response == 'thank you':
            flag = False
            # print("ROBO: You are welcome..")
            return "You are welcome.."
        elif basicM(user_response) is not None:
            if session['user'] != 'guest':
                db = client.get_database('diseasepred')
                collection = db.user_record
                record = {
                    'user_name': session['user'],
                    'question': user_response,
                    'answer': basicM(user_response)
                }
                collection.insert_one(record)

                # print(basicM(user_response))
            return basicM(user_response)
        else:
            if (user_response.find(keyword) != -1 or user_response.find(keywordone) != -1 or user_response.find(
                    keywordsecond) != -1):
                # print("ROBO: ",end="")
                # print(responseone(user_response))
                if session['user'] != 'guest':
                    db = client.get_database('diseasepred')
                    collection = db.user_record
                    record = {
                        'user_name': session['user'],
                        'question': user_response,
                        'answer': responseone(user_response)
                    }
                    collection.insert_one(record)

                #print(responseone(user_response))
                return responseone(user_response)
                sent_tokensone.remove(user_response)
            elif greeting(user_response) is not None:
                # print("ROBO: "+greeting(user_response))
                if session['user'] != 'guest':

                    db = client.get_database('diseasepred')
                    collection = db.user_record
                    record = {
                        'user_name': session['user'],
                        'question': user_response,
                        'answer': greeting(user_response)
                    }
                    collection.insert_one(record)
               # print(greeting(user_response))
                return greeting(user_response)
            elif (user_response.find("your name") != -1 or user_response.find(" your name") != -1 or user_response.find(
                    "your name ") != -1 or user_response.find(" your name ") != -1):
                if session['user'] != 'guest':
                    db = client.get_database('diseasepred')
                    collection = db.user_record
                    record = {
                        'user_name': session['user'],
                        'question': user_response,
                        'answer': IntroduceMe(user_response)
                    }
                    collection.insert_one(record)
                #print(IntroduceMe(user_response))
                return IntroduceMe(user_response)
            elif basic(user_response) is not None:
                if session['user'] != 'guest':
                    db = client.get_database('diseasepred')
                    collection = db.user_record
                    record = {
                        'user_name': session['user'],
                        'question': user_response,
                        'answer': basic(user_response)
                    }
                    collection.insert_one(record)
                #print(basic(user_response))
                return basic(user_response)
            elif fever(user_response) is not None:
                if session['user'] != 'guest':
                    db = client.get_database('diseasepred')
                    collection = db.user_record
                    record = {
                        'user_name': session['user'],
                        'quesion': user_response,
                        'answer': fever(user_response)
                    }
                    collection.insert_one(record)
                #print(fever(user_response))
                return fever(user_response)
            else:
                resultresponse = response(user_response)
                print(resultresponse)
                if session['user'] != 'guest':

                    print('The user is not guest \n')
                    #print(response(user_response))
                    db = client.get_database('diseasepred')
                    collection = db.user_record
                    record = {
                        'user_name': session['user'],
                        'quesion': user_response,
                        'answer': resultresponse
                    }
                    collection.insert_one(record)
                # print("ROBO: ",end="")
                # print(response(user_response))

                return resultresponse
                sent_tokens.remove(user_response)

    else:
        flag = False
        # print("ROBO: Bye! take care..")
        return "Bye! take care.."
