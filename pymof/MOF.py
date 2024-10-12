import numpy as np
import numba as nb
from numba import jit, objmode, types
from scipy.stats import rankdata
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Calculate variance mass ratio
@jit(nopython=True)
def _Var_Massratio(Data,window):
  # Beware of large numbers, it might overflow python int
    n = len(Data)
    mass = np.zeros(n)
    mass2 = np.zeros(n)
    assert(window > 0)

    # slicing window through data
    for start_point in range(0,n,window):
      stop_point = min(start_point+ window, n)
      Current_Data = Data[start_point : stop_point]
      with objmode(current_idx = "i8[:, :]"):
        window_dm = cdist(Current_Data, Data)
        current_idx = np.argsort(np.argsort(window_dm))

      # calculate all current points
      for i in range(start_point, stop_point):
        for j in range(i+1, stop_point):
          m = (current_idx[j%window][i]*1.0 + 1)/ (current_idx[i%window][j] + 1)
          mass[i] += m
          mass2[i] += m**2
          mass[j] += 1/m
          mass2[j] += 1/m**2

      # calculate remaining points
      for i in range(stop_point,n):
        with objmode(idx = "i8[:, :]"):
          dm = cdist([Data[i]], Data)
          idx = np.argsort(np.argsort(dm))
        for j in range(start_point, stop_point):
          m = (current_idx[j%window][i]*1.0 + 1 )/ (idx[0][j%window] + 1)
          mass[i] += m
          mass2[i] += m**2
          mass[j] += 1/m
          mass2[j] += 1/m**2

    var = mass2/(n-1)-(mass/(n-1))**2
    return var

class MOF:
  '''
  Mass ratio variance-based outlier factor (MOF)
  the outlier score of each data point is called MOF.
  It measures the global deviation of density given sample with respect to other data points.
  it is global in the outlier score depend on how isolated
  data point is with respect to all data points in the data set.
  the variance of mass ratio can identify data points that have a substantially
  lower density compared to other data points.
  These are considered outliers.
  '''
  # Parameters-free
  # ----------
  def __init__(self):
    self.name='MOF'
    self.Data = []

  def fit(self,Data, Window = 10000):

    '''
    Parameters
    ----------
    Data : numpy array of shape (n_samples, n_features)
        The input samples.
    window : integer (int)
        window size for calculation.
        default window size is 10000.
    '''
    '''
    Returns
    -------
    self : object
    '''
#  Fitted estimator.
    self.Data =Data

# Calculate mass ratio variance (MOF)
    self.decision_scores_= _Var_Massratio(Data,Window)

# ----------------
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
