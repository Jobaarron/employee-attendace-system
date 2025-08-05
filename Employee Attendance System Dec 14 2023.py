from datetime import datetime, timedelta
import os
from time import sleep
import json

# Dec 8 2023 - Mulingbayan - Start
# Dec 11 2023 - Misenas - Reviewed and checked. // Adjusted formats for better readability. 8:59PM
# Dec 13 2023 - Mulingbayan & Misenas - Approve/Deny Leave Request & few adjustments for print
# Dec 13 2023 - Ruiz - Enter your Employee ID// new Enter your Employee ID (or Q to Quit)
# Old Enter Employee ID if input is = ex. 1003 = ID not found but if input is = blank = error also if input= abc/etc = error
# New Enter Employee ID if input is Q = Quit if input = blank =Employee ID cannot be blank. Please try again. if input = abc/etc = Invalid input. Please enter a valid Employee ID.
# Dec 14 2023 - JSON File / 15days and Whole Month Attendance Report / Few changes 


class Employee:
    def __init__(self, name, employee_id):
        self.name = name
        self.employee_id = employee_id
        self.attendance = {}
        self.leave_requests = []
        self.leave_status = {}


    def clock_in(self):
        # funtion to time in or Records the time when the employee clocks in and updates the attendance dictionary with the current date and time
        now = datetime.now()
        date = now.date()
        time = now.time()
        self.attendance[date] = {'clock_in': time, 'clock_out': None}
        print(f"Clock in at {time} on {date}")
        sleep(2)
        os.system('cls')

    def clock_out(self):  
        now = datetime.now()
        date = now.date()
        time = now.time()
        if date in self.attendance:
            self.attendance[date]['clock_out'] = time
            print(f"Clock out at {time} on {date}")
            sleep(2)
            os.system('cls')
            # funtion to time out or  Records the time when the employee clocks out and updates the attendance dictionary with the current date and time


    def request_leave(self, start_date, end_date, reason):
        leave_period = {'start_date': start_date, 'end_date': end_date, 'reason': reason}
        self.leave_requests.append(leave_period)
        self.leave_status[(start_date, end_date)] = "Pending"
        print(f"Leave requested from {start_date} to {end_date} for reason: {reason}")
        sleep(4)
        os.system('cls')

    def generate_attendance_report(self, start_date, end_date):
        report = {}
        current_date = start_date
        while current_date <= end_date:
            if current_date in self.attendance:
                report[current_date] = self.attendance[current_date]
            else:
                report[current_date] = {'clock_in': None, 'clock_out': None}
            current_date += timedelta(days=1)
        return report

    def get_leave_requests(self):
        return self.leave_requests
    
    def view_leave_status(self):
        if self.leave_status:
            for (start_date, end_date), status in self.leave_status.items():
                print(f"Leave request from {start_date} to {end_date}: {status}")
                
        else:
            print("No leave requests submitted.")
            sleep(2)
            os.system('cls')
            
    

class AttendanceSystem:
    def __init__(self):
        self.employees = {}
        self.manager_authenticated = False
        self.employee_file = r"D:\Job Aarron\2nd Year First Sem Related (Archive)\Python Project (CS 121)\Final\employees.json"
        
        
        self.load_employees()
        
    def load_employees(self):
        try:
            with open(self.employee_file, 'r') as file:
                data = json.load(file)
                for employee_data in data:
                    employee = Employee(employee_data['name'], employee_data['employee_id'])
                    employee.attendance = employee_data['attendance']
                    employee.leave_requests = employee_data['leave_requests']
                    employee.leave_status = employee_data['leave_status']
                    self.employees[employee.employee_id] = employee
        except FileNotFoundError:
            pass  
    
    def save_employees(self):
         with open(self.employee_file, 'w') as file:
            data = []
            for employee in self.employees.values():
                employee_data = {
                    'name': employee.name,
                    'employee_id': employee.employee_id,
                    'attendance': employee.attendance,
                    'leave_requests': employee.leave_requests,
                    'leave_status': employee.leave_status
                }
                data.append(employee_data)
            json.dump(data, file, indent=2)
    
         

    def add_employee(self, employee):
        self.employees[employee.employee_id] = employee
        self.save_employees() 

    def get_employee(self, employee_id):
        return self.employees.get(employee_id)

    def authenticate_manager(self, password):
        return password == "hr123"
        sleep(2)
        os.system('cls')

    def set_manager_authenticated(self, value):
        self.manager_authenticated = value

    def is_manager_authenticated(self):
        return self.manager_authenticated

    def get_all_employees(self):
        return self.employees.values()

    def approve_leave_request(self, employee, start_date, end_date):
        if (start_date, end_date) in employee.leave_status:
            employee.leave_status[(start_date, end_date)] = "Approved"
            print(f"Leave request from {start_date} to {end_date} approved.")
            sleep(4)
            os.system('cls')
            
            # Update the employee's attendance to mark leave days as 'On Leave'
            current_date = start_date
            while current_date <= end_date:
                employee.attendance[current_date] = {'clock_in': 'On Leave', 'clock_out': 'On Leave'}
                current_date += timedelta(days=1)
                
            # Remove the leave request from the employee's list
            employee.leave_requests = [req for req in employee.leave_requests if req['start_date'] != start_date or req['end_date'] != end_date]
        else:
            print("Leave request not found.")
            sleep(2)
            os.system('cls')

    def deny_leave_request(self, employee, start_date, end_date):
        if (start_date, end_date) in employee.leave_status:
            employee.leave_status[(start_date, end_date)] = "Denied"
            print(f"Leave request from {start_date} to {end_date} denied.")
            # Remove the leave request from the employee's list
            employee.leave_requests = [req for req in employee.leave_requests if req['start_date'] != start_date or req['end_date'] != end_date]
        else:
            print("Leave request not found.")
            
    def generate_attendance_report_for_date(self, date):
        report = {}
        for employee in self.employees.values():
            if date in employee.attendance:
                report[employee.name] = employee.attendance[date]
            else:
                report[employee.name] = {'clock_in': None, 'clock_out': None}
        return report

def main():
    attendance_system = AttendanceSystem()
    sample_employee = Employee("Misenas Job Aarron", 1001)
    attendance_system.add_employee(sample_employee)

    sample_employee2 = Employee("Ruiz Jeremy", 1002)
    attendance_system.add_employee(sample_employee2)

    while True:
        print("\nWelcome to the Attendance Management System")
        print("Are you an Employee or Human Resources?")
        user_type = input("Enter 'E' for Employee or 'H' for Human Resources (Q to Quit Program): ").upper()
        

        if user_type == 'E':
            employee_id = input("Enter your Employee ID: ").strip()
            sleep(1)
            os.system('cls')

            if not employee_id.isdigit():
                print("Invalid input. Please enter a valid Employee ID.")
                continue
                os.system('cls')
            
            employee = attendance_system.get_employee(int(employee_id))


            if employee:
                print("\nEmployee Menu:")
                print("1. Time In")
                print("2. Time Out")
                print("3. Request Leave")
                print("4. View leave request status")
                print("5. Exit")
                choice = input("Enter your choice (1/2/3/4/5): ")

                if choice == '1':
                    employee.clock_in()
                elif choice == '2':
                    employee.clock_out()                

                    
                elif choice == '3':
                    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
                    end_date = input("Enter end date (YYYY-MM-DD): ").strip()
                    reason = input("Enter reason for leave: ").strip()

                    if not start_date or not end_date or not reason:
                        print("Invalid input. Please enter valid inputs for start date, end date, and reason.")
                    else:
                        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                        employee.request_leave(start_date, end_date, reason)
                        

                        
                elif choice == '4':
                    employee.view_leave_status()
                    
                elif choice == '5':
                    sleep(2)
                    os.system('cls')
                    main()
                else:
                    print("Invalid choice. Please enter a valid option.")
                    sleep(2)
                    os.system('cls')
            else:
                print("Employee ID not found.")
                register_choice = input("Would you like to register? (Y/N): ").upper()
                if register_choice == 'Y':
                    name = input("Enter your name: ")
                    new_employee = Employee(name, int(employee_id))
                    attendance_system.add_employee(new_employee)
                    print("New employee added successfully!")
                else:
                    print("Exiting...")

        elif user_type == 'H':
            if attendance_system.is_manager_authenticated():
                print("\nHuman Resources Menu:")
                print("1. View Attendance Report")
                print("2. View Leave Requests")    
                print("3. Exit")
                choice = input("Enter your choice (1/2/3): ")

                if choice == '1':
                    report_type = input("Enter 'C' for cutoff (15 days) report or 'M' for monthly report: ").upper()
                    
                    if report_type == 'C':
                        today = datetime.now().date()
                        start_date = today - timedelta(days=14)  
                        
                        print(f"Cutoff report from {start_date} to {today}:")
                        
                        for employee in attendance_system.get_all_employees():
                            report = employee.generate_attendance_report(start_date, today)
                            print(f"\nAttendance Report for Employee {employee.name}:")
                            for date, attendance in report.items():
                                print(f"{date}: Clock In - {attendance['clock_in']}.")
                                print(f"{date}: Clock Out - {attendance['clock_out']}")
                                
                                
                                
                    elif report_type == 'M':
                        today = datetime.now().date()
                        current_month = today.month
                        current_year = today.year
                        start_date = datetime(current_year, current_month, 1).date()
                    
                        if current_month == 12:
                            end_date = datetime(current_year + 1, 1, 1).date() - timedelta(days=1)
                        else:
                            end_date = datetime(current_year, current_month + 1, 1).date() - timedelta(days=1)
                        
                        print(f"Monthly report for {start_date.strftime('%B, %Y')}:")
                    
                        for employee in attendance_system.get_all_employees():
                            report = employee.generate_attendance_report(start_date, end_date)
                            print(f"\nAttendance Report for Employee {employee.name}:")
                            for date, attendance in report.items():
                                print(f"{date}: Clock In - {attendance['clock_in']}.")
                                print(f"{date}: Clock Out - {attendance['clock_out']}")
                               
                                
                                
    
        
                    
                    

                elif choice == '2':
                    employees_with_requests = [
                        employee for employee in attendance_system.get_all_employees() if employee.leave_requests
                    ]
                    
                    if employees_with_requests:
                        print("\nEmployees with pending leave requests:")
                        for index, employee in enumerate(employees_with_requests, start=1):
                            print(f"{index}. {employee.name}")
                            
                        try:
                            selected_index = int(input("Select an employee index to review leave requests: "))
                            selected_employee = employees_with_requests[selected_index - 1]
                            
                            print(f"\nLeave Requests for {selected_employee.name}:")
                            leave_requests = selected_employee.get_leave_requests()
                            if leave_requests:
                                for request in leave_requests:
                                    print(f"Start Date: {request['start_date']}, End Date: {request['end_date']}, Reason: {request['reason']}")
            
                                try:
                                    request_choice = input("Approve (A) or Deny (D) the leave request: ").upper()
                                    if request_choice == 'A':
                                        attendance_system.approve_leave_request(selected_employee, leave_requests[0]['start_date'], leave_requests[0]['end_date'])
                                    elif request_choice == 'D':
                                        attendance_system.deny_leave_request(selected_employee, leave_requests[0]['start_date'], leave_requests[0]['end_date'])
                                    else:
                                        print("Invalid action.")
                                        os.system('cls')
                                    
                                    
                                        
                                except IndexError:
                                    print("Invalid selection for employee.")
                                    sleep(2)
                                    os.system('cls')
                            else:
                                print("No leave requests for this employee.")
                                sleep(3)
                                os.system('cls')
                        except ValueError:
                            print("Invalid selection for employee.")
                            sleep(3)
                            os.system('cls')
                                
                        
                    else:
                        print("No employees with pending leave requests.")
                        sleep(2)
                        os.system('cls')

                

                elif choice == '3':
                    sleep(1)
                    os.system('cls')
                    main()

                else:
                    print("Invalid choice")
                    sleep(2)
                    os.system('cls')
            else:
                print("Please authenticate as a Human Resources.")
                manager_password = input("Enter Human Resources Password: ")
                authenticated = attendance_system.authenticate_manager(manager_password)
                if authenticated:
                    attendance_system.set_manager_authenticated(True)
                    print("Human Resources authenticated. Access granted.")
                    sleep(2)
                    os.system('cls')
                else:
                    print("Authentication failed. Access denied.")
                    sleep(2)
                    os.sysHtem('cls')

        elif user_type == 'Q' or user_type == 'q':
            print("Exiting the Employee Attendance Management System. Goodbye!")
            sleep(2)
            os.system('cls')
            break
        
        else:
            print("Invalid input. Please enter 'E', 'H', or 'Q'.")
            sleep(2)
            os.system('cls')

if __name__ == "__main__":
    main()

