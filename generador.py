import json, pathlib
from datetime import date
import gconst, gweb, gjson


def main():
    # Carga json
    with open(gconst.FILE_JSON, encoding="utf-8") as file:
        FILE_JSON = json.load(file)
    legislacion = FILE_JSON["legislacion"]

    gweb.guarda_css()

    # Genera índice
    t = ""
    t += gweb.cabecera("Legislación de interés para profesores de informática")
    t += '  <section class="disposiciones">\n'

    for elemento in legislacion:
        t += f'    <article class="disposicion" id="{elemento["id"]}">\n'
        t += f'      <p class="descripcion">{elemento["descripción"]}</p>\n'
        t += f'      <p class="publicacion">\n'
        t += f'        {gweb.bandera(elemento["ámbito"], 25)}\n'
        t += f'        {elemento["publicación"][0]} {elemento["publicación"][1]}\n'
        if elemento["estado"] == gconst.DEROGADO:
            t += f'        <span class="derogado">derogado</span>\n'
        t += "      </p>\n"
        t += '      <p class="fichero">\n'
        for fichero in elemento["fichero"]:
            file = pathlib.Path(f"{gconst.DIR_SITE}/{gconst.DIR_FILES}/{fichero}")
            weight = str(round(file.stat().st_size / 1024 / 1024, 1)) + " MB)"
            formato = file.suffix[1:].upper()
            t += f'        <a href="{gconst.DIR_FILES}/{fichero}">{formato}</a> ({weight}\n'
        if elemento["web"] != [""]:
            for pagina in elemento["web"]:
                t += f'        - <a href="{pagina}">web</a>\n'
        t += "      </p>\n"
        t += f'      <p class="titulo">{elemento["titulo"]}</p>\n'
        t += "    </article>\n"
        t += "\n"
    t += "  </section>\n"
    t += gweb.pie()
    with open(f"{gconst.DIR_SITE}/{gconst.FILE_INDEX}", "w", encoding="utf-8") as fichero:
        fichero.write(t)


if __name__ == "__main__":
    main()
