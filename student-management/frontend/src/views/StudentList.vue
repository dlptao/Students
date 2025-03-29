<script>
import axios from "axios";

export default {
  name: 'StudentList',
  data() {
    return {
      students: [], // Danh sách học sinh
      newStudent: { name: "", age: "", class_name: "" }
    };
  },
  mounted() {
    // eslint-disable-next-line no-debugger
    this.fetchStudents();
  },
  methods: {
    async fetchStudents() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/students");
        this.students = response.data; // Lưu dữ liệu vào biến students
      } catch (error) {
        console.error("Lỗi khi lấy danh sách học sinh:", error);
      }
    },

    async addStudent() {
      try {
        const response = await axios.post("http://localhost:5000/students", this.newStudent);
        console.log("Thêm thành công:", response.data);

        // Cập nhật danh sách học sinh sau khi thêm
        //this.students.push(response.data);
        this.fetchStudents();

        // Reset form
        this.newStudent = { name: "", age: "", class_name: "" };
      } catch (error) {
        console.error("Lỗi khi thêm học sinh:", error);
      }
    }
  }
};
</script>

<template>
  <div>
    <h1>Danh sách học sinh</h1>
    <ul>
      <li v-for="student in students" :key="student.id">
        {{ student.name }} - {{ student.age }} tuổi - {{ student.class_name }}
        <button class="btn btn-primary" @click="deleteStudent(student.id)">Xóa</button>
      </li>
    </ul>
    <form @submit.prevent="addStudent">
      <div class="row justify-content-center">
        <div class="col-sm-3">
          <div class="form-group">
            <input v-model="newStudent.name" class="form-control" placeholder="Tên" required />
          </div>
        </div>
        <div class="col-sm-2">
          <div class="form-group">
            <input v-model="newStudent.age" class="form-control" type="number" placeholder="Tuổi" required />
          </div>
        </div>
        <div class="col-sm-3">
          <div class="form-group">
            <input v-model="newStudent.class_name" class="form-control" placeholder="Lớp" required />
          </div>
        </div>
      </div>
      <button class="btn btn-success mt-4" type="submit">Thêm học sinh</button>
    </form>
  </div>
</template>
