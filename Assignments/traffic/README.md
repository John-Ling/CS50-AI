# Tests and Results

## model_a

Model A was trained using minimal parameters used in the example in CS50 AI. It performed incredibly
badly. Like really badly. I retested by converting all photos to grayscale since the network only used 1 convolution however
the performance was not improved. 
- Loss: 3.4997
- Accuracy: 0.0566

## model_b
Model B had 3 identical convolution and pooling layers instead of just 1 that model A used. Performance was much better.
- Loss: 0.23
- Accuracy: 0.9418

## model_c
Model C followed recommendations from Tensorflow and set the number of nodes two convolution layers as 64 instead of 32.
Performance increased as a result.
- Loss: 0.1392
- Accuracy: 0.9685