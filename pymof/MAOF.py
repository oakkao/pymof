import numpy as np
import numba as nb
from numba import jit, objmode, types
from scipy.stats import rankdata
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

## Scoring function for MAOF
#AAD
@jit(nopython=True)
def _CalAAD(arr, l):
  return np.mean(np.absolute(arr - np.mean(arr)))

#IQR
@jit(nopython=True)
def _CalIQR(arr, l):
  return np.percentile(arr, 75) - np.percentile(arr, 25)

#Weight
@jit(nopython=True)
def _CalWeight(arr, l):# l is lambda for weight
  return l*(np.mean(np.absolute(arr - np.mean(arr)))) + (1-l)*(np.percentile(arr, 75) - np.percentile(arr, 25))

#Range
@jit(nopython=True)
def _CalRange(arr, l):
  return np.ptp(arr)

# Calculate mass ratio matrix
@jit(nopython=True)
def _Massratio(Data,window, funcName, weightLambda):
  # Beware of large numbers, it might overflow python int
    n = len(Data)
    scores = np.zeros(n)

    assert(window > 0)

    # slicing window through data
    for start_point in range(0,n,window):
      stop_point = min(start_point+ window, n)
      Current_Data = Data[start_point : stop_point]
      with objmode(current_idx = "i8[:, :]"):
        window_dm = cdist(Current_Data, Data)
        current_idx = np.argsort(np.argsort(window_dm))

      count = np.zeros(window, dtype=np.int32)
      mass = np.zeros((window, n-1))

      # calculate all current points
      for i in range(start_point, stop_point):
        for j in range(i+1, stop_point):
          m = (current_idx[j%window][i]*1.0 + 1)/ (current_idx[i%window][j] + 1)
          mass[i,count[i]] = m
          count[i] += 1
          mass[j,count[j]] = 1/m
          count[j] += 1

      # calculate 0 -> start_points
      for i in range(start_point):
        with objmode(idx = "i8[:, :]"):
          dm = cdist([Data[i]], Data)
          idx = np.argsort(np.argsort(dm))
        for j in range(start_point, stop_point):
          m = (current_idx[j%window][i]*1.0 + 1 )/ (idx[0][j%window] + 1)
          mass[j,count[j]] = m
          count[j] += 1

      # calculate stop_point -> n
      for i in range(stop_point, n):
        with objmode(idx = "i8[:, :]"):
          dm = cdist([Data[i]], Data)
          idx = np.argsort(np.argsort(dm))
        for j in range(start_point, stop_point):
          m = (current_idx[j%window][i]*1.0 + 1 )/ (idx[0][j%window] + 1)
          mass[j,count[j]] = m
          count[j] += 1

      # calculate scores
      for i in range(start_point, stop_point):
        arr = mass[i%window]
        scores[i] = funcName(arr, weightLambda)

    return scores

class MAOF:
  '''
  Mass-Ratio-Average-Absolute-Deviation Based Outlier Factor for Anomaly Scoring (MAOF)
  This research extends the mass-ratio-variance outlier factor algorithm (MOF) by exploring other alternative statistical
  dispersion beyond the traditional variance such as range, interquartile range, average absolute deviation, and combination of previous two dispersions.
  '''
  def __init__(self):
    self.name='MAOF'
    self.Data = []
  def fit(self,Data,Window=10000, Function_name = "AAD", Weight_Lambda = 0.5):
    '''
    Parameters
    ----------
    Data : numpy array of shape (n_samples, n_features)
        The input samples.
    Window : integer (int)
        number of points for each calculation
        default window size is 10000.
    Function_name : string (str)
        A type of statistical dispersion that use for scoring.
        Function_name can be 'AAD','IQR', 'Range','Weight'.
        default function is 'AAD'
    Weight_Lambda : float
        0.0 <= Weight_Lambda <= 1.0
        A Value of lambda that use in weight-scoring function.
        score = λ AAD + (1- λ) IQR
        default weight is 0.5
    '''
    '''
    Returns
    -------
    self : object
    '''
    self.Data = Data

    assert(Function_name in ['AAD','IQR','Range','Weight'])
    funcName = _CalAAD
    if Function_name == 'IQR':
      funcName = _CalIQR
    elif Function_name == 'Range':
      funcName = _CalRange
    elif Function_name == 'Weight':
      funcName = _CalWeight
      assert(0.0 <= Weight_Lambda <= 1.0)

    # Calculate Mass-Ratio-Average-Absolute-Deviation (MAOF)
    self.decision_scores_= _Massratio(Data,Window,funcName,Weight_Lambda)

  def visualize(self):
    '''
    Parameters free
    Visualize data points
    '''
    '''
    Parameters
    ----------
    '''
    '''
    Returns
    -------
    '''
    if self.Data.shape[1] == 3:
      fig = plt.figure(figsize=(15, 15))
      ax = fig.add_subplot(111, projection='3d')
      p = ax.scatter(self.Data[:, 0], self.Data[:, 1], self.Data[:, 2], c = np.log(self.decision_scores_+0.00001), cmap='jet')
      fig.colorbar(p)
    elif self.Data.shape[1] == 2:
      fig = plt.figure(figsize=(15, 15))
      ax = fig.add_subplot()
      p = ax.scatter(self.Data[:, 0], self.Data[:, 1], c = np.log(self.decision_scores_+0.00001), cmap='jet')
      fig.colorbar(p)
    else :
      print("Cannot visualize dimension space more than 3")
    return self.decision_scores_