
import csv
import os


class Employee:
    def __init__(self, full_name, base_salary):
        self.full_name = full_name
        self.base_salary = base_salary

    def calculate_salary(self):
        return self.base_salary


class Director(Employee):
    def __init__(self, full_name, base_salary, teaching_experience, management_experience):
        super().__init__(full_name, base_salary)
        self.teaching_experience = teaching_experience
        self.management_experience = management_experience

    def calculate_salary(self):
        return (self.base_salary * self.teaching_experience / 50
                + self.management_experience * 500)


class Teacher(Employee):
    def __init__(self, full_name, base_salary, teaching_experience):
        super().__init__(full_name, base_salary)
        self.teaching_experience = teaching_experience

    def calculate_salary(self):
        return self.base_salary * self.teaching_experience / 30


class Guard(Employee):
    def __init__(self, full_name, base_salary, work_experience):
        super().__init__(full_name, base_salary)
        self.work_experience = work_experience

    def calculate_salary(self):
        return self.base_salary + self.work_experience * 250


def main():
    employees = [
        Director("Мельник Оксана Петрівна", 15000, 29, 12),
        Teacher("Коваленко Андрій Сергійович", 12000, 25),
        Teacher("Шевченко Ірина Миколаївна", 12000, 21),
        Teacher("Гриценко Марія Олександрівна", 12000, 16),
        Teacher("Бондаренко Дмитро Іванович", 12000, 12),
        Guard("Кравчук Сергій Васильович", 11000, 14),
    ]

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "pratsivnyky_zarplaty.csv")
    with open(file_path, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Посада", "ПІБ", "Базова ставка", "Педагогічний стаж",
            "Стаж керування", "Загальний досвід", "Зарплата (грн)",
        ])

        for employee in employees:
            if isinstance(employee, Director):
                role = "Директор"
                teaching_experience = employee.teaching_experience
                management_experience = employee.management_experience
                work_experience = ""
            elif isinstance(employee, Teacher):
                role = "Вчитель"
                teaching_experience = employee.teaching_experience
                management_experience = ""
                work_experience = ""
            else:
                role = "Охоронець"
                teaching_experience = ""
                management_experience = ""
                work_experience = employee.work_experience

            salary = employee.calculate_salary()
            writer.writerow([
                role, employee.full_name, employee.base_salary,
                teaching_experience, management_experience, work_experience,
                f"{salary:.2f}",
            ])
            print(f"{role}: {employee.full_name} — {salary:.2f} грн")

    print(f"\nРезультати збережено у файл: {file_path}")


if __name__ == "__main__":
    main()
