from nbt_tools.nbt import main as nbt
from PIL import Image, ImageDraw
import pprint
from nbt_tools.mcfiles import map_colors


def generate_image(filename, output_dir, output_name, debug=False):
    nbt_data = nbt.unpack_nbt_file(filename)
    #root = nbt_data[0]
    #data = root['value'][0]
    #map_data = data['value'][3]['value']

    map_data = nbt.get_tag_node(['root', 'data', 'colors'], nbt_data)
    raw_width = nbt.get_tag_node(['root', 'data', 'width'], nbt_data)
    raw_height = nbt.get_tag_node(['root', 'data', 'height'], nbt_data)

    if map_data is False or map_data is None:
        print('Map generation failed')

        return

    if debug:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(root)
        print(filename)

    raw_data = map_data['value']['value']
    width = raw_width['value'] if raw_width != False else 128 
    height = raw_height['value'] if raw_height != False else 128 

    im = Image.new('RGBA', (width, height), 'white')
    draw = ImageDraw.Draw(im)
    colors = map_colors.get_all_colors(map_colors.get_color_data())

    for x in range(0, width):
        for y in range(0, height):
            color_id = raw_data[x + y * width]

            try:
                color_rgba = tuple(colors[color_id][0:3])
                draw.point((x, y), fill=color_rgba)
            except IndexError as e:
                print(e)
                continue

    im.save('{0}/{1}.png'.format(output_dir, output_name))

    # generate upscaled image
    large_im = im.resize((width * 4, height * 4))
    large_im.save('{0}/{1}_large.png'.format(output_dir, output_name))
