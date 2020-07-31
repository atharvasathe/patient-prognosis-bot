import json

class Question:
    #class variables
    #prompt, type, answer
    def __init__(self, prompt, type, ans):
        self.prompt = prompt
        self.type = type
        self.ans = ans

class Condition:
    #class variables
    #exists, question, answer
    def __init__(self, exists, question, ans):
        self.exists = exists
        self.question = question
        self.ans = ans

class Screen:
    #class variables
    #title, condition{}, questions[]
    def __init__(self, title, condition, questions):
        self.title = title
        self.condition = condition
        self.questions = questions

class Backend:
    def __init__(self, screens):
        self.screens = screens
    #def getInitialScreen()
        #returns Screen object
    #def getNextScreen(self, screen):
        #returns Screen object
        #returns null if there are no more screens
    #def getPrevScreen(self, screen):
        #returns Screen object

#Convert JSON into a python dictionary
with open('sample2.json') as jsonFile:
    data = json.load(jsonFile)

parsedScreens = []

#Parsing
inputScreens = data["screens"]
for screen in inputScreens:
    if "condition" in screen:
        c = Condition(True, screen["condition"]["question"], screen["condition"]["answer"])
    else:
        c = Condition(False, "", "")
    parsedQuestions = []
    for question in screen["questions"]:
        q = Question(question["prompt"], question["type"], "")
        parsedQuestions.append(q)
    s = Screen(screen["title"], c, parsedQuestions)
    parsedScreens.append(s)

#Backend object contains all values needed
be = Backend(parsedScreens)

#Testing Output
#Can delete later, just to show how to access values
for screen in be.screens:
    print("Screen Title:", screen.title)
    if screen.condition.exists:
        print("Condition Question:", screen.condition.question)
        print("Condition Answer:", screen.condition.ans)
    for question in screen.questions:
        print("Question Prompt:", question.prompt)
        print("Answer Type:", question.type)
        #print("Answer:", question.ans)
    print()

print("finished")
