from nbt_tools.nbt import main as nbt
from PIL import Image, ImageDraw
import pprint
from nbt_tools.mcfiles import map_colors

def generate_image(filename, output_dir, output_name, debug = False):
    nbt_data = nbt.unpack_nbt_data(filename)
    root = nbt_data['root']['value']
    map_data = root['data']['value']
    if debug:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(root)
        print(filename)

    raw_data = map_data['colors']['value']['raw']

    # TODO: find out if there's a different width/height
    # if there is, how to get these values
    width = height = 128

    im = Image.new('RGBA', (width, height), 'white')
    draw = ImageDraw.Draw(im)
    colors = map_colors.get_all_colors(map_colors.get_color_data())

    for x in range(0, width):
        for y in range(0, height):
            color_id = raw_data[x + y * width]
            
            try:
                color_rgba = tuple(colors[color_id][0:3])
                draw.point((x,y), fill=color_rgba)
            except IndexError as e:
                #print('out of bounds ({0}, {1}) for position {2} value is "{3}"'.format(x, y, (x + y * 128), color_id))
                continue

    im.save('{0}/{1}.png'.format(output_dir, output_name))

    # generate upscaled image
    large_im = im.resize((1024, 1024))
    large_im.save('{0}/{1}_large.png'.format(output_dir, output_name))
