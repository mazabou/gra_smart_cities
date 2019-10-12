python3 generate_darknet_data.py -i data/raw/FullIJCNN2013 -o data/processed/darknet
ls data/raw/FullIJCNN2013 | grep .ppm | head -n 600 > data/processed/darknet/train.txt 
ls data/raw/FullIJCNN2013 | grep .ppm | tail -n 300 > data/processed/darknet/test.txt