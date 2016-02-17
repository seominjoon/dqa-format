import argparse
import json
import os
import shutil

import progressbar as pb

from text2int import text2int

parser = argparse.ArgumentParser()
parser.add_argument("root_dir")
parser.add_argument("out_dir")
parser.add_argument("--download_url", default="https://s3-us-west-2.amazonaws.com/ai2-vision-datasets/shining3/shining3_allquestions.zip")
parser.add_argument("--data_subtype", default="all")
parser.add_argument("--data_type", default="shining3")
parser.add_argument("--task_type", default="MultipleChoice")
parser.add_argument("--num_choices", default=4, type=int)
parser.add_argument("--valid_exts", default=".png,.jpg")
parser.add_argument("--zfill_width", default=12, type=int)
# parser.add_argument("--text2int", default=False, type=bool)  # not supported yet

ARGS = parser.parse_args()

def main(args):
    root_dir = args.root_dir
    out_dir = args.out_dir
    images_dir = os.path.join(root_dir, "images")
    questions_dir = os.path.join(root_dir, "questions")
    out_images_dir = os.path.join(out_dir, args.data_subtype)
    out_questions_json_path = os.path.join(out_dir, "%s_%s_%s_questions.json" % (args.task_type, args.data_type, args.data_subtype))
    out_annotations_json_path = os.path.join(out_dir, "%s_%s_annotations.json" % (args.data_type, args.data_subtype))

    # mkdir
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    if not os.path.exists(out_images_dir):
        os.mkdir(out_images_dir)

    valid_exts = args.valid_exts.split(",")
    print("Valid exts: %s" % ", ".join(valid_exts))

    image_paths = [os.path.join(images_dir, image_name) for image_name in os.listdir(images_dir)
                   if os.path.isfile(os.path.join(images_dir, image_name)) and os.path.splitext(image_name)[1] in valid_exts]
    out_questions_dict = {'num_choices': args.num_choices,
                          'questions': []}
    out_annotations_dict = {'annotations': []}

    question_id = 0
    string = "N=%d|" % len(image_paths)
    pbar = pb.ProgressBar(widgets=[string, pb.Percentage(), pb.Bar(), pb.ETA()], maxval=len(image_paths))
    pbar.start()
    for idx, image_path in enumerate(image_paths):
        image_name = os.path.basename(image_path)
        image_id, image_ext = os.path.splitext(image_name)
        out_image_name = "%s_%s_%s%s" % (args.data_type, args.data_subtype, str(image_id).zfill(12), image_ext)
        out_image_path = os.path.join(out_images_dir, out_image_name)
        shutil.copy(image_path, out_image_path)

        question_json_path = os.path.join(questions_dir, "%s.json" % image_name)
        if os.path.exists(question_json_path):
            question_json = json.load(open(question_json_path, "rb"))
            assert question_json['imageName'] == image_name, "image names for %s do not match" % image_name
            for question, answer_dict in question_json['questions'].iteritems():
                abcLabel = answer_dict['abcLabel']
                choices = answer_dict['answerTexts']
                assert len(choices) == args.num_choices, "number of choices should be %d!" % num_choices
                """
                if args.text2int:
                    question = text2int(question)
                    choices = [text2int(choice) for choice in choices]
                """
                answer = choices[answer_dict['correctAnswer']]

                out_question_dict = {'question_id': question_id,
                                     'image_id': image_id,
                                     'question': question,
                                     'multiple_choices': choices,
                                     }
                out_questions_dict['questions'].append(out_question_dict)

                out_annotation_dict = {'question_id': question_id,
                                       'image_id': image_id,
                                       'multiple_choice_answer': answer}
                out_annotations_dict['annotations'].append(out_annotation_dict)
                question_id += 1
        pbar.update(idx)
    pbar.finish()
    print("num images = %d, num questions = %d" % (len(image_paths), len(out_questions_dict['questions'])))

    print("Dumping json files ...")
    json.dump(out_questions_dict, open(out_questions_json_path, "wb"))
    json.dump(out_annotations_dict, open(out_annotations_json_path, "wb"))

if __name__ == "__main__":
    main(ARGS)




