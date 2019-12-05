import sys
import threading
from tkinter import Frame, Tk, Scale, HORIZONTAL, Label, Button, simpledialog
from dot_tracking_class import DotTracking


class MainGUI():
    def __init__(self, parent, fileName):
        self.DotTracking = DotTracking(fileName)
        frame = Frame(parent)
        frame.pack()
        #HUE
        self.label1 = Label(frame, text="Hue Min:")
        self.label1.grid(row=0, column=1)
        self.Hue_min = Scale(frame, from_=0, to=180, orient=HORIZONTAL, command=self.sliderUpdateMin)
        self.Hue_min.set(45)
        self.Hue_min.grid(row=0, column=2)
        self.label2 = Label(frame, text="Hue Max:")
        self.label2.grid(row=1, column=1)
        self.Hue_max = Scale(frame, from_=0, to=180, orient=HORIZONTAL, command=self.sliderUpdateMax)
        self.Hue_max.set(85)
        self.Hue_max.grid(row=1, column=2)
        #SAT
        self.label3 = Label(frame, text="Sat Min:")
        self.label3.grid(row=2, column=1)
        self.Sat_min = Scale(frame, from_=0, to=255, orient=HORIZONTAL, command=self.sliderUpdateMin)
        self.Sat_min.set(80)
        self.Sat_min.grid(row=2, column=2)
        self.label4 = Label(frame, text="Sat Max:")
        self.label4.grid(row=3, column=1)
        self.Sat_max = Scale(frame, from_=0, to=255, orient=HORIZONTAL, command=self.sliderUpdateMax)
        self.Sat_max.set(255)
        self.Sat_max.grid(row=3, column=2)
        #VAL
        self.label5 = Label(frame, text="Val Min:")
        self.label5.grid(row=4, column=1)
        self.Val_min = Scale(frame, from_=0, to=255, orient=HORIZONTAL, command=self.sliderUpdateMin)
        self.Val_min.set(80)
        self.Val_min.grid(row=4, column=2)
        self.label6 = Label(frame, text="Val Max:")
        self.label6.grid(row=5, column=1)
        self.Val_max = Scale(frame, from_=0, to=255, orient=HORIZONTAL, command=self.sliderUpdateMax)
        self.Val_max.set(255)
        self.Val_max.grid(row=5, column=2)
        #SIZE
        self.label7 = Label(frame, text="Size:")
        self.label7.grid(row=6, column=1)
        self.Size_setting = Scale(frame, from_= 1000, to = 7000, orient=HORIZONTAL, command=self.updateSize)
        self.Size_setting.set(5000)
        self.Size_setting.grid(row = 6, column = 2)
        #Buttons
        self.TestButton = Button(frame, text="Test", command=self.runTest)
        self.TestButton.grid(row=7, column=1)
        self.StartButton = Button(frame, text="Run", command=self.runAnalyze)
        self.StartButton.grid(row=7, column=2)
        self.LiveButton = Button(frame, text="Live", command=self.LiveStream)
        self.LiveButton.grid(row=7, column=3)
        # start_thread = threading.Thread(target=self.DotTracking.Start)
        # start_thread.start()
        #self.DotTracking.Start()

    def sliderUpdateMax(self, *args):
        if self.Hue_max.get() < self.Hue_min.get():
            self.Hue_max.set(self.Hue_min.get())
        if self.Sat_max.get() < self.Sat_min.get():
            self.Sat_max.set(self.Sat_min.get())
        if self.Val_max.get() < self.Val_min.get():
            self.Val_max.set(self.Val_min.get())
        self.updateHSV()

    def sliderUpdateMin(self, *args):
        if self.Hue_min.get() > self.Hue_max.get():
            self.Hue_min.set(self.Hue_max.get())
        if self.Sat_min.get() > self.Sat_max.get():
            self.Sat_min.set(self.Sat_max.get())
        if self.Val_min.get() > self.Val_max.get():
            self.Val_min.set(self.Val_max.get())
        self.updateHSV()

    def runTest(self, *args):
        self.DotTracking.test = True
        start_thread = threading.Thread(target=self.DotTracking.Start)
        start_thread.start()

    def runAnalyze(self, *args):
        self.DotTracking.test = False
        self.DotTracking.user = simpledialog.askstring("Input", "Enter user name:", parent=parent)
        start_thread = threading.Thread(target=self.DotTracking.Start)
        start_thread.start()

    def updateSize(self, *args):
        self.DotTracking.min_contour_size = self.Size_setting.get()

    def updateHSV(self, *args):
        self.DotTracking.h_low = self.Hue_min.get()
        self.DotTracking.h_high = self.Hue_max.get()
        self.DotTracking.s_low = self.Sat_min.get()
        self.DotTracking.s_high = self.Sat_max.get()
        self.DotTracking.v_low = self.Val_min.get()
        self.DotTracking.v_high = self.Val_max.get()

    def LiveStream(self, *args):
        self.DotTracking.live = True
        start_thread = threading.Thread(target=self.DotTracking.Start)
        start_thread.start()
        self.DotTracking.live = False

if __name__ == '__main__':
    parent = Tk()
    GUI = MainGUI(parent, sys.argv[1].strip())
    parent.mainloop()
    #GUI.DotTracking.Start()




























# from HSV_sliders import Ui_Form
# import PyQt5.QtCore as __PyQt5_QtCore
# import PyQt5.QtGui as __PyQt5_QtGui
# from PyQt5 import QtWidgets
# import sys
#
# class MainTrackingGUI(Ui_Form, QtWidgets.QMainWindow):
#     def __init__(self, parent=None):
#         QtWidgets.QMainWindow().__init__(self, parent)
#         self.setupUi(self)
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     ui = MainTrackingGUI()
#     ui.show()
#     sys.exit(app.exec_())