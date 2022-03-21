import os

import requests


def ensure_path(base_path: str, prefix: str, path_id: int):
    """Esta función crea el directorio en caso de que no exista"""
    path = os.path.join(base_path, f'{prefix}-{path_id:02d}')
    if not os.path.exists(path):
        os.makedirs(path)

    return path


def request_data(url: str):
    response = requests.get(url)
    return response.json()['data']


def main():
    parent_dir = os.getcwd()
    serie = input('Ingrese el nombre de la serie: ')
    url_base = f'https://www.pelisplay.co/api/serie/{serie}/'
    data = request_data(url_base)
    temporadas = int(data["n_temporadas"])

    nombre_carpeta = input('Ingrese el nombre de la carpeta: ')
    path = os.path.join(parent_dir, nombre_carpeta)
    if not (os.path.exists(path)):
        os.mkdir(path)

    for temp in range(1, temporadas + 1):
        path_temp = ensure_path(path, 'temporada', temp)

        season_data = request_data(f'{url_base}temporada-{temp}')
        episodios = int(season_data["n_episodios"])

        for episode in range(episodios):
            _epsiode_url = season_data["episodios"][episode]["url"]
            _episode_data = request_data(_epsiode_url)
            _enlaces = _episode_data["enlaces"]["online"]
            episode_path = ensure_path(path_temp, 'episodio', episode + 1)

            for index, optional_chapters in enumerate(_enlaces):
                __chapter = optional_chapters
                language = optional_chapters['idioma']
                __chapter__url = __chapter["url"]
                filename = os.path.join(
                    episode_path, f'episodio-{episode + 1}-{language}-{index}.txt')

                if os.path.isfile(filename):
                    os.remove(filename)

                with open(filename, "a") as f:
                    f.write(__chapter__url)


if __name__ == '__main__':
    main()
