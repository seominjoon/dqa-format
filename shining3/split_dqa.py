import argparse
import json
import logging
import os
import random
import shutil
from utils import get_pbar

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir")
    parser.add_argument("first_dir")
    parser.add_argument("--second_dir", default="", type=str)
    parser.add_argument('--num', default=0, type=int)
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--stop', type=int, default=1500)
    parser.add_argument('--skip_images', type=str, default='False')
    parser.add_argument('--random', type=str, default='True')
    parser.add_argument('--label', type=str, default='False', help='label=False ignores questions on labeled images')
    parser.add_argument('--quiet', type=str, default='True')

    return parser.parse_args()


def _copy(from_dir, to_dir, name, subdir="", quiet=True):
    from_path = os.path.join(from_dir, subdir, name)
    to_path = os.path.join(to_dir, subdir, name)
    if os.path.exists(from_path):
        shutil.copy(from_path, to_path)
    else:
        if not quiet:
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
    image_names = [name for name in os.listdir(os.path.join(data_dir, "images"))
                   if name.endswith(".png") and args.start <= int(os.path.splitext(name)[0]) < args.stop]
    image_names = sorted(image_names, key=lambda x: int(os.path.splitext(x)[0]))
    if args.random == 'True':
        random.shuffle(image_names)
    if num:
        pbar = get_pbar(len(image_names)).start()
        for i, image_name in enumerate(image_names):
            image_id, ext = os.path.splitext(image_name)
            json_name = "%s.json" % image_name
            if i < num:
                to_dir = first_dir
            elif second_dir:
                to_dir = second_dir
            else:
                pbar.update(i)
                continue

            subdirs = ['images', 'annotations', 'questions']
            if args.label == 'True':
                subdirs.append('imagesReplacedText')
            for subdir in subdirs:
                folder_path = os.path.join(to_dir, subdir)
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
            if args.skip_images == 'False':
                subdirs = ['images']
                if args.label == 'True':
                    subdirs.append('imagesReplacedText')
                for subdir in subdirs:
                    _copy(data_dir, to_dir, image_name, subdir=subdir)
            _copy(data_dir, to_dir, json_name, subdir='annotations')

            if args.label == 'True':
                _copy(data_dir, to_dir, json_name, subdir='questions')
            else:
                question_path = os.path.join(data_dir, 'questions', json_name)
                if os.path.exists(question_path):
                    question_json = json.load(open(question_path, 'rb'))
                    keys = question_json['questions'].keys()
                    for key in keys:
                        if question_json['questions'][key]['abcLabel']:
                            del question_json['questions'][key]
                    json.dump(question_json, open(os.path.join(to_dir, 'questions', json_name), 'wb'))
            pbar.update(i)
        pbar.finish()
    else:
        raise Exception()

    _copy(data_dir, first_dir, "categories.json")
    _copy(data_dir, second_dir, "categories.json")


if __name__ == "__main__":
    ARGS = get_args()
    split_dqa(ARGS)
