#get greeting

#click next

#click back

import tkinter as tk

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
        self.page_number=1
        self.buildPage()


    def buildPage(self):
        if self.page_number == 1:
            label = tk.Label(self, text="Patent Prognosis BOT Start Page", font=LARGE_FONT)
            label.pack(pady=10, padx=10)
            self.widgets.append(label)

            button1 = tk.Button(self, text="Next", 
                                command=lambda: self.nextPage())
            button1.pack()
            self.widgets.append(button1)
        else:
            label = tk.Label(self, text="Next page", font=LARGE_FONT)
            label.pack(pady=10, padx=10)
            self.widgets.append(label)

            button1 = tk.Button(self, text="Next", 
                                command=lambda: self.nextPage())
            button1.pack()
            self.widgets.append(button1)
        

    def destroyPage(self):
        for x in self.widgets:
            x.pack_forget()
        self.widgets=[]

    def nextPage(self):
        self.destroyPage()
        self.page_number=self.page_number+1
        self.buildPage()
        

class PageOne(tk.Frame):

     def __init__(self, parent, controller):
         tk.Frame.__init__(self, parent)
         label = tk.Label(self, text="Page One", font=LARGE_FONT)
         label.pack(pady=10, padx=10)

         button1 = tk.Button(self, text="back", 
                            command=lambda: controller.show_frame(StartPage))
         button1.pack()


app = PatientPrognosisBot()
app.mainloop()