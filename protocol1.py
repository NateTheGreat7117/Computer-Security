import argparse
import pynput
import time


class input_controller:
    def __init__(self, type):
        self.COMBO = {pynput.keyboard.Key.ctrl_l,
                      pynput.keyboard.Key.alt_l,
                      pynput.keyboard.KeyCode(char="a")}
        self.current = set()

        self.type = type.lower()
        self.activate = True

    def on_press(self, key):
        try:
            if key in self.COMBO:
                self.current.add(key)

                if all(k in self.current for k in self.COMBO):
                    print("Stopping")
                    if "x" in self.type:
                        self.mouse_listener.stop()
                        self.activate = False
        except:
            pass

    def on_release(self, key):
        try:
            if key in self.COMBO:
                self.current.remove(key)
        except:
            pass

    def run(self):
        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_press,
                                                          on_release=self.on_release)
        self.mouse_listener = pynput.mouse.Listener(suppress=True)

        self.keyboard_listener.start()

        if "x" in self.type:
            self.mouse_listener.start()
            print("Disabling mouse")

        while self.activate:
            # if self.keyboard_listener.running:
            #     pass
            # if self.mouse_listener.running:
            #     pass
            time.sleep(.1)
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
    Program to disable basic inputs to pc such as keyboard, mouse, webcam, and microphone
    ''')

    parser.add_argument("--type", type=str, default="wx",
                        help="the inputs to disable(w=keyboard,x=mouse,y=webcam,z=microphone")

    args = parser.parse_args()

    # controller = input_controller(args.type)
    controller = input_controller("x")
    controller.run()
