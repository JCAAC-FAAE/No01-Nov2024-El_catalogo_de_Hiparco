# Licensed under the EUPL
# Módulo formats.py

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ptk
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


# Impresión planisferio celeste en proyección AzimuthalEquidistant
# Esta rutina realiza la impresión de un planisferio celeste en proyección
# Azimutal Equidistante. Una "s" en la primera variable significa que se lee un fichero,
# "Constelaciones y estrellas ptolemaicas.prn", con los datos de las estrellas del
# Almagesto de Ptolomeo, en longitudes y latitudes eclípticas. Una "s" en la segunda
# variable significa que se plotean los puntos que representan a las estrellas. Una "s" en
# la tercera variable indica que se imprimen las etiquetas. Los datos del fichero son
# 1) si la constelación es boreal, zodiacal boreal, zodiacal austral, o austral.
# 2) dos caracteres que indican el código de la constelación, añadiendo una "C" en algunos
# casos, que significa que está "informada cerca".
# 3) número de secuencia de la estrella dentro de la constelación.
# 4) nombre en latín de la estrella, según la posición que ocupa en la figura.
# 5) longitud eclíptica de la estrella.
# 6) Latitud eclíptica de la estrella.
# 7) Tamaño del punto, característico de su magnitud visual.
# 8) Coordenadas relativas de la etiqueta, "L", left, "R", right, "T", top, "B", bottom,
# primera en relación a la longitud eclíptica, y segunda, en relación a la latitud
# eclíptica.
# Se sigue el mismo criterio con las Ruedas de Estrellas de los libros del saber de
# de Alfonso X de Castilla, con los datos que se encuentran en el fichero
# "Constelaciones alfonsíes ptolomeo - python.prn".
# Se sigue un criterio semejante con el fichero "Constelaciones y estrellas actuales.prn",
# donde están las coordenadas longitudes y latitudes eclípticas J2000.
# Si se procesan dos o tres de los ficheros anteriores, se puede realizar la comparación
# de las coordenadas eclípticas de las dos o tres eras, girando hacia el pasado los grados
# de precesión correspondientes, por medio de una resta de los grados de precesión real
# aplicados a cada una de las longitudes eclípticas.
def impresion_reticula_AzimuthalEquidistant(
    ptolomeo,
    plotear_puntos_ptolomeo,
    anotar_puntos_ptolomeo,
    alfonso,
    plotear_puntos_alfonso,
    anotar_puntos_alfonso,
    j2000,
    plotear_puntos_j2000,
    anotar_puntos_j2000,
):

    if plotear_puntos_ptolomeo == "s" or plotear_puntos_alfonso == "s" or plotear_puntos_j2000 == "s":
        plt.figure(figsize=[40, 40], facecolor="white")
    else:
        plt.figure(figsize=[40, 40], facecolor="none")

    projection, transform = ccrs.AzimuthalEquidistant(central_latitude=90), ccrs.PlateCarree()
    ax = plt.axes(projection=projection)

    ax.set_global()

    # We want the map to go down to -80 degrees latitude.
    ax.set_extent([-180, 180, -80, 90], ccrs.PlateCarree())

    cardinal_labels = {"east": "", "west": "-", "north": "", "south": "-"}
    longitude_formatter = LongitudeFormatter(cardinal_labels=cardinal_labels)
    latitude_formatter = LatitudeFormatter(cardinal_labels=cardinal_labels)

    if plotear_puntos_ptolomeo == "s" or plotear_puntos_alfonso == "s" or plotear_puntos_j2000 == "s":
        ax.set_facecolor("black")
        gl = ax.gridlines(
            crs=ccrs.PlateCarree(central_longitude=0),
            draw_labels=True,
            xformatter=longitude_formatter,
            yformatter=latitude_formatter,
            linewidth=0.5,
            color="white",
            alpha=1,
            linestyle="-",
            xlabel_style={"color": "black", "size": 10, "weight": "regular"},
            ylabel_style={"color": "white", "size": 10, "weight": "regular"},
        )
        # Meridians every 10 degrees, and 10 parallels.
        gl.xlocator = ptk.FixedLocator(np.arange(-180, 180, 10))
        parallels = np.linspace(-80, 90, 18, endpoint=True)
        gl.ylocator = ptk.FixedLocator(parallels)
        ax.set_title("Longitud/Latitud eclíptica", fontsize=14, fontweight="bold")
    else:
        plt.figure(figsize=[40, 40], facecolor="black")
        plt.figure().savefig("temp.png", facecolor=plt.figure().get_facecolor(), edgecolor="black")
        ax.set_facecolor("black")
        ax.set_title(" ", fontsize=14, fontweight="bold")

    if ptolomeo == "s":

        archivo = open("Constelaciones y estrellas ptolemaicas.prn", "r")

        j = 0

        while j == 0:
            linea = archivo.readline()
            if len(linea) <= 1:
                j = 1
                archivo.close()
            else:
                lon = float(linea[100:105].replace(",", "."))
                lat = float(linea[106:111].replace(",", "."))
                tam = float(linea[112:115].replace(",", "."))
                if plotear_puntos_ptolomeo == "s":
                    ax.scatter(
                        lon, lat, color="white", s=np.pi * tam**2, alpha=1, transform=transform
                    )  # dibujar punto en (lon, lat) dados
                if anotar_puntos_ptolomeo == "s":
                    if linea[136:137].strip() == "L":
                        lon_etiq = lon + float(linea[128:131].replace(",", "."))
                        ha_etiq = "left"
                    elif linea[136:137].strip() == "C":
                        lon_etiq = lon + float(linea[128:131].replace(",", "."))
                        ha_etiq = "center"
                    elif linea[136:137].strip() == "R":
                        lon_etiq = lon - float(linea[128:131].replace(",", "."))
                        ha_etiq = "right"
                    if linea[138:139].strip() == "T":
                        lat_etiq = lat + float(linea[132:135].replace(",", "."))
                        va_etiq = "top"
                    elif linea[138:139].strip() == "C":
                        lat_etiq = lat + float(linea[132:135].replace(",", "."))
                        va_etiq = "center"
                    elif linea[138:139].strip() == "B":
                        lat_etiq = lat - float(linea[132:135].replace(",", "."))
                        va_etiq = "bottom"
                    if linea[4:6].strip() + " " + linea[8:10].strip() == "PR 25":
                        print(linea[8:10].strip() + " " + linea[4:7].strip(), lon, lon_etiq, lat, lat_etiq)
                    ax.annotate(
                        linea[8:10].strip() + " " + linea[4:7].strip(),
                        (lon_etiq, lat_etiq),
                        color="brown",
                        weight="bold",
                        ha=ha_etiq,
                        va=va_etiq,
                        size=7,
                        transform=transform,
                    )

    if alfonso == "s":

        archivo = open("Constelaciones alfonsíes ptolomeo - python.prn", "r")

        j = 0

        while j == 0:
            linea = archivo.readline()
            if len(linea) <= 1:
                archivo.close()
                j = 1
            else:
                lon = float(linea[123:129].replace(",", "."))
                lat = float(linea[133:139].replace(",", "."))
                tam = float(linea[143:146].replace(",", "."))
                if plotear_puntos_alfonso == "s":
                    ax.scatter(
                        lon, lat, color="grey", s=np.pi * tam**2, alpha=1, transform=transform
                    )  # dibujar punto en (lon, lat) dados
                if anotar_puntos_alfonso == "s":
                    ax.annotate(
                        linea[10:12].strip() + " " + linea[6:9].strip(),
                        (lon - 1.0, lat - 1.0),
                        color="violet",
                        weight="bold",
                        ha="right",
                        va="bottom",
                        size=7,
                        transform=transform,
                    )

    if j2000 == "s":

        archivo = open("Constelaciones y estrellas actuales.prn", "r")

        j = 0

        while j == 0:
            linea = archivo.readline()
            if len(linea) <= 1:
                j = 1
                archivo.close()
            else:
                lon = float(linea[28:34].replace(",", "."))
                lat = float(linea[40:46].replace(",", "."))
                tam = float(linea[52:55].replace(",", "."))
                if plotear_puntos_j2000 == "s":
                    ax.scatter(
                        lon, lat, color="dodgerblue", s=np.pi * tam**2, alpha=1, transform=transform
                    )  # dibujar punto en (lon, lat) dados
                if anotar_puntos_j2000 == "s":
                    if linea[83:84].strip() == "L":
                        lon_etiq = lon + float(linea[73:76].replace(",", "."))
                        ha_etiq = "left"
                    elif linea[83:84].strip() == "C":
                        lon_etiq = lon + float(linea[73:76].replace(",", "."))
                        ha_etiq = "center"
                    elif linea[83:84].strip() == "R":
                        lon_etiq = lon - float(linea[73:76].replace(",", "."))
                        ha_etiq = "right"
                    if linea[86:87].strip() == "T":
                        lat_etiq = lat + float(linea[78:81].replace(",", "."))
                        va_etiq = "top"
                    elif linea[86:87].strip() == "C":
                        lat_etiq = lat + float(linea[78:81].replace(",", "."))
                        va_etiq = "center"
                    elif linea[86:87].strip() == "B":
                        lat_etiq = lat - float(linea[78:81].replace(",", "."))
                        va_etiq = "bottom"
                    ax.annotate(
                        linea[3:5].strip() + " " + linea[0:2].strip(),
                        (lon_etiq, lat_etiq),
                        color="green",
                        weight="bold",
                        ha=ha_etiq,
                        va=va_etiq,
                        size=7,
                        transform=transform,
                    )

    ax.invert_xaxis()

    plt.show()

    return ()


# Impresión planisferio celeste en proyección PlateCarrée/Constelación
# La primera variable es el código corto, de dos caracteres, que identifica la constelación
# que se va a procesar. Se obtiene la proyección PlateCarrée de los catálogos de estrellas
# que se quiera comparar: Almagesto, Teón, Alfonso y J2000. Las coordenadas eclípticas,
# longitudes y latitudes, están en cada uno los ficheros planos de proceso.
def impresion_reticula_PlateCarree_Constelacion(
    Constelacion, diferencia_ptolomeo_alfonso, anotar_puntos, ptolomeo, teon, alfonso, j2000
):

    if Constelacion == "HY" or Constelacion == "AG":
        plt.figure(figsize=[20, 50], facecolor="white")
    else:
        if Constelacion == "DR":
            plt.figure(figsize=[30, 60], facecolor="white")
        else:
            plt.figure(figsize=[10, 20], facecolor="white")

    if (
        Constelacion == "MA"
        or Constelacion == "MI"
        or Constelacion == "DR"
        or Constelacion == "CF"
        or Constelacion == "CS"
        or Constelacion == "PR"
        or Constelacion == "AU"
        or Constelacion == "EQ"
        or Constelacion == "AD"
        or Constelacion == "TR"
        or Constelacion == "AR"
        or Constelacion == "TA"
        or Constelacion == "GE"
        or Constelacion == "CR"
        or Constelacion == "LE"
        or Constelacion == "PI"
        or Constelacion == "CT"
        or Constelacion == "OR"
        or Constelacion == "AM"
        or Constelacion == "LP"
        or Constelacion == "CN"
        or Constelacion == "PC"
        or Constelacion == "AG"
    ):
        projection, transform = ccrs.PlateCarree(), ccrs.PlateCarree()
    else:
        if (
            Constelacion == "BO"
            or Constelacion == "CB"
            or Constelacion == "HE"
            or Constelacion == "LY"
            or Constelacion == "CY"
            or Constelacion == "OP"
            or Constelacion == "SO"
            or Constelacion == "ST"
            or Constelacion == "AL"
            or Constelacion == "DE"
            or Constelacion == "PQ"
            or Constelacion == "VI"
            or Constelacion == "LI"
            or Constelacion == "SC"
            or Constelacion == "SG"
            or Constelacion == "CP"
            or Constelacion == "AQ"
            or Constelacion == "HY"
            or Constelacion == "PT"
            or Constelacion == "CO"
            or Constelacion == "CE"
            or Constelacion == "FE"
            or Constelacion == "TU"
            or Constelacion == "CA"
            or Constelacion == "PA"
        ):
            projection, transform = ccrs.PlateCarree(central_longitude=180), ccrs.PlateCarree()

    ax = plt.axes(projection=projection)
    ax.set_facecolor("black")
    ax.text(
        -0.07,
        0.55,
        "Latitud eclíptica",
        va="bottom",
        ha="center",
        rotation="vertical",
        rotation_mode="anchor",
        transform=ax.transAxes,
    )
    ax.text(
        0.5,
        -0.2,
        "Longitud eclíptica",
        va="bottom",
        ha="center",
        rotation="horizontal",
        rotation_mode="anchor",
        transform=ax.transAxes,
    )  # We want the map to go down to 10 degrees latitude.

    add_180 = 0
    add_360 = 0

    if Constelacion == "MA":  # osa mayor
        ax.set_title("MAIORIS VRSAE", fontsize=14, fontweight="bold")
        if alfonso == "s" and j2000 == "s":
            long_min = 70
            long_max = 170
        else:
            if diferencia_ptolomeo_alfonso == "s":
                long_min = 70
                long_max = 170
            else:
                long_min = 80
                long_max = 160
        lat_min = 10
        lat_max = 60
    elif Constelacion == "MI":  # osa menor
        ax.set_title("MINORIS VRSAE", fontsize=14, fontweight="bold")
        if alfonso == "s" and j2000 == "s":
            long_min = 70
            long_max = 140
        else:
            long_min = 50
            if diferencia_ptolomeo_alfonso == "s":
                long_max = 140
            else:
                long_max = 120
        lat_min = 60
        lat_max = 90
    elif Constelacion == "DR":  # dragón
        ax.set_title("DRACONIS", fontsize=14, fontweight="bold")
        long_min = -180
        long_max = 180
        lat_min = 50
        lat_max = 90
        add_360 = 360
    elif Constelacion == "CF":  # cefeo
        ax.set_title("CEPHEUS", fontsize=14, fontweight="bold")
        long_min = -30
        long_max = 90
        lat_min = 50
        lat_max = 80
        add_360 = 360
    elif Constelacion == "BO":  # bootes
        ax.set_title("BOOTES", fontsize=14, fontweight="bold")
        long_min = 150
        if alfonso == "s" and j2000 == "s":
            long_max = 220
        else:
            if diferencia_ptolomeo_alfonso == "s":
                long_max = 220
            else:
                long_max = 200
        lat_min = 20
        lat_max = 70
        add_180 = 180
    elif Constelacion == "CB":  # corona borealis
        ax.set_title("CORONA BOREALIS", fontsize=14, fontweight="bold")
        long_min = 190
        if alfonso == "s" and j2000 == "s":
            long_max = 230
        else:
            if diferencia_ptolomeo_alfonso == "s":
                long_max = 220
            else:
                long_max = 210
        lat_min = 40
        lat_max = 60
        add_180 = 180
    elif Constelacion == "HE":  # hércules
        ax.set_title("HERCULES", fontsize=14, fontweight="bold")
        long_min = 180
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 260
        else:
            long_max = 250
        lat_min = 30
        lat_max = 80
        add_180 = 180
    elif Constelacion == "LY":  # lira
        ax.set_title("LYRA", fontsize=14, fontweight="bold")
        if alfonso == "s" and j2000 == "s":
            long_min = 270
            long_max = 290
        else:
            long_min = 250
            if diferencia_ptolomeo_alfonso == "s":
                long_max = 290
            else:
                long_max = 280
        lat_min = 50
        lat_max = 70
        add_180 = 180
    elif Constelacion == "CY":  # cisne o auis callina
        ax.set_title("CYGNUS", fontsize=14, fontweight="bold")
        if alfonso == "s" and j2000 == "s":
            long_min = 280
            long_max = 340
        else:
            long_min = 270
            if diferencia_ptolomeo_alfonso == "s":
                long_max = 340
            else:
                long_max = 320
        lat_min = 30
        lat_max = 80
        add_180 = 180
    elif Constelacion == "CS":  # cassiopeia
        ax.set_title("CASSIOPEIA", fontsize=14, fontweight="bold")
        if alfonso == "s" and j2000 == "s":
            long_min = 10
            long_max = 50
        else:
            long_min = 0
            if diferencia_ptolomeo_alfonso == "s":
                long_max = 50
            else:
                long_max = 30
        lat_min = 40
        lat_max = 60
    elif Constelacion == "PR":  # perseus
        ax.set_title("PERSEUS", fontsize=14, fontweight="bold")
        long_min = 20
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 70
        else:
            long_max = 50
        lat_min = 10
        lat_max = 50
    elif Constelacion == "AU":  # auriga
        ax.set_title("AURIGA", fontsize=14, fontweight="bold")
        long_min = 40
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 90
        else:
            long_max = 70
        lat_min = 0
        lat_max = 40
    elif Constelacion == "OP":  # ophiucus
        ax.set_title("OPHIUCUS", fontsize=14, fontweight="bold")
        if alfonso == "s" and j2000 == "s":
            long_min = 190
            long_max = 270
            lat_max = 50
        else:
            long_min = 210
            if diferencia_ptolomeo_alfonso == "s":
                long_max = 280
                lat_max = 50
            else:
                long_max = 250
                lat_max = 40
        lat_min = -10
        add_180 = 180
    elif Constelacion == "SO":  # serpentis ophiuchi
        ax.set_title("SERPENTIS OPHIUCHI", fontsize=14, fontweight="bold")
        long_min = 190
        long_max = 260
        lat_min = 0
        lat_max = 50
        add_180 = 180
    elif Constelacion == "ST":  # sagitta
        ax.set_title("SAGITTA", fontsize=14, fontweight="bold")
        long_min = 270
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 300
        else:
            long_max = 290
        lat_min = 30
        lat_max = 50
        add_180 = 180
    elif Constelacion == "AL":  # aquila
        ax.set_title("AQUILA", fontsize=14, fontweight="bold")
        long_min = 260
        long_max = 310
        lat_min = 10
        lat_max = 40
        add_180 = 180
    elif Constelacion == "DE":  # delphinis
        ax.set_title("DELPHINIS", fontsize=14, fontweight="bold")
        long_min = 270
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 320
        else:
            long_max = 300
        lat_min = 10
        lat_max = 40
        add_180 = 180
    elif Constelacion == "PQ":  # praecisionis equi
        ax.set_title("PRAECISIONIS EQUI", fontsize=14, fontweight="bold")
        long_min = 290
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 320
        else:
            long_max = 300
        lat_min = 20
        lat_max = 30
        add_180 = 180
    elif Constelacion == "EQ":  # equi
        ax.set_title("EQUI", fontsize=14, fontweight="bold")
        long_min = -60
        long_max = -10
        lat_min = 10
        lat_max = 50
    elif Constelacion == "AD":  # andrómeda
        ax.set_title("ANDROMEDA", fontsize=14, fontweight="bold")
        long_min = -20
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 40
        else:
            long_max = 20
        lat_min = 10
        lat_max = 50
    elif Constelacion == "TR":  # trianguli
        ax.set_title("TRIANGULI", fontsize=14, fontweight="bold")
        long_min = 10
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 40
        else:
            long_max = 20
        lat_min = 10
        lat_max = 30
    elif Constelacion == "AR":  # aries
        ax.set_title("ARIES", fontsize=14, fontweight="bold")
        if alfonso == "s" and j2000 == "s":
            long_min = 20
            long_max = 50
        else:
            long_min = 0
            if diferencia_ptolomeo_alfonso == "s":
                long_max = 50
            else:
                long_max = 30
        lat_min = -10
        lat_max = 20
    elif Constelacion == "TA":  # tauro
        ax.set_title("TAURUS", fontsize=14, fontweight="bold")
        if alfonso == "s" and j2000 == "s":
            long_min = 30
            long_max = 90
        else:
            long_min = 20
            if diferencia_ptolomeo_alfonso == "s":
                long_max = 90
            else:
                long_max = 70
        lat_min = -20
        lat_max = 10
    elif Constelacion == "GE":  # gemini
        ax.set_title("GEMINI", fontsize=14, fontweight="bold")
        if alfonso == "s" and j2000 == "s":
            long_min = 70
            long_max = 120
        else:
            long_min = 60
            if diferencia_ptolomeo_alfonso == "s":
                long_max = 120
            else:
                long_max = 100
        lat_min = -20
        lat_max = 20
    elif Constelacion == "CR":  # cancer
        ax.set_title("CANCER", fontsize=14, fontweight="bold")
        long_min = 80
        if alfonso == "s" and j2000 == "s":
            long_max = 130
        else:
            if diferencia_ptolomeo_alfonso == "s":
                long_max = 130
            else:
                long_max = 120
        lat_min = -20
        lat_max = 20
    elif Constelacion == "LE":  # leo
        ax.set_title("LEO", fontsize=14, fontweight="bold")
        if alfonso == "s" and j2000 == "s":
            long_min = 120
            long_max = 170
            lat_min = -35
        else:
            if diferencia_ptolomeo_alfonso == "s":
                long_min = 100
                long_max = 170
                lat_min = -35
            else:
                long_min = 100
                long_max = 150
                lat_min = -10
        lat_max = 40
    elif Constelacion == "VI":  # virgo
        ax.set_title("VIRGO", fontsize=14, fontweight="bold")
        if alfonso == "s" and j2000 == "s":
            long_min = 150
            long_max = 220
        else:
            long_min = 140
            if diferencia_ptolomeo_alfonso == "s":
                long_max = 220
            else:
                long_max = 200
        lat_min = -10
        lat_max = 30
        add_180 = 180
    elif Constelacion == "LI":  # libra
        if teon == "s":
            ax.set_title("LIBRA/ESCORPION", fontsize=14, fontweight="bold")
            long_min = 190
            long_max = 250
            lat_min = -30
        else:
            ax.set_title("LIBRA", fontsize=14, fontweight="bold")
            if alfonso == "s" and j2000 == "s":
                long_min = 210
                long_max = 240
                lat_min = -20
            else:
                long_min = 190
                if diferencia_ptolomeo_alfonso == "s":
                    long_max = 240
                else:
                    long_max = 220
                lat_min = -20
        lat_max = 20
        add_180 = 180
    elif Constelacion == "SC":  # escorpión
        ax.set_title("SCORPIUS", fontsize=14, fontweight="bold")
        if alfonso == "s" and j2000 == "s":
            long_min = 220
            long_max = 270
        else:
            long_min = 200
            if diferencia_ptolomeo_alfonso == "s":
                long_max = 270
            else:
                long_max = 250
        lat_min = -30
        lat_max = 20
        add_180 = 180
    elif Constelacion == "SG":  # sagitario
        ax.set_title("SAGITTARIUS", fontsize=14, fontweight="bold")
        if teon == "s":
            long_min = 230
            long_max = 280
        else:
            if alfonso == "s" and j2000 == "s":
                long_min = 250
                long_max = 300
            else:
                long_min = 240
                if diferencia_ptolomeo_alfonso == "s":
                    long_max = 300
                else:
                    long_max = 280
        lat_min = -30
        lat_max = 10
        add_180 = 180
    elif Constelacion == "CP":  # capricornio
        ax.set_title("CAPRICORNUS", fontsize=14, fontweight="bold")
        if teon == "s":
            long_min = 260
            long_max = 300
        else:
            if alfonso == "s" and j2000 == "s":
                long_min = 290
                long_max = 320
            else:
                long_min = 270
                if diferencia_ptolomeo_alfonso == "s":
                    long_max = 320
                else:
                    long_max = 300
        lat_min = -10
        lat_max = 10
        add_180 = 180
    elif Constelacion == "AQ":  # aquario
        ax.set_title("AQUARIUS", fontsize=14, fontweight="bold")
        if alfonso == "s" and j2000 == "s":
            long_min = 290
            long_max = 350
        else:
            long_min = 280
            if diferencia_ptolomeo_alfonso == "s":
                long_max = 350
            else:
                long_max = 340
        lat_min = -30
        lat_max = 20
        add_180 = 180
    elif Constelacion == "PI":  # pisces
        ax.set_title("PISCES", fontsize=14, fontweight="bold")
        if alfonso == "s" and j2000 == "s":
            long_min = -50
            long_max = 30
        else:
            long_min = -50
            if diferencia_ptolomeo_alfonso == "s":
                long_max = 30
            else:
                long_max = 10
        lat_min = -20
        lat_max = 30
    elif Constelacion == "CT":  # cetus
        ax.set_title("CETUS", fontsize=14, fontweight="bold")
        long_min = -30
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 40
        else:
            long_max = 30
        lat_min = -40
        lat_max = 0
    elif Constelacion == "OR":  # orionis
        ax.set_title("ORIONIS", fontsize=14, fontweight="bold")
        if alfonso == "s" and j2000 == "s":
            long_max = 90
            long_min = 50
        else:
            long_min = 40
            long_max = 70
        lat_min = -40
        lat_max = 0
    elif Constelacion == "AM":  # eridanus
        ax.set_title("ERIDANUS", fontsize=14, fontweight="bold")
        long_min = -10
        if alfonso == "s":
            long_max = 90
            lat_max = 0
        else:
            long_max = 50
            lat_max = -20
        lat_min = -60
    elif Constelacion == "LP":  # leporis
        ax.set_title("LEPORIS", fontsize=14, fontweight="bold")
        long_min = 40
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 90
        else:
            long_max = 80
        lat_min = -50
        lat_max = -30
    elif Constelacion == "CN":  # canis
        ax.set_title("CANIS", fontsize=14, fontweight="bold")
        long_min = 40
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 110
        else:
            long_max = 100
        lat_min = -70
        lat_max = -20
    elif Constelacion == "PC":  # precanis
        ax.set_title("PRECANIS", fontsize=14, fontweight="bold")
        long_min = 80
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 110
        else:
            long_max = 100
        lat_min = -20
        lat_max = -10
    elif Constelacion == "AG":  # navis
        ax.set_title("NAVIS", fontsize=14, fontweight="bold")
        long_min = 60
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 180
        else:
            long_max = 170
        lat_min = -80
        lat_max = -40
    elif Constelacion == "HY":  # hydra
        ax.set_title("HYDRA", fontsize=14, fontweight="bold")
        long_min = 70
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 220
        else:
            long_max = 200
        lat_min = -50
        lat_max = 0
        add_180 = 180
    elif Constelacion == "PT":  # patera
        ax.set_title("PATERA", fontsize=14, fontweight="bold")
        long_min = 140
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 180
        else:
            long_max = 165
        lat_min = -30
        lat_max = -10
        add_180 = 180
    elif Constelacion == "CO":  # corvus
        ax.set_title("CORVUS", fontsize=14, fontweight="bold")
        long_min = 160
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 190
        else:
            long_max = 180
        lat_min = -30
        lat_max = -10
        add_180 = 180
    elif Constelacion == "CE":  # centaurus
        ax.set_title("CENTAURUS", fontsize=14, fontweight="bold")
        long_min = 170
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 240
        else:
            long_max = 230
        lat_min = -60
        lat_max = 0
        add_180 = 180
    elif Constelacion == "FE":  # fera
        ax.set_title("FERA", fontsize=14, fontweight="bold")
        long_min = 200
        long_max = 220
        lat_min = -40
        lat_max = 0
        add_180 = 180
    elif Constelacion == "TU":  # turibuli
        ax.set_title("TURIBULI", fontsize=14, fontweight="bold")
        long_min = 230
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 260
        else:
            long_max = 250
        lat_min = -40
        lat_max = -10
        add_180 = 180
    elif Constelacion == "CA":  # corona australis
        ax.set_title("CORONA AUSTRALIS", fontsize=14, fontweight="bold")
        long_min = 240
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 280
        else:
            long_max = 260
        lat_min = -30
        lat_max = -10
        add_180 = 180
    elif Constelacion == "PA":  # pisces austrinus
        ax.set_title("PISCES AUSTRINUS", fontsize=14, fontweight="bold")
        long_min = 270
        if diferencia_ptolomeo_alfonso == "s":
            long_max = 330
        else:
            long_max = 310
        lat_min = -30
        lat_max = -10
        add_180 = 180

    ax.set_extent([long_min, long_max, lat_min, lat_max], crs=ccrs.PlateCarree())
    ax.set_xticks(range(long_min, long_max, 10), crs=ccrs.PlateCarree())
    ax.set_yticks(range(lat_min, lat_max, 10), crs=ccrs.PlateCarree())

    labels = ax.get_xticks().tolist()
    new_labels = labels

    j = 0
    for l in labels:
        if l >= 0:
            new_labels[j] = str(math.trunc(l + 0.1) + add_180) + "˚"
        else:
            new_labels[j] = str(math.trunc(l - 0.1) + add_180 + add_360) + "˚"
        j = j + 1

    ax.set_xticklabels(new_labels)

    labels = ax.get_yticks().tolist()
    new_labels = labels

    j = 0
    for l in labels:
        if l >= 0:
            new_labels[j] = str(math.trunc(l + 0.1)) + "˚"
        else:
            new_labels[j] = str(math.trunc(l - 0.1)) + "˚"
        j = j + 1

    ax.set_yticklabels(new_labels)

    if ptolomeo == "s":

        archivo = open("Constelaciones y estrellas ptolemaicas.prn", "r")

        j = 0

        while j == 0:
            linea = archivo.readline()
            if len(linea) <= 1:
                archivo.close()
                j = 1
            else:
                if linea[4:6] == Constelacion or (alfonso == "s" and Constelacion == "OP" and linea[4:8] == "SO"):
                    lon = float(linea[100:105].replace(",", "."))
                    lat = float(linea[106:111].replace(",", "."))
                    tam = float(linea[112:115].replace(",", "."))
                    ax.scatter(
                        lon, lat, color="white", s=np.pi * tam**2, alpha=1, transform=transform
                    )  # dibujar punto en (lon, lat) dados
                    if anotar_puntos == "s":
                        if linea[124:125].strip() == "L":
                            lon_etiq = lon - float(linea[116:119].replace(",", "."))
                            ha_etiq = "left"
                        else:
                            lon_etiq = lon + float(linea[116:119].replace(",", "."))
                            ha_etiq = "right"
                        if linea[126:127].strip() == "T":
                            lat_etiq = lat + float(linea[120:123].replace(",", "."))
                            va_etiq = "top"
                        else:
                            lat_etiq = lat - float(linea[120:123].replace(",", "."))
                            va_etiq = "bottom"
                        if linea[6:7] == "C":
                            etiqueta = linea[8:10].strip() + linea[6:7].strip()
                        else:
                            etiqueta = linea[8:10].strip()
                        ax.annotate(
                            etiqueta,
                            (lon_etiq, lat_etiq),
                            color="brown",
                            weight="bold",
                            ha=ha_etiq,
                            va=va_etiq,
                            size=9,
                            transform=transform,
                        )

    if teon == "s":

        archivo = open("Lugares de las fijas de los doce signos de Teón de Alejandría - python.prn", "r")

        j = 0

        while j == 0:
            linea = archivo.readline()
            if len(linea) <= 1:
                archivo.close()
                j = 1
            else:
                if linea[6:9] == Constelacion:
                    lon = float(linea[90:97].replace(",", "."))
                    lat = float(linea[98:105].replace(",", "."))
                    tam = float(linea[108:112].replace(",", "."))
                    ax.scatter(
                        lon, lat, color="orange", s=np.pi * tam**2, alpha=1, transform=transform
                    )  # dibujar punto en (lon, lat) dados
                    if anotar_puntos == "s":
                        if linea[132:133].strip() == "L":
                            lon_etiq = lon - float(linea[113:116].replace(",", "."))
                            ha_etiq = "left"
                        else:
                            lon_etiq = lon + float(linea[113:116].replace(",", "."))
                            ha_etiq = "right"
                        if linea[135:136].strip() == "T":
                            lat_etiq = lat + float(linea[119:122].replace(",", "."))
                            va_etiq = "top"
                        else:
                            lat_etiq = lat - float(linea[119:122].replace(",", "."))
                            va_etiq = "bottom"
                        ax.annotate(
                            linea[10:12].strip(),
                            (lon_etiq, lat_etiq),
                            color="orange",
                            weight="regular",
                            ha=ha_etiq,
                            va=va_etiq,
                            size=9,
                            transform=transform,
                        )

    if alfonso == "s":

        if ptolomeo == "s" and diferencia_ptolomeo_alfonso == "n":
            archivo = open("Constelaciones alfonsíes ptolomeo - python.prn", "r")
        else:
            archivo = open("Constelaciones alfonsíes j2000 - python.prn", "r")

        j = 0

        while j == 0:
            linea = archivo.readline()
            if len(linea) <= 1:
                archivo.close()
                j = 1
            else:
                if linea[6:8] == Constelacion:
                    lon = float(linea[123:129].replace(",", "."))
                    lat = float(linea[133:139].replace(",", "."))
                    tam = float(linea[143:146].replace(",", "."))
                    ax.scatter(
                        lon, lat, color="grey", s=np.pi * tam**2, alpha=1, transform=transform
                    )  # dibujar punto en (lon, lat) dados
                    if anotar_puntos == "s":
                        if ptolomeo == "s" and diferencia_ptolomeo_alfonso == "n":
                            if linea[157:158].strip() == "L":
                                lon_etiq = lon - float(linea[147:150].replace(",", "."))
                                ha_etiq = "left"
                            else:
                                lon_etiq = lon + float(linea[147:150].replace(",", "."))
                                ha_etiq = "right"
                            if linea[160:161].strip() == "T":
                                lat_etiq = lat + float(linea[152:155].replace(",", "."))
                                va_etiq = "top"
                            else:
                                lat_etiq = lat - float(linea[152:155].replace(",", "."))
                                va_etiq = "bottom"
                        else:
                            if linea[161:162].strip() == "L":
                                lon_etiq = lon - float(linea[150:153].replace(",", "."))
                                ha_etiq = "left"
                            else:
                                lon_etiq = lon + float(linea[150:153].replace(",", "."))
                                ha_etiq = "right"
                            if linea[164:165].strip() == "T":
                                lat_etiq = lat + float(linea[156:159].replace(",", "."))
                                va_etiq = "top"
                            else:
                                lat_etiq = lat - float(linea[156:159].replace(",", "."))
                                va_etiq = "bottom"
                        ax.annotate(
                            linea[9:11].strip(),
                            (lon_etiq, lat_etiq),
                            color="grey",
                            weight="regular",
                            ha=ha_etiq,
                            va=va_etiq,
                            size=9,
                            transform=transform,
                        )

    if j2000 == "s":

        if alfonso == "s":
            archivo = open("Constelaciones y estrellas actuales alfonso - python.prn", "r")
        else:
            archivo = open("Constelaciones y estrellas actuales.prn", "r")

        j = 0

        while j == 0:
            linea = archivo.readline()
            if len(linea) <= 1:
                archivo.close()
                j = 1
            else:
                if linea[0:2] == Constelacion or (
                    teon == "s" and Constelacion == "LIB" and linea[0:3].strip() == "SCO"
                ):
                    lon = float(linea[28:34].replace(",", "."))
                    lat = float(linea[40:46].replace(",", "."))
                    tam = float(linea[52:55].replace(",", "."))
                    ax.scatter(
                        lon, lat, color="dodgerblue", s=np.pi * tam**2, alpha=1, transform=transform
                    )  # dibujar punto en (lon, lat) dados
                    if anotar_puntos == "s":
                        if linea[67:68].strip() == "L":
                            lon_etiq = lon - float(linea[57:60].replace(",", "."))
                            ha_etiq = "left"
                        else:
                            lon_etiq = lon + float(linea[57:60].replace(",", "."))
                            ha_etiq = "right"
                        if linea[70:71].strip() == "T":
                            lat_etiq = lat + float(linea[62:65].replace(",", "."))
                            va_etiq = "top"
                        else:
                            lat_etiq = lat - float(linea[62:65].replace(",", "."))
                            va_etiq = "bottom"
                        ax.annotate(
                            linea[3:5].strip(),
                            (lon_etiq, lat_etiq),
                            color="pink",
                            weight="bold",
                            ha=ha_etiq,
                            va=va_etiq,
                            size=9,
                            transform=transform,
                        )

    ax.invert_xaxis()

    plt.show()

    return ()
