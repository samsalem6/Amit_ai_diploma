from core.system_manager import SystemManager

# Function to display the main menu
def show_menu():
    print("1. Add student")
    print("2. Remove student")
    print("3. Add course")
    print("4. Remove course")
    print("5. Search courses")
    print("6. Recorde grade")
    print("7. Get all students")
    print("8. Get all course")
    print("9. Enroll course")
    print("10. Exit")

def add_student(manager):
    name = input("Enter student name: ")
    student_id = manager.add_student(name)
    print(f"Student ID: {student_id}")
    print("\n" + "=" * 40)

def remove_student(manager):
    student_id = int(input("Enter student ID: "))
    manager.remove_student(student_id)
    print("\n" + "=" * 40)

def add_course(manager):
    course_name = input("Enter course name: ")
    course_id = manager.add_course(course_name)
    print(f"Course ID: {course_id}")

def remove_course(manager):
    course_id = int(input("Enter course ID: "))
    manager.remove_course(course_id)
    print("\n" + "=" * 40)

def search_courses(manager):
    search_name = input("Enter course name: ")
    courses = manager.search_courses(search_name)
    for course in courses:
        print(course)
    print("\n" + "=" * 40)

def record_grade(manager):
    student_id = int(input("Enter student ID: "))
    course_id = int(input("Enter course ID: "))
    grade = input("Enter grade: ")
    manager.record_grade(student_id, course_id, grade)
    print("\n" + "=" * 40)

def get_all_students(manager):
    students = manager.get_all_students()
    for student in students:
        print(student)
    print("\n" + "=" * 40)

def get_all_courses(manager):
    courses = manager.get_all_courses()
    for course in courses:
        print(course)
    print("\n" + "=" * 40)

def enroll_course(manager):
    student_id = int(input("Enter student ID: "))
    course_id = int(input("Enter course ID: "))
    manager.enroll_course(student_id, course_id)
    print("\n" + "=" * 40)


def main():
    manager = SystemManager()
    while True:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            add_student(manager)
        elif choice == "2":
            remove_student(manager)
        elif choice == "3":
            add_course(manager)
        elif choice == "4":
            remove_course(manager)
        elif choice == "5":
            search_courses(manager)
        elif choice == "6":
            record_grade(manager)
        elif choice == "7":
            get_all_students(manager)
        elif choice == "8":
            get_all_courses(manager)
        elif choice == "9":
            enroll_course(manager)
        elif choice == "10":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")
            print("\n" + "=" * 40)


if __name__ == "__main__":
    main()
