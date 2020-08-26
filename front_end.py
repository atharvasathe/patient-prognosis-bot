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

        container.pack()

        StartPage(container, self)

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, parent)

        self.grid_columnconfigure(0, minsize=360)
        self.grid_columnconfigure(1, minsize=360)

        #Array Widgets holds all of the tkinter Labels and Entry box widgets 
        self.widgets=[]

        #initializes backend
        self.backend = Backend()

        #builds the first screen
        self.buildInitialPage()

        #Dictionary that holds all of the answer widgets
        self.answers_dictionary={}

    #builds initial screen
    #is only called at the beginning
    def buildInitialPage(self):
        screen = self.backend.getInitialScreen()
        self.buildPage(screen)


    def buildPage(self, screen):
        current_screen = screen

        if screen is None:
            evaluation = tk.Label(self, text=self.backend.evaluate().title, wraplength=1200, font=TITLE_FONT)
            evaluation.grid(row=1)
            self.backend.print(False)
            return

        title_frame = tk.Frame(self)
        title_frame.grid(row=0, columnspan=2)
        title_frame.columnconfigure(0, minsize=1200)

        #packs the screen title in larger font
        grid_row = 0
        label = tk.Label(title_frame, text=current_screen.title, font=TITLE_FONT)
        label.grid(row=0, column=0)
        #adds the screen title to array widgets
        self.widgets.append(label)

        #loops through all Questions in Screen and displays them 
        for question in screen.questions:
            if question.display != False:
                grid_row = grid_row + 1
                self.displayQuestion(question, grid_row)

        grid_row = grid_row + 1
        #next button calls for the next screen
        button_next = tk.Button(title_frame, text="Next", 
                                command=lambda: self.nextPage(current_screen, 1))
        button_next.grid(row=0, column=2, sticky="E")
        #adds next button to array widgets
        self.widgets.append(button_next)
        #prev button calls for the prev screen
        button_prev = tk.Button(title_frame, text="Back", 
                                command=lambda: self.nextPage(current_screen, 0))
        button_prev.grid(row=0, column=1, sticky="E")
        #adds prev button to array widgets
        self.widgets.append(button_prev)

        self.pack()

       
    def destroyPage(self):
        #loops through array widgets and deletes them
        for x in self.widgets:
            x.grid_forget()
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
       

    def displayQuestion(self, question, grid_row):
        #displays question prompt
        question_prompt = tk.Label(self, text=question.prompt, font= QUESTION_FONT)
        question_prompt.grid(row=grid_row, column=0) # grid_row, 0
        #adds question prompt to array widgets
        self.widgets.append(question_prompt)

        #creates the proper entry widget depending on the answer type
        if question.type == "string":
            string_entry = tk.Entry(self, bd=2)
            string_entry.insert(0, question.ans)
            string_entry.grid(row=grid_row, column=1)
            self.widgets.append(string_entry)
            self.answers_dictionary[question.prompt] = string_entry

        elif question.type == "yn":
            yn_frame = tk.Frame(self)
            var = tk.IntVar()
            self.answers_dictionary[question.prompt] = var

            radio_entry_yes = tk.Radiobutton(yn_frame, text="Yes", variable=var, value=2)
            if question.ans == "yes":
                radio_entry_yes.select()
            radio_entry_yes.grid(row=0, column=0)
            self.widgets.append(radio_entry_yes)

            radio_entry_no = tk.Radiobutton(yn_frame, text="No", variable=var, value=1)
            if question.ans == "no":
                radio_entry_no.select()
            radio_entry_no.grid(row=0, column=1)
            self.widgets.append(radio_entry_no)
            
            yn_frame.grid(row=grid_row, column=1)

        elif question.type == "check":
            var = tk.IntVar()
            self.answers_dictionary[question.prompt] = var

            check_button = tk.Checkbutton(self, variable = var, onvalue = 2, offvalue = 1)
            if question.ans == "yes":
                check_button.select()
            elif question.ans == "no":
                check_button.deselect()
            check_button.grid(row=grid_row, column=1)
            self.widgets.append(check_button)
            

    def saveAnswers(self, screen):
        #loops through Questions and saves the answers depending on dictionary answers
        for question in screen.questions:
            if question.type == "string":
                question.ans = self.answers_dictionary[question.prompt].get()       
            else:
                if self.answers_dictionary[question.prompt].get() == 2:
                    question.ans = "yes"
                elif self.answers_dictionary[question.prompt].get() == 1:
                    question.ans = "no"    

app = PatientPrognosisBot()
app.mainloop()