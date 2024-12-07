from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
API_URL = "http://backend:8000"


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cadastro")
def create():
    return render_template("create.html")

@app.route('/insert', methods=['POST'])
def insert_pet():
    nome = request.form['nome']
    animal = request.form['animal']
    raca = request.form['raca']
    idade = int(request.form['idade'])
    adotavel = True if request.form['adotavel'] == 'Sim' else False
    sociavel = True if request.form['sociavel'] == 'Sim' else False
    data = {
        'nome': nome,
        'animal': animal,
        'raca': raca,
        'idade': idade,
        'adotavel': adotavel,
        'sociavel': sociavel
    }
    print(f'data = {data}')
    response = requests.post(f'{API_URL}/api/v1/pets/', json=data)
    if response.status_code == 201:
        return redirect(url_for('list_pets'))
    else:
        return "Erro ao inserir o pet", 400

@app.route('/listar', methods=['GET'])
def list_pets():
    response = requests.get(f'{API_URL}/api/v1/pets/')
    try:
        pets = response.json()
    except requests.exceptions.RequestException:
        pets = []

    return render_template('listing.html', pets=pets)

@app.route('/update/<int:id>', methods=['GET'])
def update_pet(id):
    response = requests.get(f'{API_URL}/api/v1/pets/{id}')
    pet = response.json()
    return render_template('update.html', pet=pet)

@app.route('/update/<int:id>', methods=['POST'])
def update_pet_post(id):
    nome = request.form['nome']
    animal = request.form['animal']
    raca = request.form['raca']
    idade = request.form['idade']
    adotavel = True if request.form['adotavel'] == 'Sim' else False
    sociavel = True if request.form['sociavel'] == 'Sim' else False
    data = {
        'nome': nome,
        'animal': animal,
        'raca': raca,
        'idade': idade,
        'adotavel': adotavel,
        'sociavel': sociavel
    }
    response = requests.patch(f'{API_URL}/api/v1/pets/{id}', json=data)
    if response.status_code == 200:
        return redirect(url_for('list_pets'))
    else:
        return "Erro ao atualizar o pet", 400

@app.route('/delete/<int:id>', methods=['POST'])
def delete_pet(id):
    response = requests.delete(f'{API_URL}/api/v1/pets/{id}')
    if response.status_code == 200:
        return redirect(url_for('list_pets'))
    else:
        return "Erro ao deletar o pet", 400

@app.route('/adopt/<int:id>', methods=['GET'])
def get_pet(id):
    response = requests.get(f'{API_URL}/api/v1/pets/{id}')
    pet = response.json()
    return render_template('adopt.html', pet=pet)

@app.route('/adopt/<int:id>', methods=['POST'])
def sell_pet_post(id):
    quantity = request.form['quantity']
    data = {
        'quantity': quantity
    }
    response = requests.put(f'{API_URL}/api/v1/pets/{id}/sell', json=data)
    if response.status_code == 200:
        return redirect(url_for('list_pets'))
    else:
        return "Erro ao vender o pet", 400
    

@app.route('/reset-database', methods=['GET'])
def reset_database():
    response = requests.delete(f'{API_URL}/api/v1/pets/')
    if response.status_code == 200:
        return redirect(url_for('list_pets'))
    else:
        return "Erro ao resetar o banco de dados", 400

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")
