import sys
from tkinter import Frame, Tk, Scale, HORIZONTAL
from dot_tracking_class import DotTracking


class MainGUI():
    def __init__(self, parent, fileName):
        self.DotTracking = DotTracking(fileName)
        frame = Frame(parent)
        frame.pack()
        self.HSV_min = Scale(frame, from_=0, to=180, orient=HORIZONTAL, command=self.sliderUpdate)
        self.HSV_min.pack()
        self.HSV_max = Scale(frame, from_=0, to=180, orient=HORIZONTAL, command=self.sliderUpdate)
        self.HSV_max.pack()
        self.DotTracking.Start()

    def sliderUpdate(self, *args):
        self.validateSliderBars()
        self.DotTracking.h_low = self.HSV_min.get()
        self.DotTracking.h_high = self.HSV_max.get()

    def validateSliderBars(self):
        if self.HSV_min.get() > self.HSV_max.get():
            self.HSV_min.set(self.HSV_max.get())
        if self.HSV_max.get() < self.HSV_min.get():
            self.HSV_max.set(self.HSV_min.get())

if __name__ == '__main__':
    parent = Tk()
    GUI = MainGUI(parent, sys.argv[1].strip())
    parent.mainloop()



























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