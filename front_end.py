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
        self.widgets=[]
        #self.page_number=1
        self.backend = Backend()
        #self.screen = Screen("")
        self.buildInitialPage()
        #self.buildPage(self.screen)

    def buildInitialPage(self):
        #self.screen = self.screen.getInitialScreen()
        screen = self.backend.getInitialScreen()
        self.buildPage(screen)


    def buildPage(self, screen):
        """ if self.page_number == 1:
            label = tk.Label(self, text="Patent Prognosis BOT Start Page", font=TITLE_FONT)
            label.pack(pady=10, padx=10)
            self.widgets.append(label)

            button1 = tk.Button(self, text="Next", 
                                command=lambda: self.nextPage(screen))
            button1.pack()
            self.widgets.append(button1)
        else:

            #temp1screen = self.backend.getInitialScreen()

            label = tk.Label(self, text= screen.text, font=TITLE_FONT)
            label.pack(pady=10, padx=10)
            self.widgets.append(label)

            button1 = tk.Button(self, text="Next", 
                                command=lambda: self.nextPage(screen))
            button1.pack()
            self.widgets.append(button1) """
        current_screen = screen
        label = tk.Label(self, text=current_screen.title, font=TITLE_FONT)
        label.pack(pady=10, padx=10)
        self.widgets.append(label)

        for question in screen.questions:
            self.displayQuestion(question)

        button_next = tk.Button(self, text="Next", 
                                command=lambda: self.nextPage(current_screen, 1))
        button_next.pack()
        self.widgets.append(button_next)

        button_prev = tk.Button(self, text="Back", 
                                command=lambda: self.nextPage(current_screen, 0))
        button_prev.pack()
        self.widgets.append(button_prev)

        
    def destroyPage(self):
        for x in self.widgets:
            x.pack_forget()
        self.widgets=[]

    def nextPage(self, screen, direction):
        self.destroyPage()
        #self.page_number=self.page_number+1
        if direction == 1:
            self.buildPage(self.backend.getNextScreen())
        else:
            self.buildPage(self.backend.getPrevScreen())
       

    def displayQuestion(self, question):
        question_prompt = tk.Label(self, text=question.prompt, font= QUESTION_FONT)
        question_prompt.pack()#side = LEFT)
        self.widgets.append(question_prompt)

        if question.type == "string":
            string_entry = tk.Entry(self, bd=2)
            string_entry.pack()#side = RIGHT)
            self.widgets.append(string_entry)
        elif question.type == "yn":
            var = tk.IntVar()
            radio_entry_yes = tk.Radiobutton(self, text="Yes", variable=var, value=1)
            radio_entry_yes.pack()#side=RIGHT)
            self.widgets.append(radio_entry_yes)

            radio_entry_no = tk.Radiobutton(self, text="No", variable=var, value=2)
            radio_entry_no.pack()#side=RIGHT)
            self.widgets.append(radio_entry_no)
            



class PageOne(tk.Frame):

     def __init__(self, parent, controller):
         tk.Frame.__init__(self, parent)
         label = tk.Label(self, text="Page One", font=TITLE_FONT)
         label.pack(pady=10, padx=10)

         button1 = tk.Button(self, text="back", 
                            command=lambda: controller.show_frame(StartPage))
         button1.pack()

""" class Screen:
    #class variables
    #title, condition{}, questions[]
    def __init__(self, text):
        self.text = text """


""" class Backend:
    def getInitialScreen(self):
        #returns Screen object
        q1 = Question("What is your name", "string", "")
        q2 = Question("Are you old?", "yn", "")
        qarray = [q1, q2]
        tempscreen = Screen("First Screen", "none", qarray)
        return tempscreen

    def getNextScreen(self, screen):
        #returns Screen object
        #returns null if there are no more screens
        q1 = Question("What is your age", "string", "")
        q2 = Question("Are you young?", "yn", "")
        qarray = [q1, q2]
        tempscreen = Screen("Second Screen", "none", qarray)
        return tempscreen

    def getPrevScreen(self, screen):
        return self.getInitialScreen()
 """
app = PatientPrognosisBot()
app.mainloop()