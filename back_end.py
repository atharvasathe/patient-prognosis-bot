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
    def __init__(self):
        self.index = 0
        self.screens = []
        self.process()
    def getInitialScreen(self):
        return self.screens[0]
    def getNextScreen(self):
        if ( self.index + 1 < len(self.screens) ):
            self.index+=1
            return self.screens[self.index]
        else:
            return None
    def getPrevScreen(self):
        if ( self.index >= 0 ):
            self.index-=1
            return self.screens[self.index]
        else:
            return None
    def process(self):
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

        self.screens = parsedScreens

#Testing Output
#Can delete later, just to show how to access values

#Dummy Front End
be = Backend()
be.process()

for screen in be.screens:
    print("Screen Title:", screen.title)
    if screen.condition.exists:
        print("Condition Question:", screen.condition.question)
        print("Condition Answer:", screen.condition.ans)
    for question in screen.questions:
        print("Question Prompt:", question.prompt)
        print("Answer Type:", question.type)
        print("Answer:", question.ans)
    print()

#Practice Screens
scr1 = be.getInitialScreen()
print("Screen 1:")
print("Screen Title:", scr1.title)
if scr1.condition.exists:
    print("Condition Question:", scr1.condition.question)
    print("Condition Answer:", scr1.condition.ans)
for question in scr1.questions:
    print("Question Prompt:", question.prompt)
    print("Answer Type:", question.type)
    print("Answer:", question.ans)
print()

scr2 = be.getNextScreen()
print("Screen 2:")
print("Screen Title:", scr2.title)
if scr2.condition.exists:
    print("Condition Question:", scr2.condition.question)
    print("Condition Answer:", scr2.condition.ans)
for question in scr2.questions:
    print("Question Prompt:", question.prompt)
    print("Answer Type:", question.type)
    print("Answer:", question.ans)
print()

scr3 = be.getPrevScreen()
print("Screen 1 again:")
print("Screen Title:", scr3.title)
if scr3.condition.exists:
    print("Condition Question:", scr3.condition.question)
    print("Condition Answer:", scr3.condition.ans)
for question in scr3.questions:
    print("Question Prompt:", question.prompt)
    print("Answer Type:", question.type)
    print("Answer:", question.ans)
print()

print("finished")
