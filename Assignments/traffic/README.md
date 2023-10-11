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
Performance slightly increased as a result.
- Loss: 0.1392
- Accuracy: 0.9685

## model_d
Model D doubled the neurons used in the dense layer from 128 to 256. Accuracy actually decreased.
- Loss: 0.2181
- Accuract: 0.9506

## model_e
Model E halved the neurons used in the dense layer from 128 to 64. Similar performance to model_d
- Loss: 0.1316
- Accuracy: 0.9506

## model_f
Model F was trained on 20 epochs instead of 10. As expected performance did increase but not as much as I thought.
- Loss: 0.1257
- Accuracy: 0.9757

## model_g
Model G was trained on 5 epochs instead of 10. Performance similar to model_c
- Loss: 0.1323
- Accuracy: 0.9664

## model_h
Model H used a 3x3 pooling matrix instead of the standard 2x2 and a 2x2 kernel matrix instead of 3x3. 
Loss value was not great.
- Loss 0.3048
- 0.9085