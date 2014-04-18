import sys, getopt, os, math

from PIL import Image

def main(argv):
	read_arguments(argv)

	input_image = Image.open(input_file)
	input_width, input_height = input_image.size

	slices_x = int(math.ceil(input_width / slice_width))
	slices_y = int(math.ceil(input_height / slice_height))

	print 'main: will be sliced to', slices_x, 'in x and', slices_y, 'in y'

	left = 0
	upper = 0

	width = slice_width
	lower = slice_height

	for x in range(slices_x + 1):
		for y in range(slices_y + 1):
			box = (left, upper, width, lower)

			working_slice = input_image.crop(box)
			working_slice.save(os.path.join(output_dir, "piece_" + str(x) + "_" + str(y) + ".jpg"), quality=85)
			working_slice.save(os.path.join(output_dir, "piece_" + str(x) + "_" + str(y) + "_lq.jpg"), quality=1)

			upper += slice_height
			prediction_y = input_height - ((y + 1) * slice_height)
			lower += (slice_height if prediction_y > slice_height else prediction_y)

		left += slice_width
		prediction_x = input_width - ((x + 1) * slice_width)
		width += (slice_width if prediction_x > slice_width else prediction_x)

		upper = 0
		lower = slice_height

def read_arguments(argv):
	print 'read_arguments: ', argv

	global input_file
	global output_dir

	global slice_width
	global slice_height

	opts = []

	try:
		opts, args = getopt.getopt(argv, "i:o:x:y:", [ "i_file=", "o_dir=", "slice_width=", "slice_height=" ] )
	except getopt.GetoptError:
		print 'img_slicer -i <input_file> -o <output_dir> -x <slice_width> -y <slice_height>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print_help()
		elif opt in ('-i', '--input'):
			input_file = arg
		elif opt in ('-o', '--ouput'):
			output_dir = arg
		elif opt in ('-x', '--width'):
			slice_width = int(arg)
		elif opt in ('-y', '--height'):
			slice_height = int(arg)

def print_help():
	print 'img_slicer -i <input_file> -o <output_dir> -x <slice_width> -y <slice_height> to slice image to pieces with input width and height in folder'

input_file = ''
output_dir = ''

slice_width = 0
slice_height = 0

main(sys.argv[1:])