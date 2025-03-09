from lib.employee import Employee
from lib.department import Department
from lib import CONN, CURSOR
import pytest


class TestEmployee:
    '''Class Employee in employee.py'''

    @pytest.fixture(autouse=True)
    def drop_tables(self):
        '''drop tables prior to each test.'''

        CURSOR.execute("DROP TABLE IF EXISTS employees")
        CURSOR.execute("DROP TABLE IF EXISTS departments")
        Department.all = {}
        Employee.all = {}

    def test_creates_table(self):
        '''contains method "create_table()" that creates table "employees" if it does not exist.'''

        Employee.create_table()
        assert (CURSOR.execute("SELECT * FROM employees"))

    def test_drops_table(self):
        '''contains method "drop_table()" that drops table "employees" if it exists.'''

        sql = """
            CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            job_title TEXT,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments (id))
        """
        CURSOR.execute(sql)
        CONN.commit()

        Employee.drop_table()

        sql_table_names = """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='employees'
        """
        result = CURSOR.execute(sql_table_names).fetchone()
        assert (result is None)

    def test_saves_employee(self):
        '''contains method "save()" that saves an Employee instance to the db and assigns the instance an id.'''

        Employee.create_table()
        department = Department.create("Payroll", "Building A, 5th Floor")
        employee = Employee("Raha", "Accountant", department.id)
        employee.save()

        sql = """
            SELECT * FROM employees
        """
        row = CURSOR.execute(sql).fetchone()
        assert ((row[0], row[1], row[2], row[3]) ==
                (employee.id, employee.name, employee.job_title, employee.department_id))

    def test_creates_employee(self):
        '''contains method "create()" that creates a new row in the db using parameter data and returns an Employee instance.'''

        Employee.create_table()
        department = Department.create("Payroll", "Building A, 5th Floor")
        employee = Employee.create("Raha", "Accountant", department.id)

        sql = """
            SELECT * FROM employees
        """
        row = CURSOR.execute(sql).fetchone()
        assert ((row[0], row[1], row[2], row[3]) ==
                (employee.id, employee.name, employee.job_title, employee.department_id))

    def test_instance_from_db(self):
        '''contains method "instance_from_db()" that takes a table row and returns an Employee instance.'''

        Employee.create_table()
        department = Department.create("Payroll", "Building A, 5th Floor")
        Employee.create("Raha", "Accountant", department.id)

        sql = """
            SELECT * FROM employees
        """
        row = CURSOR.execute(sql).fetchone()
        employee = Employee.instance_from_db(row)

        assert ((row[0], row[1], row[2], row[3]) ==
                (employee.id, employee.name, employee.job_title, employee.department_id))

    def test_finds_by_id(self):
        '''contains method "find_by_id()" that returns an Employee instance corresponding to the db row retrieved by id.'''

        Employee.create_table()
        department = Department.create("Payroll", "Building A, 5th Floor")
        employee1 = Employee.create("Raha", "Accountant", department.id)
        employee2 = Employee.create("Tal", "Senior Accountant", department.id)

        employee = Employee.find_by_id(employee1.id)
        assert (
            (employee.id, employee.name, employee.job_title, employee.department_id) ==
            (employee1.id, "Raha", "Accountant", department.id)
        )
        employee = Employee.find_by_id(employee2.id)
        assert (
            (employee.id, employee.name, employee.job_title, employee.department_id) ==
            (employee2.id, "Tal", "Senior Accountant", department.id)
        )
        employee = Employee.find_by_id(0)
        assert (employee is None)

    def test_updates_row(self):
        '''contains a method "update()" that updates an instance's corresponding db row to match its new attribute values.'''
        Employee.create_table()

        department = Department.create("Payroll", "Building A, 5th Floor")
        employee = Employee.create("Raha", "Accountant", department.id)
        id1 = employee.id

        # Assign new values for name and job_title
        employee.name = "Raha Updated"
        employee.job_title = "Senior Accountant"

        # Persist the updated name and job_title values
        employee.update()

        # assert employee row was updated, employee object state is correct
        employee = Employee.find_by_id(id1)
        assert ((employee.id, employee.name, employee.job_title, employee.department_id) ==
                (id1, "Raha Updated", "Senior Accountant", department.id))

    def test_deletes_row(self):
        '''contains a method "delete()" that deletes the instance's corresponding db row'''
        Employee.create_table()

        department = Department.create("Payroll", "Building A, 5th Floor")
        employee = Employee.create("Raha", "Accountant", department.id)
        id1 = employee.id

        employee.delete()

        # assert employee row is deleted
        assert (Employee.find_by_id(id1) is None)
        # assert employee object state is correct, id should be None
        assert ((None, "Raha", "Accountant", department.id) ==
                (employee.id, employee.name, employee.job_title, employee.department_id))

    def test_gets_all(self):
        '''contains method "get_all()" that returns a list of Employee instances for every row in the db.'''

        Employee.create_table()

        department = Department.create("Payroll", "Building A, 5th Floor")
        employee1 = Employee.create("Raha", "Accountant", department.id)
        employee2 = Employee.create("Tal", "Senior Accountant", department.id)

        employees = Employee.get_all()

        assert (len(employees) == 2)
        assert (
            (employees[0].id, employees[0].name, employees[0].job_title, employees[0].department_id) ==
            (employee1.id, "Raha", "Accountant", department.id)
            (employee1.id, "Raha", "Accountant", department.id)
            (employee1.id, "Raha", "Accountant", department.id)
            (employee1.id, "Raha", "Accountant", department.id)

    def test_gets_all(self):
        '''contains method "get_all()" that returns a list of Employee instances for every row in the db.'''

        Department.create_table()
        department = Department.create("Payroll", "Building A, 5th Floor")
        Employee.create_table()

        employee1 = Employee.create("Raha", "Accountant", department.id)
        employee2 = Employee.create("Tal", "Senior Accountant", department.id)

        employees = Employee.get_all()

        assert (len(employees) == 2)
        assert (
            (employees[0].id, employees[0].name, employees[0].job_title, employees[0].department_id) ==
            (employee1.id, "Raha", "Accountant", department.id))
        assert ((employees[1].id, employees[1].name, employees[1].job_title, employees[1].department_id) ==
            (employee2.id, "Tal", "Senior Accountant", department.id))
                ((employee2.id, "Tal", "Senior Accountant", department.id)),
                ((employee2.id, "Tal", "Senior Accountant", department.id)),
                ((employee2.id, "Tal", "Senior Accountant", department.id)),
                ((employee2.id, "Tal", "Senior Accountant", department.id)),
