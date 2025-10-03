# Use the official Python image as the base image
FROM python:3.11-slim

# Set environment variable to make Streamlit look for config in a safe place
# and disable usage stats, which solves the PermissionError (Errno 13).
# Setting these variables at the container level ensures they execute before 
# any Streamlit initialization logic.
ENV HOME="/tmp"
ENV STREAMLIT_GATHER_USAGE_STATS="false"

# Set the working directory
WORKDIR /app

# Copy the dependency file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "chatbot_app.py", "--server.port=8501", "--server.address=0.0.0.0"]