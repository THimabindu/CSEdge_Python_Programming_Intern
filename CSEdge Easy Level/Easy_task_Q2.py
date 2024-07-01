import random
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np

nltk.download('punkt')

stemmer = LancasterStemmer()

# Define intents and responses
intents = {
    "intents": [
        {
            "tag": "greeting",
            "patterns": ["Hi", "Hello", "Hey", "Hi there"],
            "responses": ["Hello!", "Hi!", "Hey there!"]
        },
        {
            "tag": "goodbye",
            "patterns": ["Bye", "Goodbye", "See you later"],
            "responses": ["Goodbye!", "See you later!", "Have a nice day!"]
        },
        {
            "tag": "thanks",
            "patterns": ["Thanks", "Thank you", "Appreciate it"],
            "responses": ["You're welcome!", "No problem!", "Anytime!"]
        },
        {
            "tag": "name",
            "patterns": ["What is your name?", "Who are you?"],
            "responses": ["I am a chatbot.", "I am your friendly chatbot."]
        }
    ]
}

# Initialize data structures
words = []
labels = []
docs_x = []
docs_y = []

# Process each intent
for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

# Stem and lower each word, and remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

# Create bag-of-words model
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)

# Generate response
def generate_response(input_text):
    bow = bag_of_words(input_text, words)
    results_index = None

    for i, doc in enumerate(docs_x):
        if bow.tolist() == bag_of_words(" ".join(doc), words).tolist():
            results_index = i
            break

    if results_index is not None:
        tag = docs_y[results_index]
        for intent in intents["intents"]:
            if intent["tag"] == tag:
                responses = intent["responses"]
        return random.choice(responses)
    else:
        return "I didn't understand that. Can you rephrase?"

# Chat function
def chat():
    print("Start talking with the bot (type 'quit' to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        response = generate_response(inp)
        print(response)

chat()
