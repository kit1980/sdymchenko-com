from PIL import Image
from os import system
from time import sleep
import subprocess
import filecmp

def key(k):
    system("xdotool key --delay 239 %s" % k)
    sleep(0.0)
def text(t):
    for c in t:
        key(c)

def start_game():
#    system("fuse-sdl --no-sound --tape /opt/files/emu/zx/LOGO.TAP &")
#    system("/home/kit/build/fuse-1.1.1/fuse --no-sound --tape /opt/files/emu/zx/LOGO.TAP &")
    system("xspect -no-sound -scale 1 -load-immed -quick-load -tap /opt/files/emu/zx/LOGO.TAP &")

    sleep(6)
    key("space")
    sleep(2)
    text("257")
    sleep(1)
    text("picat")
    key("KP_Enter")
    sleep(3)

def do_level(level):
    png = "/tmp/logo%d.png" % level
    txt = "/tmp/logo%d.txt" % level
    txt_prev = "/tmp/logo%d.txt" % (level - 1)

    while True:
        system('import -window "$(xdotool getwindowfocus -f)" ' + png)
        C = {(252, 32, 32)    : '1',
             (32, 252, 32)    : '2',
             (252, 32, 252)  : '3',
             (252, 252, 32)  : '4'}
        empty = True
        with open(txt, 'w') as txt_file:
            print>>txt_file, 6, 10
            with Image.open(png).convert("RGB") as im:
                for y in range(168, 208 + 1, 8):
                    row = ""
                    for x in range(54, 126 + 1, 8):
                        p = im.getpixel((x, y))
                        if (p != im.getpixel((x - 3, y + 6))) and p in C:
                            row += C[p]
                            empty = False
                        else:
                            row += '.'
                    print>>txt_file, row
        if not empty and (level == 1 or not filecmp.cmp(txt, txt_prev)):
            break
        sleep(1)

    plan = subprocess.check_output("picat logo-part1.pi <" + txt, shell=True)
    for k in plan.split():
        key(k)

def main():
    start_game()
    level = 1
    while True:
        do_level(level)
        level += 1

if __name__ == "__main__":
    main()

# text("pppp")
# text("a")
# key("space")
# text("aa")
# key("space")
# text("qo")
# key("space")
# text("pp")
# key("space")
# text("o")
# key("space")
