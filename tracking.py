import sys
import threading
from tkinter import Frame, Tk, Scale, HORIZONTAL, Label
from dot_tracking_class import DotTracking


class MainGUI():
    def __init__(self, parent, fileName):
        self.DotTracking = DotTracking(fileName)
        frame = Frame(parent)
        frame.pack()
        self.label1 = Label(frame, text="Hue Min:")
        #self.label1.pack()
        self.label1.grid(row=0, column=1)
        self.HSV_min = Scale(frame, from_=0, to=180, orient=HORIZONTAL, command=self.sliderUpdateMin)
        self.HSV_min.set(40)
        self.HSV_min.grid(row=0, column=2)
        self.label2 = Label(frame, text="Hue Max:")
        self.label2.grid(row=1, column=1)
        self.HSV_max = Scale(frame, from_=0, to=180, orient=HORIZONTAL, command=self.sliderUpdateMax)
        self.HSV_max.set(80)
        self.HSV_max.grid(row=1, column=2)
        start_thread = threading.Thread(target=self.DotTracking.Start)
        start_thread.start()
        #self.DotTracking.Start()

    def sliderUpdateMax(self, *args):
        if self.HSV_max.get() < self.HSV_min.get():
            self.HSV_max.set(self.HSV_min.get())
        self.updateHSV()

    def sliderUpdateMin(self, *args):
        if self.HSV_min.get() > self.HSV_max.get():
            self.HSV_min.set(self.HSV_max.get())
        self.updateHSV()

    def updateHSV(self):
        self.DotTracking.h_low = self.HSV_min.get()
        self.DotTracking.h_high = self.HSV_max.get()

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