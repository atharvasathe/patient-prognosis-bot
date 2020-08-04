import json

with open('sample2.json') as jsonFile:
    data = json.load(jsonFile)

screens = data["screens"]
for screen in screens:
    print("Screen title:", screen["title"])
    if "condition" in screen:
        print("Condition:", screen["condition"])
    for question in screen["questions"]:
        print ("Questions Prompt:", question["prompt"])
        print ("Answer type:", question["type"])

print("finished")


""" class Question:
    #class variables
    #prompt, type, answer
    def __init__(self, prompt, type_ans, answer):
        self.prompt = prompt
        self.type = type_ans
        self.answer = answer """

class Screen:
    #class variables
    #title, condition{}, questions[]
    def __init__(self, text):
        self.text = text


class Backend:
    #def getInitialScreen()
    #returns Screen object

    def getNextScreen(self):
        #returns Screen object
        #returns null if there are no more screens
        tempscreen = Screen()
        return tempscreen

    #def getPrevScreen(self, screen):
        #returns Screen object 