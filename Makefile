build_project:
	docker build -t notes-app .
	docker tag notes-app rsingh95/notes-app:notes-app
	docker run -d -p 8000:8000 notes-app

start_container:
	docker-compose up

stop_container:
	docker-compose down

test:
	docker-compose run --rm app sh -c "python manage.py test"

lint:
	poetry run isort DjangoNotesApp/app
	poetry run black --check --diff DjangoNotesApp/app
