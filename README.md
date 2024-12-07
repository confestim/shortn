<p align="center">
    <img align="center" src="src/static/img/favicon.png" alt="shortn logo" width="400px">
</p>
<h1 align="center"> shortn </h1>

<p align="center">
Pure vanilla HTML/CSS/JS ✅ • Lightweight ✅ • Functional ✅ • No plaintext passwords ✅
</p>


Simple link shortener built with flask.

> [!WARNING]
> PLEASE CHANGE THE SECRET IN `app.py` BEFORE RUNNING IN PRODUCTION (this applies to the docker installation as well)

- [Installation (no docker)](#installation-no-docker)
  - [Usage](#usage)
- [Installation (docker)](#installation-docker)
  - [Users](#users)
- [TODOs](#todos)


## Installation (no docker)
```bash
git clone https://git.confest.im/boyan_k/shortn
pip install -r requirements.txt
```

### Usage
```bash
python manage_users.py init # to create the database
python manage_users.py add # to add a user
>>> Name: admin
>>> Password: *****
>>> Again: *****

python manage_users.py list # to list users
python manage_users.py remove --username <username> # to remove a user

# Finally, running the app
python app.py
```

## Installation (docker)
This will init the database and create a user with the username `admin` and password `admin`.
```bash
docker compose up -d # remove -d for foreground
```

### Users
```bash
sudo docker exec -it shortn python src/manage_users.py add
sudo docker exec -it shortn python src/manage_users.py list
sudo docker exec -it shortn python src/manage_users.py remove --username <username>
```

> [!NOTE]
> The database is **ephemeral** and will be lost when the container is removed. That is intentional.

## TODOs
- [x] basic UI (to add links)
- [x] basic auth for UI
- [x] sqlite3 to store links
- [x] responsive? (sorta)
- [x] dockerize
