import PIL, sys
from PIL import Image
import tempfile, os

for inf in sys.argv[1:]:

    i1 = Image.open(inf)

    of1 = inf.replace(".tif", ".jpg")
    i1.save(of1, quality=95)

    squaresize = i1.size[0]/5, i1.size[1]/5

    i2 = i1.crop((
        i1.size[0]/2 - squaresize[0]/2, i1.size[1]/2 - squaresize[1]/2, i1.size[0]/2 + squaresize[0]/2, i1.size[1]/2 + squaresize[1]/2)
    )
    tfn = tempfile.mkstemp(".jpeg")[1]
    i2.save(tfn, quality=50)
    i2 = Image.open(tfn)

    i1.paste(i2, (i1.size[0]/2 - squaresize[0]/2, i1.size[1]/2 - squaresize[1]/2))
    of2 = inf.replace(".tif", "_fake.jpg")
    os.remove(tfn)

    i1.save(of2, quality=90)
