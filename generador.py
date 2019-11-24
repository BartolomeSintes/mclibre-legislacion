import json, pathlib
from datetime import date


JSON_FILE = "legislacion.json"
DIR_SITE = "docs"
DIR_FILES = "files"
INDEX_FILE = "index.html"
MES = [
    "",
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]


def fecha_a_texto(numero):
    return (
        str(int(numero[8:10]))
        + " de "
        + MES[int(numero[5:7])]
        + " de "
        + str(numero[0:4])
    )


def main():
    # Carga json
    with open(JSON_FILE, encoding="utf-8") as file:
        json_file = json.load(file)
    legislacion = json_file["legislacion"]

    # Genera índice
    t = ""
    t += "<!DOCTYPE html>\n"
    t += '<html lang="es">\n'
    t += "<head>\n"
    t += '  <meta charset="utf-8">\n'
    t += f"  <title>Legislación relacionada con la informática</title>\n"
    t += '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    t += "  <style>\n"
    t += "    html { font-family: sans-serif; font-size: 120%; }\n"
    t += "    li { margin-bottom: 20px; }\n"
    t += "    footer { border-top: black 1px solid; padding-top: 5px;}\n"
    t += "  </style>\n"
    t += "</head>\n"
    t += "\n"
    t += "<body>\n"
    t += f"  <h1>Legislación relacionada con la informática</h1>\n"

    t += "  <ul>\n"

    for elemento in legislacion:
        t += "    <li>\n"
        t += f'      <strong>{elemento["descripción"]}</strong><br>\n'
        t += f'      {elemento["titulo"]}<br>\n'
        t += f'      Publicado en {elemento["publicación"][0]} en {elemento["publicación"][1]}<br>\n'
        for fichero in elemento["fichero"]:
            file = pathlib.Path(f"{DIR_SITE}/{DIR_FILES}/{fichero}")
            weight = str(round(file.stat().st_size / 1024 / 1024, 1)) + " MB)"
            formato = file.suffix[1:].upper()
            t += f'      <a href="{DIR_FILES}/{fichero}">{formato}</a> ({weight}\n'
        t += "    </li>\n"
    t += "  </ul>\n"
    t += "\n"
    t += "  <footer>\n"
    t += f"    Última modificación de esta página: {fecha_a_texto(str(date.today()))}\n"
    t += "  </footer>\n"
    t += "</body>\n"
    t += "</html>\n"
    with open(f"{DIR_SITE}/{INDEX_FILE}", "w", encoding="utf-8") as fichero:
        fichero.write(t)


if __name__ == "__main__":
    main()
