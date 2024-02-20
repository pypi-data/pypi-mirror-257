Cycle determination (MSAP4-06)
==============================

This notebook provides the test cases described in the MSAP4-06
submodule documentation.

.. code:: ipython3

    import star_privateer as sp

.. code:: ipython3

    import numpy as np
    import matplotlib.pyplot as plt

Preprocessing
-------------

In order to demonstrate the ability of MSAP4-06, we choose KIC~3733735,
as its observing time/rotation period ratio is important and will allow
us to perform meaningful computation on the :math:`S_\mathrm{ph}` time
series. We then start by computing this ACF time series, which is
normally an IDP input provided by MSAP4-03. We consider the 2.57 days
rotation period from `Santos et
al. (2021) <https://ui.adsabs.harvard.edu/abs/2021ApJS..255...17S/abstract>`__.

.. code:: ipython3

    filename = sp.get_target_filename (sp.timeseries, '003733735')
    t, s, dt = sp.load_resource (filename)
    pcutoff = (t[-1]-t[0])/2

.. code:: ipython3

    prot = 2.57
    _, t_sph, sph = sp.compute_sph (t, s, prot, 
                                              return_timeseries=True)

.. code:: ipython3

    fig, ax = plt.subplots (1, 1)
    
    ax.plot (t_sph, sph, color='darkorange', zorder=-1)
    ax.scatter (t_sph, sph, color='darkorange', edgecolor='black',
                marker='o', s=40)
    
    ax.set_xlabel ('Time (day)')
    ax.set_ylabel (r'$S_\mathrm{ph}$ (ppm)')
    
    fig.tight_layout ()
    
    plt.savefig ('figures/kic3733735_sph_timeseries.png', dpi=300)



.. image:: cycle_determination_files/cycle_determination_6_0.png


Computing the ACF and GLS of the ACF time series
------------------------------------------------

Now that we have our :math:`S_\mathrm{ph}` time series, let’s compute
its autocorrelation function and analyse it to extract periodicities
above :math:`P_\mathrm{thresh}`.

.. code:: ipython3

    dt_sph = np.median (np.diff (t_sph))
    p_acf_sph, acf_sph = sp.compute_acf (sph - np.mean (sph), dt_sph, normalise=True,
                                            use_scipy_correlate=True, smooth=False)
    _, _, _, _, pmods_sph_acf, hacf, gacf = sp.find_period_acf (p_acf_sph, acf_sph, pcutoff=pcutoff)
    fig = sp.plot_acf (p_acf_sph, acf_sph, prot=pmods_sph_acf, 
                          xlim=(0,750), filename='figures/kic3733735_sph_acf.png')



.. image:: cycle_determination_files/cycle_determination_9_0.png


.. code:: ipython3

    pmods_sph_acf, hacf, gacf




.. parsed-literal::

    (array([], dtype=float64), array([], dtype=float64), array([], dtype=float64))



The second step is to compute the Lomb-Scargle periodogram of our
:math:`S_\mathrm{ph}` time series.

.. code:: ipython3

    p_ps, ls, ps_object = sp.compute_lomb_scargle_sph (t_sph, sph)
    (pmods_sph_fourier, e_p, 
     E_p, _, param, h_ps) = sp.compute_prot_err_gaussian_fit_chi2_distribution (p_ps[p_ps<pcutoff], ls[p_ps<pcutoff], 
                                                                                n_profile=5, threshold=0.1, verbose=False)
    fig = sp.plot_ls (p_ps, ls, filename='figures/kic3733735_sph_fourier.png', 
                         logscale=False, param_profile=param,
                         ylim=(0, 0.1),
                         xlim=(2*dt_sph, 700))



.. image:: cycle_determination_files/cycle_determination_12_0.png


Building the :math:`S_\mathrm{ph}` intermediate data products
-------------------------------------------------------------

We build here the intermediate data products related to the
:math:`S_\mathrm{ph}` analysis.

.. code:: ipython3

    IDP_SAS_LONGTERM_MODULATION_SPH_FOURIER = sp.prepare_idp_fourier (param, h_ps, ls.size,
                                                                 pcutoff=pcutoff, pthresh=None,
                                                                 pfacutoff=1)
    IDP_SAS_LONGTERM_MODULATION_SPH_TIMESERIES = np.c_[pmods_sph_acf, 
                                               np.full (pmods_sph_acf.size, -1), 
                                               np.full (pmods_sph_acf.size, -1),
                                               hacf, gacf, 
                                               np.arange (pmods_sph_acf.size)+1]

.. code:: ipython3

    pd.DataFrame (data=IDP_SAS_LONGTERM_MODULATION_SPH_FOURIER)




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
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>90.525132</td>
          <td>6.534924</td>
          <td>7.637630</td>
          <td>0.069541</td>
          <td>0.932822</td>
        </tr>
        <tr>
          <th>1</th>
          <td>369.415642</td>
          <td>17.744229</td>
          <td>19.630016</td>
          <td>0.031863</td>
          <td>0.968640</td>
        </tr>
        <tr>
          <th>2</th>
          <td>120.700176</td>
          <td>8.772988</td>
          <td>10.265226</td>
          <td>0.028122</td>
          <td>0.972269</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    pd.DataFrame (data=IDP_SAS_LONGTERM_MODULATION_SPH_TIMESERIES)




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
      </tbody>
    </table>
    </div>



Comparing the long term modulations
-----------------------------------

Finally, we complete our set with mock (and arbitrary) data to
illustrate how long term modulations from different IDP should be
compared.

.. code:: ipython3

    IDP_SAS_LONGTERM_MODULATION_FOURIER = np.array ([[90, 3, 3, 1, 1e-16],
                                                      [130, 5, 5, 1, 1e-16]])
    IDP_SAS_LONGTERM_MODULATION_TIMESERIES = np.array ([[91, -1, -1, .3, .5, 1],
                                                        [132, -1, -1, .3, .4, 1],
                                                        [180, -1, -1, .3, .6, 2]])

.. code:: ipython3

    DP4_SAS_LONGTERM_MODULATION = sp.build_long_term_modulation (
                                    IDP_SAS_LONGTERM_MODULATION_FOURIER, 
                                    IDP_SAS_LONGTERM_MODULATION_TIMESERIES,
                                    IDP_SAS_LONGTERM_MODULATION_SPH_FOURIER, 
                                    IDP_SAS_LONGTERM_MODULATION_SPH_TIMESERIES,
                                    h_acf_min=0.2, g_acf_min=0.5
                                    )

.. code:: ipython3

    DP4_SAS_LONGTERM_MODULATION




.. parsed-literal::

    array([[90.        ,  3.        ,  3.        , 91.        , -1.        ,
            -1.        , 90.52513177,  6.53492374,  7.63763039, -1.        ,
            -1.        , -1.        ]])



.. code:: ipython3

    pd.DataFrame (data=DP4_SAS_LONGTERM_MODULATION)




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
          <th>6</th>
          <th>7</th>
          <th>8</th>
          <th>9</th>
          <th>10</th>
          <th>11</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>90.0</td>
          <td>3.0</td>
          <td>3.0</td>
          <td>91.0</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>90.525132</td>
          <td>6.534924</td>
          <td>7.63763</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>-1.0</td>
        </tr>
      </tbody>
    </table>
    </div>



