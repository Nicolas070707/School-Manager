from flask import Flask, send_from_directory, request
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')


@app.route('/start_script/<week>')
def start_script(week):
    try:
        # Clear the output file before starting the script
        with open('output.txt', 'w') as f:
            f.write("")

        # Start the script with the week parameter
        subprocess.Popen(['python', 'canceledlessons.py', week])
        return 'Script started successfully'
    except Exception as e:
        return str(e), 500

@app.route('/output.txt')
def output():
    return send_from_directory('.', 'output.txt')

@app.route('/clear_output')
def clear_output():
    try:
        open('output.txt', 'w').close()  # Clear the content of output.txt
        return 'Output cleared successfully'
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(debug=True)
