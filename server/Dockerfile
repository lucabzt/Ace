# Start from the official Python base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory ('.') into the container at /app
COPY . .

# Specify the command to run on container startup
CMD ["python", "src/spade/main.py"]
