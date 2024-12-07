<p text-align="center">
  <img src="src/static/img/favicon.png" alt="shortn logo" width="400px">
</p>
<h1 text-align="center"> shortn </h1>

HTML/CSS/JS Framework Free ✅ • Lightweight ✅ • Functional ✅ • No plaintext passwords ✅


Simple link shortener built with flask.

## Installation
```bash
git clone https://git.confest.im/boyan_k/shortn
pip install -r requirements.txt
```

## Usage
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

## TODOs
- [x] basic UI (to add links)
- [x] basic auth for UI
- [x] sqlite3 to store links
- [x] responsive? (sorta)
- [ ] dockerize
