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

    def on_press(self, key):
        try:
            if key in self.COMBO:
                self.current.add(key)

                if all(k in self.current for k in self.COMBO):
                    if self.suppressed:
                        self.suppressed = False
                        print("Stopping")
                        if "x" in self.type:
                            self.mouse_listener.stop()
                    else:
                        print("Continuing")
                        self.suppressed = True
                        if "x" in self.type:
                            self.mouse_listener = pynput.mouse.Listener(suppress=True)
                            self.mouse_listener.start()
                    time.sleep(1)
        except:
            pass

    def on_release(self, key):
        try:
            if key in self.COMBO:
                self.current.remove(key)
            time.sleep(1)
        except:
            pass

    def run(self):
        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_press,
                                                          on_release=self.on_release)
        self.mouse_listener = pynput.mouse.Listener(suppress=True)
        self.suppressed = False

        self.keyboard_listener.start()

        if "x" in self.type:
            self.mouse_listener.start()
            print("Disabling mouse")
            self.suppressed = True

        while True:
            if self.keyboard_listener.running:
                pass
            if self.mouse_listener.running:
                pass



def main(type):
    def on_press(self, key):
        time.sleep(1)
        if key in self.COMBO:
            self.current.add(key)

            if all(k in self.current for k in self.COMBO):
                if "x" in self.type:
                    self.mouse_listener.stop()

    def on_release(self, key):
        if key in self.COMBO:
            self.current.remove(key)
            print("Released")
        time.sleep(1)

    keyboard_listener = pynput.keyboard.Listener(on_press=on_press,
                                                 on_release=on_release,
                                                 suppress=True)
    mouse_listener = pynput.mouse.Listener(suppress=True)

    while True:
        if "x" in type:
            if not mouse_listener.running:
                mouse_listener.start()
                print("Disabling mouse")


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
    # main("x")
