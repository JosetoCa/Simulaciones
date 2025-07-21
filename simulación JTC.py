import funciones
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve

f = 220


joa = funciones.planos(512)

matriz_A = joa.letra("D", 200)
matriz_B = joa.letra("G", 200)

A_B = joa.sumar(matriz_A, matriz_B, -120, "v")
plt.imshow(A_B, cmap= 'gray')
plt.colorbar()
plt.show()

p = funciones.planos(A_B.shape[0])
prop = funciones.propagacion(10, A_B.shape[0])

A_B_prop = prop.propaTF(A_B, z = f)
A_B_lente = A_B_prop*p.lente_delgado_centrado(f = f)
U = np.abs(prop.propaTF(A_B_lente, z = f))**2

U_prop = prop.propaTF(U, z = f)
U_lente = U_prop*p.lente_delgado_centrado(f = f)
Uf = prop.propaTF(U_lente, z = f)


ventana = p.centro_cuadrado(2.5)
contraventana = (ventana == 0)
semiUf = Uf * contraventana
p.mostrar_campo(semiUf)


