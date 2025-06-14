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
p.mostrar_campo(campo_resultante)
