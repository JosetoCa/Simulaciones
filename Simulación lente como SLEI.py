import funciones
import matplotlib.pyplot as plt
import numpy as np

f = 100

p = funciones.planos()
prop = funciones.propagacion()

primer_campo = p.centro_cuadrado(l = 5)
campo_propagado = prop.propaTF(primer_campo, z = f)
lente_10 = p.lente_delgado_centrado(f = f)
campo_a_propagar = campo_propagado*lente_10

segundo_campo = prop.propaTF(campo_a_propagar, z = f)

campo_propagado_ =  prop.propaTF(segundo_campo, z = f)
campo_a_propagar_ = campo_propagado_*lente_10

campo_resultante = prop.propaTF(campo_a_propagar_, z = f)
#p.mostrar_campo(campo_resultante)

# Muestra del sistema dos f como un sistema espacialmente invariante.

matriz = np.zeros_like(primer_campo)
radio_pix = 50
centro = p.N // 4
x = np.arange(p.N)
y = np.arange(p.N)
X, Y = np.meshgrid(x, y)

distancia_cuadrada = (X - centro)**2 + (Y - 2*centro)**2

matriz[distancia_cuadrada <= radio_pix**2] = 1


p.asignar_objeto("ventana circular",matriz)

matriz = np.zeros_like(primer_campo)
l_pix = 50

i0x = int( (p.N - l_pix) / 2 + p.N/4)
i0y = int( (p.N - l_pix) / 2)
i1y = int( (p.N + l_pix) / 2)
i1 = int( (p.N + l_pix) / 2 +p.N/4)
matriz[i0y:i1y, i0x:i1] = 1
p.asignar_objeto("ventana cuadrada",matriz)



ventana_circ = p.objetos["ventana circular"] 
campo_propagado_circ = prop.propaTF(ventana_circ, z = f)
lente_10 = p.lente_delgado_centrado(f = f)
campo_a_propagar_circ = campo_propagado_circ*lente_10
TF_ventana_circ = prop.propaTF(campo_a_propagar_circ, z = f)
p.mostrar_campo(TF_ventana_circ)
ventana_cua = p.objetos["ventana cuadrada"] 
campo_propagado_cua = prop.propaTF(ventana_cua, z = f)
lente_10 = p.lente_delgado_centrado(f = f)
campo_a_propagar_cua = campo_propagado_cua*lente_10
TF_ventana_cua = prop.propaTF(campo_a_propagar_cua, z = f)
p.mostrar_campo(TF_ventana_cua)

suma = TF_ventana_cua + TF_ventana_circ
p.mostrar_campo(suma)

ventana_cua = ventana_circ+ventana_cua 
campo_propagado_cua = prop.propaTF(ventana_cua, z = f)
lente_10 = p.lente_delgado_centrado(f = f)
campo_a_propagar_cua = campo_propagado_cua*lente_10
TF_ventana_cua = prop.propaTF(campo_a_propagar_cua, z = f)
p.mostrar_campo(TF_ventana_cua)