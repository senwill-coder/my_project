
import csv
import glob
import os
import matplotlib.pyplot as plt
import streamlit as st
CSV_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "classes")
class Student:
    def __init__(self, last_name, first_name, middle_name, birth_year, gender, average_grade):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.birth_year = int(birth_year)
        self.gender = gender
        self.average_grade = float(average_grade)
class SchoolClass:
    def __init__(self, grade, section):
        self.grade = int(grade)
        self.section = section
        self.students = []

    @property
    def name(self):
        return f"{self.grade}{self.section}"

    def promote(self):
        if self.grade == 11:
            return False
        self.grade += 1
        return True
class School:
    def __init__(self, name):
        self.name = name
        self.classes = []

    def get_students(self):
        return [student for school_class in self.classes for student in school_class.students]

    def promote_classes(self):
        self.classes = [school_class for school_class in self.classes if school_class.promote()]
        self.classes.sort(key=lambda school_class: (school_class.grade, school_class.section))
def load_school():
    school = School("Моя школа")
    file_paths = sorted(glob.glob(os.path.join(CSV_FOLDER, "klas_*.csv")))
    for file_path in file_paths:
        with open(file_path, encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            school_class = None

            for row in reader:
                if school_class is None:
                    school_class = SchoolClass(row["Паралель"], row["Вертикаль"])

                student = Student(
                    row["Прізвище"],
                    row["Ім’я"],
                    row["По батькові"],
                    row["Рік народження"],
                    row["Стать"],
                    row["Середня оцінка"].replace(",", "."),
                )
                school_class.students.append(student)

            if school_class is not None:
                school.classes.append(school_class)

    school.classes.sort(key=lambda school_class: (school_class.grade, school_class.section))
    return school
def show_statistics(school):
    students = school.get_students()
    total_students = len(students)
    total_classes = len(school.classes)
    boys = sum(student.gender == "Чоловіча" for student in students)
    girls = sum(student.gender == "Жіноча" for student in students)

    boys_percent = boys / total_students * 100 if total_students else 0
    girls_percent = girls / total_students * 100 if total_students else 0
    students_per_class = total_students / total_classes if total_classes else 0

    st.write(f"Усього учнів: {total_students}")
    st.write(f"Хлопців: {boys} ({boys_percent:.2f}%)")
    st.write(f"Дівчат: {girls} ({girls_percent:.2f}%)")
    st.write(f"Середня кількість учнів у класі: {students_per_class:.2f}")
    if school.classes:
        largest = max(len(school_class.students) for school_class in school.classes)
        smallest = min(len(school_class.students) for school_class in school.classes)
        largest_classes = ", ".join(
            school_class.name for school_class in school.classes
            if len(school_class.students) == largest
        )
        smallest_classes = ", ".join(
            school_class.name for school_class in school.classes
            if len(school_class.students) == smallest
        )
        st.write(f"Максимум: {largest} учнів — {largest_classes}")
        st.write(f"Мінімум: {smallest} учнів — {smallest_classes}")
def show_charts(school):
    students = school.get_students()
    #Кількість учнів за паралелями.
    grades = list(range(1, 12))
    counts_by_grade = [
        sum(len(school_class.students) for school_class in school.classes
            if school_class.grade == grade)
        for grade in grades
    ]
    figure, axis = plt.subplots(figsize=(10, 4))
    axis.bar(grades, counts_by_grade)
    axis.set_xticks(grades)
    axis.set_title("Кількість учнів за паралелями")
    axis.set_xlabel("Паралель")
    axis.set_ylabel("Кількість учнів")
    st.pyplot(figure)
    plt.close(figure)
    #Середня кількість учнів за вертикалями.
    sections = sorted({school_class.section for school_class in school.classes})
    averages_by_section = []
    for section in sections:
        class_sizes = [
            len(school_class.students) for school_class in school.classes
            if school_class.section == section
        ]
        averages_by_section.append(sum(class_sizes) / len(class_sizes))
    figure, axis = plt.subplots(figsize=(7, 4))
    axis.bar(sections, averages_by_section)
    axis.set_title("Середня кількість учнів за вертикалями")
    axis.set_xlabel("Вертикаль")
    axis.set_ylabel("Середня кількість учнів")
    st.pyplot(figure)
    plt.close(figure)
    #Лінійний графік кількості учнів за роком народження.
    birth_years = sorted({student.birth_year for student in students})
    counts_by_year = [
        sum(student.birth_year == year for student in students)
        for year in birth_years
    ]
    figure, axis = plt.subplots(figsize=(10, 4))
    axis.plot(birth_years, counts_by_year, marker="o")
    axis.set_xticks(birth_years)
    axis.set_title("Кількість учнів за роком народження")
    axis.set_xlabel("Рік народження")
    axis.set_ylabel("Кількість учнів")
    axis.grid(alpha=0.3)
    st.pyplot(figure)
    plt.close(figure)
    #Середня оцінка кожного учня залежно від класу.
    figure, axis = plt.subplots(figsize=(12, 5))
    for index, school_class in enumerate(school.classes):
        axis.scatter(
            [index] * len(school_class.students),
            [student.average_grade for student in school_class.students],
            alpha=0.5,
        )
    axis.set_xticks(range(len(school.classes)))
    axis.set_xticklabels([school_class.name for school_class in school.classes], rotation=60)
    axis.set_ylim(0, 12.5)
    axis.set_title("Залежність середньої оцінки учнів від класу")
    axis.set_xlabel("Клас")
    axis.set_ylabel("Середня оцінка")
    axis.grid(axis="y", alpha=0.3)
    st.pyplot(figure)
    plt.close(figure)
def main():
    st.set_page_config(page_title="Статистика школи", layout="wide")
    st.title("Статистика школи та переведення класів")
    school = load_school()
    st.header("До переведення")
    show_statistics(school)
    st.header("Графіки")
    show_charts(school)
    st.header("Переведення на наступний рік")
    if st.button("Перевести всі класи"):
        st.session_state["promoted"] = True
    if st.session_state.get("promoted", False):
        school.promote_classes()
        st.subheader("Після переведення")
        st.write("Колишні 11-ті класи випустилися. Решта перейшла до наступної паралелі.")
        st.write("Класи: " + ", ".join(school_class.name for school_class in school.classes))
        show_statistics(school)

        if st.button("Скинути переведення"):
            st.session_state["promoted"] = False
            st.rerun()
main()