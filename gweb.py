import json, pathlib
from datetime import date
import gconst, gjson


def fecha_a_texto(numero):
    return (
        str(int(numero[8:10]))
        + " de "
        + gconst.MES[int(numero[5:7])]
        + " de "
        + str(numero[0:4])
    )


def bandera(entidad, ancho):
    return f'<img src="{gconst.DIR_IMAGES}/bandera-{gconst.CODIGOS_ISO_3166[entidad]}.svg" alt="{entidad}" title="{entidad}" width="{ancho}">'


def cabecera(titulo):
    tmp = "<!DOCTYPE html>\n"
    tmp += '<html lang="es">\n'
    tmp += "<head>\n"
    tmp += '  <meta charset="utf-8">\n'
    tmp += f"  <title>{titulo}</title>\n"
    tmp += '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    tmp += f'  <link rel="stylesheet" href="{gconst.FILE_CSS}">\n'
    tmp += "</head>\n"
    tmp += "\n"
    tmp += "<body>\n"
    tmp += f"  <h1>{titulo}</h1>\n"
    tmp += "\n"
    tmp += f'  <p><img src="{gconst.DIR_IMAGES}/icono-warning.svg" alt="¡Atención!" width="50">Esta página web está en elaboración y se ofrece temporalmente en esta ubicación. Por favor, no enlace a esta web porque su ubicación definitiva puede ser otra.</p>\n'
    tmp += "\n"
    return tmp


def seccion(legislacion, id, titulo):
    tmp = f'  <section id="{id}">\n'
    tmp += f"    <h2>{titulo}</h2>\n"
    tmp += "\n"
    tmp += f'    <div class="disposiciones">\n'
    for elemento in legislacion:
        tmp += f'      <article class="disposicion" id="{elemento["id"]}">\n'
        tmp += f'        <h3>{elemento["descripción"]}</h3>\n'
        tmp += f'        <p class="publicacion">\n'
        tmp += f'          {bandera(elemento["ámbito"], 25)}\n'
        tmp += f'          {elemento["origen"]} {elemento["fecha"]}\n'
        if elemento["vigencia"] == gconst.DEROGADO:
            tmp += f'          <span class="derogado">derogado</span>\n'
        tmp += "        </p>\n"
        for version in elemento["versiones"]:
            tmp += '        <p class="fichero">\n'
            if len(elemento["versiones"]) != 1:
                tmp += f'        {version["versión"].capitalize()}: '
            for i in range(len(version["enlaces"])):
                if version["enlaces"][i]["formato"] != "web":
                    file = pathlib.Path(
                        f'{gconst.DIR_SITE}/{gconst.DIR_FILES}/{version["enlaces"][i]["url"]}'
                    )
                    weight = str(round(file.stat().st_size / 1024 / 1024, 1)) + " MB"
                    formato = file.suffix[1:].upper()
                    if version["enlaces"][i]["idioma"] == "es":
                        tmp += f'          <a href="{gconst.DIR_FILES}/{version["enlaces"][i]["url"]}" title="{weight}">{formato}</a>'
                    else:
                        tmp += f'          <a href="{gconst.DIR_FILES}/{version["enlaces"][i]["url"]}" title="{weight}">{formato}({version["enlaces"][i]["idioma"].upper()})</a>'
                else:
                    if version["enlaces"][i]["idioma"] == "es":
                        tmp += f'          <a href="{version["enlaces"][i]["url"]}">web</a>'
                    else:
                        tmp += f'          <a href="{version["enlaces"][i]["url"]}">web({version["enlaces"][i]["idioma"].upper()})</a>'
                if i < len(version["enlaces"]) - 1:
                    tmp += " -\n"
                else:
                    tmp += "\n"
            tmp += "        </p>\n"
        tmp += f'        <p class="titulo">{elemento["titulo"]}</p>\n'
        tmp += "      </article>\n"
        tmp += "\n"
    tmp += f"    </div>\n"
    tmp += "  </section>\n"
    tmp += "\n"
    return tmp


def pie():
    tmp = "\n"
    tmp += "  <footer>\n"
    tmp += (
        f"    Última modificación de esta página: {fecha_a_texto(str(date.today()))}\n"
    )
    tmp += "  </footer>\n"
    tmp += "</body>\n"
    tmp += "</html>\n"
    return tmp


def guarda_css():
    t = ""
    t += "html {\n"
    t += "  font-family: sans-serif;\n"
    t += "  font-size: 100%;\n"
    t += "}\n"
    t += "\n"
    t += "footer {\n"
    t += "  border-top: black 1px solid;\n"
    t += "  padding-top: 5px;\n"
    t += "}\n"
    t += "\n"
    t += ".derogado {\n"
    t += "  color: red;\n"
    t += "  text-transform: uppercase;\n"
    t += "}\n"
    t += "\n"
    t += "div.disposiciones {\n"
    t += "  display: flex;\n"
    t += "  flex-flow: row wrap;\n"
    t += "  justify-content: flex-start;\n"
    t += "}\n"
    t += "\n"
    t += "article.disposicion {\n"
    t += "  display: flex;\n"
    t += "  flex-direction: column;\n"
    t += "  flex: 0 1 300px;\n"
    t += "  margin: 5px;\n"
    t += "  border: black 1px solid;\n"
    t += "  text-align: center;\n"
    t += "}\n"
    t += "\n"
    t += "article.disposicion h3 {\n"
    t += "  margin: 0;\n"
    t += "  padding: 5px 10px;\n"
    t += "  background-color: #eee;\n"
    t += "  font-size: 100%;\n"
    t += "}\n"
    t += "\n"
    t += "article.disposicion p {\n"
    t += "  margin: 0;\n"
    t += "  padding: 5px 10px;\n"
    t += "}\n"
    t += "\n"
    t += "article.disposicion .fichero {\n"
    t += "  background-color: #eee;\n"
    t += "  font-size: 90%;\n"
    t += "}\n"
    t += "\n"
    t += "article.disposicion .titulo {\n"
    t += "  hyphens: auto;\n"
    t += "  text-align: justify;\n"
    t += "  font-size: 80%;\n"
    t += "}\n"
    t += "\n"
    t += "li.disposicion {\n"
    t += "  line-height: 130%;\n"
    t += "  margin-top: 10px;\n"
    t += "}\n"

    with open(f"{gconst.DIR_SITE}/{gconst.FILE_CSS}", "w", encoding="utf-8") as fichero:
        fichero.write(t)


def muestra_referencia(elemento):
    tmp = ""
    tmp += f'      <li class="disposicion" id="{elemento["id"]}">\n'
    tmp += (
        f'        <strong class="descripcion">{elemento["descripción"]}</strong><br>\n'
    )
    tmp += f'        <span class="titulo">{elemento["titulo"]}</span><br>\n'
    if elemento["vigencia"] == gconst.DEROGADO:
        tmp += f'        <span class="derogado">derogado</span><br>'
    tmp += f'        <span class="publicacion">\n'
    for version in elemento["versiones"]:
        tmp += '        <span class="fichero">\n'
        if len(elemento["versiones"]) == 1:
            tmp += f'          {elemento["origen"]} {elemento["fecha"]}</span>: '
        elif version["versión"] == "original" or version["versión"] == "anexo" :
            tmp += f'        {version["versión"].capitalize()}: {elemento["origen"]} {elemento["fecha"]}: '
        else:
            print(version)
            tmp += f'        {version["versión"].capitalize()} ({version["fecha"]}): '
        for i in range(len(version["enlaces"])):
            if version["enlaces"][i]["formato"] != "web":
                file = pathlib.Path(
                    f'{gconst.DIR_SITE}/{gconst.DIR_FILES}/{version["enlaces"][i]["url"]}'
                )
                weight = str(round(file.stat().st_size / 1024 / 1024, 1)) + " MB"
                formato = file.suffix[1:].upper()
                if version["enlaces"][i]["idioma"] == "es":
                    tmp += f'          <a href="{gconst.DIR_FILES}/{version["enlaces"][i]["url"]}" title="{weight}">{formato}</a>'
                else:
                    tmp += f'          <a href="{gconst.DIR_FILES}/{version["enlaces"][i]["url"]}" title="{weight}">{formato}({version["enlaces"][i]["idioma"].upper()})</a>'
            else:
                if version["enlaces"][i]["idioma"] == "es":
                    tmp += f'          <a href="{version["enlaces"][i]["url"]}">web</a>'
                else:
                    tmp += f'          <a href="{version["enlaces"][i]["url"]}">web({version["enlaces"][i]["idioma"].upper()})</a>'
            if i < len(version["enlaces"]) - 1:
                tmp += " -\n"
            else:
                tmp += "\n"
        tmp += "        </span><br>\n"
    tmp += "      </li>\n"
    tmp += "\n"
    return tmp


def guarda_colecciones(nombre):
    # Carga json legislación
    with open(gconst.JSON_FILE_REFERENCES, encoding="utf-8") as file:
        tmp = json.load(file)
    legislacion = gjson.ordena(tmp, "fecha")["legislacion"]

    ids = [d["id"] for d in legislacion]
    print(f"Hay {len(ids)} referencias")

    # Carga json colecciones
    with open(gconst.JSON_FILE_COLLECTIONS, encoding="utf-8") as file:
        tmp_file = json.load(file)
    coleccion = gjson.selecciona_en_json(tmp_file["colecciones"], "nombre", nombre)

    for pagina in coleccion["paginas"]:
        t = ""
        t += cabecera(pagina["titulo"])
        t += '  <p><a href="index.html">Versión en forma de fichas</a></p>\n'
        t += "\n"
        t += f"  <p>Esta web contiene actualmente {len(legislacion)} referencias legislativas.</p>\n"
        t += "\n"
        for apartado in pagina["contenido"]:
            t += f'  <h2>{apartado["apartado"]["titulo"]}</h2>\n'
            t += "\n"
            t += "  <ul>\n"
            for id in apartado["apartado"]["referencias"]:
                t += muestra_referencia(gjson.selecciona_en_json(legislacion, "id", id))
                ids.remove(id)
            t += "  </ul>\n"
            t += "\n"

        t += f"  <h2>Otros</h2>\n"
        t += "\n"
        t += "  <ul>"
        for id in ids:
            t += muestra_referencia(gjson.selecciona_en_json(legislacion, "id", id))
        t += "  </ul>"
        t += "\n"
        print(f"Quedan por ordenar {len(ids)} referencias")
        t += pie()

        with open(
            f'{gconst.DIR_SITE}/{pagina["nombre"]}', "w", encoding="utf-8"
        ) as fichero:
            fichero.write(t)

    return coleccion
