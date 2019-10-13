# Transfer learning on traffic sign detection using limited data

### TODO
- [x] Setup an aws EC2 instance
- [x] Download and prepare the GTSDB dataset 
- [ ] Train the YOLO network

---

## Part 1: Data Preparation

First, download the GTSDB dataset.

```bash
sh data_preparation/download_gtsdb.sh
```

To use the darknet framework, the dataset needs to be converted to the right format, for that use the `generate_darknet_data.py` script.

```bash
sh data_preparation/darknet/prepare_gtsdb.sh
```

You can seamlessly change the number of classes that you want to work with. This will change all the necessary files. You can pick between three options:
- 43: all sign classes
- 4: all sign categories
- 1: all signs

```bash
sh data_preparation/darknet/switch_classes.sh 4
```

The data folder structure is as follows
## Recommended Directory Structure for Training and Evaluation

```
+ data
  + raw
    + FullIJCNN2013
  + processed
    + darknet
      + obj
      + obj.names
      + obj.data
      + train.txt
      + test.txt
```
## Part 2: Training
`[WIP]`
