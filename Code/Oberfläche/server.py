from flask import Flask, send_from_directory
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def loginhtml():
    print("Serving login.html")
    return send_from_directory('login', 'login.html')

@app.route('/loginstyle.css')
def loginstyle():
    print("Serving loginstyle.css")
    return send_from_directory('login', 'loginstyle.css')

@app.route('/login.js')
def loginscript():
    print("Serving login.js")
    return send_from_directory('login', 'login.js')

@app.route('/index.html')
def html():
    print("Serving index.html")
    return send_from_directory('main', 'index.html')

@app.route('/style.css')
def style():
    print("Serving style.css")
    return send_from_directory('main', 'style.css')

@app.route('/script.js')
def script():
    print("Serving script.js")
    return send_from_directory('main', 'script.js')

@app.route('/sign.html')
def signUphtml():
    print("Serving sign.html")
    return send_from_directory('signUp', 'sign.html')

@app.route('/sign.css')
def signUpstyle():
    print("Serving sign.css")
    return send_from_directory('signUp', 'sign.css')


@app.route('/start_script/<week>')
def start_script(week):
    try:
        # Clear the output file before starting the script
        with open('output.txt', 'w') as f:
            f.write("")
        
        # Start the script with the week parameter
        process = subprocess.Popen(['python', 'canceledlessons.py', week],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Log the output and errors
        out, err = process.communicate()
        if process.returncode != 0:
            return f'Error starting script: {err.decode()}', 500
        
        return 'Script started successfully'
    except Exception as e:
        return str(e), 500

@app.route('/output.txt')
def output():
    return send_from_directory('.', 'output.txt')

@app.route('/clear_output')
def clear_output():
    try:
        with open('output.txt', 'w') as f:
            f.write("")  # Clear the content of output.txt
        return 'Output cleared successfully'
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(debug=True)