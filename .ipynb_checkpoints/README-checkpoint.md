# Solution to Comma.AI's speed challenge

### About the challenge
[The challenge](https://github.com/commaai/speedchallenge) is to predict the speed of a car from dashcam footage. Given training data: a video file `train.mp4` of dashcam footage and a `train.txt` file with the velocity of the car in each frame. The task is to generate a `test.txt` file with the velocity of the car in another `test.mp4` video.

### Files
* `preprocess_test.ipynb` - experiments to understand optical flow
* `kfold_sandbox.ipynb` - experiments to find the optimal model
* `2k19.ipynb` - testing on the [comma2k19](https://github.com/commaai/comma2k19) dataset
* `kitti.ipynb` – testing on the [Kitti](http://www.cvlibs.net/datasets/kitti/index.php) dataset
* `combined.ipynb` - testing on both datasets combined
* `final_training.ipynb` - final model is trained on both datasets and `train.mp4` 
* `plot_result.ipynb` - plot and manage the final result
* `caption.py` - play the testing video with the predicted results
* `model.h5` - final model

### Preprocess data
In order to capture the information that is provided “between frames” I used OpenCV and [this tutorial]( https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html) to calculate the optical flow between frames. Before calculating optical flow, the images were croped to a 1:3 aspect ratio. I also investigated brightness augmentation after reading [this article]( https://medium.com/weightsandbiases/predicting-vehicle-speed-from-dashcam-video-f6158054f6fd), but I ultimately got worse results by doing that. My first approach was to have the data preprocess as a separate file and save the optical flow as png/jpg images. However, the compression of the file format removed too much information. I therefore decided to do the data reprocess in the same file as the training.

### The model
Before I trained on the large dataset, I wanted to finalize the architecture of the model. I tried what other people had already built and evaluated the performance. All of these were variations of [Nvidias model for self-driving cars](https://arxiv.org/pdf/1604.07316v1.pdf). An example of a performance comparison: [SpeedNet's](https://github.com/djnugent/SpeedNet) archtechture was discarded with the validation error: (7.8748, 6.5708, 18.3810, 2.2032, 27.6969) as [this archtechture] (https://github.com/abhileshborode/Behavorial-Clonng-Self-driving-cars/blob/master/model.py) got a better result: (5.1863, 2.5656, 17.8168, 2.1441, 21.8460). Un surprisingly, as they were based on the same paper, the models were bad on the same folds.

I used K-fold cross validation to tinker with the parameters and different architectures. In the beginning I got very different results for different folds. I for example noticed that the model was handling low-speed-turns badly. This could be expected because there is a lot of movement even though the car is not moving fast. I decided to gather more data to combat this.

![alt text](https://github.com/lukaspetersson/commaai-speed-challenge/blob/main/different_folds_result.png)
Very different results for different folds.

### comma2k19 dataset

In search for more data I tried to use comma’s own dataset [comma2k19](https://github.com/commaai/comma2k19). However, it turned out that the data was only from a single highway. Since the data had too small variation, the same highway and usually the same speed, the optimizer was unable to converge to a sub-optimal solution. After training on 20% the model the model predicted 19.233625 m/s no matter what the input was.

Instead of discarding the dataset completely I decided to use a part of it (and then combine it with another dataset). The train.mp4 file had an average speed of 12.18 m/s I therefore gathered a part of the dataset that had a mean close to that value. I also discarded all night-time footage. I wrote a simple algorithm that systematically went through the entire dataset and only chose batches that would bring the average speed closer to 12.18 m/s.

### KITTI dataset
In addition to the 2k19 dataset I used the [Kitti dataset](http://www.cvlibs.net/datasets/kitti/index.php). In KITTI one can choose footage from a bunch of different driving types. To get variety to the highway data in 2k19 I choose footage from residential areas and cities. One problem with this dataset is that it is recorded in 10 fps instead of 20. One possible solution to this would be to reduce the other data to 10 fps. However, optical flow calculation works best with higher frame rate. Since only 10% of the frames were from the Kitti dataset, this solution was not used.

### Combined training
The dataset could fit in memory. I therefore trained on smaller batches conating 25000 frames from comma2k19 and 2811 frames form Kitti. To prevent converging to a unoptimal local minima I only trained for 2 epochs. I evaluated the model on `train.mp4`. The result was a MSE of *****.

### Final training
During the final training I once again thrained on the combined dataset, this time without a validation split. Since I did not load `train.mp4` in to memory I could fit more of the other data, I used this to increase the image resolution. Finaly the model was trained on `train.mp4` for 10 epochs.


### References
https://arxiv.org/pdf/1608.01230v1.pdf
https://arxiv.org/pdf/1504.06852.pdf
https://arxiv.org/pdf/1604.07316v1.pdf
https://medium.com/weightsandbiases/predicting-vehicle-speed-from-dashcam-video-f6158054f6fd
https://github.com/ryanchesler/comma-speed-challenge
https://github.com/djnugent/SpeedNet
https://towardsdatascience.com/a-comprehensive-hands-on-guide-to-transfer-learning-with-real-world-applications-in-deep-learning-212bf3b2f27a
https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html
https://github.com/diggs1711/comma-ai-speed-challenge
https://github.com/ckirksey3/steering-prediction-with-keras/blob/master/model.py
https://github.com/abhileshborode/Behavorial-Clonng-Self-driving-cars/blob/master/model.py
