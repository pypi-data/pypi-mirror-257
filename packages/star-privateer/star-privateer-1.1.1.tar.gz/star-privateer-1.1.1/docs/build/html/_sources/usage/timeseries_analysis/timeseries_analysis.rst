Time series analysis (MSAP4-02)
===============================

.. code:: ipython3

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

.. code:: ipython3

    import star_privateer as sp
    import plato_msap4_demonstrator_datasets.plato_sim_dataset as plato_sim_dataset

K2: Preprocessing
-----------------

This first part include preprocessing tasks that are not actually
included in MSAP4-02 but are useful for the subsequent analysis.

.. code:: ipython3

    t, s0, dt = sp.load_k2_example ()

.. code:: ipython3

    fig, ax = plt.subplots (1, 1, figsize=(8,4))
    
    ax.scatter (t[s0!=0]-t[0], s0[s0!=0], color='black', 
                marker='o', s=1)
    
    ax.set_xlabel ('Time (day)')
    ax.set_ylabel ('Flux (ppm)')
    
    fig.tight_layout ()
    
    plt.savefig ('figures/k2_lc.png', dpi=300)



.. image:: timeseries_analysis_files/timeseries_analysis_6_0.png


.. code:: ipython3

    pcutoff = 60
    pthresh = 60

K2: Rotation period analysis
----------------------------

In the next step, we compute the ACF and we analyse the characteristic
periodicities obtained from the function, considering only periods below
:math:`P_\mathrm{cutoff}`.

.. code:: ipython3

    p_acf, acf = sp.compute_acf (s0, dt, normalise=True,
                                use_scipy_correlate=True, verbose=True)
    _, _, _, _, prots, hacf, gacf = sp.find_period_acf (p_acf, acf, pcutoff=pcutoff)
    fig = sp.plot_acf (p_acf, acf, prot=prots, filename='figures/acf_k2.png')



.. image:: timeseries_analysis_files/timeseries_analysis_10_0.png


We can take a look at the values we have extracted from the ACF. Most
often, the rotation period can be linked to the first value of the
``prots`` array.

.. code:: ipython3

    prots[0], hacf[0], gacf[0]




.. parsed-literal::

    (2.6765510971308686, 1.219105626528322, 0.8085280511689089)



Finally we create the intermediate data product.

.. code:: ipython3

    IDP_SAS_ACF_FILT_TIMESERIES = np.c_[p_acf, acf]
    IDP_SAS_PROT_TIMESERIES = np.c_[prots, np.full (prots.size, -1), np.full (prots.size, -1),
                                    hacf, gacf, np.arange (prots.size)+1]
    np.savetxt ('data_products/IDP_SAS_PROT_TIMESERIES_K2.dat', 
                IDP_SAS_PROT_TIMESERIES)
    np.savetxt ('data_products/IDP_SAS_ACF_FILT_TIMESERIES_K2.dat', 
                IDP_SAS_ACF_FILT_TIMESERIES)
    df = pd.DataFrame (data=IDP_SAS_PROT_TIMESERIES)
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
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
          <th>4</th>
          <th>5</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>2.676551</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>1.219106</td>
          <td>0.808528</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>5.271375</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>1.142988</td>
          <td>0.761694</td>
          <td>2.0</td>
        </tr>
        <tr>
          <th>2</th>
          <td>7.947927</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.984593</td>
          <td>0.642715</td>
          <td>3.0</td>
        </tr>
        <tr>
          <th>3</th>
          <td>10.583614</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.910175</td>
          <td>0.586043</td>
          <td>4.0</td>
        </tr>
        <tr>
          <th>4</th>
          <td>13.280597</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.746789</td>
          <td>0.483461</td>
          <td>5.0</td>
        </tr>
        <tr>
          <th>5</th>
          <td>15.875421</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.743666</td>
          <td>0.437643</td>
          <td>6.0</td>
        </tr>
        <tr>
          <th>6</th>
          <td>18.592836</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.717921</td>
          <td>0.408310</td>
          <td>7.0</td>
        </tr>
        <tr>
          <th>7</th>
          <td>21.187660</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.642279</td>
          <td>0.351740</td>
          <td>8.0</td>
        </tr>
        <tr>
          <th>8</th>
          <td>23.884643</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.621054</td>
          <td>0.350691</td>
          <td>9.0</td>
        </tr>
        <tr>
          <th>9</th>
          <td>26.499899</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.533378</td>
          <td>0.282954</td>
          <td>10.0</td>
        </tr>
        <tr>
          <th>10</th>
          <td>29.156018</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.508112</td>
          <td>0.272964</td>
          <td>11.0</td>
        </tr>
        <tr>
          <th>11</th>
          <td>31.791706</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.426513</td>
          <td>0.215709</td>
          <td>12.0</td>
        </tr>
        <tr>
          <th>12</th>
          <td>34.427394</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.379729</td>
          <td>0.199663</td>
          <td>13.0</td>
        </tr>
        <tr>
          <th>13</th>
          <td>36.981355</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.304468</td>
          <td>0.152380</td>
          <td>14.0</td>
        </tr>
        <tr>
          <th>14</th>
          <td>39.637474</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.267633</td>
          <td>0.141080</td>
          <td>15.0</td>
        </tr>
        <tr>
          <th>15</th>
          <td>42.109708</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.232925</td>
          <td>0.122093</td>
          <td>16.0</td>
        </tr>
        <tr>
          <th>16</th>
          <td>44.786260</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.219537</td>
          <td>0.117616</td>
          <td>17.0</td>
        </tr>
        <tr>
          <th>17</th>
          <td>47.340221</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.192786</td>
          <td>0.100213</td>
          <td>18.0</td>
        </tr>
        <tr>
          <th>18</th>
          <td>49.955477</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.178725</td>
          <td>0.089382</td>
          <td>19.0</td>
        </tr>
        <tr>
          <th>19</th>
          <td>52.550301</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.154197</td>
          <td>0.068293</td>
          <td>20.0</td>
        </tr>
        <tr>
          <th>20</th>
          <td>55.226852</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.123732</td>
          <td>0.046698</td>
          <td>21.0</td>
        </tr>
        <tr>
          <th>21</th>
          <td>56.902250</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.051635</td>
          <td>0.020629</td>
          <td>22.0</td>
        </tr>
        <tr>
          <th>22</th>
          <td>57.678655</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.064155</td>
          <td>0.037136</td>
          <td>23.0</td>
        </tr>
        <tr>
          <th>23</th>
          <td>59.783118</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.040878</td>
          <td>0.015503</td>
          <td>24.0</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    df.to_latex (buf='data_products/idp_msap4_02_idp_prot_timeseries.tex', 
                 formatters=['{:.2f}'.format, '{:.0f}'.format, '{:.0f}'.format,
                             '{:.2f}'.format, '{:.2f}'.format, '{:.0f}'.format,],  
                 index=False, header=False)

Note that, due to the short length of this light curve, we do not show
for this first case the analysis of long term modulations.

PLATO simulation: Preprocessing
-------------------------------

This first part include preprocessing tasks that are not actually
included in MSAP4-02 but are useful for the subsequent analysis.

.. code:: ipython3

    filename = sp.get_target_filename (plato_sim_dataset, '040', filetype='csv')
    t, s0, dt = sp.load_resource (filename)

.. code:: ipython3

    fig, ax = plt.subplots (1, 1, figsize=(8,4))
    
    ax.scatter (t[s0!=0]-t[0], s0[s0!=0], color='black', 
                marker='o', s=1)
    
    ax.set_xlabel ('Time (day)')
    ax.set_ylabel ('Flux (ppm)')
    
    fig.tight_layout ()
    
    
    plt.savefig ('figures/plato_lc.png', dpi=300)



.. image:: timeseries_analysis_files/timeseries_analysis_20_0.png


.. code:: ipython3

    s = sp.preprocess (t, s0, cut=60)
    pcutoff = 60
    pthresh = 60

PLATO simulation: Rotation period analysis
------------------------------------------

This first part include preprocessing task that are not actually
included in MSAP4-02 but are useful for the subsequent analysis.

.. code:: ipython3

    fig, ax = plt.subplots (1, 1, figsize=(8,4))
    
    ax.scatter (t[s!=0]-t[0], s[s!=0], color='black', 
                marker='o', s=1)
    
    ax.set_xlabel ('Time (day)')
    ax.set_ylabel ('Flux (ppm)')
    
    fig.tight_layout ()
    
    plt.savefig ('figures/plato_lc_filtered.png', dpi=300)



.. image:: timeseries_analysis_files/timeseries_analysis_24_0.png


.. code:: ipython3

    p_acf, acf = sp.compute_acf (s, dt, normalise=True, use_scipy_correlate=True)
    _, _, _, _, prots, hacf, gacf = sp.find_period_acf (p_acf, acf, pcutoff=pcutoff)
    fig = sp.plot_acf (p_acf, acf, prot=prots, filename='figures/acf_plato_short.png')



.. image:: timeseries_analysis_files/timeseries_analysis_25_0.png


.. code:: ipython3

    IDP_SAS_ACF_FILT_TIMESERIES = np.c_[p_acf, acf]
    IDP_SAS_PROT_TIMESERIES = np.c_[prots, np.full (prots.size, -1), np.full (prots.size, -1),
                                    hacf, gacf, np.arange (prots.size)+1]
    np.savetxt ('data_products/IDP_SAS_PROT_TIMESERIES_PLATO.dat', 
                IDP_SAS_PROT_TIMESERIES)
    np.savetxt ('data_products/IDP_SAS_ACF_FILT_TIMESERIES_PLATO.dat', 
                IDP_SAS_ACF_FILT_TIMESERIES)

PLATO simulation: Long term modulation analysis
-----------------------------------------------

This time, we do not consider filtered out the data in order to consider
long term modulations. We put a period threshold at 60 days to consider
only long period in the postprocessing of our analysis. In the figure
below, note that a Gaussian smoothing window is applied before looking
for local maxima, shown in orange in the figure below.

.. code:: ipython3

    p_acf, acf = sp.compute_acf (s0, dt, normalise=True, pthresh=pthresh, 
                                use_scipy_correlate=True, verbose=True)
    (_, hacf, gacf, _, 
    pmods, hacf, gacf, acf_smooth) = sp.find_period_acf (p_acf, acf, pthresh=pthresh,
                                                         return_smoothed_acf=True)
    fig = sp.plot_acf (p_acf, acf, prot=pmods, 
                       acf_additional=acf_smooth,
                       color_additional="darkorange", 
                       filename="figures/acf_plato_long.png")



.. image:: timeseries_analysis_files/timeseries_analysis_29_0.png


.. code:: ipython3

    IDP_SAS_ACF_TIMESERIES = np.c_[p_acf, acf]
    IDP_SAS_LONGTERM_MODULATION_TIMESERIES = np.c_[pmods, np.full (pmods.size, -1), np.full (pmods.size, -1),
                                                                    hacf, gacf, np.arange (pmods.size)+1]
    np.savetxt ('data_products/IDP_SAS_LONGTERM_MODULATION_TIMESERIES_PLATO.dat', 
                IDP_SAS_PROT_TIMESERIES)
    np.savetxt ('data_products/IDP_SAS_ACF_TIMESERIES_PLATO.dat', 
                IDP_SAS_ACF_TIMESERIES)
    df = pd.DataFrame (data=IDP_SAS_LONGTERM_MODULATION_TIMESERIES)
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
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
          <th>4</th>
          <th>5</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>289.505092</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.301008</td>
          <td>0.199352</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>309.199410</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.023280</td>
          <td>0.229724</td>
          <td>2.0</td>
        </tr>
        <tr>
          <th>2</th>
          <td>330.483996</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.200066</td>
          <td>0.222273</td>
          <td>3.0</td>
        </tr>
        <tr>
          <th>3</th>
          <td>584.308760</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.092116</td>
          <td>0.065606</td>
          <td>4.0</td>
        </tr>
        <tr>
          <th>4</th>
          <td>604.933628</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.029614</td>
          <td>0.086868</td>
          <td>5.0</td>
        </tr>
        <tr>
          <th>5</th>
          <td>653.718038</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.009202</td>
          <td>0.050910</td>
          <td>6.0</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    df.to_latex (buf='data_products/idp_msap4_02_idp_longterm_modulation_timeseries.tex', 
                 formatters=['{:.2f}'.format, '{:.0f}'.format, '{:.0f}'.format,
                             '{:.2f}'.format, '{:.2f}'.format, '{:.0f}'.format,],  
                 index=False, header=False)
