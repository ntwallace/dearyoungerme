import cairo
from PIL import Image

imagesize = (512,128)
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, *imagesize)

cr = cairo.Context(surface)

# paint background
cr.set_source_rgba(0.0, 0.0, 0.0, 0.0) # transparent black
cr.rectangle(0, 0, 512, 128)
cr.fill()

# setup font
cr.select_font_face("Helvetica", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
cr.set_font_size(48)
cr.set_source_rgb(0.1, 0.1, 0.1)

# write with font
cr.move_to(100,50)
cr.show_text("hello")

# commit to surface
cr.stroke()

# save file
surface.write_to_png("/Users/Nick/Documents/ITP/Fall 2018/Pop Up Windows/python/image.png")