#get greeting

#click next

#click back

import tkinter as tk
#import read_sample

LARGE_FONT= ("Verdana", 12)

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
            label = tk.Label(self, text="Patent Prognosis BOT Start Page", font=LARGE_FONT)
            label.pack(pady=10, padx=10)
            self.widgets.append(label)

            button1 = tk.Button(self, text="Next", 
                                command=lambda: self.nextPage(screen))
            button1.pack()
            self.widgets.append(button1)
        else:

            #temp1screen = self.backend.getInitialScreen()

            label = tk.Label(self, text= screen.text, font=LARGE_FONT)
            label.pack(pady=10, padx=10)
            self.widgets.append(label)

            button1 = tk.Button(self, text="Next", 
                                command=lambda: self.nextPage(screen))
            button1.pack()
            self.widgets.append(button1) """
        current_screen = screen
        label = tk.Label(self, text=current_screen.text, font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.widgets.append(label)
        button1 = tk.Button(self, text="Next", 
                                command=lambda: self.nextPage(current_screen))
        button1.pack()
        self.widgets.append(button1)

        
    def destroyPage(self):
        for x in self.widgets:
            x.pack_forget()
        self.widgets=[]

    def nextPage(self, screen):
        self.destroyPage()
        #self.page_number=self.page_number+1
        self.buildPage(self.backend.getNextScreen(screen))


class PageOne(tk.Frame):

     def __init__(self, parent, controller):
         tk.Frame.__init__(self, parent)
         label = tk.Label(self, text="Page One", font=LARGE_FONT)
         label.pack(pady=10, padx=10)

         button1 = tk.Button(self, text="back", 
                            command=lambda: controller.show_frame(StartPage))
         button1.pack()

class Screen:
    #class variables
    #title, condition{}, questions[]
    def __init__(self, text):
        self.text = text


class Backend:
    def getInitialScreen(self):
        #returns Screen object
        tempscreen = Screen("monkey")
        return tempscreen

    def getNextScreen(self, screen):
        #returns Screen object
        #returns null if there are no more screens
        tempscreen = Screen("donkey")
        return tempscreen

    #def getPrevScreen(self, screen):
        #returns Screen object 

app = PatientPrognosisBot()
app.mainloop()