[Journal of Computational Astronomy & Astronomical Computing (JCAAC)]([https://federacionastronomica.es/index.php/the-journal/archive](https://federacionastronomica.es/index.php/the-journal/archive/contents/611-el-catalogo-de-estrellas-de-hiparco)) [`No. 1, November 2024`](https://github.com/topics/01-nov2024), page 25–48

# The Star Catalogue of Hipparchus
> It is intended to demonstrate that Hipparchus made the Almagest Star Catalogue before
Claudius Ptolemy, who rotated the solstitial and equinoctial points by the number of degrees
he thought of the precession, 1°/100 years, from the time of Hipparchus. At the beginning of
the 19th century, Delambre suggested that Ptolemy had not made any measurements, copying
the observations and measurements of Hipparchus, with some later, poorly executed ones, to
obtain the expected result. The observations and descriptions of eclipses that appear in the
Almagest are well described, and correspond to real events, up to the time of Hipparchus.
According to Delambre, and other more modern authors, the later observations and
descriptions are invented. The ecliptic longitudes and latitudes of the stars of the Almagest
have been monitored, in Plate Carrée projection. Graphs have been constructed in equidistant
azimuthal projection. Similarly, the same coordinates of the most significant stars of twenty
constellations have been taken, on the date J2000. Using two programs in Python/Cartopy, the
graphics of the stars have been constructed in the two eras, that of the first year of Antoninus
Pius, year 138 AD, and that of the Julian date 2000, rotated backwards by the degrees of the
real precession, 26.01°, between both dates. There is a difference of 1.05° between the ecliptic
longitudes of the J2000 stars, rotated, and those of the Almagest star catalogue, located
towards dates 75 years older, which suggests the existence of a systematic error.

# El catálogo de estrellas de Hiparco
> Se quiere demostrar que Hiparco realizó el Catálogo de Estrellas del Almagesto, antes que
Claudio Ptolomeo, quién giró los puntos solsticiales y equinocciales, el número de grados que
él pensaba de la precesión, 1°/100 años, desde la época Hiparco. A comienzos del siglo XIX,
Delambre, sugería que Ptolomeo no había realizado ninguna medición, copiando las
observaciones y mediciones de Hiparco, con algunas posteriores, mal ejecutadas, para obtener
el resultado esperado. Las observaciones y descripciones de eclipses que aparecen en el
Almagesto están bien descritas, y se corresponden con hechos reales, hasta la época de
Hiparco. Según Delambre, y otros autores más modernos, las observaciones y descripciones
posteriores, son inventadas. Se han monitorizado las longitudes y latitudes eclípticas de las
estrellas del Almagesto, en proyección Plate Carrée. Se han construido gráficos en proyección
azimutal equidistante. Igualmente, se han tomado las mismas coordenadas de las estrellas más
significativas de veinte constelaciones, en fecha J2000. Por medio de dos programas en
Python/Cartopy, se han construido los gráficos de las estrellas en las dos eras, la del año
primero de Antonino Pío, año 138 d.C., y la de fecha juliana 2000, girada retrocediendo los
grados de la precesión real, 26,01°, entre ambas fechas. Hay una diferencia de 1,05°, entre las
longitudes eclípticas de las estrellas J2000, giradas, y las del catálogo de estrellas del
Almagesto, situadas hacia fechas 75 años más antiguas, lo que sugiere la existencia de un error
sistemático.

# Instrucciones de uso
La descripción de las funciones principales, `impresion_reticula_AzimuthalEquidistant()` y `impresion_reticula_PlateCarree_Constelacion()`, así como de sus argumentos de entrada y las especificaciones de formato de los ficheros de datos, se encuentra en el módulo `formats.py`. 

En el módulo `check-Hiparco.py` se encuentran ejemplos de uso de ambas funciones. 

:copyright: **César M. González Crespán** 2024. Code licensed under the EUPL. Databases licensed under CC BY-NC-SA 4.0.
