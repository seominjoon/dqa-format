import argparse
import logging
import os
import shutil
from utils import get_pbar

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir")
    parser.add_argument("first_dir")
    parser.add_argument("--second_dir", default="", type=str)
    parser.add_argument('--num', default=0, type=int)

    return parser.parse_args()


def _copy(from_dir, to_dir, name, subdir=""):
    from_path = os.path.join(from_dir, subdir, name)
    to_path = os.path.join(to_dir, subdir, name)
    if os.path.exists(from_path):
        shutil.copy(from_path, to_path)
    else:
        logging.warning("%s does not exist." % from_path)


def split_dqa(args):
    data_dir = args.data_dir
    first_dir = args.first_dir
    second_dir = args.second_dir
    if not os.path.exists(first_dir):
        os.mkdir(first_dir)
    if second_dir and not os.path.exists(second_dir):
        os.mkdir(second_dir)
    num = args.num
    image_names = os.listdir(os.path.join(data_dir, "images"))
    if num:
        pbar = get_pbar(len(image_names)).start()
        for i, image_name in enumerate(image_names):
            if not image_name.endswith(".png"):
                pbar.update(i)
                continue
            image_id, ext = os.path.splitext(image_name)
            json_name = "%s.json" % image_name
            if int(image_id) < num:
                to_dir = first_dir
            elif second_dir:
                to_dir = second_dir
            else:
                pbar.update(i)
                continue

            for subdir in ['images', 'imagesReplacedText', 'annotations', 'questions']:
                folder_path = os.path.join(to_dir, subdir)
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
            for subdir in ['images', 'imagesReplacedText']:
                _copy(data_dir, to_dir, image_name, subdir=subdir)
            for subdir in ['annotations', 'questions']:
                _copy(data_dir, to_dir, json_name, subdir=subdir)
            pbar.update(i)
        pbar.finish()
    else:
        raise Exception()

    _copy(data_dir, first_dir, "categories.json")
    _copy(data_dir, second_dir, "categories.json")


if __name__ == "__main__":
    ARGS = get_args()
    split_dqa(ARGS)
