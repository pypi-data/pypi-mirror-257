import numpy as np
import scipy as sc
import sympy as sp
import matplotlib.pyplot as plt

def grad2gradminsec(grados):
    grados_tmp = int(grados)
    minutos_flotante = (grados - grados_tmp) * 60
    minutos = int(minutos_flotante)
    segundos = (minutos_flotante - minutos) * 60
    return grados_tmp, minutos, segundos

def calc_grad_angle_np(u, v):
    norma_u = np.linalg.norm(u)
    norma_v = np.linalg.norm(v)
    coseno = (u @ v) / (norma_u * norma_v)
    alpha = np.rad2deg(np.arccos(coseno))
    return alpha

def calc_rad_angle_np(u, v):
    norma_u = np.linalg.norm(u)
    norma_v = np.linalg.norm(v)
    coseno = (u @ v) / (norma_u * norma_v)
    alpha = np.arccos(coseno)
    return alpha

def calc_base_ortonormal_np(A, v):
    bon = sc.linalg.null_space(A)
    u1 = bon[:, 0]
    u2 = bon[:, 1]
    P1 = (v @ u1) * u1
    P2 = (v @ u2) * u2
    P = P1 + P2
    return P

def calc_grad_angle_sp(u, v):
    norma_u = sp.sqrt(u.dot(u))
    norma_v = sp.sqrt(v.dot(v))
    coseno = u.dot(v) / (norma_u * norma_v)
    alpha = sp.acos(coseno)
    alpha_deg = sp.deg(alpha)
    return alpha_deg

def calc_rad_angle_sp(u, v):
    norma_u = sp.sqrt(u.dot(u))
    norma_v = sp.sqrt(v.dot(v))
    coseno = u.dot(v) / (norma_u * norma_v)
    alpha = sp.acos(coseno)
    return alpha

def calc_base_ortonormal_sp(A, v):
    bon = sp.nullspace(A)
    u1 = bon[0].normalized()
    u2 = bon[1].normalized()
    P1 = (v.dot(u1)) * u1
    P2 = (v.dot(u2)) * u2
    P = P1 + P2
    return P

def proyeccion_caballera(puntos):
    angulo = 19 * np.pi / 16
    a = 0.6 * np.cos(angulo)
    b = 0.6 * np.sin(angulo)
    matriz = np.array([[1, 0, a], [0, 1, b]])
    return matriz @ puntos[:3, :]

def caballera(c, color='k'):
    puntos, aristas = c
    num_aristas = aristas.shape[1]
    proy_caballera = proyeccion_caballera(puntos)
    for i in range(num_aristas):
        a, b = aristas.T[i]
        p1 = proy_caballera.T[a]
        p2 = proy_caballera.T[b]
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color)
    plt.axis("equal")
    plt.axis('off')

def TH(v):
    # V es un vector de 3 coordenadas de numpy
    TH = np.eye(4)
    TH[:3, 3] = v
    return TH

def traslacion(v, puntos):
    puntos_tras = TH(v) @ puntos[0]
    return puntos_tras

def EH(v):
    # v= np.array, las 3 primeras componentes son las s y la 4ª un 1
    return np.diagflat(v)

def escala(s, puntos):
    # S es la misma que EH()
    return EH(s) @ puntos

def rot2(angulo):
    matriz = np.array([
        [np.cos(angulo), -1 * np.sin(angulo)],
        [np.sin(angulo), np.cos(angulo)]
    ])
    return matriz

def rotacion(angulo, eje):
    matriz = np.eye(4)
    if eje == 0:
        matriz[1:3, 1:3] = rot2(angulo)
        return matriz
    elif eje == 1:
        matriz[0:3:2, 0:3:2] = rot2(-1 * angulo)
        return matriz
    elif eje == 2:
        matriz[0:2, 0:2] = rot2(angulo)
        return matriz
    else:
        raise ValueError
