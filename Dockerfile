# Use the official Python 3.12 image from the Docker Hub as the base image
FROM python:3.12

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file to the working directory in the container.
# By copying only the requirements.txt file first, Docker can leverage its caching mechanism.
# Docker builds images incrementally, creating layers. If a file hasn't changed since the last build.
# Docker can reuse the layer from its cache instead of re-copying the file and re-running the command.
# The requirements.txt file typically changes infrequently, so Docker can often use the cache for this step.
COPY ./requirements.txt /app/requirements.txt

# Install the Python dependencies specified in the requirements.txt file.
# Since the previous step is cached, this step will also be cached if requirements.txt hasn't changed.
# This caching saves time by avoiding the need to reinstall dependencies unnecessarily.
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the rest of your application code into the working directory in the container.
# This step is more likely to change, so it will usually not be cached.
# By separating it from the dependencies, we ensure that dependency installation is only redone when necessary.
COPY ../app /app

# The port that this container should listen on at runtime
EXPOSE 8000

# Define the command to run your application using uvicorn.
# This is the entry point of the application when the container starts.
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
