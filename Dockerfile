# Use the official Python image as the base image
FROM python:3.11-slim

# Install debugging tools
RUN apt-get update && apt-get install -y wget curl && apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Set the default command to run the application
CMD ["python", "main/app.py"]
