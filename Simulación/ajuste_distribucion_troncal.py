
import numpy as np
import scipy.stats as st
import warnings
import pandas as pd


def best_fit_distribution(data, bins=200, ax=None):
    """Model data by finding best fit distribution to data"""
    
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    DISTRIBUTIONS = [st.gennorm,st.genexpon,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.nct,st.powerlognorm,st.norm, st.nct, st.uniform, st.poisson]
    #DISTRIBUTIONS = [st.norm, st.uniform ]

    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))

                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                
                except Exception:
                    pass

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass

    return (best_distribution.name, best_params)



data = pd.read_csv('Ingresos Troncal limpio.csv')

cols = [
    'Efectivo', 'Overpay', 'Monto Pasajes',
    'Monto Tarjeta Gral','Monto Tarjeta Per',
    'Monto Tarjeta Bpd', 'Recargas', 'Recargas Error',
    'Monto Total Efectivo', 'Monto Total Tarjetas'
]

df_por_dia = (
    data
    .groupby('Fecha', as_index=False)[cols]
    .sum()
)

cols_a_sumar = [
    'Efectivo', 'Monto Tarjeta Gral',
    'Monto Tarjeta Per', 'Monto Tarjeta Bpd',
    'Recargas', 'Recargas Error'
]

df_por_dia['Ingreso_Total'] = df_por_dia[cols_a_sumar].sum(axis=1)

df_por_dia['Fecha'] = pd.to_datetime(df_por_dia['Fecha'])

ingresos_totales = df_por_dia['Ingreso_Total'].values

best_fit_name, best_fit_params = best_fit_distribution(ingresos_totales, 200)

print(f"Best fit distribution: {best_fit_name}")
print(f"Best fit parameters: {best_fit_params}")



"""
data = pd.read_csv('Ingresos Troncal IQR.csv') 

best_fit_name, best_fit_params = best_fit_distribution(data['Ingreso_Total'].values, 200)
print(f"Best fit distribution: {best_fit_name}")
print(f"Best fit parameters: {best_fit_params}")
"""