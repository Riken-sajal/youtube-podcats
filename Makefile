# Makefile for managing Django project tasks

.PHONY: clean-audio clean-db migrate runserver

# Directory containing audio files
AUDIO_DIR=media/audio_files

# Database file
DB_FILE=db.sqlite3

# Virtual environment activation
VENV=/home/ubuntu/Workspace/youtube-podcats/env/bin/activate

# Clean all audio files
clean-audio:
	. $(VENV) && rm -rf $(AUDIO_DIR)/*

# Clean the database file
clean-db:
	. $(VENV) && rm -f $(DB_FILE)

# Apply migrations and create new database
migrate: clean-audio clean-db
	. $(VENV) && python manage.py makemigrations
	. $(VENV) && python manage.py migrate

login: login
	. $(VENV) && python manage.py apple_login

apple: apple
	. $(VENV) && python manage.py apple

# Full clean and migrate process
clean-migrate: clean-audio clean-db migrate

# Run the Django development server
runserver:
	. $(VENV) && gunicorn --workers 3 --timeout 3000 --bind 0.0.0.0:8000 podcast.wsgi:application

kill-server:
    kill -9 `sudo lsof -t -i:8000`
