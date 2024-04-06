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
    compile_result = subprocess.run(['nargo', 'build'], capture_output=True, text=True)
    compile_result = subprocess.run(['nargo', 'compile'], capture_output=True, text=True)
    if compile_result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Failed to compile Noir project: {compile_result.stderr}")
    prove_result = subprocess.run(['nargo', 'prove'], capture_output=True, text=True)
    if prove_result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Failed to generate proof: {prove_result.stderr}")
    return {"result": prove_result.stdout}

@app.post('/verify-proof')
async def verify_proof(request: ProofRequest):
    verify_result = subprocess.run(['nargo', 'verify', json.dumps(request.data)], capture_output=True, text=True)
    if verify_result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Failed to verify proof: {verify_result.stderr}")
    return {"result": verify_result.stdout}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
