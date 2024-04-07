from pymem import Pymem,process
import pyMeow as mw
import keyboard

proc = mw.open_process("gzdoom.exe")
pm = Pymem("hl2.exe")
resolution = (310,90)
tier0 = process.module_from_name(pm.process_handle,"tier0.dll").lpBaseOfDll
printf_address = pm.read_uint(tier0+0x406B0)
shell = pm.allocate(resolution[0]*resolution[1])
mw.overlay_init(target="Entryway - DOOM 2: Hell on Earth",fps = 144,trackTarget=True)
doom_window_pos = list(mw.get_window_position().values())
doom_window_pos[0]+=1
doom_window_pos[1]+=80

def printf(string):
    size = len(string.encode('utf-8'))
    pm.write_string(shell,string)
    pm.start_thread(printf_address,shell)
    pm.write_bytes(shell,bytes([0]*size),size)

def translate():
    frame = mw.pixel_enum_region(*doom_window_pos, resolution[0], resolution[1])
    out = ""
    ascii_chars = "@%#*+=-:. "[::-1]
    for pixel in frame:
        x, y = pixel["x"], pixel["y"]
        if x == resolution[0] - 1:
            out += "\n"
        r, g, b = pixel["color"]["r"], pixel["color"]["g"], pixel["color"]["b"]
        gray = (r * 0.299 + g * 0.587 + b * 0.114)
        out += ascii_chars[int(gray / 256 * len(ascii_chars))]
    return out
 

def getxrange():
    for i in range(312):
        printf(".")
    printf("\n")

def getyrange():
    for i in range(200):
        printf(str(i+1))
        printf("\n")


def megaprint(ascii, n=8):
    segment_length = len(ascii) // n
    for i in range(1, n):
        printf(ascii[(i-1)*segment_length : i*segment_length])
    printf(ascii[(n-1)*segment_length:])


import time
def main():
    while True:
        out = translate()
        megaprint(out)
    time.sleep(0.03)
    pm.free(shell)
    

if __name__ == "__main__":
    while not keyboard.is_pressed("l"):
        pass
    main()