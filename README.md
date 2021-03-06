# Introduction

This library implements some functionf for removing collinearity from a dataset of features. It can be used both for supervised and for unsupervised machine learning problems.

Collinearity is evaluated calculating __Pearson's linear correlation coefficient__ between the features. The user sets a __threshold__, which is the maximum absolute value allowed for the correlation coefficients in the correlation matrix. 

For __unsupervised problems__, the algorithm selects only those features that produce a correlation matrix whose off-diagonal elements are, in absolute value, less than the threshold. 

For __supervised problems__, the importance of the features with respect to the target variable is calculated using a univariate approach. Then, the features are added with the same unsupervised approach, starting from the most important ones.

# Objects

The main object is __SelectNonCollinear__. It can be imported this way:

```python
from collinearity import SelectNonCollinear
```

> collinearity.__SelectNonCollinear__(_correlation_threshold=0.4, scoring=f_classif_)

Parameters:

__correlation_threshold : _float (between 0 and 1), default = 0.4___

Only those features that produce a correlation matrix with off-diagonal elements that are, in absolute value, less than this threshold will be chosen.

__scoring : _callable, default=f_classif___

The scoring function for supervised problems. It must be the same accepted by [sklearn.feature_selection.SelectKBest](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectKBest.html).

# Methods

This object supports the main methods of scikit-learn Estimators:

> fit(X,y=None)

Identifies the features to consider. For supervised problems, _y_ is the target array and the algorithm is:
- Sort the features by scoring descending
- Take the most important feature (i.e. the first feature)
- Take the next feature if it shows a linear correlation coefficient with the already selected feature that is, in absolute value, lower than the threshold
- Keep adding features as long as the correlation constraint holds

For unsupervised problems, we have `y = None` and the algorithm is:
- Take the couple of features that have the lowest absolute value of the linear correlation coefficient.
- If it's lower than the threshold, consider these features
- Keep adding features as long as the correlation matrix doesn't show off-diagonal elements whose absolute value is greater than the threshold. 

> transform(X)

Selects the features according to the result of _fit_. It must be called after _fit_.

> fit_transform(X,y=None)

Calls _fit_ and then _transform_

> get_support()

Returns an array of _True_ and _False_ of size X.shape[1]. A feature is selected if the value on this array corresponding to its index is _True_, otherwise it's not selected.

# Examples

The following examples explain how the main objects work. The code to run in advance for initializing the environment is:

```python
from collinearity import SelectNonCollinear
from sklearn.feature_selection import f_regression
import numpy as np
from sklearn.datasets import load_diabetes

X,y = load_diabetes(return_X_y=True)
```

## Unsupervised problems


This example shows how to perform selection according to minimum collinearity in unsupervised problems. 

Let's consider, for this example, a threshold equal to 0.3.

```python
selector = SelectNonCollinear(0.3)
```

If we apply the selection to the features and calculate the correlation matrix, we have:

```python
np.corrcoef(selector.fit_transform(X),rowvar=False)

# array([[1.       , 0.1737371 , 0.18508467, 0.26006082],
#       [0.1737371 , 1.        , 0.0881614 , 0.03527682],
#       [0.18508467, 0.0881614 , 1.        , 0.24977742],
#       [0.26006082, 0.03527682, 0.24977742, 1.        ]])

```
As we can see, no off-diagonal element is greater than the threshold.

## Supervised problems

For this problem, we must set the value of the `scoring` argument in the constructor. 

Let's consider a threshold equal to 0.4 and a scoring equal to `f_regression`.

```python
selector = SelectNonCollinear(correlation_threshold=0.4,scoring=f_regression)

selector.fit(X,y)
```

The correlation matrix is:
```python
np.corrcoef(selector.transform(X),rowvar=False)

# array([[ 1.       ,  0.1737371 ,  0.18508467,  0.33542671,  0.26006082,
#        -0.07518097,  0.30173101],
#       [ 0.1737371 ,  1.        ,  0.0881614 ,  0.24101317,  0.03527682,
#        -0.37908963,  0.20813322],
#       [ 0.18508467,  0.0881614 ,  1.        ,  0.39541532,  0.24977742,
#        -0.36681098,  0.38867999],
#       [ 0.33542671,  0.24101317,  0.39541532,  1.        ,  0.24246971,
#        -0.17876121,  0.39042938],
#       [ 0.26006082,  0.03527682,  0.24977742,  0.24246971,  1.        ,
#         0.05151936,  0.32571675],
#       [-0.07518097, -0.37908963, -0.36681098, -0.17876121,  0.05151936,
#         1.        , -0.2736973 ],
#       [ 0.30173101,  0.20813322,  0.38867999,  0.39042938,  0.32571675,
#        -0.2736973 ,  1.        ]])
```

Again, no off-diagonal element is greater than the threshold in absolute value.

## Use in pipelines

It's possible to use `SelectNonCollinear` inside a pipeline, if necessary.

```python
pipeline = make_pipeline(SelectNonCollinear(correlation_threshold=0.4, scoring=f_regression), LinearRegression())
```
# Contact the author

For any questions, you can contact me at gianluca.malato@gmail.com
