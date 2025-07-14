import funciones
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve

f = 180


p = funciones.planos()
prop = funciones.propagacion()

matriz_A = p.letra("A", 900)
matriz_B = p.letra("A", 900)

A_prop = prop.propaTF(matriz_A, z = f)
A_lente = A_prop*p.lente_delgado_centrado(f = f)
filtro = np.conj(prop.propaTF(A_lente, z = f))

B_prop = prop.propaTF(matriz_B, z = f)
B_lente = B_prop*p.lente_delgado_centrado(f = f)
U1 = filtro*prop.propaTF(B_lente, z = f)
U1_prop = prop.propaTF(U1, z = f)
U1_lente = U1_prop*p.lente_delgado_centrado(f = f)
U2 = prop.propaTF(U1_lente, z = f)

p.mostrar_campo(U2 )




plt.imshow(np.abs(fftconvolve(np.flipud(np.fliplr(matriz_B)), matriz_A , mode = "same")), cmap='gray')
plt.colorbar()
plt.show()

