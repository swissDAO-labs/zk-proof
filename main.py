from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import json
import uvicorn

app = FastAPI()

class ProofRequest(BaseModel):
    data: dict

@app.post('/create-proof')
async def create_proof(request: ProofRequest):
    """
        curl -X 'POST' \
            'http://localhost:8080/create-proof' \
            -H 'accept: application/json' \
            -H 'Content-Type: application/json' \
            -d '{
            "data": {
                "nonce": 123456,
                "user_input": "sunset over mountains",
                "image": "image_identifier_or_hash"
            }
        }'
    """
    compile_result = subprocess.run(['nargo', 'build'], capture_output=True, text=True)
    compile_result = subprocess.run(['nargo', 'compile'], capture_output=True, text=True)
    if compile_result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Failed to compile Noir project: {compile_result.stderr}")
    prove_result = subprocess.run(['nargo', 'prove'], capture_output=True, text=True)
    if prove_result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Failed to generate proof: {prove_result.stderr}")
    
    # Read the proof from file: 
    with open("./proofs/scarif.proof", "r") as fp:
        proof = fp.read()
    return {"proof": proof}

@app.post('/verify-proof')
async def verify_proof(request: ProofRequest):
    """
        curl -X 'POST' \
            'http://localhost:8080/verify-proof' \
            -H 'accept: application/json' \
            -H 'Content-Type: application/json' \
            -d '{
            "data": {
                "nonce": 123456,
                "user_input": "sunset over mountains",
                "image": "image_identifier_or_hash",
                "proof": "cryptographic_proof_here"
            }
        }'
    """
    verify_result = subprocess.run(['nargo', 'verify', json.dumps(request.data)], capture_output=True, text=True)
    if verify_result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Failed to verify proof: {verify_result.stderr}")
    return {"result": verify_result.stdout}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
