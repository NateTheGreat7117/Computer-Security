import argparse
import pynput
import time


class input_controller:
    def __init__(self):
        self.COMBO = {pynput.keyboard.Key.ctrl_l,
                 pynput.keyboard.Key.alt_l,
                 pynput.keyboard.KeyCode(char="a")}
        self.current = set()

    def on_press(self, key):
        time.sleep(1)
        if key in self.COMBO:
            self.current.add(key)

            if all(k in self.current for k in self.COMBO):
                if not self.suppressed:
                    self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_press,
                                                                      on_release=self.on_release,
                                                                      supress=True)
                    self.keyboard_listener.start()
                else:
                    self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_press,
                                                                      on_release=self.on_release)
                    self.keyboard_listener.start()
                    print("stopping")

    def on_release(self, key):
        if key in self.COMBO:
            self.current.remove(key)
            print("Released")
        time.sleep(1)

    def run(self, type):
        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_press,
                                                          on_release=self.on_release,
                                                          supress=True)
        self.suppressed = False

        while True:
            if "w" in type:
                if not self.keyboard_listener.running:
                    self.keyboard_listener.start()
                    print("Starting")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
    Program to disable basic inputs to pc such as keyboard, mouse, webcam, and microphone
    ''')

    parser.add_argument("--type", type=str, default="wx",
                        help="the inputs to disable(w=keyboard,x=mouse,y=webcam,z=microphone")

    args = parser.parse_args()

    controller = input_controller()
    controller.run(args.type)
