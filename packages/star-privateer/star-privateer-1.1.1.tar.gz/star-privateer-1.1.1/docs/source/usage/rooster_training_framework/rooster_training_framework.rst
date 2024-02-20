ROOSTER training framework (MSAP4-03)
=====================================

This notebook provide an example of the analysis of a set of stars with
catalog-existing reference :math:`P_\mathrm{rot}`, and use the set to
train an instance of ROOSTER.

First we need to import the demonstrator module and the auxiliary module
containing the dataset we are going to work with.

**Note:** This notebook has been designed for the purpose of scientific
justification of PLATO MSAP4-03. The notebook illustrated the precise
flowchart envisaged for PLATO MSAP4-03 is cs_rooster_sph_analysis.ipynb

.. code:: ipython3

    import star_privateer as sp
    import plato_msap4_demonstrator_datasets.kepler_dataset as kepler_dataset

.. code:: ipython3

    sp.__version__




.. parsed-literal::

    '1.1.1'



We also need to import some other modules to run the notebook and to
check that the outputs directory that we need exist. In addition to
``star_privateer`` requirements, you should make sure that the
```pathos``
module <https://pathos.readthedocs.io/en/latest/index.html>`__ is
installed in order to run the analysis in parallel.

.. code:: ipython3

    import os, pathos
    import numpy as np
    import matplotlib.pyplot as plt
    from tqdm import tqdm
    
    if not os.path.exists ('rooster_training_features') :
        os.mkdir ('rooster_training_features')
    if not os.path.exists ('rooster_instances') :
        os.mkdir ('rooster_instances')

Running the analysis pipeline
-----------------------------

We are going to work with a sample of 1991 *Kepler* stars analysed by
Santos et al. (2019, 2021). The light curves have been calibrated with
the KEPSEISMIC method (see García et al. 2011, 2014), and all of them
have been filtered with a 55-day high-pass filter. We can get the
identifiers of the stars in the dataset with the following instruction:

.. code:: ipython3

    list_kic = sp.get_list_targets (kepler_dataset)

The next step is to run the analysis pipeline on every light curve in
the dataset. The analysis pipeline in its default behaviour will compute
the Lomb-Scargle periodogram (LSP) of the light curve as well as its
auto-correlation function (ACF). ACF and LSP will then be used to
compute a composite spectrum (CS), obtained by multiplying one by
another. The feature computed for each stars are stored in a dedicated
csv file identified by the star identifier (in this case, the KIC of the
star). We are going to parallelise the analysis process with ``pathos``
in order to gain some computation time and control memory leakages that
could arise from calling ``analysis_pipeline`` in a loop.

.. code:: ipython3

    def analysis_wrapper (kic) :
        """
        Analysis wrapper to speed computation
        by parallelising process and control
        memory usage.
        """
        str_kic = str (kic).zfill (9)
        filename = sp.get_target_filename (kepler_dataset, str_kic)
        fileout = 'rooster_training_features/{}.csv'.format(str_kic)
        fileplot = 'rooster_training_features/{}.png'.format(str_kic)
        if not os.path.exists (fileout) :
            t, s, dt = sp.load_resource (filename)
            (p_ps, p_acf, 
             ps, acf, 
             cs, features, 
             feature_names, 
             fig) = sp.analysis_pipeline (t, s, pmin=0.1, pmax=60,
                                          wavelet_analysis=False, plot=True,
                                          filename=fileplot, figsize=(10,16), 
                                          lw=1, dpi=300)
            df = sp.save_features (fileout, kic, features, feature_names)
            plt.close ("all")

Now that are wrapper function is defined, we just create a
``ProcessPool`` that we run with ``imap``:

   Note: by default ``imap``, on the contrary to ``map``, is a
   non-blocking process. Nevertheless, in order to display a progress
   bar with ``tqdm`` we need to use it, and the ``list`` encapsulation
   is there to ensure the process is blocking.

.. code:: ipython3

    process_pool = pathos.pools._ProcessPool (processes=4, 
                                              maxtasksperchild=10)
    with process_pool as p :
        list (tqdm (p.imap (analysis_wrapper,
                            list_kic,
                            ),
                    total=len (list_kic))
              )
        p.close ()


.. parsed-literal::

    100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1991/1991 [00:02<00:00, 813.84it/s]


After running the analysis pipeline, it is possible to concatenate the
feature obtained for each star into one big DataFrame.

.. code:: ipython3

    df = sp.build_catalog_features ('rooster_training_features')

This is typically what the DataFrame is going to look like:

.. code:: ipython3

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
          <th>891901</th>
          <td>72.869400</td>
          <td>51.574947</td>
          <td>5.641531</td>
          <td>11.498762</td>
          <td>16.801211</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.013099</td>
          <td>0.013099</td>
          <td>784.128871</td>
          <td>773.889578</td>
          <td>620.957800</td>
          <td>6.840314e+04</td>
          <td>0.0</td>
          <td>0.277619</td>
          <td>0.109637</td>
          <td>0.122620</td>
        </tr>
        <tr>
          <th>1162339</th>
          <td>73.786255</td>
          <td>78.690215</td>
          <td>-1.000000</td>
          <td>9.241541</td>
          <td>12.330192</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>-1.000000</td>
          <td>-1.000000</td>
          <td>2264.578879</td>
          <td>2190.576851</td>
          <td>-1.000000</td>
          <td>8.107581e+05</td>
          <td>0.0</td>
          <td>0.864250</td>
          <td>0.429628</td>
          <td>0.911895</td>
        </tr>
        <tr>
          <th>1163248</th>
          <td>72.325512</td>
          <td>59.625771</td>
          <td>31.106914</td>
          <td>10.129668</td>
          <td>14.071197</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.461511</td>
          <td>0.461511</td>
          <td>541.792440</td>
          <td>541.775945</td>
          <td>536.567054</td>
          <td>1.771122e+04</td>
          <td>0.0</td>
          <td>0.271948</td>
          <td>0.135494</td>
          <td>0.242804</td>
        </tr>
        <tr>
          <th>1164583</th>
          <td>49.879590</td>
          <td>43.891695</td>
          <td>46.649025</td>
          <td>9.570083</td>
          <td>15.528976</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>5.788649</td>
          <td>5.788649</td>
          <td>1650.038075</td>
          <td>1642.510883</td>
          <td>1699.105727</td>
          <td>1.188174e+05</td>
          <td>0.0</td>
          <td>0.635193</td>
          <td>0.317102</td>
          <td>0.470231</td>
        </tr>
        <tr>
          <th>1433067</th>
          <td>73.786360</td>
          <td>83.226618</td>
          <td>47.031942</td>
          <td>13.608601</td>
          <td>21.562106</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>1.743351</td>
          <td>1.743351</td>
          <td>1220.871088</td>
          <td>1261.758571</td>
          <td>1197.588777</td>
          <td>3.545902e+04</td>
          <td>0.0</td>
          <td>0.348045</td>
          <td>0.222222</td>
          <td>0.142060</td>
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
          <th>12647815</th>
          <td>10.332284</td>
          <td>10.421169</td>
          <td>10.439065</td>
          <td>0.916122</td>
          <td>1.113599</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.052547</td>
          <td>0.052547</td>
          <td>4731.203891</td>
          <td>4731.485721</td>
          <td>4725.580181</td>
          <td>1.736751e+06</td>
          <td>0.0</td>
          <td>0.993603</td>
          <td>0.606440</td>
          <td>0.928364</td>
        </tr>
        <tr>
          <th>12737258</th>
          <td>40.694822</td>
          <td>77.607082</td>
          <td>40.528748</td>
          <td>3.924354</td>
          <td>4.862094</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.874980</td>
          <td>0.874980</td>
          <td>2129.783908</td>
          <td>2155.527066</td>
          <td>2138.397742</td>
          <td>4.015526e+05</td>
          <td>0.0</td>
          <td>0.675193</td>
          <td>0.421634</td>
          <td>3.076674</td>
        </tr>
        <tr>
          <th>12784167</th>
          <td>18.391466</td>
          <td>12.709734</td>
          <td>46.124761</td>
          <td>2.039831</td>
          <td>2.621296</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>1.764008</td>
          <td>1.764008</td>
          <td>631.230913</td>
          <td>615.325577</td>
          <td>642.343757</td>
          <td>1.074141e+04</td>
          <td>0.0</td>
          <td>0.000056</td>
          <td>0.082313</td>
          <td>2.219790</td>
        </tr>
        <tr>
          <th>12834290</th>
          <td>52.170605</td>
          <td>57.295905</td>
          <td>53.100124</td>
          <td>5.944460</td>
          <td>7.698935</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>1.524360</td>
          <td>1.524360</td>
          <td>520.273316</td>
          <td>527.046251</td>
          <td>531.063571</td>
          <td>9.395823e+03</td>
          <td>0.0</td>
          <td>0.197379</td>
          <td>0.076179</td>
          <td>0.122809</td>
        </tr>
        <tr>
          <th>12834663</th>
          <td>89.966120</td>
          <td>91.438937</td>
          <td>-1.000000</td>
          <td>4.284101</td>
          <td>4.735059</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>-1.000000</td>
          <td>-1.000000</td>
          <td>1084.671035</td>
          <td>1084.671035</td>
          <td>-1.000000</td>
          <td>2.799866e+03</td>
          <td>0.0</td>
          <td>0.089992</td>
          <td>0.139271</td>
          <td>0.367917</td>
        </tr>
      </tbody>
    </table>
    <p>1991 rows × 17 columns</p>
    </div>



.. code:: ipython3

    df.to_csv ("training_features.csv")

Training and testing ROOSTER
----------------------------

Now that we have analysed a large sample of stars, we are able to use it
to train the random forest ROOSTER methodology (see Breton et al. 2021).
First, let’s (arbitrarily) divide our DataFrame into a training set and
a test set.

.. code:: ipython3

    df_train = df.loc[df.index[::2]]
    df_test = df.loc[df.index[1::2]]

The DataFrames let us obtain all the input we require to train and test
ROOSTER:

.. code:: ipython3

    (training_id, training_p_candidates, 
     training_features, feature_names) = sp.create_rooster_feature_inputs (df_train)
    (test_id, test_p_candidates, 
     test_features, test_feature_names) = sp.create_rooster_feature_inputs (df_test)

Now, let’s instantiate a new ROOSTER object. The main attributes of
ROOSTER are its two random forest classifiers, ``RotClass`` and
``PeriodSel``. The properties of these classifiers can be specified by
the user by passing the optional arguments of
``sklearn.ensemble.RandomForestClassifier`` to the created ROOSTER
instance.

.. code:: ipython3

    seed = 104359357
    chicken = sp.ROOSTER (n_estimators=100, random_state=np.random.RandomState (seed=seed))
    chicken.RotClass, chicken.PeriodSel




.. parsed-literal::

    (RandomForestClassifier(random_state=RandomState(MT19937) at 0x13483C440),
     RandomForestClassifier(random_state=RandomState(MT19937) at 0x13483C440))



The training is performed as follows:

.. code:: ipython3

    chicken.train (training_id, training_p_candidates,
                   training_features, feature_names=feature_names,
                   catalog='santos-19-21', verbose=True)


.. parsed-literal::

    Training RotClass with 390 stars with detected rotation and 494 without detected rotation.
    Training PeriodSel with 390 stars.


Once properly trained, ROOSTER performances can be assessed with our
test set:

.. code:: ipython3

    results = chicken.test (test_id, test_p_candidates, test_features, 
                            feature_names=test_feature_names, 
                            catalog='santos-19-21', verbose=True)


.. parsed-literal::

    Testing RotClass with 394 stars with detected rotation and 501 without detected rotation.
    Testing PeriodSel with 394 stars.


The score obtained during the test set can be accessed through the
``getScore`` function, as well as the number of elements used for the
training and the test steps.

.. code:: ipython3

    chicken.getScore ()




.. parsed-literal::

    (0.9329608938547486, 0.9238578680203046)



.. code:: ipython3

    chicken.getNumberEltTrain ()




.. parsed-literal::

    (884, 390)



.. code:: ipython3

    chicken.getNumberEltTest ()




.. parsed-literal::

    (895, 394)



The :math:`P_\mathrm{rot}` computed by ROOSTER for the test set are
returned when calling the function and it can be interesting to plot the
distribution to compare it to the reference catalog values.

.. code:: ipython3

    prot_rooster = results[3]
    prot_ref = sp.get_prot_ref (results[2], catalog='santos-19-21')

Let’s take a look at the corresponding histogram

.. code:: ipython3

    fig, ax = plt.subplots (1, 1)
    
    bins = np.linspace (0, 80, 20, endpoint=False)
    
    ax.hist (prot_rooster, bins=bins, color='darkorange', label='ROOSTER')
    ax.hist (prot_ref, bins=bins, facecolor='none',
            edgecolor='black', label='Ref')
    
    ax.set_xlabel (r'$P_\mathrm{rot}$ (day)')
    ax.set_ylabel (r'Number of stars')
    
    ax.legend ()




.. parsed-literal::

    <matplotlib.legend.Legend at 0x133e19e80>




.. image:: rooster_training_framework_files/rooster_training_framework_34_1.png


Finally, let’s save our trained ROOSTER instance to be able to use it
again later (for example in the next tutorial notebook !)

.. code:: ipython3

    chicken.save ('rooster_instances/rooster_tutorial')

