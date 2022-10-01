# Family Budget
![main workflow](https://github.com/mswierkocki/Family-Budget/actions/workflows/main.yml/badge.svg) ![develop workflow](https://github.com/mswierkocki/Family-Budget/actions/workflows/develop.yml/badge.svg)    
### Simple Family Budget APP
**Description**  
Family Budget example app based on [task](TASKS.md).
The project contain authorisation, tests, fixtures, filtering and pagination.
Entire project is available as an open source project on GitHub.
Commits were add on regular basis. Made with my best judgement.

**Features**
- The application allow for creating several users. 
- Users can create a list of any number of budgets 
- Users can share it with any number of users.
- The budget consists of income and expenses.
- They are grouped into categories.
- REST Api is under /api/

**Tech**
- Python 3.8
- Django 3.0
    - decouple
    - bootstrapV5
    - REST framework
    - django-filters
    - django-seed
    - django-rest-multiple-models
- docker-compose
- Gitlab Actions


# How to
## **Install the application in a local environment**
1. We start with creation of [virtual environments](https://docs.python.org/3/library/venv.html)
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
>> Note: requirements.txt is minimal to work, dev friendly req are in requirements.DEV.txt
2. (Optional) Create `.env` file with configuration variables or use defaults:
    ```text
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    SECRET_KEY=django-insecure-1=django-insecure-1=django-insecure-1=django-insec
    ```
    Otherwise will be used default settings
3. Run migrations.
    ```
    python manage.py migrate
    ```
4. (Optional) Load example categories to DB
    ```
    python manage.py loaddata ExpenseCategories.json
    ```
4. (Only once) Create superuser to be able to login with provided credentials:
    ``` 
    python manage.py createsuperuser
    ```
    And follow instructions
5. Run server! - To start serving app run:
    ``` 
    python manage.py runserver
    ```
> You can now visit it in browser http://127.0.0.1:8000/  
> Admin Panel is under http://127.0.0.1:8000/admin/  
> And You can add user with http://127.0.0.1:8000/admin/auth/user/add/  
## **Install with docker compose**
First time run require to build our images first
```
docker-compose up --build -d

```
Option -d (--detach) is very usefull!  
> #### The `<ctrl>-p <ctrl>-q` sequence is intended for detaching from containers you are attached to with stdin (and may also require a tty connection).</quote>

To start containsers run 
```
docker-compose up
```  
or ```docker-compose up -d```   
To stop  containsers run ```docker-compose down```  
After setting up I recommend changeing default root password which is `example` during first run using:
```
docker exec -it fba-db mysql -u root -p

ALTER USER 'root'@'localhost' IDENTIFIED BY 'NewPassword';
```
And update it in the Env vars or .env file.  
After setup its worth to consiver .env file
Run migrations cmd``
run collect static
run seed scripts?
```
docker exec -it fba-web sh
```
And in container sh:
```
python manage.py collectstatic
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata ExpenseCategories.json
```
Basic checks may be done with `docker ps` or `docker logs <container_name>`  
Example server serving this docker containers is under: http://mforge.pl:8800/


# Extra
add optional BUDGET_PARAMS  may be added to env vars or .env file

Additional cases and things to take under consideration are in [CASES.md](CASES.md) file.
