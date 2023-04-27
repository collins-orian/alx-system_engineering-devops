#!/usr/bin/python3
"""
Using https://jsonplaceholder.typicode.com
returns info about employee TODO progress
Implemented using recursion
"""
import re
import requests
import sys


"""REST API url"""
API = "https://jsonplaceholder.typicode.com"


if __name__ == '__main__':
    if len(sys.argv) > 1:

        '''uses regular expressions to check if first command-line argument is an integer'''
        if re.fullmatch(r'\d+', sys.argv[1]):
            id = int(sys.argv[1])

            '''requests users from the API'''
            user_request = requests.get('{}/users/{}'.format(API, id)).json()

            '''requests the todos from the API'''
            todos_request = requests.get('{}/todos'.format(API)).json()

            '''gets the username, tasks and tasks done from the information
            gotten from the api'''
            user_name = user_request.get('name')
            todos = list(filter(lambda x: x.get('userId') == id, todos_request))
            todos_completed = list(filter(lambda x: x.get('completed'), todos))
            
            '''prints final output'''
            print(
                'Employee {} is done with tasks({}/{}):'.format(
                    user_name,
                    len(todos_completed),
                    len(todos)
                )
            )
            for todo_done in todos_completed:
                print('\t {}'.format(todo_done.get('title')))
