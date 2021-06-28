# 2021 Neurocomputing

Supplementary material for the article submited to Neurocomputing in 2021.

- doc-generation: Documentation about the different functions, methods, etc. utilized.
- Sorce code: Folder that contains the source code for the different experiments. It contais:
    1. The source code of the learning process for the 8DOF, 16DOF and 24DOF quadruped, the hexapod and octopod.
    2. The source code to run the best individual obtained for each morphology and type of experiment (no development and growth)
    
Once the MultiNEAT library and its dependences have been installed, the source code can be run by:

```
# For running the learning experiment of the 8 DOF quadruped without development (NoDev):
python main.py --port 19997 --test False type nodev quad8DOF
```

```
# For running the best individual obtained at the end of the learning process, of the hexapod morphology for the growth experiment:
python main.py --port 19997 --test True type growth hexapod
```

The selected port number (19997) is the predefined port number in V-REP to work in Synchronous mode. Furthermore, information about how to run the "main.py" program is provided typing:

```
python main.py -h
```

- videos: Videos that show the best gait for each morpholoy and type of experiment.
- vrep_scenes: VREP scenes for each morpholoy.

