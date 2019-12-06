import kmeans
import numpy as np
import sys 
import os 
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import zscore
import collections 

hempredictFolder = sys.argv[1] 
kmeans.overallTest(hempredictFolder)

# print(overall)