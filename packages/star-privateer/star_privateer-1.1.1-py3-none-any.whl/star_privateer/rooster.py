import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import importlib.resources
import star_privateer as sp
from astropy.io import fits
from astropy.table import Table
import pickle
import warnings


'''
Copyright 2023 Sylvain Breton

This file is part of star-privateer.

star-privateer is free software: you can redistribute it and/or modify it under the
terms of the GNU Lesser General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

star-privateer is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with
star-privateer. If not, see <https://www.gnu.org/licenses/>.  
'''

def create_rooster_feature_inputs (df, return_err=False) :
  '''
  Take a DataFrame created by ``build_catalog_features``
  and return ready-to-use input array for ROOSTER training
  and classification.
  '''
  # Sort to avoid any issues with indexes and columns
  df = df.sort_index (axis=0)
  df = df.sort_index (axis=1)
  target_id = df.index.to_numpy ()
  p_candidates = df[['prot_ps', 'prot_acf', 'prot_cs']].to_numpy ()
  features = df.to_numpy ()
  feature_names = df.columns 
  if return_err :
    e_p_err  = df[['e_prot_ps', 'e_prot_acf', 'e_prot_cs']].to_numpy ()
    E_p_err  = df[['E_prot_ps', 'E_prot_acf', 'E_prot_cs']].to_numpy ()
    return target_id, p_candidates, e_p_err, E_p_err, features, feature_names 
  else :
    return target_id, p_candidates, features, feature_names 

def load_rooster_instance (instance='rooster_default', filename=None,
                           on_the_fly=False, verbose=False, seed=None) :
 '''
 Load by default one of the pre-trained ROOSTER instances
 provided by the PLATO MSAP4 demonstrator. If ``filename``
 is provided, load the ROOSTER instance saved under this
 name.

 Returns
 -------
   ROOSTER object.
 '''
 if filename is None :
   if not on_the_fly :
     filename = importlib.resources.path (sp.rooster_instances, 
                                          instance)
     with filename as f :
       if verbose :
         print ("Loading ROOSTER instance saved at {}".format (f))
       try :
         rooster_instance = pickle.load (open (f, "rb"))
       except ValueError :
         warnings.warn ("scikit-learn version not compatible with saved instance, training on the fly")
         on_the_fly = True
   if on_the_fly :   
     rooster_instance = train_on_the_fly (seed=seed, verbose=verbose)
 else :
   if verbose :
     print ("Loading ROOSTER instance saved at {}".format (filename))
   with open (filename, 'rb') as f :
     rooster_instance = pickle.load (f)
 return rooster_instance

def train_on_the_fly (seed=None, verbose=False) :
  '''
  Train ROOSTER on the fly with available dataset of the
  module if default saved instance is not compatible with
  scikit-learn version of the environment.
  '''
  if verbose :
    print ("Training ROOSTER on the fly.")
  if seed is None :
    seed = 104359357
  resource = "training_features.csv"
  filename = importlib.resources.path (sp.rooster_instances, resource) 
  with filename as f :
    df = pd.read_csv (f, index_col=0)
    if verbose :
      print ("Showing a sample of the DataFrame used for training")
      print (df.sample (5))
  df_train = df.loc[df.index[::2]]
  df_test = df.loc[df.index[1::2]]
  (training_id, training_p_candidates, 
   training_features, feature_names) = sp.create_rooster_feature_inputs (df_train)
  (test_id, test_p_candidates, 
   test_features, test_feature_names) = sp.create_rooster_feature_inputs (df_test)
  chicken = sp.ROOSTER (n_estimators=100, 
                        random_state=np.random.RandomState (seed=seed))
  chicken.train (training_id, training_p_candidates,
                 training_features, feature_names=feature_names,
                 catalog='santos-19-21', verbose=verbose)
  if verbose :
    results = chicken.test (test_id, test_p_candidates, test_features, 
                            feature_names=test_feature_names, 
                            catalog='santos-19-21', verbose=verbose)
    print ("Accuracy RotClass: {0:.2f} -- Accuracy PeriodSel: {1:.2f}".format (*chicken.getScore ()))
  return chicken


def load_santos_catalog (old=False, extended=False) :
 '''
 Load Santos et al. (2019, 2021) reference catalog.

 The ``extended`` option returns concatenated catalogs
 with original Vizier table name.
 '''
 if extended :
   old = True
 if old :
   f = importlib.resources.path (sp.catalogs, 'santos_2019_catalog.fit')
   with f as filename :
     hdul = fits.open (filename)
     hdu = hdul[1]
     df1 = Table (data=hdu.data).to_pandas ()
     hdul.close ()
     if not extended :
       df1 = df1[['KIC', 'Prot']]
       df1 = df1.rename (columns={'KIC':'target_id', 'Prot':'prot'})
   f = importlib.resources.path (sp.catalogs, 'santos_2021_catalog.fit')
   with f as filename :
     hdul = fits.open (filename)
     hdu = hdul[1]
     df2 = Table (data=hdu.data).to_pandas ()
     hdul.close ()
     if not extended :
       df2 = df2[['KIC', 'Prot']]
       df2 = df2.rename (columns={'KIC':'target_id', 'Prot':'prot'})
   df = pd.concat ([df1, df2])
   if extended :
     df = df.set_index ('KIC')
   else :
     df = df.set_index ('target_id')
 else :
   f = importlib.resources.path (sp.catalogs, 'santos-19-21.csv')
   with f as filename :
     df = pd.read_csv (filename, index_col='target_id')
 return df

def load_plato_sim_catalog () :
 '''
 Load catalog with PLATO simulation data.
 '''
 f = importlib.resources.path (sp.catalogs, 'plato-sim.csv')
 with f as filename :
   df = pd.read_csv (filename)
 # light curve for star 255 is missing 
 df = df.drop (labels=255)
 df = df.rename (columns={'#light_curve_number':'target_id', 'stellar_period':'prot'}) 
 df = df.set_index ('target_id')
 return df

def load_reference_catalog (catalog='santos-19-21') :
  '''
  Load a reference catalog to use for the training.
  
  Parameters
  ----------
  
  catalog: str
    Catalog to consider for the training. Only currently implemented
    option is 'santos-19-21' (see Santos et al. 2019, 2021).

  Returns
  -------
  A pandas Dataframe with target id (``target_id``) as index 
  and reference rotation period (``prot``) as column. 
  '''

  if catalog=='santos-19-21' :
    df = load_santos_catalog ()
  elif catalog=='plato-sim' :
    df = load_plato_sim_catalog ()
  elif catalog=='all' :
    list_df = []
    list_df.append (load_santos_catalog ())
    list_df.append (load_plato_sim_catalog ())
    df = pd.concat (list_df)
  else :
    raise Exception ("Requested catalog is not available.")

  return df

def get_prot_ref (target_id, catalog='santos-19-21') :
  '''
  Get the reference period for an array of target
  identifier.
  '''
  if type (catalog) is str :
    df = load_reference_catalog (catalog=catalog)
  else :
    df = catalog
  prot = df.loc[target_id, 'prot'].to_numpy ()
  return prot

def attribute_rot_class (target_id, p_candidates=None, 
                         catalog='santos-19-21') :
  '''
  Consider an input set of target id and assess
  their existence in the chosen reference catalog.
  If the target is in the catalog, the chosen class
  will be ``rot``, otherwise it will be ``no_rot``.
  If ``p_candidates`` is not None, stars for which
  none of the analysis method were able to retrieve
  the correct period will be removed.

  Parameters
  ----------
  catalog : str or DataFrame
    Key of one the catalog included in the module (``plato-sim``)
    or ``santos-19-21``. Otherwise, a one-column pandas DataFrame can be
    directly provided. Index must be the id of the targets, and the 
    column name has to be ``prot``.

  Returns
  -------
  A pandas Dataframe with ``target_id`` as index
  and ``target_class`` as column.
  '''
  if type (catalog) is str :
    df_ref = load_reference_catalog (catalog=catalog)
  else :
    df_ref = catalog
  df = pd.DataFrame (index=target_id)
  df['target_class'] = 'no_rot' 
  df.loc[np.intersect1d(df.index, df_ref.index), 'target_class'] = 'rot'
  df = df.sort_index ()
  return df

def attribute_period_sel (target_id, p_candidates, 
                          catalog='santos-19-21', tolerance=0.1) :
  '''
  Consider an input set of periods (obtained in the standard
  framework with power spectrum (Lomb-Scargle or Wavelets), ACF and CS) 
  for each target id 
  and compare it to the reference ``prot`` value to attribute
  the ``target_class`` that the ``PeriodSel`` classifier will
  use for its training. Target with ``target_id`` not matching
  the reference catalog will be removed as well as those for
  which none of the analysis method were able to provide the
  correct rotation period (with a 10% tolerance). 

  Parameters
  ----------

  catalog : str or DataFrame
    Key of one the catalog included in the module (``plato-sim``)
    or ``santos-19-21``. Otherwise, a one-column pandas DataFrame can be
    directly provided. Index must be the id of the targets, and the 
    column name has to be ``prot``.
 
  p_candidates : ndarray
    Array of candidates period. First dimension must
    have the same size as ``target_id``. Standard requested
    ordering is ``p_ps``, ``p_acf``, ``p_cs``. The given ordering
    is used to infer class priority when several candidate periods
    match the reference value. 

  tolerance : float
    Must larger than 0 and smaller than 1. Tolerance 
    between the closest measured period to the true rotation 
    period in order to keep the target in the set. Optional,
    default ``0.1``.

  Returns
  -------
  A pandas DataFrame with ``target_id`` as index and ``target_class``
  as column. ``target_class`` is a number from 0 to ``p_candidates.shape[1]``.
  In the standard ordering, class 0 therefore corresponds to ``p_ps``, 
  class 1 to ``p_acf`` and class 2 to ``p_cs``. 
  '''
  if type (catalog) is str :
    df_ref = load_reference_catalog (catalog=catalog)
  else :
    df_ref = catalog
  df = pd.DataFrame (index=target_id)
  df = df.join (df_ref[["prot"]])
  # Replacing NaN for targets without prot in the catalog
  df[df.isna ()] = -1
  p_ref = df["prot"].to_numpy ()
  def cond (ii) :
    return np.abs (p_candidates[:,ii] - p_ref) < tolerance*p_ref
  df["target_class"] = -1
  for ii in range (p_candidates.shape[1]-1, -1, -1) :
      df.loc[cond(ii), "target_class"] = ii
  # Assigning -2 to case where no reference
  df.loc[p_ref==-1, "target_class"] = -2
  return df[["target_class"]]

def wrapper_manage_dataset (target_id, p_candidates, features,
                            catalog="santos-19-21", e_p_err=None, E_p_err=None,
                            tolerance=0.1) :
  '''
  Wrapper that will be used before ROOSTER train and test.
  '''
  df_rot_class = attribute_rot_class (target_id, p_candidates=p_candidates,
                                      catalog=catalog)
  df_period_sel = attribute_period_sel (target_id, p_candidates, 
                                        catalog=catalog, tolerance=tolerance)
  cond_rot_class = df_period_sel["target_class"]!=-1
  X_rot_class = features[cond_rot_class,:]
  df_rot_class = df_rot_class.loc[cond_rot_class]
  cond_period_sel = (df_period_sel["target_class"]!=-1)&(df_period_sel["target_class"]!=-2)
  X_period_sel = features[cond_period_sel,:]
  p_candidates_reduced = p_candidates[cond_period_sel,:]
  df_period_sel = df_period_sel.loc[cond_period_sel]
  if e_p_err is not None :
    e_p_err_reduced = e_p_err_reduced[cond_period_sel,:]
  else :
    e_p_err_reduced = None
  if E_p_err is not None :
    E_p_err_reduced = E_p_err_reduced[cond_period_sel,:]
  else :
    E_p_err_reduced = None
  return (X_rot_class, df_rot_class, X_period_sel, 
          df_period_sel, p_candidates_reduced,
          e_p_err_reduced, E_p_err_reduced)

class ROOSTER :
  '''
  ROOSTER object, wrapping a random forest classifiers framework designed
  to analyse surface rotation in stellar light curves. 
  '''

  def __init__ (self, **kwargs) :
    '''
    Initiate a new ROOSTER instance. A ``RotClass`` and a
    ``PeriodSel`` classifiers are both created as attributes
    of the ROOSTER object. Additional parameters provided
    when initialising a ROOSTER instance will be passed
    to ``sklearn.ensemble.RandomForestClassifier``.
    '''
    self.RotClass = RandomForestClassifier (**kwargs)
    self.PeriodSel = RandomForestClassifier (**kwargs)
    self.__trained__ = False
    self.__tested__ = False
    self.__feature_names__ = None


  def train (self, target_id, p_candidates, 
             features, feature_names=None, 
             catalog='santos-19-21', verbose=False,
             tolerance=0.1) :
    '''
    Train ROOSTER classifiers with the provided training set. 
    '''
    (X_rot_class, df_rot_class, 
     X_period_sel, df_period_sel,
     p_candidates_reduced, _, _) = wrapper_manage_dataset (target_id, p_candidates, features,
                                                           catalog, tolerance=tolerance)
    if verbose :
      n_rot = df_rot_class.loc[df_rot_class['target_class']=='rot'].index.size
      n_no_rot = df_rot_class.loc[df_rot_class['target_class']=='no_rot'].index.size
      print ('Training RotClass with {} stars with detected rotation and {} without detected rotation.'.format(n_rot, n_no_rot))
      print ('Training PeriodSel with {} stars.'.format(X_period_sel.shape[0]))
    self.RotClass.fit (X_rot_class, df_rot_class['target_class'])
    self.PeriodSel.fit (X_period_sel, df_period_sel['target_class'])
    self.__trained__ = True
    self.__ntrainRotClass__ = X_rot_class.shape[0]
    self.__ntrainPeriodSel__ = X_period_sel.shape[0]
    if feature_names is not None :
      self.__feature_names__ = feature_names

  def test (self, target_id, p_candidates, features,
            catalog='santos-19-21', verbose=False,
            feature_names=None, e_p_err=None, E_p_err=None,
            tolerance=0.1) :
    '''
    Test ROOSTER classifiers with the provided test set. 
    '''
    if not self.__trained__ :
      raise Exception ("You must train your ROOSTER instance before testing it !")
    if feature_names is None :
      warnings.warn ('No feature_names provided, sanity check could not be performed.')
    elif np.any (feature_names!=self.__feature_names__) :
      raise Exception ('You did not provide the same features that were used to train ROOSTER !')
    (X_rot_class, df_rot_class, 
     X_period_sel, df_period_sel,
     p_candidates_reduced,
     e_p_err_reduced, E_p_err_reduced) = wrapper_manage_dataset (target_id, p_candidates, features,
                                                                 catalog, e_p_err=e_p_err, E_p_err=E_p_err,
                                                                 tolerance=tolerance)
    if verbose :
      n_rot = df_rot_class.loc[df_rot_class['target_class']=='rot'].index.size
      n_no_rot = df_rot_class.loc[df_rot_class['target_class']=='no_rot'].index.size
      print ('Testing RotClass with {} stars with detected rotation and {} without detected rotation.'.format(n_rot, n_no_rot))
      print ('Testing PeriodSel with {} stars.'.format(X_period_sel.shape[0]))
    self.__RotClassTestScore__ = self.RotClass.score (X_rot_class, df_rot_class['target_class'])
    self.__PeriodSelTestScore__ = self.PeriodSel.score (X_period_sel, df_period_sel['target_class'])
    predictedRotClass = self.RotClass.predict(X_rot_class)
    predictedPeriodSel = self.PeriodSel.predict(X_period_sel).astype (int)
    # Selecting periods among the candidate values
    predictedPeriods = p_candidates_reduced[np.arange (p_candidates_reduced.shape[0]),predictedPeriodSel]
    self.computePeriodSelTrueAccuracy (df_period_sel.index, predictedPeriods, tolerance=0.1,
                                       catalog=catalog)
    self.__tested__ = True
    self.__ntestRotClass__ = X_rot_class.shape[0]
    self.__ntestPeriodSel__ = X_period_sel.shape[0]

    if e_p_err_reduced is not None and E_p_err_reduced is not None :       
      # Selecting uncertainties if proper input are provided
      predicted_ePeriods = e_p_err_reduced[np.arange (p_candidates_reduced.shape[0]),predictedPeriodSel]
      predicted_EPeriods = E_p_err_reduced[np.arange (p_candidates_reduced.shape[0]),predictedPeriodSel]
      return (df_rot_class.index, predictedRotClass, 
              df_period_sel.index, predictedPeriods,
              predicted_ePeriods, predicted_EPeriods)

    else :
      return (df_rot_class.index, predictedRotClass, 
              df_period_sel.index, predictedPeriods)

  def computePeriodSelTrueAccuracy (self, target_id, predicted_periods, tolerance=0.1,
                                    catalog='santos-19-21') :
    '''
    Compute PeriodSel true Accuracy for a given sample
    of target by comparing the reference period value
    to the value chosen by ROOSTER, with a ``tolerance``
    interval. 
    '''
    if type (catalog) is str :
      df_ref = load_reference_catalog (catalog=catalog)
    else :
      df_ref = catalog
    ref_periods = df_ref.loc[target_id, 'prot'].to_numpy()
    cond = np.abs (ref_periods-predicted_periods) < tolerance * ref_periods
    self.__PeriodSelTrueAccuracy__ = target_id[cond].size / target_id.size
    return self.__PeriodSelTrueAccuracy__

  def getNumberEltTrain (self) :
    '''
    Return a tuple of integer, corresponding to the number
    of elements used to train each ROOSTER classifier.
    '''
    if not self.__trained__ :
      raise Exception ("You must train your ROOSTER instance first !")
    return (self.__ntrainRotClass__, self.__ntrainPeriodSel__)

  def getNumberEltTest (self) :
    '''
    Return a tuple of integer, corresponding to the number
    of elements used to train each ROOSTER classifier.
    '''
    if not self.__tested__ :
      raise Exception ("You must use a test set with your ROOSTER instance first !")
    return (self.__ntestRotClass__, self.__ntestPeriodSel__)

  def getFeatureNames (self) :
    '''
    Get name of feature that ROOSTER requires for classification.
    '''
    if self.__feature__names is None :
      warnings.warn ("Feature names have not been provided by the user, returning None.")
    return self.__feature_names__ 

  def getScore (self) :
    '''
    Returns ROOSTER classifying scores. Scores are returned in the 
    following order: ``RotClassTestScore``, ``PeriodSelTestScore``.
    The ROOSTER instance must have been trained and tested before.
    '''
    if not self.__trained__ :
      raise Exception ("You must train and test your ROOSTER instance first !")
    if not self.__tested__ :
      raise Exception ("You must use a test set with your ROOSTER instance first !")
    return self.__RotClassTestScore__, self.__PeriodSelTrueAccuracy__

  def isTrained (self) :
    return self.__trained__

  def isTested (self) :
    return self.__tested__

  def analyseSet (self, features, p_candidates,
                  e_p_err=None, E_p_err=None, 
                  feature_names=None) :
    '''
    Analyse provided targets using ROOSTER. 
    '''
    if feature_names is None :
      warnings.warn ('No feature_names provided, sanity check could not be performed.')
    elif np.any (feature_names!=self.__feature_names__) :
      raise Exception ('You did not provide the feature that were used to train ROOSTER !')
    rotation_score = self.RotClass.predict_proba (features)[:,1]
    periodsel = self.PeriodSel.predict (features)
    prot = p_candidates[np.arange (p_candidates.shape[0]),periodsel]
    if e_p_err is None or E_p_err is None :
      return rotation_score, prot
    else :
      e_prot_err = e_p_err[np.arange (p_candidates.shape[0]),periodsel]
      E_prot_err = E_p_err[np.arange (p_candidates.shape[0]),periodsel]
      return rotation_score, prot, e_prot_err, E_prot_err

  def save (self, filename) :
    '''
    Save the ROOSTER instance as ``filename``.
    '''
    with open (filename, 'wb') as f :
      pickle.dump (self, f)
