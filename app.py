import subprocess
from flask import Flask, request, send_file, jsonify
import os

app = Flask(__name__)

# Define the path to the voice model and the output file
VOICE_MODEL = 'en_US-lessac-medium.onnx'
OUTPUT_WAV = 'output.wav'

@app.route('/tts', methods=['POST'])
def text_to_speech():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400

        text = data['text']

        # The command to execute Piper
        # It reads text from standard input
        command = [
            'piper',
            '--model', VOICE_MODEL,
            '--output_file', OUTPUT_WAV
        ]

        # Execute the command, passing the text to stdin
        # Using text=True requires Python 3.7+
        result = subprocess.run(command, input=text, text=True, capture_output=True, check=True)

        # Check if the output file was created
        if not os.path.exists(OUTPUT_WAV):
             # If the file doesn't exist, something went wrong. Return Piper's error output.
             return jsonify({"error": "Failed to generate audio", "details": result.stderr}), 500

        # Send the generated .wav file back to the client
        return send_file(OUTPUT_WAV, mimetype='audio/wav')

    except subprocess.CalledProcessError as e:
        # If the Piper command itself fails
        return jsonify({"error": "Piper command failed", "details": e.stderr}), 500
    except Exception as e:
        # For any other errors
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # For local testing, not used by Waitress in production
    app.run(debug=True, host='0.0.0.0', port=5000)