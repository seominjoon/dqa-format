import argparse
import os

import progressbar as pb

from resize import resize


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("in_data_dir")
    parser.add_argument("out_data_dir")
    parser.add_argument("x", type=int)
    parser.add_argument("y", type=int)
    parser.add_argument("--out_ext", default="PNG")
    parser.add_argument("--in_exts", default=['.jpg', 'jpeg', '.png'], nargs='*')
    return parser.parse_args()


def main(args):
    in_data_dir = args.in_data_dir
    out_data_dir = args.out_data_dir
    size = (args.x, args.y)
    out_ext = args.out_ext
    in_exts = args.in_exts

    if not os.path.exists(out_data_dir):
        os.mkdir(out_data_dir)

    in_images_dir = os.path.join(in_data_dir, "images")
    out_images_dir = os.path.join(out_data_dir, "images")
    if not os.path.exists(out_images_dir):
        os.mkdir(out_images_dir)

    names = os.listdir(in_images_dir)
    pbar = pb.ProgressBar(widgets=["N=%d|" % len(names), pb.Percentage(), pb.Bar(), pb.ETA()], maxval=len(names))
    pbar.start()
    for i, name in enumerate(os.listdir(in_images_dir)):
        if os.path.splitext(name)[1] in in_exts:
            in_path = os.path.join(in_images_dir, name)
            out_path = os.path.join(out_images_dir, name)
            resize(in_path, out_path, size, out_ext)
        pbar.update(i)
    pbar.finish()

if __name__ == "__main__":
    ARGS = get_args()
    main(ARGS)
