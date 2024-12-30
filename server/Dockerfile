FROM node:22-slim AS client-build

# Set the working directory in the container
WORKDIR /client-app

# Copy the client dependencies and install them
COPY ./client-hub/package.json ./
RUN npm install

# Copy the rest of the client code and build the production files
COPY ./client ./
RUN npm run build


# Start from the official Python base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

# Copy the entire project directory ('.') into the container at /app
COPY ./server ./

# Copy the client build files into the container at /app/static/client
COPY --from=client-build /client-app/build ./client/

EXPOSE 5000

# Specify the command to run on container startup
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
