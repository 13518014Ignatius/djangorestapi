# User Management API

## Description

This is a backend program consisting of a REST API HTTP server connected to a database.

The program was made with Python using the Django framework, with SQLite3 as the database.

There are five API Endpoints:
1. Login: a POST endpoint for authentication, using username and password. If successful, the endpoint returns a token for subsequent API calls.
2. Register: A POST endpoint to register a user.
3. List Users: A GET endpoint to get a list of all users in the database.
4. Add User: A POST endpoint similar to register, with the requirement that the caller of the endpoint must be logged in.
5. Remove User: A DELETE endpoint to remove a user.

The endpoint functions are in the endpoints.py file.
The test cases are in the tests.py file.

## How to setup

1. Clone the program (requiring git) or download the zip file.
2. Install Python
    - Windows: Download and install python from the Microsoft Store or the official Python website
    - Linux: Go to the terminal and type "apt update" "apt install python3"
    - Verify that Python is installed by typing the command "python3 --version" on the command prompt or the terminal
3. Install pip
    - Windows: Download get-pip.py from https://bootstrap.pypa.io/get-pip.py, then run the command "python3 get-pip.py" on the get-pip.py directory
    - Linux: Go to the terminal and type "apt get python3-pip"
    - pip is installed by default with Python versions 2.7.9+ and 3.4+.
    - Verify that pip is installed by typing the command "pip -V" on the command prompt or the terminal
4. Create a Python virtual environment and activate it.
    - Type "python -m venv /path/to/new/virtual/environment" to create a virtual environment
    - Go to the virtual environment directory, then type "Scripts/activate.bat" on Windows or "bin/activate.bat" on Linux to activate the Python virtual environment
5. Install the dependencies
    - Django: python3 -m pip install Django
    - rest_framework: python3 -m pip install djangorestframework
6. The program is ready to be used.
7. To run the tests, type "python3 manage.py test" in the directory of the program.

## Test Results
Proof of each test can be found in the images named test_results.png and code_coverage.png

### Test Case
All test cases finished running with no failures or errors.

### Code Coverage
100% coverage for endpoints.py and tests.py.
96% coverage for the entire project.
