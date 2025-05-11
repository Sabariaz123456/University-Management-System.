import streamlit as st

# --- Classes (Same as your code) ---

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_name(self):
        return self.name


class Student(Person):
    def __init__(self, name, age, roll_number):
        super().__init__(name, age)
        self.roll_number = roll_number
        self.courses = []

    def register_for_courses(self, course):
        self.courses.append(course)
        course.add_student(self)


class Instructor(Person):
    def __init__(self, name, age, salary):
        super().__init__(name, age)
        self.salary = salary
        self.courses = []

    def assign_course(self, course):
        self.courses.append(course)
        course.set_instructor(self)


class Course:
    def __init__(self, name):
        self.name = name
        self.students = []
        self.instructor = None

    def add_student(self, student):
        self.students.append(student)

    def set_instructor(self, instructor):
        self.instructor = instructor


class Department:
    def __init__(self, name):
        self.name = name
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)


class UniversityManagementSystem:
    def __init__(self):
        self.students = []
        self.instructors = []
        self.departments = []

    def add_student(self, student):
        self.students.append(student)

    def add_instructor(self, instructor):
        self.instructors.append(instructor)

    def add_department(self, department):
        self.departments.append(department)

    def show_summary(self):
        st.subheader("📋 University Summary")
        st.markdown("### 🎓 Students")
        for student in self.students:
            st.markdown(f"- **{student.get_name()}** (Roll: {student.roll_number})")

        st.markdown("### 🧑‍🏫 Instructors")
        for instructor in self.instructors:
            st.markdown(f"- **{instructor.get_name()}** (Salary: {instructor.salary})")

        st.markdown("### 🏢 Departments and Courses")
        for dept in self.departments:
            st.markdown(f"#### Department: {dept.name}")
            for course in dept.courses:
                instructor_name = course.instructor.get_name() if course.instructor else "None"
                st.markdown(f"- **Course**: {course.name} | **Instructor**: {instructor_name}")
                for student in course.students:
                    st.markdown(f"    - Student: {student.get_name()}")


# --- Streamlit UI ---

st.set_page_config(page_title="University Management", layout="centered")
st.title("🎓 University Management System")

# 💡 Instructions
st.info("""
### 📝 Instructions

Welcome to the University Management System. Here’s how to use the app:

1. **Add Student**  
   - Enter the student’s name, age, and roll number.  
   - Select the courses the student wants to register for.  
   - Click **"Add Student"**.

2. **Add Instructor**  
   - Enter the instructor’s name, age, and salary.  
   - Select the courses the instructor will teach.  
   - Click **"Add Instructor"**.

3. **Create Course**  
   - Enter a new course name.  
   - Click **"Add Course"** to add it to the system.

4. **Summary**  
   - View all added students, instructors, courses, and departments.

> **Note:** All data is stored in memory during the session. It will reset when you refresh or restart the app.
""")

# 🔁 Initialize session state
if "ums" not in st.session_state:
    st.session_state.ums = UniversityManagementSystem()
    st.session_state.courses = []
    st.session_state.dept = Department("Computer Science")
    st.session_state.ums.add_department(st.session_state.dept)

ums = st.session_state.ums
dept = st.session_state.dept
courses = st.session_state.courses

# 🧭 Tabs
tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Student", "👨‍🏫 Add Instructor", "📚 Create Course", "📊 Summary"])

# ➕ Add Student
with tab1:
    st.subheader("Add New Student")
    name = st.text_input("Student Name")
    age = st.number_input("Age", min_value=16, max_value=100, step=1)
    roll = st.text_input("Roll Number")

    course_options = [course.name for course in courses]

    if not course_options:
        st.warning("⚠️ No courses available. Please create a course first in the '📚 Create Course' tab.")

    selected_courses = st.multiselect("Register for Courses", course_options)

    if st.button("Add Student"):
        if name and roll:
            student = Student(name, age, roll)
            for cname in selected_courses:
                for course in courses:
                    if course.name == cname:
                        student.register_for_courses(course)
            ums.add_student(student)
            st.success(f"Student **{name}** added successfully!")
        else:
            st.error("Please fill in all fields.")

# 👨‍🏫 Add Instructor
with tab2:
    st.subheader("Add New Instructor")
    name = st.text_input("Instructor Name")
    age = st.number_input("Age ", min_value=25, max_value=100, step=1, key="instructor_age")
    salary = st.number_input("Salary", min_value=30000, step=5000)
    selected_courses = st.multiselect("Assign to Courses", [course.name for course in courses], key="assign_courses")

    if st.button("Add Instructor"):
        if name:
            instructor = Instructor(name, age, salary)
            for cname in selected_courses:
                for course in courses:
                    if course.name == cname:
                        instructor.assign_course(course)
            ums.add_instructor(instructor)
            st.success(f"Instructor **{name}** added successfully!")
        else:
            st.error("Please enter instructor name.")

# 📚 Create Course
with tab3:
    st.subheader("Create New Course")
    course_name = st.text_input("Course Name")
    if st.button("Add Course"):
        if course_name:
            course = Course(course_name)
            courses.append(course)
            dept.add_course(course)
            st.success(f"Course **{course_name}** added to {dept.name} department!")
        else:
            st.error("Please enter a course name.")

# 📊 Summary
with tab4:
    ums.show_summary()



