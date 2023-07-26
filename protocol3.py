import tensorflow as tf
import pyautogui
import numpy as np
import keyboard
import argparse
import pynput
import cv2


def main(type):
    BASE_PATH = "C:/Users/Natha/Artificial Intelligence/Tensorflow Image Recognition/FaceVerification"

    def get_image(path):
        byte_img = tf.io.read_file(path)
        img = tf.io.decode_jpeg(byte_img)
        img = tf.image.resize(img, (120, 120))
        return img

    detection_model = tf.keras.models.load_model(BASE_PATH + "/face_detection")
    location_model = tf.keras.models.load_model(BASE_PATH + "/face_location", compile=False)
    classification_model = tf.keras.models.load_model(BASE_PATH + "/face_verification")

    cap = cv2.VideoCapture(0)

    keyboard_listener = pynput.keyboard.Listener(suppress=True)
    mouse_listener = pynput.mouse.Listener(suppress=True)

    inputs = True
    record = True

    while True:
        if record:
            ret, frame = cap.read()

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resized = cv2.resize(rgb, (120, 120))
            numpy = np.array([resized]) / 255.0

            class_id = detection_model.predict(numpy, verbose=0)
            location = location_model.predict(numpy, verbose=0)

            point = location[0] * [640, 480, 640, 480]

            bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

            detection = cv2.putText(bgr, f"Score: {class_id[0][0]}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
                                    2)

            if class_id[0][0] >= .5:
                detection = cv2.rectangle(bgr, (int(point[0]), int(point[1])),
                                          (int(point[2]), int(point[3])), color=(0, 255, 0))

            # cropped = frame[int(point[1]):int(point[3]), int(point[0]):int(point[2]), :]

            prediction = classification_model.predict(
                [np.expand_dims(get_image(BASE_PATH + "/images/Nathan3.jpeg"), axis=0), numpy], verbose=0)

            if prediction >= 0.5 and class_id[0][0] > .8:
                print("Yes")
                if mouse_listener.running:
                    mouse_listener.stop()
                if keyboard_listener.running:
                    keyboard_listener.stop()
                inputs = True
            else:
                print("No")
                if inputs:
                    if "v" in type or "z" in type:
                        keyboard_listener = pynput.keyboard.Listener(suppress=True)
                        keyboard_listener.start()
                    if "w" in type or "z" in type:
                        mouse_listener = pynput.mouse.Listener(suppress=True)
                        mouse_listener.start()
                    if "x" in type or "z" in type:
                        pyautogui.press("volumemute")
                    if "y" in type or "z" in type:
                        pyautogui.press("playpause")
                inputs = False

            cv2.imshow("Image", detection)
            cv2.waitKey(1)

        if keyboard.is_pressed("q"):
            print("Stopped")
            cap.release()
            cv2.destroyAllWindows()
            record = False
        if keyboard.is_pressed("c"):
            cap = cv2.VideoCapture(0)
            record = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
    Program to disable keyboard and mouse when the user's face is not detected in the webcam
    ''')

    parser.add_argument("--type", type=str, default="x",
                        help="the devices to disable when the user's face is not detected(v=keyboard,w=mouse,x=audio,y=pause,z=all")

    args = parser.parse_args()

    main(args.type)
