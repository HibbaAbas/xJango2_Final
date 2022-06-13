#imports
import speech_recognition as sr
import pyttsx3
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import datetime 
from datetime import date
import pyjokes
import wikipedia

#WAKE = "Hey jango"
#get audio from mic, return as string
def get_audio():
    r = sr.Recognizer()
    r.energy_threshold = 300
    mic = sr.Microphone(device_index=1)

    with mic as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
    return said.lower()

#tests similarity between two sentences
def similarity(user_input, command):
    X = user_input
    Y = command

    #tokenize sentences
    X_list = word_tokenize(X)
    Y_list = word_tokenize(Y)

    #create list of stop words
    sw = stopwords.words('english')
    vx =[]; vy =[]

    #remove stop words from sentences
    X_set = {w for w in X_list if not w in sw}
    Y_set = {w for w in Y_list if not w in sw}

    #form sets with key words
    rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set: vx.append(1)
        else: vx.append(0)
        if w in Y_set: vy.append(1)
        else: vy.append(0)

    c = 0
    #cosine formula
    for i in range(len(rvector)):
        c+= vx[i]*vy[i]
    cosine = c / float((sum(vx)*sum(vy))**0.5)
    #cosine = str(cosine)
    print("similarity is: " + str(cosine))
    return cosine

#set up Jango's speak function
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 30)
def speak(text):
    engine.say(text)
    engine.runAndWait()

name_comm = "What is your name"
date_comm = "What is the date"
date_comm_2 = "What day is today"
time_comm = "what is the time"
joke_comm = "tell me a joke"
wiki_comm = "I want to make a wikipedia search"

def time():
    now = datetime.now()
    current_time = now.strftime("%H: %M")
    speak(current_time)

def dateC():
    today = date.today()
    d1 = today.strftime("%m/%d")
    speak("Today's date is " + d1)

def joke():
    joke = pyjokes.get_joke()
    speak(joke)

def wikiC():
    speak ("Ok, what would you like to search?")
    search = get_audio()
    speak(wikipedia.summary(search, sentences = 2))
    speak ("I hope you were satisified with the result")


#figure out what the command is
def uCommand(user_comm):
    if similarity(user_comm, name_comm) > 0.3:
        speak("my name is jango")
    elif similarity(user_comm, date_comm) > 0.2 or similarity(user_comm, date_comm_2) > 0.2:
        dateC()
    elif similarity(user_comm, time_comm) > 0.3:
        time()
    elif similarity(user_comm, joke_comm) >0.2:
        joke()
    elif similarity(user_comm, wiki_comm) >0.2:
        wikiC()
    else:
        speak("sorry, I did not understand your command")
speak("I await your command")

i = 0
while i < 1:
    user_comm = get_audio()
    if "hey" in user_comm:
        print("command detected")
        uCommand(user_comm)
    elif "stop" in user_comm:
        i = 1
    else:
        print("command not yet dtected")

