import ntpath
import argparse

from os import path
from PIL import Image, ImageOps

parser = argparse.ArgumentParser(description="Instagram Image Processor", add_help=False)

parser.add_argument('--image-path', nargs=1, action='store', help='path to the original image to be converted')
parser.add_argument('--output-path', nargs=1, action='store', help='path to the where the new image is going to be stored')
parser.add_argument("-h", "--help", action="help", help="Show this message and leaves.")

args = parser.parse_args()

def get_file_name(path_str):
    _, file_name = ntpath.split(path_str)
    file_name_split = file_name.split('.')
    return file_name_split[0]


def get_file_ext(path_str):
    _, file_name = ntpath.split(path_str)
    file_name_split = file_name.split('.')
    return file_name_split[1]


image_path = args.image_path[0]
output_path = args.output_path[0]


def save_image():
    img_with_border.save(path.join(output_path, f"{get_file_name(image_path)}_ig_resized.{get_file_ext(image_path)}"))


if not path.exists(image_path) or \
    not path.isfile(image_path) :
    print("image path does not exist or is not a file")
elif not path.exists(output_path) or \
    not path.isdir(output_path) :
    print("output path does not exist or is not a directory")
else :    
    old_im = Image.open(image_path) 

    old_size = old_im.size

    image_width, image_height = old_size[0], old_size[1]

    print(f"width={image_width}, height={image_height}")

    portrait_aspect_ratio = 4/5
    landscape_aspect_ratio = 5/4
    original_image_aspect_ratio = image_height/image_width

    if image_height == image_width :
        print("image is square")
    elif original_image_aspect_ratio == portrait_aspect_ratio or \
        original_image_aspect_ratio == landscape_aspect_ratio:
        print("image already in final aspect ratio")
    elif image_height > image_width:
        new_width = int(image_height * portrait_aspect_ratio)
        print(f"processing for portrait. New aspect ratio={image_height}/{new_width}")

        width_difference = ( new_width - image_width ) // 2

        img_with_border = ImageOps.expand(old_im,border=(width_difference, 0, width_difference, 0),fill='white')

        save_image()

    else:
        new_height = int(image_width / landscape_aspect_ratio)
        print(f"processing for landscape. New aspect ratio={new_height}/{image_width}")

        height_difference = ( new_height - image_height ) // 2

        img_with_border = ImageOps.expand(old_im,border=(0, height_difference, 0, height_difference),fill='white')

        save_image()

    