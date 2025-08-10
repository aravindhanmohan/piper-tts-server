# Use a lean Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# --- FIX STARTS HERE ---
# First, update the package lists, then install wget.
# The "-y" flag auto-confirms the installation.
# Finally, clean up the apt cache to keep the image small.
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*
# --- FIX ENDS HERE ---

# Install Piper TTS and a production-ready web server (Waitress)
RUN pip install piper-tts flask waitress

# Download a voice model. This is a standard, good-quality US English voice.
RUN wget 'https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx' -O en_US-lessac-medium.onnx
RUN wget 'https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json' -O en_US-lessac-medium.onnx.json

# Copy our web server script into the container
COPY app.py .

# Expose port 10000. Render will map its internal port to this.
EXPOSE 10000

# The command to run when the container starts.
# This version uses sh -c to allow Render to dynamically insert the correct port number via the $PORT environment variable.
CMD sh -c "waitress-serve --host=0.0.0.0 --port=${PORT:-10000} app:app"
