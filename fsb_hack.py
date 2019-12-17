import io
import os
import random
import string  # (Zur Verarbeitung von Standard Python Strings)
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from termcolor import colored, cprint
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

warnings.filterwarnings('ignore')

nltk.download('stopwords')
# salutations
GREETING_INPUTS = ("bonjour", "salut", "salutations", "Mon pote", "ce qui est possible", "hé")
GREETING_RESPONSES = ["salut", "hé", "salut de dieu", "Wech wech mon pote", "bonjour","Je suis content de te parler."]

# insultes
INDIGNITY_INPUTS = ("cul", "truie", "dork", "maladroit", "stupide", "merde")
INDIGNITY_RESPONSES = ["Nous devons être gentils les uns avec les autres. "," Si vous voulez dire. "," Pensez à ce que vous dites. ",
                        "Je ne pense pas que ce soit bien.", "Tu ne devrais pas dire ça",
                        "Oh oui, vous êtes un très beau contemporain ..."]

nltk.download('popular', quiet=True)

# Pour le premier départ, sinon commentez
nltk.download('punkt')
nltk.download('wordnet')

# Lire dans le corpus
with open('chatbot_de.txt', 'r', encoding='utf8', errors='ignore') as fin:
    raw = fin.read().lower()

# Tokenization
# sent_tokens convertit en liste de phrases
sent_tokens = nltk.sent_tokenize(raw)

# word_tokens convertit en liste de mots (non utilisé.)
word_tokens = nltk.word_tokenize(raw)

# Prétraitement
lemmer = WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
def trivia(sentence):
    # '' 'Si l'entrée de l'utilisateur est dans le message d'accueil,
    # le bot répond avec un message d'accueil aléatoire comme réponse,
    # la même chose s'applique aux insultes' ''
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
        if word.lower() in INDIGNITY_INPUTS:
            return random.choice(INDIGNITY_RESPONSES)


# Antwort Erzeugung
def response(user_response):
    stop_words = stopwords.words('french')
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=stop_words)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if (req_tfidf == 0):
        robo_response = robo_response + "Je suis désolé, je ne vous comprends pas."
        return robo_response
    else:
        robo_response = robo_response + sent_tokens[idx]
        return robo_response


'''
édition
(La bibliothèque termcolor est utilisée pour rendre la sortie de la console plus claire)
'''
flag = True
clear = lambda: os.system('clear')
clear()
print(colored("DamDamou: ", 'green', attrs=['bold']) + colored(
    "Bonjour, je m'appelle DamDamou. Je connais beaucoup de chatbots mais je pense que je suis le meilleur. Demandez-moi! Si vous voulez quitter, tapez 'Bye'.",
    'cyan'))
while (flag == True):
    user_response = input()
    user_response = user_response.lower()
    if (user_response != 'bye'):
        if (user_response == 'Danke dir' or user_response == 'Danke'):
            flag = False
            print(colored("DamDamou: ", 'green', attrs=['bold']) + colored("Gerne..", 'cyan'))
        else:
            if (trivia(user_response) != None):
                print(colored("DamDamou: ", 'green', attrs=['bold']) + colored(trivia(user_response), 'cyan'))
            else:
                print(colored("DamDamou: ", 'green', attrs=['bold']), end="")
                print(colored(response(user_response), 'cyan'))
                sent_tokens.remove(user_response)
    else:
        flag = False
        print(colored("DamDamou: ", 'green', attrs=['bold']) + colored("Au revoir! Faites attention.", 'cyan'))


