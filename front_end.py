import tkinter as tk
from back_end import Question, Condition, Screen, Backend

TITLE_FONT= ("Verdana", 12)
QUESTION_FONT= ("verdana", 10)
QUESTION_PAD_X= 5
QUESTION_PAD_Y= 5
ANSWER_PAD_X= 5
ANSWER_PAD_Y= 5

class PatientPrognosisBot(tk.Tk):

    def __init__(self, *args, **kwargs):
    
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        self.geometry("1280x720")

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

def qf(stringtoprint):
    print(stringtoprint)

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #Array Widgets holds all of the tkinter Labels and Entry box widgets 
        self.widgets=[]

        #initializes backend
        self.backend = Backend()

        #builds the first screen
        self.buildInitialPage()

        #Dictionary that holds all of the answer widgets
        self.answers_dictionary={}

        #Question tkinter Frame
        self.question_frame = tk.Frame(self)
        #self.question_frame.geometry("640x720")
        self.question_frame.pack(side="left")

        #Answer tkinter Frame
        self.answer_frame = tk.Frame(self)
        self.answer_frame.pack(side="right")


    #builds initial screen
    #is only called at the beginning
    def buildInitialPage(self):
        screen = self.backend.getInitialScreen()
        self.buildPage(screen)


    def buildPage(self, screen):
        current_screen = screen

        if screen is None:
            return

        #packs the screen title in larger font
        label = tk.Label(self, text=current_screen.title, font=TITLE_FONT)
        label.pack(pady=10, padx=10)
        #adds the screen title to array widgets
        self.widgets.append(label)

        #loops through all Questions in Screen and displays them 
        for question in screen.questions:
            self.displayQuestion(question)

        #next button calls for the next screen
        button_next = tk.Button(self, text="Next", 
                                command=lambda: self.nextPage(current_screen, 1))
        button_next.pack(side="bottom")
        #adds next button to array widgets
        self.widgets.append(button_next)
        #prev button calls for the prev screen
        button_prev = tk.Button(self, text="Back", 
                                command=lambda: self.nextPage(current_screen, 0))
        button_prev.pack(side="bottom")
        #adds prev button to array widgets
        self.widgets.append(button_prev)

       
    def destroyPage(self):
        #loops through array widgets and deletes them
        for x in self.widgets:
            x.pack_forget()
        #clears array widgets
        self.widgets=[]

    def nextPage(self, screen, direction):
        self.saveAnswers(screen)
        #self.printScreen(screen)
        self.destroyPage()

        #calls next or prev depending on the direction parameter
        if direction == 1:
            self.buildPage(self.backend.getNextScreen())
        else:
            self.buildPage(self.backend.getPrevScreen())
       

    def displayQuestion(self, question):
        #displays question prompt
        question_prompt = tk.Label(self.question_frame, text=question.prompt, font= QUESTION_FONT)
        question_prompt.pack(padx=QUESTION_PAD_X, pady=QUESTION_PAD_Y)#side = "left")
        #adds question prompt to array widgets
        self.widgets.append(question_prompt)

        #creates the proper entry widget depending on the answer type
        if question.type == "string":
            string_entry = tk.Entry(self.answer_frame, bd=2)
            string_entry.insert(0, question.ans)
            string_entry.pack(padx=ANSWER_PAD_X, pady=ANSWER_PAD_Y)#side = "right")
            self.widgets.append(string_entry)
            self.answers_dictionary[question.prompt] = string_entry

        elif question.type == "yn":
            var = tk.IntVar()
            self.answers_dictionary[question.prompt] = var

            radio_entry_yes = tk.Radiobutton(self.answer_frame, text="Yes", variable=var, value=2)
            if question.ans == "Yes":
                radio_entry_yes.select()
            radio_entry_yes.pack(padx=ANSWER_PAD_X, pady=ANSWER_PAD_Y)#side = "right")
            self.widgets.append(radio_entry_yes)

            radio_entry_no = tk.Radiobutton(self.answer_frame, text="No", variable=var, value=1)
            if question.ans == "No":
                radio_entry_no.select()
            radio_entry_no.pack(padx=ANSWER_PAD_X, pady=ANSWER_PAD_Y)#side = "right")
            self.widgets.append(radio_entry_no)

        elif question.type == "check":
            var = tk.IntVar()
            self.answers_dictionary[question.prompt] = var

            check_button = tk.Checkbutton(self.answer_frame, variable = var, onvalue = 2, offvalue = 1)
            if question.ans == "Yes":
                check_button.select()
            elif question.ans == "No":
                check_button.deselect()
            check_button.pack(padx=ANSWER_PAD_X, pady=ANSWER_PAD_Y)
            self.widgets.append(check_button)
            

    def saveAnswers(self, screen):
        #loops through Questions and saves the answers depending on dictionary answers
        for question in screen.questions:
            if question.type == "string":
                question.ans = self.answers_dictionary[question.prompt].get()       
            else:
                if self.answers_dictionary[question.prompt].get() == 2:
                    question.ans = "Yes"
                elif self.answers_dictionary[question.prompt].get() == 1:
                    question.ans = "No"    


    def printScreen(self, screen):
        print(screen.title)
        for question in screen.questions:
            print("Question Prompt:", question.prompt)
            print("Answer Type:", question.type)
            print("Answer:", question.ans)
            print("Display:", question.display)

class PageOne(tk.Frame):

     def __init__(self, parent, controller):
         tk.Frame.__init__(self, parent)
         label = tk.Label(self, text="Page One", font=TITLE_FONT)
         label.pack(pady=10, padx=10)

         button1 = tk.Button(self, text="back", 
                            command=lambda: controller.show_frame(StartPage))
         button1.pack()

app = PatientPrognosisBot()
app.mainloop()