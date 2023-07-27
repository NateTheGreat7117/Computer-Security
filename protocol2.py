import pyautogui
import argparse
import keyboard
import time
import cv2
import os


def main(record_time):
    cap = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    recordings = os.listdir("recordings")
    index = 0
    if len(recordings) > 0:
        index = int(recordings[-1][-5])
    out = cv2.VideoWriter(f'recordings/output{index+1}.avi', fourcc, 20.0, (640, 480))

    pyautogui.hotkey("winleft", "altleft", "r")

    capture = True
    print("Starting")

    start = time.time()

    while True:
        ret, frame = cap.read()

        if capture:
            out.write(frame)
        else:
            out.release()

        if (keyboard.is_pressed("ctrl") and keyboard.is_pressed("alt") and keyboard.is_pressed("a")) or \
           (record_time != "none" and capture and 0 < int(record_time) < time.time() - start):
            if not capture:
                out = cv2.VideoWriter(f'recordings/output{index}.avi', fourcc, 20.0, (640, 480))
                print("Starting")
                start = time.time()
            else:
                print("Stopping")
            capture = not capture
            time.sleep(.5)
            pyautogui.hotkey("winleft", "altleft", "r")
            index += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
    Program to record computer screen, webcam, and microphone when a specific key code is detected
    ''')

    parser.add_argument("--time", type=str, default="none",
                        help="optional time to record computer usage")

    args = parser.parse_args()

    main(args.time)
