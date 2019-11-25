import cv2
from datetime import datetime
import csv
from time import time


# get username and set output CSV and video filenames
user = input("Enter user name: ")
csv_filename = user + ' ' + \
               datetime.strftime(datetime.now(), "%y%m%d%H%M%S") + '.csv'
out_filename = user + ' ' + \
               datetime.strftime(datetime.now(), "%y%m%d%H%M%S") + '.mp4'

# setup video capture and output files
cap = cv2.VideoCapture(0)
start_time = time()

if not cap.isOpened():
    print("Error opening camera.")

else:
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

    out = cv2.VideoWriter(out_filename,
                          cv2.VideoWriter_fourcc('m', 'p', '4', 'a'),
                          frame_rate, (frame_width, frame_height))

    # process the video
    while(cap.isOpened()):
        # capture frame and get time in milliseconds
        ret, frame = cap.read()
        frametime = round((time() - start_time), 3)

        # convert to HSV colour space and blur to reduce noise
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        frame_out = frame
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_hsv = cv2.blur(frame_hsv, (5, 5))
        frame_h, frame_s, frame_v = cv2.split(frame_hsv)

        # threshold and AND to separate only yellow pixels
        thresh_h = cv2.inRange(frame_h, 18, 32)
        thresh_s = cv2.inRange(frame_s, 75, 255)
        thresh_v = cv2.inRange(frame_v, 150, 255)
        tracker = cv2.bitwise_and(thresh_h, thresh_s)
        tracker = cv2.bitwise_and(tracker, thresh_v)

        # find contours around objects (white space) in tracker image
        contours, hierarchy = cv2.findContours(tracker, cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) >= 1:
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            cont = contours[0]  # select only the largest contour

            # draw circle around spot in output frame
            ((cx, cy), r) = cv2.minEnclosingCircle(cont)
            position = (int(cx), int(cy))
            cv2.circle(frame_out, position, 1, (0, 0, 255), 1)
            cv2.circle(frame_out, position, int(r), (0, 0, 128), 1)

        else:
            position = (0, 0)   # if no contour is found

        # write data to CSV file
        with open(csv_filename, 'a', newline='') as writefile:
            writer = csv.writer(writefile)
            writer.writerow(position + (frametime,))
        writefile.close()

        out.write(frame_out)

        if ret:
            cv2.imshow('output', frame_out)
#            cv2.imshow('thresh h', thresh_h)
#            cv2.imshow('thresh s', thresh_s)
#            cv2.imshow('thresh v', thresh_v)
#            cv2.imshow('tracker', tracker)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            print("Break")
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
