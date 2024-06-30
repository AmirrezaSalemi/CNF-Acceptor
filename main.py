from tkinter import *
from tkinter import filedialog
from tkinter import colorchooser

dic = {

}


def setBackGround():
    color = colorchooser.askcolor()
    if color[1]:
        window.config(background=color[1])


def open_grammar():
    file_path = filedialog.askopenfilename(filetypes=[("txt files", "*.txt")])
    if file_path:
        global Variables
        global Terminals
        global Start_Var
        global rules
        global dic
        dic.clear()
        Guide.config(state=NORMAL)
        Answer.config(state=NORMAL)
        entry.delete(0, END)
        Answer.delete(1.0, END)
        Guide.delete('1.0', END)
        with open(file_path, 'r') as file:
            txt = file.readlines()

        Variables = txt[0].strip().split('Variables: ')
        Variables.remove(Variables[0])
        Variables = Variables[0].split(', ')

        Terminals = txt[1].strip().split('Terminals: ')
        Terminals.remove(Terminals[0])
        Terminals = Terminals[0].split(', ')

        Start_Var = txt[2].strip().split('Start_Var: ')
        Start_Var.remove(Start_Var[0])
        Start_Var = str(Start_Var[0])

        rules = {

        }

        for NON_TERMINAL in Variables:
            rules[NON_TERMINAL] = []

        for i in range(4, len(txt)):
            spl = txt[i].strip().split(', ')
            rules[spl[0]].append(spl[1])
        emptys = []
        for NoneTerminal in rules:
            if len(rules[NoneTerminal]) == 0:
                emptys.append(NoneTerminal)
        for i in emptys:
            rules.pop(i)

        Guide.insert(END, 'NoneTerminals -> ', 'violet')
        Guide.insert(END, str(Variables) + '\n', 'blue')

        Guide.insert(END, 'Terminals -> ', 'violet')
        Guide.insert(END, str(Terminals) + '\n', 'blue')

        Guide.insert(END, 'StartVariable -> ', 'violet')
        Guide.insert(END, str(Start_Var) + '\n', 'blue')

        Guide.insert(END, 'Rules -> ', 'violet')
        Guide.insert(END, str(rules) + '\n', 'blue')
        Guide.config(state=DISABLED)
        Answer.config(state=DISABLED)


def check(event):
    Answer.config(state=NORMAL)
    Answer.delete(1.0, END)
    for symbol in entry.get():
        if symbol not in Terminals:
            Symbol_Error()
            return False
        else:
            continue
    CYK()
    Answer.config(state=DISABLED)


def Symbol_Error():
    Answer.insert(END, 'symbol isn\'t in Terminals.')
    Answer.config(fg='red')


def CYK():
    n = len(entry.get())
    inp = entry.get()
    if inp in dic:
        if dic[inp]:
            Answer.insert(END, 'The input string is accepted.')
            Answer.config(fg='green')
        else:
            Answer.insert(END, 'The input string is not accepted.')
            Answer.config(fg='red')

    elif n > 0:
        table = [[set() for tmp in range(n)] for tmp in range(n)]

        for i in range(n):
            for rule in rules:
                if inp[i] in rules[rule]:
                    table[i][i].add(rule)

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                for k in range(i, j):
                    for rule in rules:
                        for production in rules[rule]:
                            if len(production) == 2 and production[0] in table[i][k] and production[1] in table[k + 1][j]:
                                table[i][j].add(rule)
        if Start_Var in table[0][n - 1]:
            dic[inp] = True
            Answer.insert(END, 'The input string is accepted.')
            Answer.config(fg='green')
        else:
            dic[inp] = False
            Answer.insert(END, 'The input string is not accepted.')
            Answer.config(fg='red')


with open('GrammarTest.txt', 'r') as file:
    txt = file.readlines()

Variables = txt[0].strip().split('Variables: ')
Variables.remove(Variables[0])
Variables = Variables[0].split(', ')

Terminals = txt[1].strip().split('Terminals: ')
Terminals.remove(Terminals[0])
Terminals = Terminals[0].split(', ')

Start_Var = txt[2].strip().split('Start_Var: ')
Start_Var.remove(Start_Var[0])
Start_Var = str(Start_Var[0])

rules = {

}

for NON_TERMINAL in Variables:
    rules[NON_TERMINAL] = []

for i in range(4, len(txt)):
    spl = txt[i].strip().split(', ')
    rules[spl[0]].append(spl[1])
emptys = []
for NoneTerminal in rules:
    if len(rules[NoneTerminal]) == 0:
        emptys.append(NoneTerminal)
for i in emptys:
    rules.pop(i)

window = Tk()
window.geometry('500x300')
window.resizable(width=False, height=False)
window.title('CYK')
window.configure(background='Dark Gray')

MenuBar = Menu(window)
MenuBar.add_cascade(label='Open File', command=open_grammar)
MenuBar.add_cascade(label='BackGround Color', command=setBackGround)
window.config(menu=MenuBar)

entry = Entry(window, width=100, fg='black', bg='white')
entry.pack(padx=10, pady=(10, 25))

Answer = Text(window, width=50, height=0)
Answer.pack()
Answer.config(state=DISABLED)

Guide = Text(window)
Guide.pack(padx=10, pady=10)
Guide.tag_config('blue', foreground='blue')
Guide.tag_config('violet', foreground='purple')

Guide.insert(END, 'NoneTerminals -> ', 'violet')
Guide.insert(END, str(Variables) + '\n', 'blue')

Guide.insert(END, 'Terminals -> ', 'violet')
Guide.insert(END, str(Terminals) + '\n', 'blue')

Guide.insert(END, 'StartVariable -> ', 'violet')
Guide.insert(END, str(Start_Var) + '\n', 'blue')

Guide.insert(END, 'Rules -> ', 'violet')
Guide.insert(END, str(rules) + '\n', 'blue')

Guide.config(state=DISABLED)

entry.bind('<KeyRelease>', check)

mainloop()
