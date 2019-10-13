import re
import argparse
import os
import glob
from collections import defaultdict

import pandas as pd
from PIL import Image
from tqdm import tqdm


parser = argparse.ArgumentParser(description='Prepare GTSDB for using the darknet framework.')
parser.add_argument('--raw_data_dir', '-i', type=str, required=True,
                     help='Raw data directory.')
parser.add_argument('--darknet_data_dir', '-o', type=str, required=True,
                     help='Directory where data will be generated.')

args = parser.parse_args()
args.raw_data_dir = os.path.abspath(args.raw_data_dir)
args.darknet_data_dir = os.path.abspath(args.darknet_data_dir)

pC = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 15, 16]
mC = [33, 34, 35, 36, 37, 38, 39, 40]
dC = [11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
sign_category_dict = defaultdict(lambda:3)
for category_id, sign_ids in enumerate([pC, mC, dC]):
    sign_category_dict.update({sign_id:category_id for sign_id in sign_ids})

def generate_obj_names():
    print('Generating obj.names file.')

    # load the readme file which contains all class names
    readme_file = os.path.join(args.raw_data_dir, 'ReadMe.txt')
    with open(readme_file, 'r') as f:
        lines = f.readlines()

    # use a regex pattern to filter out misc. lines and extract class names
    extract_class_pattern = re.compile(r'^\d{1,2}\s\=\s(.*)\n')
    extract_class_name = lambda l: re.search(extract_class_pattern, l)
    class_names = [captured.group(1) for captured in map(extract_class_name, lines) if captured is not None]

    # write class names to file
    obj_names_file = os.path.join(args.darknet_data_dir, 'obj.names.43')
    with open(obj_names_file, 'w') as f:
        f.write('\n'.join(class_names))

    # write category names to file
    category_names_file = os.path.join(args.darknet_data_dir, 'obj.names.4')
    with open(category_names_file, 'w') as f:
        f.write('\n'.join(['prohibatory', 'mandatory', 'danger', 'other']))

    sign_names_file = os.path.join(args.darknet_data_dir, 'obj.names.1')
    with open(sign_names_file, 'w') as f:
        f.write('sign\n')

def generate_obj_files():
    print('Generating annotation file.')

    # get file list
    files = glob.glob(os.path.join(args.raw_data_dir, "*.ppm"))

    # load csv files containing annotation data
    gt_file = os.path.join(args.raw_data_dir, "gt.txt")
    df = pd.read_csv(gt_file, index_col=0 , sep=';', names=['file', 'xmin', 'ymin', 'xmax', 'ymax', 'class'])
    df['category'] = df.apply(lambda x: sign_category_dict[x['class']], axis=1)

    # create obj/ dir if it doesn't exist
    for folder in ['obj', 'obj.43', 'obj.4', 'obj.1']:
        obj_dir = os.path.join(args.darknet_data_dir, folder)
        os.makedirs(obj_dir, exist_ok=True)

    for file in tqdm(files):
        # note that the dataframe index is the filename (multiple rows can have the same index)
        # there can be multiple bounding boxes (defined by a row) for a single image (defined by the index)

        idx = os.path.basename(file)
        # save image in the jpeg format
        img = Image.open(file)
        img_filename = os.path.join(args.darknet_data_dir, 'obj', idx[:-4]+'.jpg')
        img.save(img_filename)

        annotation_filename = os.path.join(args.darknet_data_dir, '%s', idx[:-4]+'.txt')
        img_width, img_height = img.size
        
        bounding_boxes_43, bounding_boxes_4, bounding_boxes_1 = [], [], []
        if idx in df.index:
            for _, bb in df.loc[[idx]].iterrows():
                xmin, ymin, xmax, ymax, class_id, category_id = bb 

                # compute the new "darknet" annotations
                x_center = (xmin + xmax) / 2. / img_width
                y_center = (ymin + ymax) / 2. / img_height
                bb_width = (xmax - xmin) / img_width
                bb_height = (ymax - ymin) / img_height

                # <object-class> <x_center> <y_center> <width> <height>
                bb_annotation_43 = ' '.join(map(str, [class_id, x_center, y_center, bb_width, bb_height]))
                bb_annotation_4 = ' '.join(map(str, [category_id, x_center, y_center, bb_width, bb_height]))
                bb_annotation_1 = ' '.join(map(str, [0, x_center, y_center, bb_width, bb_height]))
                bounding_boxes_43.append(bb_annotation_43)
                bounding_boxes_4.append(bb_annotation_4)
                bounding_boxes_1.append(bb_annotation_1)

        # save the sample's annotation file
        for folder, bounding_boxes in zip(['obj.43', 'obj.4', 'obj.1'], 
                                          [bounding_boxes_43, bounding_boxes_4, bounding_boxes_1]):
            with open(annotation_filename %folder, 'w') as f:
                f.write('\n'.join(bounding_boxes))

def main():
    generate_obj_names()
    generate_obj_files()

if __name__ == '__main__':
    main()
