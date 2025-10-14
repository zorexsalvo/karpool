.PHONY: build up down logs shell test clean

# Build the Docker image
build:
	docker-compose build

# Start the application
up:
	docker-compose up

# Start the application in background
up-d:
	docker-compose up -d

# Stop the application
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Shell into the web container
shell:
	docker-compose exec web bash

# Run Django management commands
manage:
	docker-compose exec web python manage.py $(filter-out $@,$(MAKECMDGOALS))

# Run migrations
migrate:
	docker-compose exec web python manage.py migrate

# Create superuser
createsuperuser:
	docker-compose exec web python manage.py createsuperuser

# Clean up containers and volumes
clean:
	docker-compose down -v
	docker system prune -f

# Help
help:
	@echo "Available commands:"
	@echo "  build          - Build Docker images"
	@echo "  up             - Start the application"
	@echo "  up-d           - Start the application in background"
	@echo "  down           - Stop the application"
	@echo "  logs           - View application logs"
	@echo "  shell          - Open bash shell in web container"
	@echo "  manage [cmd]   - Run Django management command"
	@echo "  migrate        - Run database migrations"
	@echo "  createsuperuser - Create Django superuser"
	@echo "  clean          - Clean up containers and volumes"
	@echo "  help           - Show this help message"

%:
	@: