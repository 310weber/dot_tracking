import tkinter as tk
import threading
from time import sleep

class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def increment_var(self):
        data.var += 1

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title("GUI Window")
        self.root.geometry("200x100")

        label = tk.Label(self.root, text="Click the Button")
        label.pack()

        btn1 = tk.Button(self.root, text = "Increment", fg = "green",\
                              command = self.increment_var)
        btn1.pack()
        
        btn2 = tk.Button(self.root, text = "Reset", fg = "red",\
                              command = data.reset)
        btn2.pack()
        self.root.mainloop()


class Data():       # Class to hold data passed between threads

    def __init__(self):
        self.var = 0

    def reset(self):
        self.var = 0

data = Data()
app = App()
print('Now we can continue running code while mainloop runs!')

# Anything you want to run after the window opens here:
for i in range(100):
    print(data.var)
    sleep(1)