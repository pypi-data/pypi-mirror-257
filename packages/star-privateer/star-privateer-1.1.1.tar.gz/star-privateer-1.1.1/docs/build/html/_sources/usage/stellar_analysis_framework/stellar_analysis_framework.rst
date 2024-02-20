Analysis framework for rotation period extraction (MSAP4-03)
============================================================

This notebook provide an example of the analysis performed by the PLATO
MSAP4-03 submodules: results from Lomb-Scargle periodogram,
autocorrelation functions and composite spectrum are used to produce a
set of features exploited by an existing instance of ROOSTER to return
the final rotation period of the analysed target. You will find that
what is done here is very similar to the ROOSTER tutorial notebook
(``rooster_training_framework``, you should run it before doing this
tutorial), the only big difference is actually that we will use here a
pre-trained ROOSTER instance !

Here, the MSAP4-01A and MSAP4-02 steps required to feed MSAP4-03 are
included in order to be able to run this notebook independently from the
MSAP4-01A and MSAP4-02 notebooks.

Note that, due its significant computing time, the MSAP4-01B component
dedicated to background analysis is executed independently in another
notebook.

**Note:** This notebook has been designed for the purpose of scientific
justification of MSAP4-03. The notebook illustrated the precise
flowchart envisaged for MSAP4-03 is cs_rooster_sph_analysis.ipynb

.. code:: ipython3

    import star_privateer as sp

A simple example
----------------

.. code:: ipython3

    import importlib
    import tqdm
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    
    if not os.path.exists ('stellar_analysis_features') :
        os.mkdir ('stellar_analysis_features')
    if not os.path.exists ('stellar_analysis_plots') :
        os.mkdir ('stellar_analysis_plots')    

Our working case is KIC 3733735, a well-known *Kepler* fast rotating
star.

.. code:: ipython3

    filename = sp.get_target_filename (sp.timeseries, '003733735')
    t, s, dt = sp.load_resource (filename)

The first thing we have to do is run the analysis pipeline. In
particular, we can take a look at the plots made from the different
analysis methods.

.. code:: ipython3

    p_in = np.linspace (0, 100, 1000)
    (p_ps, p_acf, ps, acf, 
     cs, features, feature_names, _) = sp.analysis_pipeline (t, s, periods_in=p_in, figsize=(8,10),
                                                                wavelet_analysis=False, plot=True,
                                                                filename='stellar_analysis_plots/003733735.png',
                                                            )



.. image:: stellar_analysis_framework_files/stellar_analysis_framework_7_0.png


We then save the results to a csv file:

.. code:: ipython3

    fileout = 'stellar_analysis_features/003733735.csv'
    df = sp.save_features (fileout, 3733735, features, feature_names)

As in the previous tutorial, let’s build a feature catalog. This is
actually not required here because we are analysing only one star, but
this step allows to ROOSTER-analyse several stars together with a simple
framework.

.. code:: ipython3

    df = sp.build_catalog_features ('stellar_analysis_features')

Then, let’s load the ROOSTER instance that we have trained in the
previous tutorial:

.. code:: ipython3

    chicken = sp.load_rooster_instance (filename='rooster_instances/rooster_tutorial')

As previously, let’s split the DataFrame into ROOSTER required inputs:

.. code:: ipython3

    (target_id, p_candidates, 
     e_p_candidates, E_p_candidates, 
     features, feature_names) = sp.create_rooster_feature_inputs (df, return_err=True)

Here, we can see that there is actually (almost) nothing to do, as the
three methods have yielded the same :math:`P_\mathrm{rot}` estimate.
However, we need ROOSTER to provide us with the rotation score of the
target. ROOSTER will also select one of the three ``p_candidates`` as
the final estimate for our target.

.. code:: ipython3

    p_candidates




.. parsed-literal::

    array([[2.53459872, 2.69724228, 2.49267822]])



The ``analyseSet`` function implemented in ROOSTER allows to analyse the
features we extracted with the analysis pipeline. By providing
``feature_names``, we ensure that ROOSTER was trained with the same
features that those we extracted.

.. code:: ipython3

    rotation_score, prot, e_p, E_p = chicken.analyseSet (features, p_candidates, e_p_err=e_p_candidates,
                                                         E_p_err=E_p_candidates, feature_names=feature_names)

We finally get the rotation score and the final :math:`P_\mathrm{rot}`.
A rotation score above 0.5 means that the ROOSTER analysis favours a
detection of stellar surface rotation signal.

.. code:: ipython3

    rotation_score, prot, e_p, E_p




.. parsed-literal::

    (array([0.85]), array([2.53459872]), array([0.21810524]), array([0.2634447]))



Analysing a PLATO simulated light curves dataset
------------------------------------------------

In order to illustrate the pipeline features described above, we can
apply the pipeline to a larger dataset of 255 PLATO simulated light
curves in order to check what we recover.

.. code:: ipython3

    import plato_msap4_demonstrator_datasets.plato_sim_dataset as plato_sim_dataset
    
    if not os.path.exists ('plato_sim_features') :
        os.mkdir ('plato_sim_features')
    if not os.path.exists ('plato_sim_plots') :
        os.mkdir ('plato_sim_plots')

.. code:: ipython3

    list_id = sp.get_list_targets (plato_sim_dataset)

Note that in the current version of the demonstrator, we apply a 55-day
high-pass finite impulse response filter to the simulated light curves
(``preprocess``) function in order to remove low-frequency systematics
while preserving at most the signature of stellar activity in the data.
In the future, data product calibrated specifically for MSAP4 or
dedicated calibration step aimed at reducing systematics at most would
allow to significantly improve the analysis performances.

.. code:: ipython3

    for elt in tqdm.tqdm (list_id) :
        str_elt = str (elt).zfill (3)
        fileout = 'plato_sim_features/{}.csv'.format(str_elt)
        filename = sp.get_target_filename (plato_sim_dataset, str_elt, filetype='csv')
        if not os.path.exists (fileout) :
            t, s, dt = sp.load_resource (filename)
            s = sp.preprocess (t, s, cut=60)
            (p_ps, p_acf, ps, acf, 
             cs, features, feature_names, fig) = sp.analysis_pipeline (t, s, periods_in=p_in, plot=True,
                                                                    wavelet_analysis=False, filename='plato_sim_plots/{}.png'.format(str_elt),
                                                                    figsize=(10,16), lw=1, dpi=300)
            df = sp.save_features (fileout, str_elt, features, feature_names)
            plt.close ()


.. parsed-literal::

    100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 255/255 [53:47<00:00, 12.66s/it]


We can now analyse the obtained features with ROOSTER to provide our
final results.

.. code:: ipython3

    df = sp.build_catalog_features ('plato_sim_features')
    (target_id, p_candidates, 
     e_p_candidates, E_p_candidates, 
     features, feature_names) = sp.create_rooster_feature_inputs (df, return_err=True)
    rotation_score, prot, e_p, E_p = chicken.analyseSet (features, p_candidates, e_p_err=e_p_candidates,
                                                         E_p_err=E_p_candidates, feature_names=feature_names)
    df




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>prot_ps</th>
          <th>prot_acf</th>
          <th>prot_cs</th>
          <th>e_prot_ps</th>
          <th>E_prot_ps</th>
          <th>e_prot_acf</th>
          <th>E_prot_acf</th>
          <th>e_prot_cs</th>
          <th>E_prot_cs</th>
          <th>sph_ps</th>
          <th>sph_acf</th>
          <th>sph_cs</th>
          <th>h_ps</th>
          <th>fa_prob_ps</th>
          <th>hacf</th>
          <th>gacf</th>
          <th>hcs</th>
        </tr>
        <tr>
          <th>target_id</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>42.955113</td>
          <td>36.333101</td>
          <td>43.493825</td>
          <td>5.139282</td>
          <td>6.755867</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>1.912061</td>
          <td>1.912061</td>
          <td>809.302045</td>
          <td>770.205688</td>
          <td>804.306555</td>
          <td>4.573669e+06</td>
          <td>0.0</td>
          <td>0.519065</td>
          <td>0.174074</td>
          <td>0.793561</td>
        </tr>
        <tr>
          <th>1</th>
          <td>33.388871</td>
          <td>32.631736</td>
          <td>33.120942</td>
          <td>7.850812</td>
          <td>14.820267</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>5.036273</td>
          <td>5.036273</td>
          <td>197.317073</td>
          <td>196.574388</td>
          <td>196.840239</td>
          <td>5.452245e+03</td>
          <td>0.0</td>
          <td>0.096116</td>
          <td>0.046063</td>
          <td>1.016956</td>
        </tr>
        <tr>
          <th>2</th>
          <td>17.529157</td>
          <td>18.215161</td>
          <td>17.308463</td>
          <td>1.997207</td>
          <td>2.586628</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.428188</td>
          <td>0.428188</td>
          <td>131.463440</td>
          <td>133.232528</td>
          <td>131.613358</td>
          <td>9.626133e+03</td>
          <td>0.0</td>
          <td>0.381460</td>
          <td>0.162757</td>
          <td>0.898856</td>
        </tr>
        <tr>
          <th>3</th>
          <td>21.247463</td>
          <td>20.819311</td>
          <td>20.921406</td>
          <td>2.308992</td>
          <td>2.950196</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.723273</td>
          <td>0.723273</td>
          <td>108.132491</td>
          <td>108.598706</td>
          <td>108.520429</td>
          <td>1.468874e+04</td>
          <td>0.0</td>
          <td>0.594810</td>
          <td>0.308409</td>
          <td>0.976351</td>
        </tr>
        <tr>
          <th>4</th>
          <td>28.636742</td>
          <td>28.527595</td>
          <td>10.903680</td>
          <td>3.606657</td>
          <td>4.821026</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>2.464250</td>
          <td>2.464250</td>
          <td>156.739595</td>
          <td>156.837205</td>
          <td>151.043171</td>
          <td>8.556843e+02</td>
          <td>0.0</td>
          <td>0.023167</td>
          <td>0.022881</td>
          <td>0.419789</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>250</th>
          <td>31.871195</td>
          <td>29.326201</td>
          <td>31.219175</td>
          <td>9.996470</td>
          <td>26.822076</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>4.063947</td>
          <td>4.063947</td>
          <td>213.718124</td>
          <td>204.403237</td>
          <td>201.613782</td>
          <td>4.368693e+04</td>
          <td>0.0</td>
          <td>0.828921</td>
          <td>0.426961</td>
          <td>0.876983</td>
        </tr>
        <tr>
          <th>251</th>
          <td>20.214171</td>
          <td>19.117933</td>
          <td>20.219246</td>
          <td>1.917448</td>
          <td>2.366382</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>1.732660</td>
          <td>1.732660</td>
          <td>187.913408</td>
          <td>178.909159</td>
          <td>187.920598</td>
          <td>8.072857e+04</td>
          <td>0.0</td>
          <td>0.688094</td>
          <td>0.313389</td>
          <td>0.822466</td>
        </tr>
        <tr>
          <th>252</th>
          <td>36.903489</td>
          <td>37.840036</td>
          <td>36.899833</td>
          <td>5.608447</td>
          <td>8.057559</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>5.557462</td>
          <td>5.557462</td>
          <td>1488.425513</td>
          <td>1506.314545</td>
          <td>1488.392507</td>
          <td>8.011975e+06</td>
          <td>0.0</td>
          <td>1.514718</td>
          <td>0.754955</td>
          <td>0.974245</td>
        </tr>
        <tr>
          <th>253</th>
          <td>17.182045</td>
          <td>17.416555</td>
          <td>17.492527</td>
          <td>2.098990</td>
          <td>2.777632</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>2.240773</td>
          <td>2.240773</td>
          <td>164.770235</td>
          <td>164.286478</td>
          <td>164.154739</td>
          <td>1.954305e+04</td>
          <td>0.0</td>
          <td>0.614294</td>
          <td>0.262884</td>
          <td>0.984653</td>
        </tr>
        <tr>
          <th>254</th>
          <td>18.950440</td>
          <td>18.722102</td>
          <td>19.007517</td>
          <td>1.989637</td>
          <td>2.518474</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.604018</td>
          <td>0.604018</td>
          <td>1210.035639</td>
          <td>1214.842364</td>
          <td>1208.098251</td>
          <td>7.215866e+06</td>
          <td>0.0</td>
          <td>0.810962</td>
          <td>0.296969</td>
          <td>0.972721</td>
        </tr>
      </tbody>
    </table>
    <p>255 rows × 17 columns</p>
    </div>



Next, let’s load the reference catalog for these simulated light curves
in order to compare the results from our pipeline with what was injected
in the data.

.. code:: ipython3

    prot_ref = sp.get_prot_ref (target_id, catalog='plato-sim')
    cond_0 = (rotation_score>0.5)
    cond_1 = (np.abs (prot - prot_ref) < 0.1 * prot_ref) 
    cond_2 = (np.abs (prot - prot_ref) < 0.1 * prot_ref) & (rotation_score>0.5)
    score_0 = target_id[cond_0].size / target_id.size
    score_1 = target_id[cond_1].size / target_id.size
    score_2 = target_id[cond_2].size / target_id.size
    score_0, score_1, score_2




.. parsed-literal::

    (0.9529411764705882, 0.615686274509804, 0.6039215686274509)



The score computed here means that we were able to successfully detect a
rotation signal and recover the correct rotation period for about **61%
of the stars** in the sample. We can take a look at histograms to check
the rotation score of our population and to compare the input rotation
periods distribution to the one we recover.

.. code:: ipython3

    fig, (ax1, ax2) = plt.subplots (1, 2, figsize=(10, 4))
    
    bins = np.linspace (0, 1, 20, endpoint=False)
    ax1.hist (rotation_score, bins=bins, color='darkorange')
    ax1.axvline (0.5, ls='--', color='blue', lw=2)
    bins = np.linspace (0, 80, 20, endpoint=False)
    ax2.hist (prot, bins=bins, color='darkorange')
    ax2.hist (prot_ref, bins=bins, facecolor='none',
             edgecolor='black', label='Ref')
    
    ax1.set_ylabel (r'Number of stars')
    ax1.set_xlabel (r'Rotation score')
    ax2.set_xlabel (r'$P_\mathrm{rot}$ (day)')
    
    ax1.set_xlim (0, 1)
    ax2.set_xlim (0, 80)




.. parsed-literal::

    (0.0, 80.0)




.. image:: stellar_analysis_framework_files/stellar_analysis_framework_32_1.png

