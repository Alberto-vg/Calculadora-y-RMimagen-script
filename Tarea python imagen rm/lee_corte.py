import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

# Cargar el volumen NIfTI
img = nib.load('sub-01_T1w.nii')
vol = img.get_fdata()

# Obtener el tamaño del volumen
sx = vol.shape[0]
sy = vol.shape[1]
sz = vol.shape[2]

# Obtener los puntos medios de cada eje
mx = int(sx / 2)
my = int(sy / 2)
mz = int(sz / 2)

# Sacar los cortes de cada plano
# sagital = plano en X fijo
sagital = vol[mx, :, :]     # (sy, sz)

# coronal = plano en Y fijo
coronal = vol[:, my, :]     # (sx, sz)

# axial = plano en Z fijo
axial = vol[:, :, mz]       # (sx, sy)

# Rotar cada uno
# (rot90 es de numpy, (usarlo directo porque solo gira la matriz)
sagital_rot = np.rot90(sagital)   # ahora aprox (sz, sy)
coronal_rot = np.rot90(coronal)   # ahora aprox (sz, sx)
axial_rot = np.rot90(axial)       # ahora aprox (sy, sx)

# Obtener las dimensiones finales de cada imagen ya rotada
sag_h = sagital_rot.shape[0]
sag_w = sagital_rot.shape[1]

cor_h = coronal_rot.shape[0]
cor_w = coronal_rot.shape[1]

ax_h = axial_rot.shape[0]
ax_w = axial_rot.shape[1]

# "lienzo" (imagen grande) donde vamos a pegar:
# [sagital | coronal]
# [axial   | (vacío )]

#  calcular:
# - Alto total: fila de arriba (debe tener altura suficiente para sagital y coronal).
#               fila de abajo agrega axial debajo de sagital.
#   Entonces el alto total es el máximo entre:
#   (alto de la fila superior) + (alto de la fila inferior)
#   donde:
#      alto fila superior = max(sag_h, cor_h)
#      alto fila inferior = ax_h
alto_fila_superior = sag_h
if cor_h > alto_fila_superior:
    alto_fila_superior = cor_h

alto_fila_inferior = ax_h

alto_total = alto_fila_superior + alto_fila_inferior

# - Ancho total: necesitamos suficiente ancho para poner
#   sagital a la izquierda y coronal a la derecha.
#   El ancho de la columna izquierda será max(sag_w, ax_w)
#   El ancho de la columna derecha será (cor_w)
ancho_col_izq = sag_w
if ax_w > ancho_col_izq:
    ancho_col_izq = ax_w

ancho_col_der = cor_w

ancho_total = ancho_col_izq + ancho_col_der

# Crear la imagen final llena de ceros
final_img = np.zeros((alto_total, ancho_total))

# --- Pegar SAGITAL en la esquina superior izquierda ---
# Empieza en (fila 0, col 0)
final_img[0:sag_h, 0:sag_w] = sagital_rot

# --- Pegar CORONAL en la esquina superior derecha ---
# Empieza en (fila 0, col = ancho_col_izq)
inicio_col_coronal = ancho_col_izq
final_img[0:cor_h, inicio_col_coronal:inicio_col_coronal+cor_w] = coronal_rot

# --- Pegar AXIAL debajo de SAGITAL (esquina inferior izquierda) ---
# Empieza en (fila = alto_fila_superior, col = 0)
inicio_fila_axial = alto_fila_superior
final_img[inicio_fila_axial:inicio_fila_axial+ax_h, 0:ax_w] = axial_rot

# Mostrar todo
plt.imshow(final_img)
plt.title("Sagital (arriba izq) | Coronal (arriba der) | Axial (abajo izq)")
plt.axis('off')
plt.show()

# Información
print("sagital_rot:", sagital_rot.shape)
print("coronal_rot:", coronal_rot.shape)
print("axial_rot:", axial_rot.shape)
print("final_img:", final_img.shape)

