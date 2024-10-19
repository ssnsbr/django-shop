# # Pull base image
# FROM python:3.10.6
FROM python:3.10

# # Set environment variables
# # disables an automatic check for pip updates each time
# ENV PIP_DISABLE_PIP_VERSION_CHECK 1 
# # Python will not try to write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# # ensures our console output is not buffered by Docker
ENV PYTHONUNBUFFERED 1

WORKDIR /shop_backend


# install system dependencies
# RUN apt-get update && apt-get install -y netcat

# # Install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# copy entrypoint.sh
# COPY ./entrypoint.sh .
# RUN ./entrypoint.sh
# RUN sed -i 's/\r$//g' /usr/src/shop_backend/entrypoint.sh
# RUN chmod +x /usr/src/shop_backend/entrypoint.sh

# # Copy project
# COPY ./shop_backend ./shop_backend
COPY . .

# # Collect static files for the Django application
# RUN python manage.py collectstatic --noinput

# EXPOSE 8000
RUN mkdir logs
# RUN python manage.py makemigrations
# RUN python manage.py migrate

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
