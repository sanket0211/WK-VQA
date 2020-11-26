import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
#import pandas as pd
import time
import json
complete={}

import matplotlib.pyplot as plt


plt.style.use('seaborn-whitegrid')
import numpy as np

fig = plt.figure()
ax = plt.axes()

plt.title("Accuracy of answering v/s number of kg-facts")
plt.xlabel("Increasing kg-facts")
plt.ylabel("accuracy");


x = ['ex1','ex2','ex3','ex4','ex5','ex6','ex7','ex8']
y = [94.41,83.83,63.01,42.28,40.91,41.75,38.66,41.05]
ax.plot(x,y)
plt.savefig('foo.png')
