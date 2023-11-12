# Use the official Python 3.11 slim image as the base image
FROM python:3.11-slim

# Set a label for the image
LABEL name="garmin-project"

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file to the working directory
COPY ./requirements.txt ./

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code to the working directory
COPY ./src ./src

# Set the command to run when the container starts
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]