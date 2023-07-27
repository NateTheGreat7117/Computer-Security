from playsound import playsound
import pyautogui
import argparse
import pynput
import time
import math
import os


class controller:
    def __init__(self):
        self.start = time.time()
        self.COMBO = {pynput.keyboard.Key.ctrl_l,
                      pynput.keyboard.Key.alt_l,
                      pynput.keyboard.KeyCode(char="a")}
        self.current = set()
        self.suppressed = False

        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_press)
        self.mouse_listener = pynput.mouse.Listener(on_move=self.on_move,
                                                    on_click=self.on_click,
                                                    on_scroll=self.on_scroll)

        self.play_audio = True
        self.muted = True
        self.paused = True

    def on_press(self, key):
        self.start = time.time()

    def on_move(self, x, y):
        self.start = time.time()

    def on_click(self, x, y, button, pressed):
        self.start = time.time()

    def on_scroll(self, x, y, dx, dy):
        self.start = time.time()

    def on_deactivate(self, key):
        try:
            if key in self.COMBO:
                self.current.add(key)

                # Check if hotkey is pressed
                if all(k in self.current for k in self.COMBO):
                    if self.play_audio:
                        self.play_audio = False
                    if self.mouse_listener.running:
                        self.mouse_listener.stop()
                    mouse_listener = pynput.mouse.Listener(on_move=self.on_move,
                                                           on_click=self.on_click,
                                                           on_scroll=self.on_scroll)  # Create new mouse listener
                    mouse_listener.start()
                    if self.keyboard_listener.running:
                        self.keyboard_listener.stop()  # Stop the listener from searching for the hotkey
                    print("hotkey detected")
                    self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_press)  # Look for any key press
                    print("New keyboard listener has begun")
                    self.keyboard_listener.start()
                    self.start = time.time()
                    self.suppressed = False
                    if self.muted:
                        pyautogui.press("volumemute")
                    if self.paused:
                        pyautogui.press("playpause")
        except Exception as e:
            print(e)

    def on_release(self, key):
        try:
            if key in self.COMBO:
                self.current.remove(key)
        except Exception:
            pass

    def run(self, type, deactive_time, volume):
        self.keyboard_listener.start()
        self.mouse_listener.start()

        while True:
            global start
            if time.time() - self.start >= deactive_time:
                self.play_audio = True
                if self.keyboard_listener.running and not self.suppressed:
                    self.keyboard_listener.stop()
                if self.mouse_listener.running and not self.suppressed:
                    self.mouse_listener.stop()

                if "s" in type:
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                    break
                if "t" in type:
                    if volume != -1:
                        pyautogui.press('volumedown', presses=50)
                        x = math.floor(volume / 2)
                        pyautogui.press('volumeup', presses=x)
                    while self.play_audio:
                        playsound('recordings/iphone_alarm.mp3')
                if "u" in type or "w" in type:
                    if not self.suppressed:
                        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_deactivate,
                                                                          on_release=self.on_release,
                                                                          suppress=True)
                        self.keyboard_listener.start()
                        self.suppressed = True
                if "v" in type or "w" in type:
                    if not self.suppressed:
                        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_deactivate,
                                                                          on_release=self.on_release)
                        self.mouse_listener = pynput.mouse.Listener(suppress=True)
                        self.keyboard_listener.start()
                        self.mouse_listener.start()
                        print("Disabling mouse")
                        self.suppressed = True
                if "x" in type:
                    pyautogui.press("volumemute")
                    self.muted = True
                if "y" in type:
                    pyautogui.press("playpause")
                    self.paused = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
    Program to activate a function such as play audio or disable keyboard after there is no activity detected on computer.
    ''')

    parser.add_argument("--type", type=str, default="x",
                        help="the functions to enable when there is no activity detected(s=put computer to sleep,t=play audio,u=disable keyboard,v=disable mouse,w=disable inputs(keyboard, mouse),x=mute audio,y=pause,z=all")
    parser.add_argument("--time", type=int, default=300,
                        help="the amount of time with no activity detected on the computer before something happens")
    parser.add_argument("--volume", type=int, default=-1,
                        help="the volume to play the audio if it is chosen. -1 to keep the volume the same")

    args = parser.parse_args()

    pc_controller = controller()
    pc_controller.run(args.type, args.time, args.volume)
