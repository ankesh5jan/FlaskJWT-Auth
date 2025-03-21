# Use the official Python image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the application port (change as needed)
EXPOSE 5000

CMD ["python3","app.py"]
