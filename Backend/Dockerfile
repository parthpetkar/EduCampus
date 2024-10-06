# Use the full version of the Python Docker image
FROM python:3.11

# Set the working directory
WORKDIR /

# Copy requirements file into the container
COPY requirements.txt .

# Create a virtual environment and install dependencies
RUN python -m venv venv

# Activate the virtual environment and install dependencies (for Linux-based systems)
RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port your application runs on
EXPOSE 5000

# Command to run your Flask app inside the virtual environment
CMD ["./venv/bin/python", "app.py"]
