import argparse
import pynput
import time
import os

start = time.time()
COMBO = {pynput.keyboard.Key.ctrl_l,
         pynput.keyboard.Key.alt_l,
         pynput.keyboard.KeyCode(char="a")}
current = set()
suppressed = False


def on_press(key):
    global start
    start = time.time()


def on_deactivate(key):
    global keyboard_listener
    global mouse_listener
    global suppressed
    global COMBO
    global current
    global start

    try:
        if key in COMBO:
            current.add(key)

            if all(k in current for k in COMBO):
                if "u" in functions or "w" in functions:
                    keyboard_listener.stop()
                    keyboard_listener = pynput.keyboard.Listener(on_press=on_press)
                    keyboard_listener.start()
                if "v" in functions or "w" in functions:
                    mouse_listener.stop() # Free mouse
                    keyboard_listener.stop()
                    mouse_listener = pynput.mouse.Listener() # Create to mouse listener
                    mouse_listener.start() # Start mouse listener
                    keyboard_listener = pynput.keyboard.Listener(on_press=on_press) # Create new keyboard listener
                    keyboard_listener.start() # Start listening for key presses
                start = time.time()
                suppressed = False
                print("hotkey detected")
    except Exception as e:
        print(e)


def on_release(key):
    try:
        if key in COMBO:
            current.remove(key)
    except:
        pass


keyboard_listener = pynput.keyboard.Listener(on_press=on_press)
mouse_listener = pynput.mouse.Listener()


def main(type, deactive_time):
    global keyboard_listener
    global mouse_listener
    global functions
    global suppressed

    functions = type

    keyboard_listener.start()

    while True:
        global start
        if time.time() - start >= deactive_time:
            if "s" in type:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            if "t" in type:
                pass
            if "u" in type or "w" in type:
                if not suppressed:
                    keyboard_listener.stop()
                    keyboard_listener = pynput.keyboard.Listener(on_press=on_deactivate,
                                                                 on_release=on_release,
                                                                 suppress=True)
                    keyboard_listener.start()
                    suppressed = True
            if "v" in type or "w" in type:
                if not suppressed:
                    keyboard_listener.stop()
                    mouse_listener.stop()
                    keyboard_listener = pynput.keyboard.Listener(on_press=on_deactivate,
                                                                 on_release=on_release)
                    mouse_listener = pynput.mouse.Listener(suppress=True)
                    keyboard_listener.start()
                    mouse_listener.start()
                    print("Disabling mouse")
                    suppressed = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
    Program to activate a function such as play audio or disable keyboard after there is no activity detected on computer.
    ''')

    parser.add_argument("--type", type=str, default="x",
                        help="the functions to enable when there is no activity detected(s=put computer to sleep,t=play audio,u=disable keyboard,v=disable mouse,w=disable inputs(keyboard, mouse),x=stop audio audio,y=pause,z=all")
    parser.add_argument("--time", type=int, default=300,
                        help="the amount of time with no activity detected on the computer before something happens")

    args = parser.parse_args()

    main(args.type, args.time)
