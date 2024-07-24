# Makefile for managing Django project tasks

.PHONY: clean-audio clean-db migrate runserver

# Directory containing audio files
AUDIO_DIR=media/audio_files

# Database file
DB_FILE=db.sqlite3

# Virtual environment activation
VENV=~/ENVs/Podcast_seed/bin/activate

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

# Full clean and migrate process
clean-migrate: clean-audio clean-db migrate

# Run the Django development server
runserver:
    kill -9 `sudo lsof -t -i:8000`
	. $(VENV) && gunicorn --workers 3 --timeout 3000 --bind 0.0.0.0:8000 scrapping.wsgi:application
