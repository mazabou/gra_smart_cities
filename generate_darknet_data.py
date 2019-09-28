import re
import argparse
import os

import pandas as pd
from PIL import Image
from tqdm import tqdm


parser = argparse.ArgumentParser(description='')
parser.add_argument('--raw_data_dir', '-i', type=str, required=True,
                     help='an integer for the accumulator')
parser.add_argument('--darknet_data_dir', '-o', type=str, required=True,
                     help='an integer for the accumulator')

args = parser.parse_args()

args.raw_data_dir = os.path.abspath(args.raw_data_dir)
args.darknet_data_dir = os.path.abspath(args.darknet_data_dir)

def generate_obj_names():
    print('Generating obj.names file.')
    readme_file = os.path.join(args.raw_data_dir, 'ReadMe.txt')
    with open(readme_file, 'r') as f:
        lines = f.readlines()
    
    extract_class_pattern = re.compile(r'^\d{1,2}\s\=\s(.*)\n')
    extract_class_name = lambda l: re.search(extract_class_pattern, l)
    class_names = [captured.group(1) for captured in map(extract_class_name, lines) if captured is not None]

    obj_names_file = os.path.join(args.darknet_data_dir, 'obj.names')
    with open(obj_names_file, 'w') as f:
        f.write('\n'.join(class_names))

def generate_obj_files():
    print('Generating annotation file.')
    gt_file = os.path.join(args.raw_data_dir, "gt.txt")
    df = pd.read_csv(gt_file, index_col=0 , sep=';', names=['file', 'xmin', 'ymin', 'xmax', 'ymax', 'class'])

    obj_dir = os.path.join(args.darknet_data_dir, "obj")
    os.makedirs(obj_dir, exist_ok=True)

    for idx in tqdm(df.index.unique()):
        # save image in the jpeg format
        img = Image.open(os.path.join(args.raw_data_dir, idx))
        img_filename = os.path.join(obj_dir, idx[:-4]+'.jpg')
        img.save(img_filename)

        # save annotation file
        annotation_filename = os.path.join(obj_dir, idx[:-4]+'.txt')
        img_width, img_height = img.size
        
        bounding_boxes = [] 
        for _, bb in df.loc[[idx]].iterrows():
            xmin, ymin, xmax, ymax, class_id = bb 
            x_center = (xmin + xmax) / 2. / img_width
            y_center = (ymin + ymax) / 2. / img_height
            bb_width = (xmax - xmin) / img_width
            bb_height = (ymax - ymin) / img_height

            # <object-class> <x_center> <y_center> <width> <height>
            bb_annotation = ' '.join(map(str, [class_id, x_center, y_center, bb_width, bb_height]))
            bounding_boxes.append(bb_annotation)

        with open(annotation_filename, 'w') as f:
            f.write('\n'.join(bounding_boxes))

def main():
    generate_obj_names()
    generate_obj_files()

if __name__ == '__main__':
    main()
