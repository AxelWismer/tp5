from scipy.stats import chi2, ks_2samp, kstat, kstatvar, kstest, ksone, anderson_ksamp
# Devuelve el valor critico de la tabla

v = 1
alpha = 0.001

for v in range(1, 11):
    print("v", v,  ksone.ppf(1 - alpha / 2, v))

prob = 1 - 0.99


