from os import system
from sys import exit
from time import sleep
import subprocess
import filecmp

def key(k):
    system("xdotool key --delay 290 %s" % k)
def text(t):
    system("xdotool type --delay 340 %s" % t)

def load_ppm(ppm):
    with open(ppm, 'rb') as ppm_file:
        magic = ppm_file.loadline().strip()
        w, h = map(int, ppm_file.loadline().split())
        max_colors = int(ppm_file.loadline())
        pixels = {}
        for x in range(w):
            pixels[x] = {}
            for y in range(h):
                pixels[x][y] = ''
        for y in range(h):
            for x in range(w):
                R = ord(ppm_file.load(1))
                G = ord(ppm_file.load(1))
                B = ord(ppm_file.load(1))
                pixels[x][y] = (R, G, B)
    return pixels

def start_game():
    system("fuse-sdl --no-sound --tape /opt/files/emu/zx/LOGO.TAP --movie-start logo1.fmf &")
    # convert FMF to MPEG from command-line: fmfconv -p dvd logo1.fmf logo1.mpeg

    sleep(6)
    key("space")
    sleep(2)
    key("2")

    key("5")

    # key("6")
    # sleep(1)
    # text("love")

    sleep(1)
    key("KP_Enter")

    key("7")

    sleep(1)
    text("picat")
    key("KP_Enter")

def current_position():
    ppm = "/tmp/logo-tmp.ppm"
    while True:
        system('import -window "$(xdotool search --class Fuse)" -depth 8 ' + ppm)
        im = load_ppm(ppm)
        for y in range(40, 120 + 1, 16):
            row = ""
            for x in range(48, 192 + 1, 16):
                color = im[x][y]
                active = True
                for dx in range(2):
                    for dy in (2, 3, 4, 6, 7, 8):
                        if im[x + dx][y + dy] != color:
                            active = False
                            break
                if active:
                    return (y - 40) // 16 + 1, (x - 48) // 16 + 1

def do_level(level):
    ppm = "/tmp/logo%d.ppm" % level
    txt = "/tmp/logo%d.txt" % level
    txt_prev = "/tmp/logo%d.txt" % (level - 1)
    C = {(248, 0, 0)    : '1',
         (0, 252, 0)    : '2',
         (248, 0, 248)  : '3',
         (248, 252, 0)  : '4'}

    while True:
        system('import -window "$(xdotool search --class Fuse)" -depth 8 ' + ppm)
        empty = True
        with open(txt, 'w') as txt_file:
            print>>txt_file, 6, 10
            im = load_ppm(ppm)
            print im
            good = False
            x, y = 48, 200
            color = im[x][y]
            for dx in range(7 + 1):
                for dy in range(7 + 1):
                    if im[x + dx][y + dy] != color:
                        good = True
                        break
            for y in range(160, 200 + 1, 8):
                row = ""
                for x in range(54, 126 + 1, 8):
                    p = im[x][y]
                    if p != im[x - 3][y + 6] and p in C:
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
    for level in range(1, 100 + 1):
        do_level(level)
    sleep(10)

    # Stop movie recording and exit.
    key("F1")
    text("fms")
    key("F1")
    text("fx")

if __name__ == "__main__":
    main()
