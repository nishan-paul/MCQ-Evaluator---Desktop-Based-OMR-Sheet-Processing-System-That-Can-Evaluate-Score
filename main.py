import tkinter.ttk
from tkinter import *
from tkinter.ttk import *
from developer_functions_3 import *

root = tkinter.Tk()
root.title("MCQ-EVALUATOR")
root.geometry("1000x400")

T = tkinter.Text(root, height=3, width=400, font=("Times", 15))
T.tag_configure("center", justify='center')
T.insert(tkinter.END,
         "WELCOME TO MCQ-EVALUATOR.\n SELECT ANY FOLDER FROM YOUR COMPUTER TO EVALUATE THE ANSWER SHEETS OF STUDENTS.\n YOU CAN SET SOLUTION OF QUESTION PAPER IN EXCEL FILE.")
T.tag_add("center", "1.0", "end")
T.pack(pady=50)

photo = PhotoImage(file="images/button_image.png")
btn = Button(root, image=photo, command=browse_folder)
btn.pack(pady=50)

root.mainloop()
cursor.close()
connection.close()
