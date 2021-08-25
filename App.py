from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import requests
import json
import random

# initializations
app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/')
def Index():
    response = requests.get("http://localhost:8080/get")

    # students = json.load(json.dumps(response.text, indent=15))

   # students = json.load(response.text)
    students = response.json()
    columns = ['Id', 'First Name', 'Last Name',
               'Age', 'Year', 'Edit', 'Delete']

    dataChart = []
    dataLabel = []
    backgroundColor = []
    borderColor = []
    for student in students:
        dataLabel.append(str(student["firstName"]))
        dataChart.append(student["age"])
        rand_color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255), 0.5)
        backgroundColor.append('rgba'+str(rand_color))
        # print(backgroundColor)
    # for student in students:
    # print(student["id"])

    # print(student["id"])
    # print(json.dump(json.loads(student),indent=4,sort_keys=True))
    # print(data.status_code)

    return render_template('index.html', dataStudent=students, columns=columns, dataChart=json.dumps(dataChart), dataLabel=json.dumps(dataLabel), bgColor=json.dumps(backgroundColor))


@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        aid = request.form['id']
        afirstName = request.form['firstName']
        alastName = request.form['lastName']
        aage = request.form['age']

        if len(aid) == 0 or len(afirstName) == 0 or len(alastName) == 0 or len(aage) == 0:
            flash('Add all field obligatori')
        else:
            payload = {
                'id': int(aid),
                'firstName': afirstName,
                'lastName': alastName,
                'age': int(aage)
            }
            response = requests.post(
                'http://localhost:8080/create', data=json.dumps(payload))
            print(response.status_code)
            print(response.text)
            flash('Student Added Success')

    return redirect(url_for('Index'))


@app.route('/edit/<string:id>')
def get_student(id):
    response = requests.get("http://localhost:8080/get/"+id)
    data = response.json()
    return render_template('edit-student.html', student=data)


@app.route('/update/<string:id>', methods=['POST'])
def update_student(id):
    if request.method == 'POST':
        # bid = request.form['id']
        bfirstName = request.form['firstName']
        blastName = request.form['lastName']
        bage = request.form['age']

        if len(bfirstName) == 0 or len(blastName) == 0 or len(bage) == 0:
            flash('Complete fields')
        else:
            payload = {
                'id': int(id),
                'firstName': bfirstName,
                'lastName': blastName,
                'age': int(bage)
            }
            response = requests.put(
                'http://localhost:8080/update/'+id, data=json.dumps(payload)
            )
            if response.status_code == 200:
                flash('Student Updated Success')
            else:
                flash('Error update')
        # print(response.status_code)
        # print(response.text)
    return redirect(url_for('Index'))


@app.route('/delete/<string:id>')
def delete_student(id):
    response = requests.delete("http://localhost:8080/delete/"+id)
    print(response.status_code)

    flash('Student Removed Success')
    return redirect(url_for('Index'))


# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
