# An agent model for promoting modest technologies
by Yuji Saikai, a PhD student at University of Wisconsin—Madison. A paper is available [here](https://wisc.academia.edu/saikai).

**Abstract**  
Promotion of a technology often encounters a gap between private and public benefits if it has only modest appeal to individuals. Information is crucial at the early stages of the adoption process. At the late phase, what if the society is saturated with the required information for decision making, yet people have not made up their minds or are indifferent? The issue becomes complex if individual decisions involve social interaction. To provide a policy tool for the scenario, we build an agent-based model and emphasize the inadequacy of the gold standard, RCT, for studying complex systems.  

The model is built on [Mesa](https://github.com/projectmesa/mesa). The model class (TechAdopt in model.py) accepts a grid size, a random seed, and a list of intervention modes. You may spefify them as well as the number of steps in run.py. For a single run, _run.py 2_ or _run.py 1_ and go to <http://localhost:8889> for visualization. For a batch run, in addition, set the number of iterations in batch.py. You should have a directory for an output file at the parent level.
