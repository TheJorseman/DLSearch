# DLSearch

Intenta ser una biblioteca para hacer scrapping de datos en IG,FB y TW para después entrenar modelos de Deep Learning para hacer reconocimiento facial. Además de crear un sistema que sirva para hacer búsqueda de personas mediante una fotografía.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

## Usage
### Uso Scrapping Instagram
```python
from DLSearch.services.instagram import Instagram

# Sera necesario proporcionar usuario y contraseñas mediante un json como:
# {
#    "username" : "tj_chido",
#    "password" : "qmwneb150"
#}
# O crear el objeto Instagram como Instagram(username='username', password='password')
credentials = "credentials/ig_credentials.json"
output_path = 'output'
scrapping = Instagram(credentials=credentials)
scrapping.login()
# Obtiene todos los seguidores de una persona que tenga su perfil como publico
following = scrapping.get_all_following('username')
# Se usa para continuar el scrapping a partir de cierto usuario
following = following.get_nodes_after('dualipa')
print([node.username for node in following])
# No funciona obtener followers
#followers = scrapping.get_all_followers()
#print([node.username for node in followers])

# La descarga de hashtags si funciona xD
#scrapping.download_from_hashtag("rem", output_path, limit=1000)
for user in following:
    print("Download media from ", user.username)
    # Descarga todas las imagenes de una persona xD, aun no funciona para videos
    media = scrapping.download_all_media(user, output_path)
scrapping.close()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)