import json


def ordena(json, criterio):
    final = dict(json)
    final["legislacion"] = sorted(
        final["legislacion"], key=lambda x: x[criterio][1], reverse=False
    )
    return final


def selecciona(lista, campo, valor):
    lista2 = lista[:]
    for elemento in lista2[:]:
        if elemento[campo] != valor:
            lista2.remove(elemento)
    return lista2
