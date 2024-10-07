# dtxplus-chatbot

## Before Proceeding with the installation
- Ensure that you have the provided `.env` and `data.json` files with you.
- Please install the latest version of PostgreSQL from [here](https://www.postgresql.org/download/).
- Ensure that you also have `pgAdmin4` installed along with this. `pgAdmin4` is a UI for PostgreSQL that is used to easily navigate the database. It usually comes bundled with PostgreSQL.
- Perform the initial setup of PostgreSQL by setting a password for the `postgres` user.
- Create a database using `pgAdmin4` with a name of your choice (e.g. chatbot-db).
- Modify the database details in the `# Postgres details` section of the `.env` file.
> [!CAUTION]
> Please make sure that the database details you enter in the `.env` file are the same as that you have for your PostgreSQL database.

## Installation instructions
- Clone this repository into a location of your choice.
- Create a python virtual environment in the location.
    ```shell
    python -m venv .venv
    ```
> [!TIP]
> Use `python3` instead of `python` if the above doesn't work.
- Activate the virtual environment
    - On linux
    ```shell
    source .venv/bin/activate
    ``` 
    - On windows cmd
    ```shell
    .venv\Scripts\activate.bat
    ```
> [!TIP]
> Your terminal/command prompt should have the (.venv) indicator if the virtual environment was successfully activated.
- Install all required python packages
    ```shell
    pip install -r requirements.txt
    ``` 
- Verify that Django is installed successfully by running - 
    ```shell
    python -m django --version
    ``` 
    This should successfully print the installed Django version if Django is correctly installed.

- Navigate to the `django_project` directory - 
    ```shell
   cd django_project
    ```
- Paste in the provided `.env` and `data.json` files here. This is very important before proceeding.

> [!WARNING]
> Please ensure that you have pasted the `.env` and `data.json` files in the outer `django_project` directory and not the inner one.
> All commands from here on out are executed from this outer `django_project` directory.

> [!WARNING]
> Please again verify that the database details in the `.env` file are the same for the database you have created.

> [!TIP]
> You can change other LLM details too in the `.env` file.

- Perform the django database migrations - 
    ```shell
    python manage.py migrate
    ```
- Populate the django database with dummy data - 
    ```shell
    python manage.py loaddata data.json
    ```

- Start the application using - 
    ```shell
    python manage.py runserver
    ```

- Navigate to the server link in the command output on your web browser after the command runs successfully.
- Press `ctrl+c` to terminate the server after you are done.

