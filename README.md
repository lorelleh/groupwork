# AAE5303 groupwork
## Visual Odometry with ORB-SLAM3
This repository contains the implementation and analysis of monocular visual odometry using the ORB-SLAM3 framework on the HKisland_GNSS03 UAV aerial imagery dataset.

---

### Key Results
| Metric | Value | Description |
|--------|-------|-------------|
| ATE RMSE | 1.373 m | Global accuracy after Sim(3) alignment |
| RPE Trans Drift | 4.02 m/m | Translation drift rate (delta=10 m) |
| RPE Rot Drift | 147.83 deg/100m | Rotation drift rate (delta=10 m) |
| Completeness | 4.81% | Matched poses / total ground-truth poses |

---

### Introduction
ORB-SLAM3 is a state-of-the-art visual SLAM system capable of monocular, stereo, and visual-inertial odometry.

This assignment focuses on Monocular VO mode, which:
- Uses only camera images for pose estimation
- Enables 6-DoF trajectory tracking without GPS/IMU
- Is robust to dynamic objects and illumination changes

---

# 2.UNet Semantic Segmentation 
## 2.1. Overview
This experiment implements multi-class semantic segmentation using the **PyTorch UNet** framework on the AMtown dataset.
- Dataset: AMtown (26 classes)
- Training set: splits 01 + 03
- Test set: split 02
- Image scale: 0.5
- Model: UNet (n_channels=3, n_classes=26, bilinear=False)
- Optimizer: AdamW
- Loss: CrossEntropyLoss + DiceLoss (weighted fusion)

## 2.2. Hyperparameters
```python
SCALE = 0.5
BATCH_SIZE = 2
EPOCHS = 10
LEARNING_RATE = 2e-4
VAL_PERCENT = 0.1
NUM_CLASSES = 26
USE_AMP = True
```

## 2.3. Evaluation Metrics
- **mIoU (mean Intersection over Union)**: Average IoU across all valid classes
- **mean Dice**: Mean Dice similarity coefficient for region overlap
- **FWIoU (Frequency Weighted IoU)**: IoU weighted by class pixel frequency
- **Pixel Accuracy**: Overall pixel-wise classification accuracy

## 2.4. Results
### 2.4.1 Overall Performance
| Metric | With Background | Without Background |
|--------|-----------------|---------------------|
| mean IoU | 0.8297 | 0.8248 |
| mean Dice | 0.8906 | 0.8866 |
| Pixel Accuracy | 0.9775 | 0.9775 |
| **FWIoU** | **0.9580** | — |

### 2.4.2 Per-class Results (Valid Classes Only)
ID | Class | IoU | Dice
---|-------|-----|------
0 | background | 0.8975 | 0.9460
1 | - | 0.9479 | 0.9732
2 | - | 0.9272 | 0.9622
3 | - | 0.9493 | 0.9740
5 | - | 0.7346 | 0.8470
6 | - | 0.8830 | 0.9378
13 | - | 0.9791 | 0.9894
14 | - | 0.9618 | 0.9805
15 | - | 0.9260 | 0.9616
16 | - | 0.7429 | 0.8525
17 | - | 0.9441 | 0.9713
19 | - | 0.9676 | 0.9836
20 | - | 0.6403 | 0.7807
24 | - | 0.7261 | 0.8413
25 | - | 0.2179 | 0.3579

### 2.4.3 Empty / Non-predicted Classes
Classes 4, 7, 8, 9, 10, 11, 12, 18, 21, 22, 23 have no valid samples or predictions (IoU/Dice = 0.0).

## 2.5. Conclusion
1. The UNet model achieves strong overall segmentation performance: **mIoU ≈ 83%, mean Dice ≈ 89%, FWIoU ≈ 95.8%**.
2. Most major classes have IoU > 90%, indicating stable segmentation.
3. Classes 20, 24, and 25 show relatively low accuracy and require more data, augmentation, or loss weighting.
4. A large number of empty classes exist; class merging or removal is recommended for future simplification.

#Appendix
### 🔗 Access to Model Weights

All trained model checkpoints are hosted externally due to GitHub's file size limits.
- Download link: https://drive.google.com/drive/folders/1zsZdff4LPjpMcnU846Pm7wCTq5qtn5OS?usp=sharing
- File list:
  - `checkpoint_epoch1.pth` ~ `checkpoint_epoch10.pth`
- Place the downloaded files into the `checkpoints/` folder in your local copy of the repository.
---

## 3D Reconstruction
*(To be completed by the 3D Reconstruction module team)*



