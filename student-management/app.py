from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Cấu hình MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Thay 'root' bằng user của bạn
app.config['MYSQL_PASSWORD'] = '12345'  # Thay bằng mật khẩu MySQL của bạn
app.config['MYSQL_DB'] = 'student_db'

mysql = MySQL(app)

# API lấy danh sách học sinh
@app.route('/students', methods=['GET'])
def get_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.close()

    student_list = [{"id": s[0], "name": s[1], "age": s[2], "class_name": s[3]} for s in students]
    return jsonify(student_list)

# API thêm học sinh mới
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO students (name, age, class_name) VALUES (%s, %s, %s)", 
                (data['name'], data['age'], data['class_name']))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Student added successfully"}), 201

# API xóa học sinh
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Student deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
