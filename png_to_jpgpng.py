import sys, getopt, os

from PIL import Image
from sys import stdout

def main(argv):
	print 'Argument list: ', argv

	remove_original = False
	input_folder_path = ''
	output_quality = 85

	opts = []

	try:
		opts, args = getopt.getopt(argv, "hr:i:q:", ['rm_origin=', 'i_fldr=', 'quality='])
	except getopt.GetoptError:
		print 'png_to_jpgpng -i <input_folder>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'png_to_jpgpng -i <input_folder> to convert'
			print 'png_to_jpgpng -i <input_folder> -r True to convert and remove originals'
			print 'png_to_jpgpng -i <input_folder> -q 85 to convert with quality 85'
		elif opt in ("-i", "--input"):
			input_folder_path = arg
		elif opt in ("-r", "--rmorigin"):
			remove_original = True
		elif opt in ("-q", "--quality"):
			output_quality = int(arg)

	file_list = list(get_images(input_folder_path))
	counter   = 0

	for input_file in file_list:
		output_file_color = os.path.splitext(input_file)[0] + '.jpg'
		output_file_alpha = os.path.splitext(input_file)[0] + '_alphachannel.png'

		input_image = Image.open(input_file)

		output_image_color = Image.new('RGB', input_image.size, (255, 255, 255))
		output_image_color.paste(input_image, input_image)

		output_image_alpha = Image.new('RGBA', input_image.size, (255, 255, 255, 0))
		output_image_alpha.paste(input_image, input_image)

		origin_data = output_image_alpha.getdata()
		new_data = []

		for item in origin_data:
			new_data.append((0, 0, 0, item[3]))

		output_image_alpha.putdata(new_data)

		try:
			input_image.save(output_file_color, quality=output_quality)
			output_image_alpha.save(output_file_alpha)

			if remove_original:
				os.remove(input_file)
		except IOError:
			print 'Cannot convert', input_file

		counter +=1 
		percent = (counter / (len(file_list) * 1.0)) * 100

		stdout.write("\rProcessing %d%%, file %d of %d %s" % (percent, counter, len(file_list), os.path.split(input_file)[1]))
		stdout.flush()
	
	stdout.write("\rProcessing %d%%, file %d of %d .................................. [ DONE ]" % (percent, counter, len(file_list)))

def get_images(path):
	for root, dirs, files in os.walk(path):
		for f in files:
			if f.endswith('.png') and "_alphachannel." not in f:
				yield os.path.normpath(os.path.join(root, f))

main(sys.argv[1:])