# HandGestureRecognition



Abstract : in this project I propose a method to classify hand gesture recognition based on feature extraction followed by a SVM classifier. A well known method to perform hand gesture recognition is to use the convexity defects.This method performs well to classify number gestures (1,2,3,,5) 

Number gestures  ( source : [1] )

However it is not relevant when it comes to more complex gestures. For example such an algorithm is not able to differentiate a “two” from a “spoke”.


Spoke gesture

I propose an algorithm which uses convexity deflects in combination with other features to classify some predefined gestures namely : 


Motivation : hand gesture recognition can have several real-life implications. A first one would be to give a computer the ability to understand sign language, and thus to create translation or sign to speech algorithms. Another application could be to give users the ability to control machines by hand gestures in a “Kinect”-style.






Problem definition : we want to recognize 7 predefined hand gestures namely : 



To do so, we want to train a SVM classifier by feeding it with some manually constructed features. 
We are going to use the notion of convexity defects which implies the notion of convex hull.
The convex hull given a set of points, the convex hull is the smallest convex set of points that contains all the points.


Convex hull (source : Wikipedia)

Once we find the convex hull we can define the convexity defect points. Given a set of points ( a contour for example ) and its convexity hull any deviation of the contour from its convex hull is a convexity defect. However all of them are not relevant, only the maximum  convexity defect points are interesting in our application. A maximum  convexity defect is a convexity defect whose distance to the contour is a local maximum. For simplicity let’s however call this set of points convexity defects.


Convexity defects are drawn in red (source : theailearner.com)


Related work :

The method of  “convexity defects” to recognize signs is well know in the litterature, in particular the paper [1] “ Hand-gesture recognition using computer-vision techniques” by Rios-Soria & Schaeffer & Garza-Villarreal released in 2013 provides an effective overview of the method. I used this method as a base for my algorithm and tried to add few other features to simply enhance the capabilities of the algorithm.

Methodology : 

Features

The method I propose is to use a SVM classifier trained with hand-crafted features.
Those features are : 

“CONVEXITY DEFECTS” : the number of maximal convexity defects detected
“MAX DISTANCE” : the maximum distance from the convexity defects to the contour
“MAX ANGLE” : the maximum angle between the barycentre of the contour and the convexity defects
“TIGHTNESS” : the ratio ( area of the mask) over ( area of the convex hull )
“PEAKS” : the number of peaks detected the contour of the mask


Each of these features individually do not have enough discriminating power to differentiate "complex" gestures. Nevertheless their union makes it possible to achieve respectable results.




Features extraction 

Convexity defects 

Finding convexity defects is the more time-consuming feature extraction in the algorithm.

Segmentation

The first step is to compute a segmentation of the hand. The most common method used in the litterature for this use case is the HSV color segmentation. The reasons for this are simple, often hand gesture recognition is performed with a fixed camera on a fixed background of fixed colour. Chances are that the hand of the user is of a different color than the background. The HSV space makes it very simple to segment part of the image according to their color. A calibration is to be made to find the exact color of the hand and how it diverges from background. It can be as simple as asking the user to show his hand in a defined region in order to capture the HSV code of the hand. In my case I achieved good results by setting a low threshold at (0,0,0) and a high threshold at (22 , 83, 222) in open-cv scale HSV space. Once we have the mask we can downsample it to make the next steps easier, I chose to downsample to a 256x256 mask.


HSV segmentation

Find edges

The next step is to find the edges of the mask. To do so I used a scratch Canny Edge detector.



From edges to contour
A crucial point in finding convexity defects is to have an order contour, which means when iterating over the contour the next point is a direct neighbour of the current point. It is not the case currently as the canny edge detector is not designed to order the points. To do so I create a distance matrix between all points and iterate over the points in order of the nearest neighbours.


Convex hull

The point of having a sorted contour is that we can now apply the “Jarvis Walk'' algorithm (aka the gift wrapping algorithm) to find the convex hull. My implementation of this algorithm is the following :
 
 Start from the western point add it to the list of convexity hull points

Find the “more counter-clockwise” point with respect to the current point, it becomes the next point add it to the list of convexity hull points

Repeat 2) until the next point is the western point


Results of the Jarvis Walk

e) Find convexity defects

Given a contour and a convexity hull we can find convexity defects by looking at the maximum divergence of contour from convex hull between two consecutive convex hull points.


Distance of every contour point (mapped from yellow to dark blue) between two consecutive convex hull points (cyan) and detected convexity point (green)


 If we do so for every pair of convex hull points, this is what we get as a result : 

Convexity defects not filtered

As we can see a lot of detected convexity points are not relevant. This is because some convex hull points are very close to each other especially around  smooth angles like fingertips. We have to perform a non maximum suppression step. To perform this non-maximum suppression step I chose a distance criterion where a convexity defect is kept if and only if its distance to the convex hull is greater than a threshold T. This threshold is set to ⅕ of the length of the hand as recommended in the paper [2]. It has proven to provide good results with my experimental data.


Convexity defects filtered by height

We now have a correct convexity defect extractor.
This method is relatively efficient for “number” gesture recognition and can be used to count fingers : number of convexity defects +1.






Counting fingers with convexity defects

However this method can not differentiate a “Shaka” from a “Spoke” or a “Rock”. If we want our classifier to perform well on these “complex” gestures we need to provide it more features.

Max distance 

While executing the non maximum suppression step for each frame we keep in memory the largest distance from the convex hull to the contour (between two consecutive convex hull points). We are going to use this distance as an additional feature

Max angle
 
Once we have found the convexity defects, we compute the angle formed by the origin point (0,0) the barycenter of the contour and each convexity defect point. We keep in memory the largest angle. We are going to use this angle as an additional feature.

Tightness 

To compute the “Tightness”, we compute the area of the mask, the area of the convex hull and compute the ratio between those two value.

Tightness representation for “five”

Tightness representation for “fist”

Peaks

The last feature I extract from the frame is the “PEAKS” features. It represents the number of “peaks” in the contour. The idea is to think the contour as : y as a function of x. We compute the gradient with respect to x and smooth it with a Savitzky-Golay. Then we count the local maximums in the plot and use this number as an additional feature in the model.






Training and evaluation

To train my model I built a dataset composed of :
A training set of 15 photos with different angle/scale for each class
A test set of 5 photos with different angle/scale for each class

I trained a CSVM with a gaussian kernel and a grid search hyperparameter tuning by cross validation. The best hyperparameter found were : 
C : 1
gamma : 1

Training set score for SVM: 0.980952
Testing  set score for SVM: 1.000000

The model achieves perfect results on the test dataset. This is not surprising as this dataset is not very challenging but yet this proves that the method is promising. 

Finally I tested this algorithm on a live video sequence. The actual implementation is not optimized for live stream and only allows a debit of around 1 frame per second.
The algorithm classifies correctly every still gesture. 






Result of the algorithm on a live video



Conclusion :
The proposed algorithm combines a well known feature when it comes to hand gesture recognition to other interesting features. By adding those simple features to the model we can considerably enhance the performance of the algorithm. While the “convexity defect” detector can only classify “number gesture” the proposed classifier can be trained on several other “complex” gestures. The proposed classifier has shown great robustness when it comes to differentiate close gestures such as “Spoke”,“Peace” and “Rock”.

The classifier would for sure benefit from a larger and more diverse dataset, but still the method looks promising. Next step would be to build a better dataset, train the model on more classes and optimise the performance in terms of execution time to allow live streaming.

References :

[1]  Hand-gesture recognition using computer-vision techniques by Rios-Soria & Schaeffer & Garza-Villarreal
[2] Hand Gesture Recognition Based on Convex Defect Detection

