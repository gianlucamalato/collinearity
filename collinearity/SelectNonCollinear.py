from sklearn.feature_selection import SelectKBest,f_classif,f_regression
import numpy as np


def remove_collinearity_unsupervised(X,corr_threshold=0.4):
  n = X.shape[1]
  corr_matrix = np.abs(np.corrcoef(X,rowvar=False))
  chosen_indices = []

  min_corr = 1
  best_couple = None
  for i in range(0,corr_matrix.shape[0]):
    for j in range(i+1,corr_matrix.shape[1]):
      if corr_matrix[i,j] < min_corr:
        best_couple = [i,j]
        min_corr = corr_matrix[i,j]
  
  if min_corr > corr_threshold:
    return [False]*n

  chosen_indices.extend(best_couple)

  stop = False

  while not stop:
    stop = True
    for i in range(X.shape[1]):
      if i in chosen_indices:
        continue
      else:
        max_corr =np.max(np.abs(np.corrcoef(X[:,chosen_indices + [i]],rowvar=False) - np.identity(len(chosen_indices)+1)))
        if max_corr < corr_threshold:
          chosen_indices.append(i)
          stop = False
  mask = [i in chosen_indices for i in range(X.shape[1])]

  return mask


  


def remove_collinearity_supervised(X,y,scoring=f_classif,corr_threshold=0.4):
  s = SelectKBest(scoring,k="all")
  s.fit(X,y)
  scores = [(i,s.scores_[i]) for i in range(len(s.scores_))]
  scores.sort(key = lambda x : -x[1])

  selected_features = []
  for i in range(len(scores)):
    if len(selected_features) == 0:
      selected_features.append(scores[0][0])
    else:
      f = scores[i][0]
      max_corr =np.max(np.abs(np.corrcoef(X[:,selected_features + [f]],rowvar=False) - np.identity(len(selected_features)+1)))
      if max_corr < corr_threshold:
        selected_features.append(f)

  mask = [i in selected_features for i in range(X.shape[1])]
  return mask


class SelectNonCollinear:

  def __init__(self,correlation_threshold=0.5, scoring=f_classif):
    self.correlation_threshold_ = correlation_threshold
    self.scoring_ = scoring
  
  def fit(self,X,y=None):
    if y is None:
      self.mask_ = remove_collinearity_unsupervised(X,self.correlation_threshold_)
    else:
      self.mask_ = remove_collinearity_supervised(X,y,self.scoring_,self.correlation_threshold_)
  
  def transform(self,X):
    return X[:,self.mask_]
  
  def fit_transform(self,X,y=None):
    self.fit(X,y)
    return self.transform(X)

  def set_params(correlation_threshold):
    self.correlation_threshold_ = correlation_threshold
  
  def get_support(self):
    return self.mask_