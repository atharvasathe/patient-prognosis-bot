import json

class Question:
    #class variables
    #strin prompt, string type, string answer
    def __init__(self, prompt, type, ans, display):
        self.prompt = prompt
        self.type = type
        self.ans = ans
        self.display = display

class Condition:
    #class variables
    #string question, string answer
    def __init__(self, question, ans):
        self.question = question
        self.ans = ans

class Screen:
    #class variables
    #string title, conditions[], questions[]
    def __init__(self, title, conditions, questions):
        self.title = title
        self.conditions = conditions
        self.questions = questions
    #bool complex
    #determines whether condtions, answer type, and display are printed or not
    def print(self, complex):
        print("Screen Title:", self.title)
        if (complex):
            for condition in self.conditions:
                print("Condition Question:", condition.question)
                print("Condition Answer:", condition.ans)
        for question in self.questions:
            print("Question:", question.prompt)
            if (complex):
                print("Answer Type:", question.type)
            print("Answer:", question.ans)
            if (complex):
                print("Display:", question.display)

class Backend:
    def __init__(self):
        self.index = 0
        self.screens = []
        self.process()
    #Gets First Screen
    def getInitialScreen(self):
        self.index = 0
        return self.screens[0]
    #Gets Next Screen
    def getNextScreen(self):
        self.index+=1
        self.checkConds(True)
        if ( self.index < len(self.screens) ):
            return self.screens[self.index]
        else:
            return None
    #Gets Previous Screen
    def getPrevScreen(self):
        self.index-=1
        self.checkConds(False)
        if ( self.index >= 0 ):
            return self.screens[self.index]
        else:
            return None
    #Initializes values and Parses JSON file
    def process(self):
        #Convert JSON into a python dictionary
        with open('questions.json') as jsonFile:
            data = json.load(jsonFile)

        #Parsing
        parsedScreens = []
        inputScreens = data["screens"]
        for screen in inputScreens:
            parsedConditions = []
            for condition in screen["conditions"]:
                c = Condition(condition["question"], condition["answer"])
                parsedConditions.append(c)
            parsedQuestions = []
            for question in screen["questions"]:
                q = Question(question["prompt"], question["type"], question["answer"], True)
                parsedQuestions.append(q)
            s = Screen(screen["title"], parsedConditions, parsedQuestions)
            parsedScreens.append(s)

        self.screens = parsedScreens
    #Checks if conditions are met to display question(s)
    def checkConds(self, forward):
        #Check if index is in range
        if ( self.index < len(self.screens) and self.index > 0 ):
            conditionList = self.screens[self.index].conditions
            prevQuestionList = self.screens[self.index - 1].questions
            currQuestionList = self.screens[self.index].questions
            #Make sure conditions exist
            if len(conditionList) > 0:
                #Iterate to next screen (one condition)
                if len(conditionList) == 1:
                    if conditionList[0].ans != prevQuestionList[0].ans:
                        if (forward):
                            self.getNextScreen()
                        else:
                            self.getPrevScreen()
                #Hide specific questions from screen
                elif len(conditionList) == len(prevQuestionList) == len(currQuestionList):
                    size = len(conditionList)
                    numHidden = 0
                    for i in range(size):
                        if conditionList[i].ans != prevQuestionList[i].ans:
                            currQuestionList[i].display = False
                            numHidden+=1
                    #All questions were hidden
                    if ( numHidden == size ):
                        if (forward):
                            self.getNextScreen()
                        else:
                            self.getPrevScreen()
                    if ( self.index < len(self.screens) ):
                        self.screens[self.index].questions = currQuestionList
                #Iterate to next screen (multiple conditions)
                elif len(conditionList) == len(prevQuestionList):
                    skip = False
                    size = len(conditionList)
                    for i in range(size):
                        if conditionList[i].ans != "" and conditionList[i].ans != prevQuestionList[i].ans:
                            skip = True
                            break
                    if (skip):
                        if (forward):
                            self.getNextScreen()
                        else:
                            self.getPrevScreen()
    #Uses JSON file to evaluate user's answers
    def evaluate(self):
        #Convert JSON into a python dictionary
        with open('importance.json') as jsonFile:
            data = json.load(jsonFile)

        #Evaluation
        inputScreens = data["screens"]
        messages = data["messages"]
        i = 0
        total = 0
        for screen in inputScreens:
            #stores trigger answers
            trigList = screen["triggers"]
            #stores imporance of answers
            ratingList = screen["ratings"]
            #stores questions which contain the user answers
            qList = self.screens[i].questions
            
            if (len(trigList) > 0 and len(trigList) == len(ratingList) == len(qList)):
                for x in range(len(trigList)):
                    trigger = trigList[x]
                    ans = qList[x].ans
                    rat = ratingList[x]
                    if (trigger != "" and ans != ""):
                        #check if answer is "triggered"
                        if (trigger[0] == ">"):
                            ansNum = int(ans)
                            trigNum = int(trigger[1:])
                            if (ansNum > trigNum):
                                #Add to Total
                                total+=rat
                        elif (trigger[0] == "<"):
                            ansNum = int(ans)
                            trigNum = int(trigger[1:])
                            if (ansNum < trigNum):
                                #Add to Total
                                total+=rat
                        else:
                            if (trigger == ans):
                                #Add to Total
                                total+=rat
            i+=1
        #use total to determine a final message
        #use thresholds in messages list to determine which message to return
        fmessage = ""
        backupMessage = ""
        for m in messages:
            txt = m["text"]
            thresh = m["threshold"]
            #The backup message should always be available in case none of the thresholds are passed
            if (thresh == -1):
                backupMessage = txt
            else:
                if (total >= thresh):
                    fmessage = txt
                    break
        if (fmessage == ""):
            fmessage = backupMessage
        conds = []
        questions = []
        lastScreen = Screen(fmessage, conds, questions)
        return lastScreen
    #bool complex
    #determines whether condtions, answer type, and display are printed or not
    def print(self, complex):
        print("User Answers:")
        i = 0
        for scr in self.screens:
            print("Screen", i, ":")
            scr.print(complex)
            print()
            i+=1

#Dummy Front End
be = Backend()

#Evaluation and Output
#example of what happens after the last screen in the frontend
scr = be.evaluate()
scr.print(False)
print()
be.print(False)
