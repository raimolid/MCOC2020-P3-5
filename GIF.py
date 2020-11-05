import glob
from PIL import Image

import re
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text)]

fp_in = "caso_3/frame_*.png"
fp_out = "caso_3.gif"

listaImagenes = sorted(glob.glob(fp_in))

print("sorted(glob.glob(fp_in)): ", listaImagenes)
listaImagenes.sort(key=natural_keys)
print("listaImagenes: ", listaImagenes)
ing, *ings = [Image.open(f) for f in listaImagenes]
ing.save(fp = fp_out, format='Gif', append_images=ings, saveall=True, duration=150, loop=0)



