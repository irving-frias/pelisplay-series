import os
from argparse import ArgumentParser
from urllib.parse import urlparse

import requests
from tqdm import tqdm


def extract_name(url: str, domain: str = 'www.pelisplay.co') -> str:
    """Devuelve el nombre de la serie si el dominio es el apropiado"""
    parsed_url = urlparse(url)
    last_element = parsed_url.path.split('/')[-1]
    if parsed_url.hostname == domain:
        return last_element
    raise ValueError('La URL no es válida')


def extract_name(url: str, domain: str = 'www.pelisplay.co') -> str:
    """Devuelve el nombre de la serie si el dominio es el apropiado"""
    parsed_url = urlparse(url)
    last_element = parsed_url.path.split('/')[-1]
    if parsed_url.hostname == domain:
        return last_element
    raise ValueError('La URL no es válida')


def ensure_path(base_path: str, prefix: str, path_id: int):
    """Esta función crea el directorio en caso de que no exista"""
    path = os.path.join(base_path, f'{prefix}-{path_id:02d}')
    if not os.path.exists(path):
        os.makedirs(path)

    return path


def request_data(url: str):
    response = requests.get(url)
    return response.json()['data']


def main(url: str, path: str):
    serie = extract_name(url)
    url_base = f'https://www.pelisplay.co/api/serie/{serie}/'
    data = request_data(url_base)
    print(data)
    temporadas = int(data["n_temporadas"])

    if not (os.path.exists(path)):
        os.mkdir(path)

    for temp in range(1, temporadas + 1):
        path_temp = ensure_path(path, 'temporada', temp)

        season_data = request_data(f'{url_base}temporada-{temp}')
        print(season_data)
        episodios = int(season_data["n_episodios"])
        print(f'Temporada: {temp}')

        for episode in tqdm(range(episodios)):
            _epsiode_url = season_data["episodios"][episode]["url"]
            _episode_data = request_data(_epsiode_url)
            print(_episode_data)
            _enlaces = _episode_data["enlaces"]["online"]
            episode_path = ensure_path(path_temp, 'episodio', episode + 1)

            for index, optional_chapters in enumerate(_enlaces):
                __chapter = optional_chapters
                language = optional_chapters['idioma']
                __chapter__url = __chapter["url"]
                filename = os.path.join(
                    episode_path,
                    f'episodio-{episode + 1}-{language}-{index}.txt',
                )

                if os.path.isfile(filename):
                    os.remove(filename)

                with open(filename, "a") as f:
                    f.write(__chapter__url)


if __name__ == '__main__':
    parser = ArgumentParser(
        'Este programa te permite descargar series desde pelisplay.co'
    )
    parser.add_argument(
        '-u', '--url', type=str, required=True, help='URL de la serie'
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        required=False,
        help='Directorio en el que deseas almacenar la serie',
        default='pelisplay',
    )

    args = parser.parse_args()

    main(args.url, args.output)
