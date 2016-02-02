import json
import os
import urllib

import argparse
from progress.bar import Bar

parser = argparse.ArgumentParser()
parser.add_argument('--task_type', default='MultipleChoice')
parser.add_argument('--data_type', default='shining')
parser.add_argument('--data_subtype', default='train1')
parser.add_argument('--download', default=False, type=bool)
parser.add_argument('raw_file_path')
parser.add_argument('q_dir_path')
parser.add_argument('a_dir_path')
parser.add_argument('raw_dir_path')
parser.add_argument('--image_dir_path', default='.')

ARGS = parser.parse_args()


def format_json(args):
    # transform raw json file (set1.json) to json format required for VQA eval
    raw = json.load(open(args.raw_file_path, 'rb'))
    q, a = {}, {}
    questions, annotations = [], []

    info = {}
    num_choices = 4
    task_type = args.task_type
    data_type = args.data_type
    license = {}
    data_subtype = args.data_subtype
    q['info'] = info
    q['num_choices'] = num_choices
    q['task_type'] = task_type
    q['data_type'] = data_type
    q['license'] = license
    q['data_subtype'] = data_subtype
    q['questions'] = questions

    a['info'] = info
    a['data_type'] = data_type
    a['data_subtype'] = data_subtype
    a['annotations'] = annotations

    q_json_name = "%s_%s_%s_questions.json" % (task_type, data_type, data_subtype)
    a_json_name = "%s_%s_%s_annotations.json" % (task_type, data_type, data_subtype)
    q_file_path = os.path.join(args.q_dir_path, q_json_name)
    a_file_path = os.path.join(args.a_dir_path, a_json_name)


    urls = []
    for r in raw:
        image_url = r['URL']
        pid = r['pid']
        question = r['Question']
        choice_1 = r['Choice 1']
        choice_2 = r['Choice 2']
        choice_3 = r['Choice 3']
        choice_4 = r['Choice 4']
        correct_choice = r['Correct Choice']

        inputs = [image_url, pid, question, choice_1, choice_2, choice_3, choice_4, correct_choice]
        if any(len(i) == 0 for i in inputs):
            continue

        image_name = os.path.basename(image_url)
        image_id = int(os.path.splitext(image_name)[0])
        question_id = int(pid)
        multiple_choices = [choice_1, choice_2, choice_3, choice_4]
        answer_type = 'other'  # dummy
        multiple_choice_answer = multiple_choices[int(correct_choice)-1]
        question_type = 'what'  # dummy

        qq = {'image_id': image_id, 'question_id': question_id, 'question': question,
            'multiple_choices': multiple_choices}
        aa = {'image_id': image_id, 'question_id': question_id, 'question_type': question_type,
            'multiple_choice_answer': multiple_choice_answer, 'answer_type': answer_type}
        questions.append(qq)
        annotations.append(aa)
        urls.append(image_url)

    if args.download:
        image_folder_path = os.path.join(args.image_dir_path, "%s_%s_images" % (data_type, data_subtype))
        if not os.path.exists(image_folder_path):
            os.mkdir(image_folder_path)
        bar = Bar('Downloading images', max=len(urls))
        for url in urls:
            raw_image_name = os.path.basename(url)
            image_id = int(os.path.splitext(raw_image_name)[0])
            image_name = "%s_%s_%s.png" % (data_type, data_subtype, str(image_id).zfill(12))
            urllib.urlretrieve(url, os.path.join(image_folder_path, image_name))
            bar.next()
        bar.finish()

    json.dump(q, open(q_file_path, 'wb'))
    json.dump(a, open(a_file_path, 'wb'))

def format_json_raw(args):
    # transform raw json file (set1.json) to json format required for VQA eval
    raw = json.load(open(args.raw_file_path, 'rb'))
    questions = []

    info = {}
    num_choices = 4
    task_type = args.task_type
    data_type = args.data_type
    license = {}
    data_subtype = args.data_subtype

    q_json_name = "%s_%s_%s_questions.json" % ('raw', data_type, data_subtype)
    q_file_path = os.path.join(args.q_dir_path, q_json_name)

    image_folder_path = os.path.join(args.image_dir_path, "%s_%s_images" % (data_type, data_subtype))
    if args.download and not os.path.exists(image_folder_path):
        os.mkdir(image_folder_path)

    urls = []
    for r in raw:
        image_url = r['URL']
        pid = r['pid']
        question = r['Question']
        choice_1 = r['Choice 1']
        choice_2 = r['Choice 2']
        choice_3 = r['Choice 3']
        choice_4 = r['Choice 4']
        correct_choice = r['Correct Choice']

        inputs = [image_url, pid, question, choice_1, choice_2, choice_3, choice_4, correct_choice]
        if any(len(i) == 0 for i in inputs):
            continue

        raw_image_name = os.path.basename(image_url)
        image_id = int(os.path.splitext(raw_image_name)[0])
        image_name = "%s_%s_%s.png" % (data_type, data_subtype, str(image_id).zfill(12))
        image_path = os.path.join(image_folder_path, image_name)
        question_id = int(pid)
        multiple_choices = [choice_1, choice_2, choice_3, choice_4]
        answer_type = 'other'  # dummy
        multiple_choice_answer = multiple_choices[int(correct_choice)-1]
        question_type = 'what'  # dummy

        qq = {'img_path': image_path, 'ques_id': question_id, 'question': question,
              'MC_ans': multiple_choices, 'ans': multiple_choice_answer}
        questions.append(qq)
        urls.append(image_url)
    json.dump(questions, open(q_file_path, 'wb'))

if __name__ == "__main__":
    format_json(ARGS)
    format_json_raw(ARGS)

