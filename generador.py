import json, pathlib
from datetime import date
import gconst, gweb, gjson


def main():
    # Carga json
    with open(gconst.FILE_JSON, encoding="utf-8") as file:
        FILE_JSON = json.load(file)
    legislacion = FILE_JSON["legislacion"]
    legislacion = gjson.ordena(FILE_JSON, "fecha")
    legislacion = legislacion["legislacion"]

    gweb.guarda_css()

    # Genera índice
    t = ""
    t += "\n"
    t += gweb.cabecera("Legislación de interés para profesores de informática")

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
