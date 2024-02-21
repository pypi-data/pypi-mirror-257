class Employee:
    raiseAmt = 1.05

    def __init__(self, first, last, salary):
        self.first = first
        self.last = last
        self.salary = salary
        self.email = f'{first.lower()}.{last.lower()}@company.com'
        self.className = self.__class__.__name__

    def __repr__(self):
        return f'Employee\n--------\nName: {self.first} {self.last}\nEmail: {self.email}\nSalary: {self.salary}'

    def apply_raise(self):
        self.salary = int(self.salary * self.raiseAmt)

    def __int__(self):
        return self.salary

    def worker_type(self):
        return self.className

    def is_workday(self, weekday: int):
        if int(weekday) == weekday:
            if weekday == 6 or weekday == 7:
                return 'It is not a workday'
            else:
                return 'It is a workday'
        else:
            return 'Input a number as weekday. 1 = Monday, 7 = Sunday'


class Manager(Employee):
    raiseAmt = 1.10

    def __init__(self, first, last, salary, emps=None):
        super().__init__(first, last, salary)
        if emps is None:
            self.emps = []
        else:
            self.emps = emps

    def get_employees(self, rType):
        if rType.lower() == 's':
            employees = ''
            for emp in self.emps:
                employees += f'{emp}\n'
            return employees
        elif rType.lower() == 'l':
            return self.emps
        else:
            return 'Must specify a valid return type for employees (String = S, List = L'

    def add_employee(self, emp):
        if emp not in self.emps:
            self.emps.append(emp.title())

    def remove_employee(self, emp):
        if emp in self.emps:
            self.emps.remove(emp)

    def __repr__(self):
        employees = ''
        for emp in self.emps:
            employees += f'--> {emp}\n'
        return f'Manager\n-------\nName: {self.first} {self.last}\nEmail: {self.email}\nSalary: {self.salary}\n\nEmployees:\n{employees}'
