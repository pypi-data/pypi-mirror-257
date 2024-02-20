Fourier analysis (MSAP4-01A)
============================

.. code:: ipython3

    import star_privateer as sp
    import plato_msap4_demonstrator_datasets.plato_sim_dataset as plato_sim_dataset

.. code:: ipython3

    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd

K2: Rotation period analysis
----------------------------

.. code:: ipython3

    t, s, dt = sp.load_k2_example ()

.. code:: ipython3

    fig, ax = plt.subplots (1, 1, figsize=(8,4))
    
    ax.scatter (t[s!=0]-t[0], s[s!=0], color='black', 
                marker='o', s=1)
    
    ax.set_xlabel ('Time (day)')
    ax.set_ylabel ('Flux (ppm)')
    
    fig.tight_layout ()



.. image:: fourier_analysis_files/fourier_analysis_5_0.png


As we want to recover rotation periods below 45 days, we only consider
the section of the periodogram verifying
:math:`P < P_\mathrm{cutoff} = 60` days.

.. code:: ipython3

    pcutoff = 60

As a preprocessing step, we compute the Lomb-Scargle periodogram (in the
SAS framework, it will be directyly provided by MSAP1).

.. code:: ipython3

    p_ps, ls = sp.compute_lomb_scargle (t, s)

Now we perform the periodogram analysis.

.. code:: ipython3

    cond = p_ps < pcutoff
    (prot, e_p, E_p, 
     _, param, h_ps) = sp.compute_prot_err_gaussian_fit_chi2_distribution (p_ps[cond], ls[cond], n_profile=20, 
                                                                           threshold=0.1, plot_procedure=False,
                                                                           verbose=False)
    fig= sp.plot_ls (p_ps, ls, filename='figures/fourier_k2.png', param_profile=param, 
                     logscale=False, xlim=(0.1, 5))



.. image:: fourier_analysis_files/fourier_analysis_11_0.png


.. code:: ipython3

    IDP_SAS_PROT_FOURIER = sp.prepare_idp_fourier (param, h_ps, ls.size,
                                                  pcutoff=pcutoff, pthresh=None,
                                                  pfacutoff=1e-6)
    
    df = pd.DataFrame (data=IDP_SAS_PROT_FOURIER)
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
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>2.786835</td>
          <td>0.027592</td>
          <td>0.028150</td>
          <td>18241.430962</td>
          <td>1.000000e-16</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1.393417</td>
          <td>0.013796</td>
          <td>0.014075</td>
          <td>9355.805501</td>
          <td>1.000000e-16</td>
        </tr>
        <tr>
          <th>2</th>
          <td>0.786985</td>
          <td>0.056182</td>
          <td>0.065540</td>
          <td>2472.622236</td>
          <td>1.000000e-16</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    df.to_latex (buf='data_products/idp_sas_prot_fourier_k2_211015853.tex', 
                 formatters=['{:.2f}'.format, '{:.2f}'.format, '{:.2f}'.format,
                             '{:.2f}'.format, '{:.0e}'.format],  
                 index=False, header=False)
    np.savetxt ('data_products/IDP_SAS_PROT_FOURIER_K2.dat', 
                 IDP_SAS_PROT_FOURIER)

PLATO: Rotation period analysis
-------------------------------

The PLATO simulation below encompasses both rotational modulation and
low-frequency modulations due to activity. In order to analyse the
rotational signal, we first filter out frequencies above 60 days (in
PLATO, this will be done outside MSAP4).

.. code:: ipython3

    filename = sp.get_target_filename (plato_sim_dataset, '040', filetype='csv')
    t, s, dt = sp.load_resource (filename)
    s_filtered = sp.preprocess (t, s, cut=60)

.. code:: ipython3

    fig, ax = plt.subplots (1, 1, figsize=(8,4))
    
    ax.scatter (t[s!=0]-t[0], s[s!=0], color='black', 
                marker='o', s=1, label="Unfiltered")
    ax.scatter (t[s!=0]-t[0], s_filtered[s_filtered!=0], color='darkorange', 
                marker='o', s=1, label="Filtered")
    
    ax.set_xlabel ('Time (day)')
    ax.set_ylabel ('Flux (ppm)')
    
    ax.legend ()
    
    fig.tight_layout ()



.. image:: fourier_analysis_files/fourier_analysis_17_0.png


As we want to recover rotation periods below 60 days, we only consider
the section of the periodogram verifying
:math:`P < P_\mathrm{cutoff} = 60` days.

.. code:: ipython3

    pcutoff = 60

As a preprocessing step, we compute the Lomb-Scargle periodogram (in the
SAS framework, it will be directyly provided by MSAP1).

.. code:: ipython3

    p_ps, ls = sp.compute_lomb_scargle (t, s_filtered)

Now we perform the periodogram analysis.

.. code:: ipython3

    cond = p_ps < pcutoff
    (prot, e_p, E_p, 
     _, param, h_ps) = sp.compute_prot_err_gaussian_fit_chi2_distribution (p_ps[cond], 
                                                                           ls[cond], 
                                                                           n_profile=20, 
                                                                           threshold=0.1,
                                                                           verbose=False)
    sp.plot_ls (p_ps, ls, filename='figures/fourier_plato_short.png', param_profile=param, 
                logscale=False, xlim=(1, pcutoff), 
                ylim=(1e-3, 1.25e6),
                )
    IDP_SAS_PROT_FOURIER = sp.prepare_idp_fourier (param, h_ps, ls.size,
                                                      pcutoff=pcutoff, pthresh=None,
                                                      pfacutoff=1e-6)
    df = pd.DataFrame (data=IDP_SAS_PROT_FOURIER)
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
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>25.969122</td>
          <td>2.720310</td>
          <td>3.441268</td>
          <td>791101.027115</td>
          <td>1.000000e-16</td>
        </tr>
        <tr>
          <th>1</th>
          <td>36.172726</td>
          <td>3.871280</td>
          <td>4.925569</td>
          <td>660816.783569</td>
          <td>1.000000e-16</td>
        </tr>
        <tr>
          <th>2</th>
          <td>50.083306</td>
          <td>2.931017</td>
          <td>3.319557</td>
          <td>99449.921037</td>
          <td>1.000000e-16</td>
        </tr>
        <tr>
          <th>3</th>
          <td>19.091161</td>
          <td>2.501881</td>
          <td>3.390534</td>
          <td>93860.256080</td>
          <td>1.000000e-16</td>
        </tr>
      </tbody>
    </table>
    </div>




.. image:: fourier_analysis_files/fourier_analysis_23_1.png


.. code:: ipython3

    df.to_latex (buf='data_products/idp_sas_prot_fourier_plato_040.tex', 
                 formatters=['{:.2f}'.format, '{:.2f}'.format, '{:.2f}'.format,
                             '{:.2f}'.format, '{:.0e}'.format],  
                 index=False, header=False)
    np.savetxt ('data_products/IDP_SAS_PROT_FOURIER_PLATO.dat', 
                 IDP_SAS_PROT_FOURIER)

PLATO: Long term modulation analysis
------------------------------------

This time, we are interested in recovering long term modulations. We
consider the section of the periodogram verifying
:math:`P > P_\mathrm{tresh} = 60` days.

.. code:: ipython3

    pthresh = 60

As a preprocessing step, we compute the Lomb-Scargle periodogram (in the
SAS framework, it will be directyly provided by MSAP1).

.. code:: ipython3

    p_ps, ls = sp.compute_lomb_scargle (t, s)

Now we perform the periodogram analysis.

.. code:: ipython3

    (plongterm, e_p, E_p, 
     _, param, h_ps) = sp.compute_prot_err_gaussian_fit_chi2_distribution (p_ps[p_ps>pthresh], 
                                                                           ls[p_ps>pthresh], 
                                                                           n_profile=5, 
                                                                           threshold=0.1, 
                                                                           verbose=False)
    fig = sp.plot_ls (p_ps, ls, filename='figures/fourier_plato_long.png', param_profile=param, 
                        logscale=False, xlim=(1,8*pthresh))
    IDP_SAS_LONGTERM_MODULATION_FOURIER = sp.prepare_idp_fourier (param, h_ps, ls.size,
                                                                     pcutoff=None, pthresh=pthresh,
                                                                     pfacutoff=1e-6)
    df = pd.DataFrame (data=IDP_SAS_LONGTERM_MODULATION_FOURIER)
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
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>347.077309</td>
          <td>16.527491</td>
          <td>18.267227</td>
          <td>8.754753e+06</td>
          <td>1.000000e-16</td>
        </tr>
        <tr>
          <th>1</th>
          <td>694.154619</td>
          <td>33.054982</td>
          <td>36.534454</td>
          <td>2.280495e+06</td>
          <td>1.000000e-16</td>
        </tr>
      </tbody>
    </table>
    </div>




.. image:: fourier_analysis_files/fourier_analysis_31_1.png


.. code:: ipython3

    df.to_latex (buf='data_products/idp_sas_longterm_modulation_fourier_plato_040.tex', 
                 formatters=['{:.2f}'.format, '{:.2f}'.format, '{:.2f}'.format,
                             '{:.2f}'.format, '{:.0e}'.format],  
                 index=False, header=False)
    np.savetxt ('data_products/IDP_SAS_LONGTERM_MODULATION_FOURIER_PLATO.dat', 
                 IDP_SAS_LONGTERM_MODULATION_FOURIER)

