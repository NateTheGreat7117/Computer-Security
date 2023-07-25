import argparse
import win32api
import win32gui
import pynput
import time


class input_controller:
    def __init__(self, type):
        self.COMBO = {pynput.keyboard.Key.ctrl_l,
                      pynput.keyboard.Key.alt_l,
                      pynput.keyboard.KeyCode(char="a")}
        self.current = set()

        self.type = type.lower()

        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_press,
                                                          on_release=self.on_release)
        self.mouse_listener = pynput.mouse.Listener(suppress=True)
        self.suppressed = False

        self.keyboard_listener.start()

    def on_press(self, key):
        try:
            if key in self.COMBO:
                self.current.add(key)

                if all(k in self.current for k in self.COMBO):
                    if self.suppressed:
                        self.suppressed = False
                        print("Stopping")
                        if "x" in self.type or "z" in self.type:
                            self.mouse_listener.stop()
                        if "y" in self.type or "z" in self.type:
                            self.toggle_mic()
                    else:
                        print("Continuing")
                        self.suppressed = True
                        if "x" in self.type or "z" in self.type:
                            self.mouse_listener = pynput.mouse.Listener(suppress=True)
                            self.mouse_listener.start()
                        if "y" in self.type or "z" in self.type:
                            self.toggle_mic()
                    time.sleep(1)
        except:
            pass

    def on_release(self, key):
        try:
            if key in self.COMBO:
                self.current.remove(key)
        except:
            pass

    def toggle_mic(self):
        WM_APPCOMMAND = 0x319
        APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000

        hwnd_active = win32gui.GetForegroundWindow()
        win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)

    def run(self):
        if "x" in self.type or "z" in self.type:
            self.mouse_listener.start()
            print("Disabling mouse")
            self.suppressed = True
        if "y" in self.type or "z" in self.type:
            self.toggle_mic()

        while self.run:
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
    Program to disable basic inputs to pc such as keyboard, mouse, and microphone
    ''')

    parser.add_argument("--type", type=str, default="wx",
                        help="the inputs to disable(w=keyboard,x=mouse,y=microphone,z=all")

    args = parser.parse_args()

    controller = input_controller(args.type)
    controller.run()
