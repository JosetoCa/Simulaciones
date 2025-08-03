import funciones
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve

f = 220
mm = 10

joa = funciones.planos(512, tamaño_mm=mm)

matriz_A = joa.recorte("C:\Proyectos\Simulaciones\ImSpeckle\\4-150-1.tif", (2))

matriz_B = joa.letra("Z", tamaño_fuente=int(round(2* joa.N / joa.tamaño_mm)))*np.max(matriz_A)


#matriz_B = np.zeros_like(matriz_A)
#matriz_B = joa.recorte("C:\Proyectos\Simulaciones\ImSpeckle\\4-150-1.tif", (2))

#matriz_B = joa.recorte("C:\Proyectos\Simulaciones\ImSpeckle\\4-150-1.tif", 2)


A_B = joa.sumar(matriz_A, matriz_B, -150, "v")
plt.imshow(A_B, cmap= 'gray')
plt.colorbar()
plt.show()



p = funciones.planos(A_B.shape[0])
prop = funciones.propagacion(mm, A_B.shape[0])

A_B_prop = prop.propaTF(A_B, z = f)




A_B_lente = A_B_prop*p.lente_delgado_centrado(f = f)

p.mostrar_campo(np.abs(A_B_lente)**(1/2))

U = np.abs(prop.propaTF(A_B_lente, z = f))**2

U_prop = prop.propaTF(U, z = f)
U_lente = U_prop*p.lente_delgado_centrado(f = f)
Uf = prop.propaTF(U_lente, z = f)
p.mostrar_campo(Uf)


ventana = p.centro_cuadrado(2.5)
contraventana = (ventana == 0)
semiUf = Uf * contraventana
p.mostrar_campo(semiUf)
