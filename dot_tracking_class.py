import sys
import cv2
from datetime import datetime
import csv
import msvcrt
class DotTracking():
    def __init__(self, fileName):
        self.fileName = fileName
        # user = input("Enter user name: ")
        # self.csv_filename = user + ' ' + \
        #                datetime.strftime(datetime.now(), "%y%m%d%H%M%S") + '.csv'
        # self.out_filename = user + ' ' + \
        #                datetime.strftime(datetime.now(), "%y%m%d%H%M%S") + '.mp4'
        # f = open(self.csv_filename, "w+")
        # f.write("Time, X, Y, Delta X (px), Delta Y(px), Delta X (mmm), Delta Y (mm), Delta (mm), Speed (mm/s)\n")
        # f.close()
        self.colour = 'green'
        self.show_tracker = True
        self.last_position = (0, 0)
        self.last_time = 0
        self.x_scaling = 17.786
        self.y_scaling = 17.786
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scaling = 0.5
        self.font_thickness = 1
        self.min_contour_size = 4000
        self.no_contour = False
        self.test = False
        self.out_filename = ""
        if self.colour == 'green':
            self.h_low = 45
            self.h_high = 85
            self.s_low = 90
            self.s_high = 255
            self.v_low = 90
            self.v_high = 255
        elif colour == 'yellow':
            self.h_low = 18
            self.h_high = 32
            self.s_low = 125
            self.s_high = 255
            self.v_low = 150
            self.v_high = 255
        else:
            self.h_low = 40
            self.h_high = 90
            self.s_low = 50
            self.s_high = 255
            self.v_low = 50
            self.v_high = 255

    # if no commandline arguments are sent, load the default video
    # if len(sys.argv) == 1:
    #     print("Please enter a filename.")
    #     sys.argv = sys.argv + ['moving_colours.mp4']

    # get username and set output CSV and video filenames
    # user = input("Enter user name: ")
    # csv_filename = user + ' ' + \
    #                datetime.strftime(datetime.now(), "%y%m%d%H%M%S") + '.csv'
    # out_filename = user + ' ' + \
    #                datetime.strftime(datetime.now(), "%y%m%d%H%M%S") + '.mp4'



    # For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255].


    def Start(self):
        # setup video capture and output files
        cap = cv2.VideoCapture(self.fileName)

        if self.test == False:
            user = input("Enter user name: ")
            self.csv_filename = user + ' ' + \
                           datetime.strftime(datetime.now(), "%y%m%d%H%M%S") + '.csv'
            self.out_filename = user + ' ' + \
                           datetime.strftime(datetime.now(), "%y%m%d%H%M%S") + '.mp4'
            f = open(self.csv_filename, "w+")
            f.write("Time, X, Y, Delta X (px), Delta Y(px), Delta X (mmm), Delta Y (mm), Delta (mm), Speed (mm/s)\n")
            f.close()

        if not cap.isOpened():
            print("Error opening file.")

        else:
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float
            frame_rate = cap.get(cv2.CAP_PROP_FPS)

            out = cv2.VideoWriter(self.out_filename,
                                  cv2.VideoWriter_fourcc('m', 'p', '4', 'a'),
                                  frame_rate, (frame_width, frame_height))

            # Process the video
            while(cap.isOpened()):
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    key = key.decode("utf-8")
                    if key == 'x':
                        print ("Aborted.")
                        break

                # capture frame and get frame time in milliseconds
                ret, frame = cap.read()
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                frametime = cap.get(cv2.CAP_PROP_POS_MSEC)

                # convert to HSV colour space and blur to reduce noise
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                frame_out = frame
                frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                frame_hsv = cv2.blur(frame_hsv, (5, 5))
                frame_h, frame_s, frame_v = cv2.split(frame_hsv)

                # threshold and AND to separate yellow pixels
                thresh_h = cv2.inRange(frame_h, self.h_low, self.h_high)
                thresh_s = cv2.inRange(frame_s, self.s_low, self.s_high)
                thresh_v = cv2.inRange(frame_v, self.v_low, self.v_high)
                tracker = cv2.bitwise_and(thresh_h, thresh_s)
                tracker = cv2.bitwise_and(tracker, thresh_v)

                # find contours around objects (white space) in tracker image
                contours, hierarchy = cv2.findContours(tracker, cv2.RETR_TREE,
                                                       cv2.CHAIN_APPROX_SIMPLE)

                tracker = cv2.cvtColor(tracker, cv2.COLOR_GRAY2RGB) # turn tracker into RGB for overlay graphics
                if len(contours) >= 1:
                    contours = sorted(contours, key=cv2.contourArea, reverse=True)
                    cont = contours[0]  # select only the largest contour

                    # draw circle around spot in output frame
                    if cv2.contourArea(cont) > self.min_contour_size:
                        ((cx, cy), r) = cv2.minEnclosingCircle(cont)
                        position = (int(cx), int(cy))
                        cv2.circle(frame_out, position, 1, (0, 0, 255), 3)
                        cv2.circle(frame_out, position, int(r), (0, 0, 128), 3)
                        cv2.circle(tracker, position, 1, (0, 0, 255), 3) # add dot to center of tracked object in output video file
                        cv2.circle(tracker, position, int(r), (0, 0, 255), 2)
                        #no_contour = False
                    else:
                        position = (0, 0)  # if no contour is found
                        no_contour = True
                else:
                    position = (0, 0)   # if no contour is found
                    no_contour = True

                if (self.last_position[0] ==0 and self.last_position[1] == 0) or (position[0] == 0 and position[1]==0): # check to see if tracked object was/is outside FOV
                    delta_px = (0,0)
                else:
                    delta_px = (position[0] - self.last_position[0], position[1] - self.last_position[1])
                delta_mm = (delta_px[0]/self.x_scaling, delta_px[1]/self.y_scaling)
                delta_pos = pow((pow(delta_mm[0], 2) + pow(delta_mm[1], 2)), 0.5)
                delta_time = frametime - self.last_time
                if delta_time > 0:
                    speed = delta_pos / delta_time * 1000
                else:
                    speed = 0

                if self.no_contour == False:
                    speed = int(speed)
                    (text_width, text_height) = cv2.getTextSize(str(speed), self.font, self.font_scaling, thickness=self.font_thickness)[0]
                    cv2.putText(tracker, str(speed), (60 - text_width, 15), self.font, fontScale=self.font_scaling, color=(0, 0, 255), thickness=self.font_thickness)
                    cv2.putText(tracker, 'mm/s', (70, 15), self.font, fontScale=self.font_scaling, color=(0, 0, 255), thickness=self.font_thickness)
                else:
                    cv2.putText(tracker, 'No object', (70, 15), self.font, fontScale=self.font_scaling, color=(0, 0, 255), thickness=self.font_thickness)

                cv2.putText(tracker, 'H:' + str(self.h_low) + ':' + str(self.h_high), (550, 15), self.font, fontScale=self.font_scaling, color=(0, 0, 255), thickness=self.font_thickness)
                cv2.putText(tracker, 'S:' + str(self.s_low) + ':' + str(self.s_high), (550, 30), self.font, fontScale=self.font_scaling, color=(0, 0, 255), thickness=self.font_thickness)
                cv2.putText(tracker, 'V:' + str(self.v_low) + ':' + str(self.v_high), (550, 45), self.font, fontScale=self.font_scaling, color=(0, 0, 255), thickness=self.font_thickness)
                cv2.putText(tracker, 'Size:' + str(self.min_contour_size), (550, 60), self.font, fontScale=self.font_scaling, color=(0, 0, 255), thickness=self.font_thickness)

                # add frame timestamp to tracker
                (text_width, text_height) = cv2.getTextSize(str(int(frametime)), self.font, self.font_scaling, thickness=self.font_thickness)[0]
                cv2.putText(tracker, str(int(frametime)), (60 - text_width, 30), self.font, fontScale=self.font_scaling, color=(0, 0, 255), thickness=self.font_thickness)
                cv2.putText(tracker, 'ms', (70, 30), self.font, fontScale=self.font_scaling, color=(0, 0, 255), thickness=self.font_thickness)


                self.last_position = position
                self.last_time = frametime

                if self.show_tracker:
                    cv2.imshow("Tracking image", tracker)

                # write data to CSV file
                if self.test == False:
                    with open(self.csv_filename, 'a', newline='') as writefile:
                        writer = csv.writer(writefile)
                        if self.no_contour == False:
                            writer.writerow((frametime,) + position + delta_px + delta_mm + (delta_pos,) + (speed,))
                        else:
                            writer.writerow((frametime,))
                    writefile.close()
                    out.write(tracker)
                no_contour = False

                if ret:
                    cv2.imshow('output', frame_out)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                else:
                    print("Break")
                    break

            cap.release()
            out.release()
            cv2.destroyAllWindows()
