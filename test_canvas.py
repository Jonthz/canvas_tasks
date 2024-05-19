import requests
from bs4 import BeautifulSoup

# Read the token from the file
with open('token.txt', 'r') as file:
    canvas_token = file.read().strip()

# Rest of the code
canvas_base_url = 'https://aulavirtual.espol.edu.ec//api/v1'
course_id = '24122'

headers = {
    'Authorization': f'Bearer {canvas_token}'
}

# URL para obtener las tareas del curso
url = f'{canvas_base_url}/courses/{course_id}/assignments'

# Hacer la solicitud GET
response = requests.get(url, headers=headers)

# Verificar la respuesta
if response.status_code == 200:
    assignments = response.json()
    for assignment in assignments:  
        print("Título de la tarea:", assignment['name'])
        print("Fecha de entrega:", assignment['due_at'])
        print("Puntos:", assignment['points_possible'])
        html_description = assignment['description']
        soup = BeautifulSoup(html_description, 'html.parser')
        formatted_description = soup.get_text(separator='\n').strip()
        formatted_description = "\n".join([line.strip() for line in formatted_description.split("\n") if line.strip()])
        print("Descripción:", formatted_description)
        print()
        print("-"*40)
else:
    print(f'Error: {response.status_code}')
    print(response.text)
