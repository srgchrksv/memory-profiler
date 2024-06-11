# memory-profiler

When processing large datasets it is important to use memory with maximum efficiency.
Or you can get out of RAM, job will not be done and machine can become unresponsive.

### Example of memory usage investigation

Our task is to apply face mesh on each image from a dataset. For face mesh we will use google's mediapipe package. 

*First example is creating an instance of a very complex object FaceMesh() on each iteration.*
![facemesh/plots/linear.png](facemesh/plots/linear.png)

*Second example is creating an instance of a very complex object FaceMesh() and closes it on each iteration.* 
![facemesh/plots/linear_close_resources.png](facemesh/plots/linear_close_resources.png)

*Third example once creating an instance of a very complex object FaceMesh() and reuses it on each iteration.*
![facemesh/plots/constant.png](facemesh/plots/constant.png)

## Run same memory profiling benchmarks 

You can use 