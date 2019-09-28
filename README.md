# Transfer learning on traffic sign detection using limited data

### TODO
- [x] Setup an aws EC2 instance
- [x] Download and prepare the GTSDB dataset 
- [ ] Train the YOLO network

---

## Part 1: Data Preparation

First, download the GTSDB dataset.

```bash
sh download_gtsdb.sh
```

To use the darknet framework, the dataset needs to be converted to the right format, for that use the `generate_darknet_data.py` script.

```bash
sh prepare_gtsdb.sh
```

`TODO`: Find the official train/test split to ensure coherence when comparing different network's validation scores.

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
