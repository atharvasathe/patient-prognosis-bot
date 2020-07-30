import json

class Question:
    #txt is a list of the questions
    #ans is an Answer object (contains list of answers)
    def __init__(self, txt, ans):
        self.txt = txt
        self.ans = ans
    def addAnswer(self,ansText):
        self.ans.txt.append(ansText)
class Answer:
    #txt is a list of answers
    #type is the type of answers
    def __init__(self,type):
        self.txt = []
        self.type = type

#JSON
#overarching question is the key
#array contains the answer type and if needed subquestions to display on same page
with open('questions.json') as jsonFile:
    dictFile = json.loads(jsonFile.read())

listOfQs = []

#parsing dictionary intro question objects which contain answer objects
for x in dictFile:
    #x is the key
    #dictFile[x] is the value
    #Greeting
    if (len(dictFile[x]) == 0):
        ans = Answer("")
        listOfText = []
        listOfText.append(x)
        q = Question(listOfText, ans)
    #Single Question or Multiple Questions
    else:
        ans = Answer(dictFile[x][0])
        listOfText = []
        listOfText.append(x)
        for i in range(1,len(dictFile[x])):
            listOfText.append(dictFile[x][i])
        q = Question(listOfText, ans)
    listOfQs.append(q)

for q in listOfQs:
    print("Questions: " + str(q.txt))
    print("Answer Type: " + q.ans.type)
    print("Answers: " + str(q.ans.txt) + "\n")