# 2023 GECCO

This folder presents the supplementary material of the article submited to the GECCO 2023 conference [Link](https://gecco-2023.sigevo.org/HomePage). The article is titled: "Guiding the exploration of the solution space in walking robot through growth-based morphological development"

These experiments have been carried out with the following experimental setup:

- Ubuntu 18.04 LTS
- CoppeliaSim_Edu_V4_0_0_Ubuntu18_04 [Link](https://www.coppeliarobotics.com/previousVersions)
- Python 3.6
- MultiNEAT Library, which can be downloaded from two gitHub repositories ([Link](https://github.com/peter-ch/MultiNEAT), or [Link](https://github.com/peter-ch/MultiNEAT)) or from conda [Link](https://anaconda.org/conda-forge/multineat)

The article is structured in two folders, which represent the experiment performed with both morphologies: the quadruped and the NAO one. Each folder has a descriptive name of the type of experiment carried out, as well as the requiered files to run the experiments:

- A ".py" file with a descriptive name of the experiment which have the "main" function and the core of the experimento (e.g "NAO_growth_and_noise_input_sigma.py")
- The "supportFile.py" file with general functions to execute the main file.
- CoppeliaSim files to work with the "Remote LegacyAPI" of the CoppeliaSim: remoteApi.so, sim.py, simConst.py.
- The robot scene (e.g. naoScene0.ttt, naoScene5.ttt)



