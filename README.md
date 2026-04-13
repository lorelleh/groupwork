# AAE5303 groupwork
## 1.Visual Odometry with ORB-SLAM3
This repository contains the implementation and analysis of monocular visual odometry using the ORB-SLAM3 framework on the HKisland_GNSS03 UAV aerial imagery dataset.

---

### 1.1. Key Results
| Metric | Value | Description |
|--------|-------|-------------|
| **ATE RMSE** | **2.8163 m** | Global accuracy after Sim(3) alignment (scale corrected)  |
| **RPE Trans Drift** | **1.6177 m/m** | Translation drift rate (mean error per meter, delta=10 m) |
| **RPE Rot Drift** | **111.6816 deg/100m** | Rotation drift rate (mean angle per 100 m, delta=10 m) |
| **Completeness** | **97.19%** | Matched poses / total ground-truth poses (1900 / 1955) |
| **Estimated poses** | **2,198** | Trajectory poses in `CameraTrajectory.txt` |

---

### 1.2. ORB Feature Extraction Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `nFeatures` | 1500 | Features per frame |
| `scaleFactor` | 1.2 | Pyramid scale factor |
| `nLevels` | 8 | Pyramid levels |
| `iniThFAST` | 15 | Initial FAST threshold |
| `minThFAST` | 5 | Minimum FAST threshold |

---

### 1.3. Evaluation Results

```
================================================================================
VISUAL ODOMETRY EVALUATION RESULTS
================================================================================

Ground Truth: RTK trajectory (1,955 poses)
Estimated:    ORB-SLAM3 camera trajectory (2,198 poses)
Matched Poses: 1,900 / 1,955 (97.19%)  ← Completeness

METRIC 1: ATE (Absolute Trajectory Error)
────────────────────────────────────────
RMSE:   2.8163 m
Mean:   1 m
Std:    1 m

METRIC 2: RPE Translation Drift (distance-based, delta=10 m)
────────────────────────────────────────
Mean translational RPE over 10 m: 16.3102 m
Translation drift rate:           1.6310 m/m

METRIC 3: RPE Rotation Drift (distance-based, delta=10 m)
────────────────────────────────────────
Mean rotational RPE over 10 m: 10.6715 deg
Rotation drift rate:        106.7148 deg/100m

================================================================================
```

### 1.4. Trajectory Alignment Statistics

| Parameter | Value |
|-----------|-------|
| **Sim(3) scale correction** | 1.0931 |
| **Sim(3) translation** | [-0.2262, -0.9340, 0.2420] m |
| **Association threshold** | \(t_{max\_diff}\) = 0.1 s |
| **Association rate (Completeness)** | 97.19% |

### 1.5. Performance Analysis

| Metric | Value | Grade | Interpretation |
|--------|-------|-------|----------------|
| **ATE RMSE** | 2.82 m | A | Very small global error after alignment, high global accuracy |
| **RPE Trans Drift** | 1.62 m/m | B | Acceptable local translation drift per distance |
| **RPE Rot Drift** | 111.68 deg/100m | C | Moderate rotation drift, no severe orientation error |
| **Completeness** | 97.19% | B | Most poses can be successfully evaluated |

---

### 1.6. Trajectory Comparison

![Trajectory Evaluation](https://github.com/lorelleh/groupwork/blob/dff0b8200b465ca4f50e749d0c8e242a99001ec5/ppt/Trajectory%20Comparison.png)

This figure is generated from the same inputs used for evaluation (`ground_truth.tum` and `CameraTrajectory_sec.tum`) and includes:

1. **Top-Left**: 2D trajectory before alignment (matched poses only). This reveals scale/rotation mismatch typical for monocular VO.
2. **Top-Right**: 2D trajectory after Sim(3) alignment (scale corrected). Remaining discrepancy reflects drift and local tracking errors.
3. **Bottom-Left**: Distribution of ATE translation errors (meters) over all matched poses.
4. **Bottom-Right**: ATE translation error as a function of the matched pose index (highlights where drift accumulates).

**Reproducibility**: the figure can be regenerated using `scripts/evaluate_vo_accuracy.py` (which integrates `evo_ape` functionality) together with the `--save_results` output.

---


## 2.UNet Semantic Segmentation 
### 2.1. Overview
This experiment implements multi-class semantic segmentation using the **PyTorch UNet** framework on the AMtown dataset.
- Dataset: AMtown (26 classes)
- Training set: splits 01 + 03
- Test set: split 02
- Image scale: 0.5
- Model: UNet (n_channels=3, n_classes=26, bilinear=False)
- Optimizer: AdamW
- Loss: CrossEntropyLoss + DiceLoss (weighted fusion)

---

### 2.2. Hyperparameters
```python
SCALE = 0.5
BATCH_SIZE = 2
EPOCHS = 10
LEARNING_RATE = 2e-4
VAL_PERCENT = 0.1
NUM_CLASSES = 26
USE_AMP = True
```

### 2.3. Evaluation Metrics
- **mIoU (mean Intersection over Union)**: Average IoU across all valid classes
- **mean Dice**: Mean Dice similarity coefficient for region overlap
- **FWIoU (Frequency Weighted IoU)**: IoU weighted by class pixel frequency
- **Pixel Accuracy**: Overall pixel-wise classification accuracy

---

### 2.4. Results
#### 2.4.1 Overall Performance
| Metric | With Background | Without Background |
|--------|-----------------|---------------------|
| mean IoU | 0.8297 | 0.8248 |
| mean Dice | 0.8906 | 0.8866 |
| Pixel Accuracy | 0.9775 | 0.9775 |
| **FWIoU** | **0.9580** | — |

#### 2.4.2 Per-class Results (Valid Classes Only)
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

#### 2.4.3 Unet prediction samples
<img width="842" height="674" alt="amtown_unet_prediction_samples" src="https://github.com/user-attachments/assets/194d2241-1b99-4bf3-a4cd-504413904d3b" />

#### 2.4.4 Empty / Non-predicted Classes
Classes 4, 7, 8, 9, 10, 11, 12, 18, 21, 22, 23 have no valid samples or predictions (IoU/Dice = 0.0).

---

### 2.5. Conclusion
1. The UNet model achieves strong overall segmentation performance: **mIoU ≈ 83%, mean Dice ≈ 89%, FWIoU ≈ 95.8%**.
2. Most major classes have IoU > 90%, indicating stable segmentation.
3. Classes 20, 24, and 25 show relatively low accuracy and require more data, augmentation, or loss weighting.
4. A large number of empty classes exist; class merging or removal is recommended for future simplification.

### 2.6 Appendix
🔗 Access to Model Weights

All trained model checkpoints are hosted externally due to GitHub's file size limits.
- Download link: https://drive.google.com/drive/folders/1zsZdff4LPjpMcnU846Pm7wCTq5qtn5OS?usp=sharing
- File list:
  - `checkpoint_epoch1.pth` ~ `checkpoint_epoch10.pth`
- Place the downloaded files into the `checkpoints/` folder in your local copy of the repository.

---

## 3D Reconstruction
*(To be completed by the 3D Reconstruction module team)*



