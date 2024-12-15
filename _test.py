import requests

url = 'https://api.imgbb.com/1/upload'
api_key = '74117d162959f42cdbdb185cd2457f03'
img = open('D:/Pokedex IA/150 - Mewtwo/104.jpg', 'rb')  # Asegúrate de usar la ruta correcta de tu imagen

import requests

def upload_images(images: list):
    # Asegúrate de que la lista `images` no esté vacía
    if not images:
        return []

    # Crear el diccionario de archivos para la solicitud
    files = {f'image[{index}]': image for index, image in enumerate(images)}

    # Crear el diccionario de datos para la solicitud
    data = { 'key': api_key }

    # Enviar la solicitud POST
    response = requests.post(url, data=data, files=files)
    json_data = response.json()

    # Verificar si la respuesta es exitosa
    if response.status_code == 200 and 'data' in json_data:
        # Extraer las URLs de las imágenes
        urls = [image['url'] for image in json_data['data']]
        return urls
    else:
        # Si hubo un error, puedes manejarlo aquí
        print(f"Error: {json_data.get('error', 'Unknown error')}")
        return []

# Ejemplo de uso
images = [open('D:/Pokedex IA/150 - Mewtwo/104.jpg', 'rb'), open('D:/Pokedex IA/150 - Mewtwo/105.jpg', 'rb')]  # Asegúrate de usar rutas correctas
uploaded_urls = upload_images(images)

# Imprimir las URLs de las imágenes subidas
print(uploaded_urls)

# No olvides cerrar los archivos después de usarlos
for img in images:
    img.close()
