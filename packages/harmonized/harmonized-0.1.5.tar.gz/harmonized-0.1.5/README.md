# Harmonized

When developing prototypes with Python conversion and casting can be time consuming and challeging. With harmonized we try to ease this process by providing ready to use helper scripts and tools.

## hexcolor

Working with colors in RGB space. Converting between hex strings like #FF4470, RGB normed floats [0.0 - 1.0] and HSV normed floats. Quickstart ...


Create color:

	from harmonized import hexcolor
	color = hexcolor.HexColor("#FF4470")

Get color values:

	# get RGB values
	print(color.r, color.g, color.b)

	# get HSV values
	print(color.h, color.s, color.v)

	# get HexColor string
	print(color)

Set via rgb or hsv floats:

	# set red via rgb
	color.set_from_hsv(0, 1, 1)

	# set red via rgb
	color.set_from_rgb(1, 0, 0)



## inout

Simplified handling of loading and writing files. Making reading from file or HTTP exchangable with local file reading. Local caching possible.

