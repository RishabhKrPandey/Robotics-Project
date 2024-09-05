Flow of code:
1) Importing the required libraries- cv2,numpy and google.colab.patches
2) I read the image in form of pixels (bgr format).
3) Converted it to grayscale form.
4) Detected the edges using the canny detection method.
5) Found contours and displayed them as a separate image using copy command.
6) Used blur command directly to blur the image by providing an argument for dimensions of the blurring box.
7) Created a mask to aid in detecting the bright spots.
8) Implemented bitwise and command to return 0 (black) values for all pixel values not belonging in the range (200,255) for all dimensions of all pixels.
9) Finally, used the waitkey command to prevent the windows from closing.


Challenges Faced and Solutions:
1) I had to choose colab because I was not able to install the libraries for OpenCV and Jupyter notebook directly into my local machine due to some build dependencies error.
2) I was having error in executing cv2.imshow() which I had to resolve by importing google.colab.patches (Got solution from internet). 
3) Used lower and upper thresholds for mask as [200 200 200] and [255 255 255] but I was getting some bright points towards the lower part of image and therefore increased the lower threshold to [220 220 220].
4) Used the grayscale image for masking but it was giving an error because of the dimensions of threshold values and grayscale image not matching (3 vs 2). I used the original image then. 
