import pyautogui
import argparse
import cv2


def main(type):
    cap = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    pyautogui.hotKey("winleft", "altleft", "r")

    while True:
        ret, frame = cap.read()

        out.write(frame)

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