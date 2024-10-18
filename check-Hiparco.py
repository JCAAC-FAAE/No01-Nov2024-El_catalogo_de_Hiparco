# Licensed under the EUPL
# check-Hiparco.py

import formats as f


def main():

    # impresión planisferio celeste AzimuthalEquidistant
    ptolomeo = "s"
    plotear_puntos_ptolomeo = "s"
    anotar_puntos_ptolomeo = "s"
    alfonso = "n"
    plotear_puntos_alfonso = "s"
    anotar_puntos_alfonso = "s"
    j2000 = "s"
    plotear_puntos_j2000 = "s"
    anotar_puntos_j2000 = "s"
    x = f.impresion_reticula_AzimuthalEquidistant(
        ptolomeo,
        plotear_puntos_ptolomeo,
        anotar_puntos_ptolomeo,
        alfonso,
        plotear_puntos_alfonso,
        anotar_puntos_alfonso,
        j2000,
        plotear_puntos_j2000,
        anotar_puntos_j2000,
    )

    # Impresión planisferio celeste PlateCarree Constelación
    Constelacion = "OR"
    diferencia_ptolomeo_alfonso = "n"
    anotar_puntos = "s"
    ptolomeo = "s"
    teon = "n"
    alfonso = "n"
    j2000 = "s"
    x = f.impresion_reticula_PlateCarree_Constelacion(
        Constelacion, diferencia_ptolomeo_alfonso, anotar_puntos, ptolomeo, teon, alfonso, j2000
    )
    print(x)


main()
