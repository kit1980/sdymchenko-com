from PIL import Image
from os import system
from sys import exit
from time import sleep
import subprocess
import filecmp

def key(k):
    system("xdotool search --class Fuse windowactivate key --delay 250 %s" % k)
def text(t):
    system("xdotool type --delay 340 %s" % t)

def start_game():
#    system("fuse-sdl --no-sound --tape /opt/files/emu/zx/LOGO.TAP &")
    system("/home/kit/build/fuse-1.1.1/fuse --no-sound --tape /opt/files/emu/zx/LOGO.TAP &")

    sleep(6)
    key("space")
    sleep(2)
    text("2")

    text("5")

    text("6")
    sleep(1)
    text("love")
    sleep(1)
    key("KP_Enter")

    text("7")

    sleep(1)
    text("picat")
    key("KP_Enter")
    sleep(3)

def current_position():
    png = "/tmp/logo-tmp.png"
    while True:
        system('import -window "$(xdotool search --class Fuse)" ' + png)
        with Image.open(png).convert("RGB") as im:
            for y in range(40, 120 + 1, 16):
                row = ""
                for x in range(48, 192 + 1, 16):
                    color = im.getpixel((x, y))
                    active = True
                    for dx in range(2):
                        for dy in (2, 3, 4, 6, 7, 8):
                            if im.getpixel((x + dx, y + dy)) != color:
                                active = False
                                break
                    if active:
                        return (y - 40) // 16 + 1, (x - 48) // 16 + 1

def do_level(level):
    png = "/tmp/logo%d.png" % level
    txt = "/tmp/logo%d.txt" % level
    txt_prev = "/tmp/logo%d.txt" % (level - 1)

    while True:
        system('import -window "$(xdotool search --class Fuse)" ' + png)
        C = {(255, 0, 0)    : '1',
             (0, 255, 0)    : '2',
             (255, 0, 255)  : '3',
             (255, 255, 0)  : '4'}
        empty = True
        with open(txt, 'w') as txt_file:
            print>>txt_file, 6, 10
            with Image.open(png).convert("RGB") as im:
                good = False
                x, y = 48, 40
                color = im.getpixel((x, y))
                for dx in range(6):
                    for dy in range(6):
                        if im.getpixel((x + dx, y + dy)) != color:
                            good = True
                            break
                for y in range(160, 200 + 1, 8):
                    row = ""
                    for x in range(54, 126 + 1, 8):
                        p = im.getpixel((x, y))
                        if (p != im.getpixel((x - 3, y + 6))) and p in C:
                            row += C[p]
                            empty = False
                        else:
                            row += '.'
                    print>>txt_file, row
        if good and not empty and (level == 1 or not filecmp.cmp(txt, txt_prev)):
            break
        sleep(0.5)

    plan = subprocess.check_output("picat logo-part1.pi <" + txt, shell=True)
    curr_r, curr_c = 1, 1
    for move in plan.strip().split("\n")[::-1]:
        r, c = map(int, move.split())
        while True:
            keys = ""
            if r > curr_r:
                keys += (r - curr_r) * 'a'
            else:
                keys += (curr_r - r) * 'q'
            if c > curr_c:
                keys += (c - curr_c) * 'p'
            else:
                keys += (curr_c - c) * 'o'
            text(keys)
            curr_r, curr_c = current_position()
            if (c, r) == (curr_c, curr_r):
                key("space")
                break


def main():
    start_game()
    level = 1
    while True:
        do_level(level)
        level += 1

if __name__ == "__main__":
    main()
