# Source code

Once the MultiNEAT library and its dependences have been installed, to run the source code, both for the learning case as the case that shows how the best individual behave, follow the next steps:

1. Open the scene related with the desired morphology contained in the "vrep_scenes" folder in the VREP simulator. 

2. For example, to run the learning experiment of the 8 DOF quadruped without development (nodev) type:

```
python main.py --port 19997 --test False --type nodev quad8DOF
```

For running the best individual obtained at the end of the learning process, of the 8 DOF quadruped morphology for the growth experiment type:

```
python main.py --port 19997 --test True --type growth quad8DOF
```

The selected port number (19997) is the predefined port number in V-REP to work in Synchronous mode. 

Furthermore, more information about how to run the "main.py" script is provided typing:

```
python main.py -h
```
