import json, pathlib
from datetime import date
import gconst, gweb, gjson


def main():
    gweb.guarda_colecciones("Comunidad Valenciana")

    # Carga json
    with open(gconst.JSON_FILE_REFERENCES, encoding="utf-8") as file:
        tmp = json.load(file)
    legislacion = gjson.ordena(tmp, "fecha")["legislacion"]

    gweb.guarda_css()

    # Genera índice
    t = ""
    t += "\n"
    t += gweb.cabecera("Legislación de interés para profesores de informática")

    t += '  <p><a href="lista.html">Versión en forma de lista</a></p>\n'
    t += "\n"
    t += f"  <p>Esta web contiene actualmente {len(legislacion)} referencias legislativas.</p>\n"
    t += "\n"

    grupo = gjson.selecciona(legislacion, "ámbito", "Unión Europea")
    grupo = gjson.selecciona(grupo, "vigencia", "vigente")
    t += gweb.seccion(grupo, "ue", "Legislación Unión Europea")

    grupo = gjson.selecciona(legislacion, "ámbito", "España")
    grupo = gjson.selecciona(grupo, "vigencia", "vigente")
    t += gweb.seccion(grupo, "es", "Legislación Española")

    grupo = gjson.selecciona(legislacion, "ámbito", "Comunidad Valenciana")
    grupo = gjson.selecciona(grupo, "vigencia", "vigente")
    t += gweb.seccion(grupo, "es-cv", "Legislación Comunidad Valenciana")

    grupo = gjson.selecciona(legislacion, "vigencia", "derogado")
    t += gweb.seccion(grupo, "derogada", "Legislación derogada")

    t += gweb.pie()
    with open(
        f"{gconst.DIR_SITE}/{gconst.FILE_INDEX}", "w", encoding="utf-8"
    ) as fichero:
        fichero.write(t)


if __name__ == "__main__":
    main()
