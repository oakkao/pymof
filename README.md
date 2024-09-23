# pymof

## Mass-ratio-variance based outlier factor

### Latest news
1. Documents are editted.
2. Works with a static dataset of size below 1000 data points.

### Introduction

An outlier of a finite dataset in statistics is defined as a data point that differs significantly from others. It is normally surrounded by a few data points
while normal ones are engulfed by others. This behavior leads to the proposed outlier factor called Mass-ratio-variance based Outlier Factor (MOF). A score is assigned to a data point from the variance of the mass-ratio distribution from the rest of data points. Within a sphere of an outlier, there will be few data points compared with a normal one. So, the mass-ratio of an outlier will be different from that of a normal data point. The algorithm to generate MOF requires no parameter and embraces the density concept. 

## Citation

If you use this package in your research, please consider citing the below papers.

BibTex for the package:
```
@inproceedings{changsakul2021mass,
  title={Mass-ratio-variance based Outlier Factor},
  author={Changsakul, Phichapop and Boonsiri, Somjai and Sinapiromsaran, Krung},
  booktitle={2021 18th International Joint Conference on Computer Science and Software Engineering (JCSSE)},
  pages={1--5},
  year={2021},
  organization={IEEE}
}
```

## Installation
To install `pymof`, type the following command in the terminal

```
pip install pymof            # normal install
pip install --upgrade pymof  # or update if needed
```

**Required Dependencies** :
- Python 3.9 or higher
- numpy>=1.23
- numba>=0.56.0
- scipy>=1.8.0
- scikit-learn>=1.2.0
- matplotlib>=3.5


## Documentation
----

The outlier score of each data point is calculated using the Mass-ratio-variance based Outlier Factor (MOF). MOF quantifies the global deviation of a data point's density relative to the rest of the dataset. This global perspective is crucial because an outlier's score depends on its overall isolation from all other data points. By analyzing the variance of the mass ratio, MOF can effectively identify data points with significantly lower density compared to their neighbors, indicating their outlier status.

#### MOF() object

> Initialize a model object `MOF`

    Parameters :
    Return :
            self : object
                    object of MOF model
#### MOF.fit(Data)
> Fit data to  `MOF` model\
> **Note** The number of data points should not exceed **10000** due to the computation of all pair distances.

    Parameters :
            Data  : numpy array of shape (n_points, d_dimensions)
                    The input samples.
    Return :
            self  : object
                    fitted estimator
#### MOF.visualize()
> Visualize data points with `MOF`'s scores\
> **Note** cannot visualize data points having a dimension greather than 3

    Parameters :
    Return :
        decision_scores_ : numpy array of shape (n_samples)
                                    decision score for each point
#### MOF attributes
| Attributes | Type | Details |
| ------ | ------- | ------ |
| MOF.Data | numpy array of shape (n_points, d_dimensions) | input data for model |
| MOF.MassRatio | numpy array of shape (n_samples, n_points) | MassRatio for each a pair of points |
| MOF.decision_scores_ | numpy array of shape (n_samples) | decision score for each point |

### Sample usage
```
# This example demonstrates  the usage of MOF
from pymof import MOF
import numpy as np
X = [[-2.30258509,  7.01040212,  5.80242044],
    [ 0.09531018,  7.13894636,  5.91106761],
    [ 0.09531018,  7.61928251,  5.80242044],
    [ 0.09531018,  7.29580291,  6.01640103],
    [-2.30258509, 12.43197678,  5.79331844],
    [ 1.13140211,  9.53156118,  7.22336862],
    [-2.30258509,  7.09431783,  5.79939564],
    [ 0.09531018,  7.50444662,  5.82037962],
    [ 0.09531018,  7.8184705,   5.82334171],
    [ 0.09531018,  7.25212482,  5.91106761]]
X = np.array(X)
c = MOF()
c.fit(X)
scores = c.decision_scores_
print(scores)
c.visualize()
```
**Output**
```
[0.34541068 0.11101711 0.07193073 0.07520904 1.51480377 0.94558894 0.27585581 0.06242823 0.2204504  0.02247725]
```
![](https://github.com/oakkao/pymof/blob/main/examples/example.png?raw=true)
