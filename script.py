from tkinter import *
import random as r

with open("picList.txt", "r") as f:
    data = [x.strip().split(";")[1].upper() for x in f.readlines()]

dir = "assets/" 

class application(Tk):

    #statistics
    with open("currentLevel.txt", "r") as f:
        dataStrip = f.read().split(";")
        curLVL = int(dataStrip[0])
        curCoins = int(dataStrip[1])

    letters_typed = 0
    word = ""

    hint_index = 0
    curHint = ""

    def __init__(self):
        super().__init__()
        self.init_window()

    def init_window(self):
        self.title("4 Pics - 1 Word!")
        self.geometry("450x600")

        #Body Frame
        background = Frame(self, height=600, width=450, bg="#212531")
        background.pack(fill=BOTH)

        self.header()
        self.body()

    def header(self):
        #HEADER ELEMENTS
        self.Header = Frame(self, height=50, width=450, bg="#4471C4")
        self.Header.place(x=225, y=20, anchor=N)

        #Statistics
        lvlLabel = Label(self.Header, text=f"Level: {self.curLVL + 1}", font="Arial 22 bold", fg="white", bg="#4471C4", width=8)
        lvlLabel.place(x=0, y=25, anchor=W)

        coinsLabel = Label(self.Header, text=self.curCoins, font="Arial 22 bold", fg="white", bg="#4471C4", width=3)
        coinsLabel.place(x=420, y=25, anchor=E)

        self.coins = PhotoImage(file=f"{dir}coins.png")
        self.coins = self.coins.subsample(13)
        coinsPic = Label(self.Header, image=self.coins, bg="#4471C4")
        coinsPic.place(x=315, y=0)

    def body(self):
        #BODY ELEMENTS
        try:
            data[self.curLVL]
        except IndexError:
            self.congratulations = Frame(self, height=600, width=450, bg="green")
            self.congratulations.place(x=0, y=0)

            self.cong = Label(self.congratulations, text="You Win!", fg="white", bg="green", font="ArialBlack 30 bold")
            self.cong.place(x=225, y=300, anchor=CENTER)
            
            self.nwGmBut = Button(self.congratulations, text="New Game?", bg="black", fg ="white",font="ArialBlack 20 bold", borderwidth=0, command=self.newGame)
            self.nwGmBut.place(x=225, y=500, anchor=CENTER)
            
        else:
            #Pictures
            self.picture = PhotoImage(file=f"pics/{data[self.curLVL]}.png") #300x300
            self.labelpic = Label(self, image=self.picture, borderwidth=0)
            self.labelpic.place(x=225, y=90, anchor=N) 

            #Keyboard
            self.keyboardFrame = Frame(self, bg="red")
            self.keyboardFrame.place(x=225, y=480, anchor=N)

            self.key = PhotoImage(file=f"{dir}blank.png")

            word = data[self.curLVL]
            letters = word + "".join([chr(r.randint(65,90)) for x in range(12-len(word))])
            kblist = "".join(r.sample(letters, len(letters)))

            style = "ArialBlack 20 bold"
            self.kb_but = [Button(self.keyboardFrame, text=i, image=self.key, font=style,
                            bg="#212531", fg ="black", borderwidth=0, compound="center", 
                            command=lambda i=i, j=j: self.countChar(i, j)) 
                            for i, j in zip(kblist, range(12))]
            
            for i in range(12):
                self.kb_but[i].grid(row=i // 6, column=i % 6)

            #Hint and Pass Button
            self.hint = PhotoImage(file=f"{dir}hint.png")
            self.Pass = PhotoImage(file=f"{dir}Pass.png")

            self.genFrame = Frame(self, bg="red")
            self.genFrame.place(x=375, y=480, anchor=NW)

            self.hintBut = Button(self.genFrame, image=self.hint, bg="#212531", fg ="black", borderwidth=0, command=self.hintFn)
            self.PassBut = Button(self.genFrame, image=self.Pass, bg="#212531", fg ="black", borderwidth=0, command=self.PassFn)

            self.hintBut.grid(row=0, column=0)
            self.PassBut.grid(row=1, column=0)

            #Letter Slots
            self.key1 = PhotoImage(file=f"{dir}blankText.png")

            self.slotsFrame = Frame(self, bg="#212531")
            self.slotsFrame.place(x=225, y=410, anchor=N)
            self.slots = [Label(self.slotsFrame, image=self.key1, borderwidth=0, bg="#212531", 
                                text=" ", font=style, fg="white", compound="center") for i in range(len(data[self.curLVL]))]

            for i in range(len(self.slots)):
                self.slots[i].grid(row=0, column=i, padx=1)
                
            #Reset Progress Button
            if self.curLVL>0:
                self.Reset = PhotoImage(file=f"{dir}Restart.png")
                self.rstFrame = Frame(self, bg="red")
                self.rstFrame.place(x=10, y=80, anchor=NW)
                self.rstBut = Button(self.rstFrame, image=self.Reset, bg="#212531", fg ="black", borderwidth=0, command=self.oneBack)
                self.rstBut.grid(row=0, column=0)

    def newGame(self):
        self.curLVL = 0
        self.curCoins = 100
        
        self.reset()
        self.clearOUT()
        self.congratulations.destroy()

    def oneBack(self):
        if self.curLVL>0:
            self.curLVL -= 1
            self.curCoins -= 10
                
            self.reset()
            self.clearOUT()
    
    def clearOUT(self):
        with open("currentLevel.txt","w") as f:
            f.write(f"{self.curLVL};{self.curCoins}")

        self.Header.destroy()
       
        self.labelpic.destroy()
        self.keyboardFrame.destroy()
        self.slotsFrame.destroy()

        self.header()
        self.body()
    
    def PassFn(self):
        if (self.curCoins - 10) >= 0:
            self.curCoins -= 10
            self.curLVL+=1

            self.curHint = ""
            self.hint_index = 0
            self.reset()
            self.clearOUT()

    def hintFn(self):

        if (self.curCoins - 2) >= 0 and self.hint_index < len(data[self.curLVL]):
            self.curCoins -= 2

            with open("currentLevel.txt","w") as f:
                f.write(f"{self.curLVL};{self.curCoins}")

            self.Header.destroy()
            self.header()

            self.curHint += data[self.curLVL][self.hint_index]
            self.slots[self.hint_index].config(text=data[self.curLVL][self.hint_index], fg="#A2FF7C")
            self.hint_index += 1

    def reset(self):
        self.letters_typed = 0
        self.word = ""            

    def countChar(self, char, ind):
        if self.letters_typed < len(data[self.curLVL]) and self.kb_but[ind].cget("fg") == "black":
  
            self.slots[self.letters_typed].config(text=char, fg="white")
            self.letters_typed+=1
            self.word+=char
            self.kb_but[ind].config(fg="#ADADAD")

            if self.letters_typed == len(data[self.curLVL]):

                if self.word == data[self.curLVL]:
                    self.curLVL += 1
                    self.curCoins += 10
                    self.curHint = ""
                    self.hint_index = 0

                    self.reset()
                    print("Success")
                    self.clearOUT()

                else:
                    print(self.word, data[self.curLVL])
                    #reset
                    for i in range(12):
                        if i < len(data[self.curLVL]): 
                            if i < len(self.curHint):
                                self.slots[i].config(text=self.curHint[i], fg="#A2FF7C")
                            else:
                                self.slots[i].config(text=" ")

                        self.kb_but[i].config(fg="black")
                    self.reset()

def main():
    root = application()
    root.mainloop()

if __name__== "__main__":
    main()
