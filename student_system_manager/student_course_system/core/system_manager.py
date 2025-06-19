from model.student import Student
from model.course import Course

class SystemManager:
    def __init__(self):
        self.students = {}
        self.courses = {}

    def add_student(self, name):
        student = Student(name)
        self.students[student.student_id] = student
        print("Student added successfully.")
        return student.student_id
    
    def remove_student(self, student_id):
        if student_id in self.students:
            student = self.students[student_id]
            if not student.enrolled_courses:
                del self.students[student_id]
                print("Student removed successfully")
            else:
                print("Student has enrolled courses. Cannot remove.")
        else:
            print("Invalid student ID.")

    def add_course(self, name):
        course = Course(name)
        self.courses[course.course_id] = course
        print("Course added successfully.")
        return course.course_id
    
    def remove_course(self, course_id):
        if course_id in self.courses:
            course = self.courses[course_id]
            if not course.enrolled_students:
                del self.courses[course_id]
                print("Course removed successfully")
            else:
                print("Course has enrolled student. Cannot remove.")
        else:
            print("Invalid Course ID.")

    def enroll_course(self, student_id, course_id):
        if student_id in self.students and course_id in self.courses:
            student = self.students[student_id]
            course = self.courses[course_id]

            if course.name not in  student.enrolled_courses:
                student.enroll_in_course(course.name)
                course.enroll_student(student.name)
                print("Student enrolled in ccourse successfully.")
            else:
                print("Student is already enrolled in the course")
        else:
            print("Invalid student or course ID.")

    def search_courses(self, serach_name):
        result = []
        for course in self.courses.values():
            if serach_name.lower() == course.name.lower():
                result.append(course.name)
        return result
    
    def record_grade(self, student_id, course_id, grade):
        if student_id in self.students and course_id in self.courses:
            student = self.students[student_id]
            course = self.courses[course_id]
            student.add_grade(course.name, grade)
            print("Grade recorded successfully.")
        else:
            print("Invaild student or course ID.")

    def get_all_students(self):
        return list(self.students.values())
    
    def get_all_courses(self):
        return list(self.courses.values())