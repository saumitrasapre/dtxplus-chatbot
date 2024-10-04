# dtxplus-chatbot

## Installation instructions
- Clone this repository into a location of your choice.
- Create a python virtual environment in the location.
    ```shell
    python3 -m venv .venv
    ```
- Activate the virtual environment
    - On linux
    ```shell
    source .venv/bin/activate
    ``` 
    - On windows cmd
    ```shell
    .venv\Scripts\activate.bat
    ```
    (Your terminal/command prompt should have the (.venv) indicator if the virtual environment is successfully activated.)
- Install all required python packages
    ```shell
    pip install -r requirements.txt
    ``` 
- Verify that Django is installed successfully by running - 
    ```shell
    python -m django --version
    ``` 
    This should successfully print the installed Django version if Django is correctly installed.

- Start the application using - 
    ```shell
    python3 django_project/manage.py runserver
    ```

- Navigate to the server link on your web browser after the command runs successfully.

