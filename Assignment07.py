# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Rich Sialana, 2025-03-11, Updated Script
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''

FILE_NAME: str = 'Enrollments.json'

#My Data Variables
students: list = [] #table of student data
menu_choice: str #Hold the choice made by user


# Classes --------------------------------------------- #
class Person:
    '''Store Person data: first and last name
    ChangeLog:
    Rich Sialana, 11 Mar 25, Class Created
    '''

    def __init__(self, first_name: str = '', last_name: str = ''): #__init__ constructor, calls when new instance is created
        self.first_name = first_name #self parameter representing the instance of the clasess
        self.last_name = last_name

    @property #decorator
    def first_name(self): #method name
        return self.__first_name

    @first_name.setter #decorator that designates the follow method as a setter for first_name propert
    def first_name(self, value: str):
        if not value.isalpha():
            raise ValueError('First name must contain only letters.')
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value: str):
        if not value.isalpha():
            raise ValueError('Last name must contain only letters.')
        self.__last_name = value

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

    def to_dict(self):
        return {'FirstName': self.first_name, 'LastName': self.last_name}

class Student(Person): #Person specifies that the Student class inherits from the Person class
    '''Stores Student data: first name last name, and course name
    Changelog:
    Rich Sialana, 11 Mar 25, Created Student class

    '''
    def __init__(self, first_name: str = '', last_name: str = '', course_name: str = ''):
        super().__init__(first_name, last_name) #super() returns a temporary object of the parent class
        self.course_name = course_name


    @property
    def course_name(self):
        return self.__course_name

    @course_name.setter
    def course_name(self, value: str):
        self.__course_name = value

    def __str__(self): #should return a string below I had it returning a dictionary
        # student_dict = super().to_dict()
        # student_dict['CourseName'] = self.course_name
        # return student_dict
        return f'{self.first_name} {self.last_name} Course: {self.__course_name}'

    def to_dict(self):
        students_dict = super().to_dict() #get the first & last names from Peron
        students_dict['CourseName'] = self.__course_name #Add the course name
        return students_dict
# Processing -------------------------------------- #
class FileProcessor:
    '''
    A collection of processing layer functions that work Json files

    ChangeLog:
    Rich Sialana, 11 Mar 25, Created class
    '''
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        '''This function reads data from Json file and loads it into a list of dictionary row
        ChangeLog:
        Rich Sialana, 11 Mar 25, Created Function
        : param file_name: string data with name of file to read from
        : param student_data: list of dictionary rows to be filled with file data
        :return: list'''

        try:
            with open(file_name,'r') as file:
                data = json.load(file)
            #file = open(file_name, 'r')

            #file.close()
            for item in data:
                student = Student(item['FirstName'], item['LastName'], item['CourseName'])
                student_data.append(student)
        except FileNotFoundError:
            IO.output_error_messages(message = 'File not found')
        except Exception as e:
            IO.output_error_messages(message = 'Error: There was a problem with reading the file.', error = e)
        return students

        # return student_data
        # with open(file_name, 'r') as file:
        #     data = json.load(file)

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        '''This function writes data to a json file with data from a list of dictionary rows
        ChangeLog:
        Rich Sialana, 11 Mar 25, Created function

        :param file_name: string data with name of file to write to
        :param student_data: list of dictionary rows to be writen to the file
        :return: None
        '''

        try:
            with open(file_name, 'w') as file:
                json.dump([student.to_dict() for student in student_data], file)
            IO.output_student_and_course_names(student_data=student_data)


        except Exception as e:
            message = 'Error: There was a problem with writing to the file.\n'
            message += 'Please check that the file is not open by another program.'
            IO.output_error_messages(message=message,error=e)

        # finally: code not needed
        #     with open(file, 'w') as file:
        #         json.dump([student.to_dict() for student in student_data], file)
            #originally write codes below but got an error.
            # if file.closed == False: @=
            #     file.close()

#Presentation -------------------------------------- #
class IO:
    ''' A collection of presentation layer functions that manage user input and output

    Changelog:
    Rich Sialana, 11 Mar 25, Created class
    '''

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        ''' This function displays the custom error messages to the user
        ChangeLog:
        Rich Sialana, 11 Mar 25, Created function

        :param message: string with message data to display
        :paeram error: Exception object with technical message to display

        :return: None
        '''
        print(message, end='\n\n')
        if error is not None:
            print('-- Technical Error Message -- ')
            print(error, error.__doc__, type(error), sep='\n')


    @staticmethod
    def output_menu(menu: str):
        '''This function displays the menu of choices to the user

        ChangeLog:
        Rich Sialana, 11 Mar 25, Created function

        :return: None
        '''

        print() #Adding extra space to make it look nicer
        print(menu)
        print() #Adding extra space to make it look nicer


    @staticmethod
    def input_menu_choice():
        ''' This function gets a menu choice from the user

        ChangeLog:
        Rich Sialana, 11 Mar 24, Created function

        :return: string with user's choice
        '''

        choice = '0'

        try:
            choice = input ('Enter you menu choice number: ')
            if choice not in ('1', '2', '3', '4'): #note these are strings
                raise Exception('Please, choose only 1, 2, 3, or 4')
        except Exception as e:
            IO.output_error_messages(e.__str__()) #Not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        ''' This function displays the student and course names to the user

        ChangeLog:
        Rich Sialana, 11 Mar 24, Created Function
        :param student_data: list of dictionary rows to be displayed

        :return: None
        '''

        print('-'* 50)
        for student in student_data:
            print(f'Student {student.first_name} {student.last_name} is enrolled in {student.course_name}')
        print('-'* 50)

    @staticmethod
    def input_student_data(student_data: list):
        ''' This function gets the student's first name and last name, with a course name from the user

        ChangeLog:
        Rich Sialana,11 Mar 25,Created function

        :param student_data: list of dictionary rows to be filled with input data

        :return: list
        '''

        try:
            # Input the data
            student_first_name = input('Enter the student\'s first name: ')
            if not student_first_name.isalpha():
                raise ValueError('The first name should only be Alpha.')
            student_last_name = input('Enter the student\'s last name: ')
            if not student_last_name.isalpha():
                raise ValueError('The last name should only be Alpha.')
            course_name = input('Please enter the course name: ')
            student = Student(first_name=student_first_name, last_name=student_last_name, course_name=course_name)
            student_data.append(student)
            print()
            print(f'You have registered {student_first_name} {student_last_name} for {course_name}.')
        except ValueError as e:
            IO.output_error_messages(message='Error: Invalid input.  Names should only be Alpha.')
        except Exception as e:
            IO.output_error_messages(message='Error: There was a problem with your entered data.', error=e)
        return student_data
#Main body
#When the program starts, read the file data into a list of lists (table)
#Extract the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=[])

#Processing the input data
while (True):
    #menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    #User input
    if menu_choice == '1':  #this will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        #continue
    #Show current data
    elif menu_choice == '2':
        IO.output_student_and_course_names(students)
        continue

    #Save data to file
    elif menu_choice == '3':
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    #Exit / stop loop
    elif menu_choice == '4':
        break
    # else: removed because it duplicating
    #     print('Please, choose only 1, 2, 3, or 4')

print('Program.  Mahalo :)')














