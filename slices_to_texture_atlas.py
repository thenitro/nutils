import sys, getopt, os

from PIL import Image


def main(argv):
    print('main: ', argv)

    input_folder_path = ''
    atlas_size = 0

    try:
        opts, args = getopt.getopt(argv, "i:s:", ['i_fldr=', 'size='])
    except getopt.GetoptError:
        print('slices_to_texture_atlas -i <input_folder> -s <atlas_size>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('slices_to_texture_atlas -i <input_folder> -s <atlas_size> to convert texture to altas')
        elif opt in ("-i", "--input"):
            input_folder_path = arg
        elif opt in ("-s", "--size"):
            atlas_size = int(arg)

    file_list = list(get_images(input_folder_path))
    counter = 0

    output = Image.new("RGBA", (atlas_size, atlas_size), (0, 0, 0, 0))

    x = 0
    y = 0

    max_y = 0

    xml = open(input_folder_path + '/atlas.xml', 'w')
    xml.write('<TextureAtlas imagePath="atlas.png">')

    for input_file in file_list:
        input_image = Image.open(input_folder_path + '/' + input_file)

        print(x, y, input_image.size)

        counter += 1
        max_y = max(max_y, input_image.size[1])

        if x + input_image.size[0] + 1 > atlas_size:
            x = 0
            y += max_y + 1
            max_y = 0

        xml.write('<SubTexture name="' + os.path.splitext(input_file)[0] + '" ' +
                  'x="' + str(x) + '" ' +
                  'y="' + str(y) + '" ' +
                  'width="' + str(input_image.size[0]) + '" ' +
                  'height="' + str(input_image.size[1]) + '" ' +
                  'frameX="0" frameY="0" ' +
                  'frameWidth="' + str(input_image.size[0]) + '" ' +
                  'frameHeight="' + str(input_image.size[1]) + '" />')

        output.paste(input_image, (x, y))

        x += input_image.size[0] + 1

    xml.write('</TextureAtlas>')
    xml.close()

    output.save(input_folder_path + '/atlas.png')


def get_images(path):
    for file in os.listdir(path):
        if file.endswith('.png'):
            yield file


main(sys.argv[1:])
