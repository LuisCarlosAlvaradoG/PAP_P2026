from scipy.special import gamma, gammaln
import numpy as np

# Ingreso Alimentadora días entre semana

gamma_am_week = gamma(1 + (1/11400.5385))

# Ingreso Alimentadora Sabado

n_am_st = 10028.3971
cociente_am_st = gammaln((n_am_st - 1) / 2) - gammaln(n_am_st / 2)
gamma_am_st = np.sqrt(n_am_st / 2) * np.exp(cociente_am_st)

# Ingreso Troncal días entre semana

gamma_tr_week = gamma(1 + (1/19.1272))

# Ingreso Troncal domingo

gamma_tr_sd = gamma(1 + (1/6.0617))

# Costos Generales

gamma_cg = gamma(1 + (1/1.4785))

# Costos Operativos Alimentadoras

m_co_am = 0.9467

gamma_co_am = gamma(m_co_am + 0.5) / gamma(m_co_am)

# Costos Operativos Troncal

m_co_tr = 0.9467

gamma_co_tr = gamma(m_co_tr + 0.5) / gamma(m_co_tr)


# Kilómetros Programados Alimentadoras

gamma_km_am = gamma(1 + (1/16.8852))

# Kilometros Programados Troncal

gamma_km_tr = gamma(1 + (1/56184577.6611))

# Utilidad Operativa Alimentadoras

n_uo_am = 3.3439
cociente_uo_am = gammaln((n_uo_am - 1) / 2) - gammaln(n_uo_am / 2)
gamma_uo_am = np.sqrt(n_uo_am / 2) * np.exp(cociente_uo_am)

# Utilidad Operativa Troncal

gamma_uo_tr = gamma(1 + (1/12.4201))







# Resultados
print("Valor de gamma para ingresos alimentadora días entre semana:", gamma_am_week)
print("Valor de gamma para ingresos alimentadora sábado:", gamma_am_st)
print("Valor de gamma para ingresos troncal días entre semana:", gamma_tr_week)
print("Valor de gamma para ingresos troncal domingo:", gamma_tr_sd)
print("Valor de gamma para costos generales:", gamma_cg)
print("Valor de gamma para costos operativos alimentadoras:", gamma_co_am)
print("Valor de gamma para costos operativos troncal:", gamma_co_tr)
print("Valor de gamma para kilómetros programados alimentadoras:", gamma_km_am)
print("Valor de gamma para kilómetros programados troncal:", gamma_km_tr)
print("Valor de gamma para utilidad operativa alimentadoras:", gamma_uo_am)
print("Valor de gamma para utilidad operativa troncal:", gamma_uo_tr)