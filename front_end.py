import tkinter as tk
from back_end import Question, Condition, Screen, Backend

TITLE_FONT= ("Verdana", 12)
QUESTION_FONT= ("verdana", 10)

class PatientPrognosisBot(tk.Tk):

    def __init__(self, *args, **kwargs):
    
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

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
        button_next.pack()
        #adds next button to array widgets
        self.widgets.append(button_next)
        #prev button calls for the prev screen
        button_prev = tk.Button(self, text="Back", 
                                command=lambda: self.nextPage(current_screen, 0))
        button_prev.pack()
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
        question_prompt = tk.Label(self, text=question.prompt, font= QUESTION_FONT)
        question_prompt.pack()#side = LEFT)
        #adds question prompt to array widgets
        self.widgets.append(question_prompt)

        #creates the proper entry widget depending on the answer type
        if question.type == "string":
            string_entry = tk.Entry(self, bd=2)
            string_entry.pack()#side = RIGHT)
            self.widgets.append(string_entry)
            self.answers_dictionary[question.prompt] = string_entry
        elif question.type == "yn":
            var = tk.StringVar()
            self.answers_dictionary[question.prompt] = var
            radio_entry_yes = tk.Radiobutton(self, text="Yes", variable=var, value="yes")
            radio_entry_yes.pack()#side=RIGHT)
            self.widgets.append(radio_entry_yes)

            radio_entry_no = tk.Radiobutton(self, text="No", variable=var, value="no")
            radio_entry_no.pack()#side=RIGHT)
            self.widgets.append(radio_entry_no)
        elif question.type == "check":
            var = tk.StringVar()
            self.answers_dictionary[question.prompt] = var
            check_button = tk.Checkbutton(self, variable = var, onvalue = "yes", offvalue = "no")
            check_button.pack()
            self.widgets.append(check_button)
            

    def saveAnswers(self, screen):
        #loops through Questions and saves the answers depending on dictionary answers
        for question in screen.questions:
            question.ans = self.answers_dictionary[question.prompt].get()       

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