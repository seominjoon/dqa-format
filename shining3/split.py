import argparse
import json
import os
import copy

parser = argparse.ArgumentParser()
parser.add_argument("questions_path")
parser.add_argument("annotations_path")
parser.add_argument("--subtype", default='all')
parser.add_argument("--first_name", default='train')
parser.add_argument("--second_name", default='test')
parser.add_argument('--ratio', default=0.7, type=float)

ARGS = parser.parse_args()


def main(args):
    questions_path = args.questions_path
    annotations_path = args.annotations_path
    subtype = args.subtype
    first_name = args.first_name
    second_name = args.second_name
    ratio = args.ratio

    first_questions_path = os.path.join(os.path.dirname(questions_path), os.path.basename(questions_path).replace(subtype, first_name))
    first_annotations_path = os.path.join(os.path.dirname(annotations_path), os.path.basename(annotations_path).replace(subtype, first_name))
    second_questions_path = os.path.join(os.path.dirname(questions_path), os.path.basename(questions_path).replace(subtype, second_name))
    second_annotations_path = os.path.join(os.path.dirname(annotations_path), os.path.basename(annotations_path).replace(subtype, second_name))

    print("loading json files ...")
    questions = json.load(open(questions_path, 'rb'))
    annotations = json.load(open(annotations_path, 'rb'))

    split_idx = int(ratio * len(questions['questions']))

    print("making copies ...")
    first_questions = copy.deepcopy(questions)
    first_questions['questions'] = first_questions['questions'][:split_idx]
    first_annotations = copy.deepcopy(annotations)
    first_annotations['annotations'] = first_annotations['annotations'][:split_idx]
    second_questions = copy.deepcopy(questions)
    second_questions['questions'] = second_questions['questions'][split_idx:]
    second_annotations = copy.deepcopy(annotations)
    second_annotations['annotations'] = second_annotations['annotations'][split_idx:]

    print("Split: %s = %d, %s = %d" % (first_name, len(first_questions['questions']), second_name, len(second_questions['questions'])))

    print("dumping json files ...")
    json.dump(first_questions, open(first_questions_path, 'wb'))
    json.dump(first_annotations, open(first_annotations_path, 'wb'))
    json.dump(second_questions, open(second_questions_path, 'wb'))
    json.dump(second_annotations, open(second_annotations_path, 'wb'))

if __name__ == "__main__":
    main(ARGS)
