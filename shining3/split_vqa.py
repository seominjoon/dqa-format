import argparse
import json
import os
import copy

parser = argparse.ArgumentParser()
parser.add_argument("root_dir")
parser.add_argument("first_dir")
parser.add_argument("second_dir")
parser.add_argument("--questions_name", default='questions.json')
parser.add_argument("--annotations_name", default='annotations.json')
parser.add_argument("--second_name", default='test')
parser.add_argument('--ratio', default=0.7, type=float)

ARGS = parser.parse_args()


def main(args):
    questions_path = os.path.join(args.root_dir, args.questions_name)
    annotations_path = os.path.join(args.root_dir, args.annotations_name)
    ratio = args.ratio

    first_questions_path = os.path.join(args.first_dir, 'questions.json')
    first_annotations_path = os.path.join(args.first_dir, 'annotations.json')
    second_questions_path = os.path.join(args.second_dir, 'questions.json')
    second_annotations_path = os.path.join(args.second_dir, 'annotations.json')

    if not os.path.exists(args.first_dir):
        os.mkdir(args.first_dir)
    if not os.path.exists(args.second_dir):
        os.mkdir(args.second_dir)

    print("loading json files ...")
    questions = json.load(open(questions_path, 'rb'))
    annotations = json.load(open(annotations_path, 'rb'))

    split_idx = int(ratio * len(questions['questions']))

    # Very inefficient copying now ...
    print("making copies ...")
    first_questions = copy.deepcopy(questions)
    first_questions['questions'] = questions['questions'][:split_idx]
    first_annotations = copy.deepcopy(annotations)
    first_annotations['annotations'] = annotations['annotations'][:split_idx]
    second_questions = copy.deepcopy(questions)
    second_questions['questions'] = questions['questions'][split_idx:]
    second_annotations = copy.deepcopy(annotations)
    second_annotations['annotations'] = annotations['annotations'][split_idx:]

    print("Split: first = %d, second = %d" % (len(first_questions['questions']), len(second_questions['questions'])))

    print("dumping json files ...")
    json.dump(first_questions, open(first_questions_path, 'wb'))
    json.dump(first_annotations, open(first_annotations_path, 'wb'))
    json.dump(second_questions, open(second_questions_path, 'wb'))
    json.dump(second_annotations, open(second_annotations_path, 'wb'))

if __name__ == "__main__":
    main(ARGS)
