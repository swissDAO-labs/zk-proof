from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/create-proof', methods=['POST'])
def create_proof():
    data = request.json
    # Assuming 'data' contains the necessary information for Nargo
    # Adjust the command based on how you use Nargo
    result = subprocess.run(['nargo', 'create-proof', json.dumps(data)], capture_output=True, text=True)
    return jsonify({"result": result.stdout}), 200

@app.route('/verify-proof', methods=['POST'])
def verify_proof():
    data = request.json
    # Adjust the command based on how you use Nargo
    result = subprocess.run(['nargo', 'verify-proof', json.dumps(data)], capture_output=True, text=True)
    return jsonify({"result": result.stdout}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)
