import os
from PIL import Image
from math import ceil
import argparse

__author__ = 'CWSI.PL'


def get_images_info(path):
    images = {}
    for root, dirs, files in os.walk(path):
        for name in files:
            with Image.open(os.path.join(root, name)) as temp_img:
                images[name] = temp_img.size
    print(images)
    return images


def get_standard_size(size_list):
    count = len(size_list)
    standard_x = 0
    standard_y = 0

    for size in size_list:
        standard_x += size[0]
        standard_y += size[1]
    else:
        standard_x = standard_x / count
        standard_y = standard_y / count

    return standard_x, standard_y


def open_image(file_path):
    with Image.open(file_path) as current_image:
        temp_img = current_image.copy()

    return temp_img


def merge_images(path, canvas_width=760, in_row=5, output_file="main.png"):
    img_dict = get_images_info(path)

    if not img_dict:
        raise BaseException("Couldn't gather information about images!")

    img_count = len(img_dict.keys())

    standard_size = get_standard_size(img_dict.values())

    space_between = 2

    thumb_offset_y = 0
    thumb_offset_x = 0

    img_index = 0
    temp_img_index = 0

    if img_count < in_row:
        thumb_x = int(canvas_width / img_count - space_between)
        width_percent = (float(thumb_x) / float(standard_size[0]))
        thumb_y = int((float(standard_size[1]) * float(width_percent)))
        canvas_height = thumb_y + space_between
    else:
        thumb_x = int(canvas_width / in_row - space_between)
        width_percent = (float(thumb_x) / float(standard_size[0]))
        thumb_y = int((float(standard_size[1]) * float(width_percent)))
        canvas_height = int(ceil(img_count / in_row) * thumb_y)

    main_img = Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255, 255))

    for img_filename in img_dict.keys():
        original_img = open_image(os.path.join(path, img_filename))

        thumb_img = original_img.resize((thumb_x, thumb_y), Image.ANTIALIAS)

        if img_index >= in_row:
            thumb_offset_y += thumb_y + space_between
            thumb_offset_x = 0
            temp_img_index += img_index
            images_left = img_count - temp_img_index

            if (img_count - temp_img_index) < in_row:
                thumb_offset_x = ((canvas_width - (2*space_between)) - (images_left * thumb_x)) / 2

            img_index = 0

        offset = (int(thumb_offset_x), int(thumb_offset_y))
        main_img.paste(thumb_img, offset)

        img_index += 1
        thumb_offset_x += thumb_x + space_between

    main_img.save(os.path.join(path, output_file), "PNG")
    main_img.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Image Merge Script - creates one image from all images in directory (by CWSI.PL)",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--directory', help="Directory with images", required=True)
    parser.add_argument('-o', '--output', help="Output file name (PNG)", default="main.png", required=False)
    parser.add_argument('-w', '--width', help="Canvas width", type=int, default=760, required=False)
    parser.add_argument('-r', '--row', help="Image count in a row", type=int, default=5, required=False)
    args = parser.parse_args()

    print("Working directory: %s" % args.directory)
    print("Output file: %s" % args.output)

    merge_images(args.directory, args.width, args.row, args.output)