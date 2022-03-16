import requests
import os

# Para el nombre de la serie, debes de ir a la pagina https://www.pelisplay.co/
# buscar la serie que prefieras, le das click a ver la serie.
# debes de copiar el nombre de tu serie, pero el nombre que sale en el enlace.
# por ejemplo 'https://www.pelisplay.co/serie/marvel-m-o-d-o-k'
# copiamos lo ultimo 'marvel-m-o-d-o-k' y lo pegamos en donde nos lo piden.
# Para el nombre de la carpeta, puedes ponerle el nombre que quieras, preferiblemente sin espacion, ni caracteres especiales.

parent_dir = os.getcwd()
print("Ingrese el nombre de la serie: ")
serie = input()
url_base = 'https://www.pelisplay.co/api/serie/'+ serie +'/'
resquest = requests.get(url_base)
resquest_response = resquest.json()
print("Ingrese el nombre de la carpeta: ")
data = resquest_response["data"]
temporadas = int(data["n_temporadas"])
nombre_carpeta = input()
path = os.path.join(parent_dir, nombre_carpeta)

if not (os.path.exists(path)):
  os.mkdir(path)

for number in range(temporadas):
  _episodes = list()
  temp = str(number + 1)
  tepm_path = os.path.join(path, "temporada-" + temp)
  if not (os.path.exists(tepm_path)):
    os.mkdir(tepm_path)
  url = url_base + 'temporada-' + temp
  r = requests.get(url)
  response = r.json()
  episodios = int(response["data"]["n_episodios"])
  for episode in range(episodios):
    _episodio = response["data"]["episodios"][episode]["url"]
    _r = requests.get(_episodio)
    _response = _r.json()
    _enlaces = _response["data"]["enlaces"]["online"]
    episodio_path = os.path.join(tepm_path, "episodio-" + str(episode + 1))
    if not (os.path.exists(episodio_path)):
      os.mkdir(episodio_path)
    counter = 0
    for optional_chapters in _enlaces:
      __chapter = optional_chapters
      __chapter__url = __chapter["url"]
      filename = episodio_path + "/" + "episodio-"+ str(episode + 1) + "-" + __chapter["idioma"] + "-" + str(counter) + ".txt"
      if os.path.isfile(filename):
        os.remove(filename)
        f = open(filename, "a")
        f.write(__chapter__url)
        f.close()
        counter = counter + 1
      else:
        f = open(filename, "a")
        f.write(__chapter__url)
        f.close()
        counter = counter + 1