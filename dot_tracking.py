import sys
import cv2
from datetime import datetime
import csv
import msvcrt

colour = 'green'
show_tracker = True
last_position = (0, 0)
last_time = 0
x_scaling = 16.254
y_scaling = 16.254
font = cv2.FONT_HERSHEY_SIMPLEX
font_scaling = 0.5
font_thickness = 1

# if no commandline arguments are sent, load the default video
if len(sys.argv) == 1:
    print("Please enter a filename.")
    sys.argv = sys.argv + ['moving_colours.mp4']

# get username and set output CSV and video filenames
user = input("Enter user name: ")
csv_filename = user + ' ' + \
               datetime.strftime(datetime.now(), "%y%m%d%H%M%S") + '.csv'
out_filename = user + ' ' + \
               datetime.strftime(datetime.now(), "%y%m%d%H%M%S") + '.mp4'

f = open(csv_filename, "w+")
f.write("Time, X, Y, Delta X (px), Delta Y(px), Delta X (mmm), Delta Y (mm), Delta (mm), Speed (mm/s)\n")
f.close()

# For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255].
if colour == 'green':
    h_low = 45
    h_high = 85
    s_low = 80
    s_high = 255
    v_low = 80
    v_high = 255
elif colour == 'yellow':
    h_low = 18
    h_high = 32
    s_low = 125
    s_high = 255
    v_low = 150
    v_high = 255
else:
    h_low = 40
    h_high = 90
    s_low = 50
    s_high = 255
    v_low = 50
    v_high = 255

# setup video capture and output files
cap = cv2.VideoCapture(sys.argv[1])

if not cap.isOpened():
    print("Error opening file.")

else:
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float
    frame_rate = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(out_filename,
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
        thresh_h = cv2.inRange(frame_h, h_low, h_high)
        thresh_s = cv2.inRange(frame_s, s_low, s_high)
        thresh_v = cv2.inRange(frame_v, v_low, v_high)
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
            ((cx, cy), r) = cv2.minEnclosingCircle(cont)
            position = (int(cx), int(cy))
            cv2.circle(frame_out, position, 1, (0, 0, 255), 3)
            cv2.circle(frame_out, position, int(r), (0, 0, 128), 3)
            cv2.circle(tracker, position, 1, (0, 0, 255), 3) # add dot to center of tracked object in output video file
            cv2.circle(tracker, position, int(r), (0, 0, 255), 2)
        else:
            position = (0, 0)   # if no contour is found

        if last_position[0] ==0 and last_position[1] == 0:
            delta_px = (0,0)
        else:
            delta_px = (position[0] - last_position[0], position[1] - last_position[1])
        delta_mm = (delta_px[0]/x_scaling, delta_px[1]/y_scaling)
        delta_pos = pow((pow(delta_mm[0], 2) + pow(delta_mm[1], 2)), 0.5)
        delta_time = frametime - last_time
        if delta_time > 0:
            speed = delta_pos / delta_time * 1000
        else:
            speed = 0

        speed = int(speed)
        (text_width, text_height) = cv2.getTextSize(str(speed), font, font_scaling, thickness=font_thickness)[0]
        cv2.putText(tracker, str(speed), (60 - text_width, 15), font, fontScale=font_scaling, color=(0, 0, 255), thickness=font_thickness)
        cv2.putText(tracker, 'mm/s', (70, 15), font, fontScale=font_scaling, color=(0, 0, 255), thickness=font_thickness)
        (text_width, text_height) = cv2.getTextSize(str(int(frametime)), font, font_scaling, thickness=font_thickness)[0]
        cv2.putText(tracker, str(int(frametime)), (60 - text_width, 30), font, fontScale=font_scaling, color=(0, 0, 255), thickness=font_thickness)
        cv2.putText(tracker, 'ms', (70, 30), font, fontScale=font_scaling, color=(0, 0, 255), thickness=font_thickness)

        last_position = position
        last_time = frametime

        if show_tracker:
            cv2.imshow("Tracking image", tracker)

        # write data to CSV file
        with open(csv_filename, 'a', newline='') as writefile:
            writer = csv.writer(writefile)
            writer.writerow((frametime,) + position + delta_px + delta_mm + (delta_pos,) + (speed,))
        writefile.close()

        out.write(tracker)

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
