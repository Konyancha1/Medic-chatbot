import streamlit as st
import nltk
import string
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title("Medibot: A Medical Chatbot")
st.write("Hello there! I am Medibot, a medic chatbot. How can I be of service?")

f = open('Research data on pregnancy (1).txt', 'r', errors='ignore')
raw = f.read()

raw = raw.lower()
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

sentence_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
  return [lemmer.lemmatize(token) for token in tokens]
remove_punctuations = dict((ord(punkt), None) for punkt in string.punctuation)

def LemNormalize(text):
  return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punctuations)))

greetings = ['hello', 'hi', 'how are you']
responses_greetings = ['Hello', 'Hi, how are you?']

def greet(sentence):
  for word in sentence.split():
    if word.lower() in greetings:
      return random.choice(responses_greetings)

def response(user_input):
    chat_response = ''
    if not sentence_tokens:
        chat_response = chat_response + "I am sorry, I am unable to understand you"
        return chat_response
    TfidVec = TfidfVectorizer(tokenizer= LemNormalize, stop_words = 'english')
    tfidf = TfidVec.fit_transform(sentence_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    if len(vals.argsort()[0]) > 1:
        index = vals.argsort()[0][-2]
    else:
        index = vals.argsort()[0][0]
    flat = vals.flatten()
    flat.sort()
    if len(flat) > 1:
        req_tfidf = flat[-2]
    else:
        req_tfidf = flat[-1]
    if(req_tfidf == 0):
        chat_response = chat_response + "I am sorry, I am unable to understand you"
        return chat_response
    else:
        chat_response = chat_response + sentence_tokens[index]
        return chat_response

input_text = st.text_input("You: ", "")
if st.button("Send"):
    user_input = input_text.lower()
    if(user_input != 'bye'):
        if(user_input == 'thank you' or user_input == 'thanks so much'):
            st.write("Medibot: You're welcome")
        else:
            if greet(user_input) is not None:
                st.write("Medibot: " + greet(user_input))
            else:
                sentence_tokens.append(user_input)
                word_tokens = nltk.word_tokenize(user_input)
                final_words = list(set(word_tokens))
                response_text = response(user_input)
                sentence_tokens.remove(user_input)
                st.write("Medibot: " + response_text)
    else:
        st.write("Medibot: Goodbye!")