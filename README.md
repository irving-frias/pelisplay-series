# pelisplay-series

## Instrucciones de uso

1. Ingresa a la página de [pelisplay](https://www.pelisplay.co/) para buscar la serie que prefieras.
2. Una vez encontrada, puedes dar click en _ver la serie_.
3. Debes copiar el enlace principal de la serie, por ejemplo `https://www.pelisplay.co/serie/marvel-m-o-d-o-k`
4. Una vez teniendo el enlace, puedes ingresar eso dentro del script como parámetro.

Para ejecutar el script puedes hacerlo mediante la siguiente linea de comandos:

```bash
python3 pelisplay-series.py --url https://www.pelisplay.co/serie/marvel-m-o-d-o-k
```

O si quieres almacenarlo en un directorio específico (el default es _pelisplay_) puedes agregar el parámetro:

```bash
python3 pelisplay-series.py --url https://www.pelisplay.co/serie/marvel-m-o-d-o-k --output mi_directorio
```
