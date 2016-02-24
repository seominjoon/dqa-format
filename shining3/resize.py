import argparse
from PIL import Image


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_image_path")
    parser.add_argument("output_image_path")
    parser.add_argument("x", type=int)
    parser.add_argument("y", type=int)
    parser.add_argument("--out_ext", default="PNG")
    return parser.parse_args()


def main(args):
    input_image_path = args.input_image_path
    output_image_path = args.output_image_path
    size = (args.x, args.y)
    out_ext = args.in_ext
    resize(input_image_path, output_image_path, size, out_ext)


def resize(input_image_path, output_image_path, size, ext):
    bg = Image.new("RGBA", size, (255, 255, 255, 0))
    im = Image.open(input_image_path)
    im.thumbnail(size, Image.ANTIALIAS)
    bg.paste(im, (0, 0))
    bg.save(output_image_path, ext)

if __name__ == "__main__":
    ARGS = get_args()
    main(ARGS)
