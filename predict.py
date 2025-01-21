# Prediction interface for Cog ⚙️
# https://cog.run/python

import os
import json
import time
import requests
import subprocess
from cog import BasePredictor, Input, ConcatenateIterator

MODEL_NAME = "deepseek-r1:70b"
OLLAMA_API = "http://127.0.0.1:11434"
OLLAMA_GENERATE = OLLAMA_API + "/api/generate"
MODEL_CACHE = "checkpoints"
MODEL_URL = "https://weights.replicate.delivery/default/ollama/deepseek-r1/70b.tar"

def download_weights(url, dest):
    start = time.time()
    print("downloading url: ", url)
    print("downloading to: ", dest)
    subprocess.check_call(["pget", "-xf", url, dest], close_fds=False)
    print("downloading took: ", time.time() - start)
    
def wait_for_ollama(timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(OLLAMA_API)
            if response.status_code == 200:
                print("Ollama server is running")
                return True
        except requests.ConnectionError:
            pass
        time.sleep(1)
    print("Timeout waiting for Ollama server")
    return False

class Predictor(BasePredictor):
    def setup(self):
        """Setup necessary resources for predictions"""
        # set environment variable OLLAMA_MODELS to 'checkpoints'
        os.environ["OLLAMA_MODELS"] = MODEL_CACHE

        # Download weights - comment out to use ollama to donwload the weights
        print("Downloading weights")
        if not os.path.exists(MODEL_CACHE):
            download_weights(MODEL_URL, MODEL_CACHE)

        # Start server
        print("Starting ollama server")
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the server to start
        if not wait_for_ollama():
            raise RuntimeError("Failed to start Ollama server")

        # Load model
        print("Running model")
        subprocess.check_call(["ollama", "run", MODEL_NAME], close_fds=False)

    def predict(self,
        prompt: str = Input(description="Input text for the model"),
        top_p: float = Input(description="Controls diversity of the output. Lower values make the output more focused, higher values make it more diverse.", default=1.0, ge=0.0, le=1.0),
        temperature: float = Input(description="Controls randomness. Lower values make the model more deterministic, higher values make it more random.", default=1.0, ge=0.00, le=2.0),
        repeat_penalty: float = Input(description="Helps to reduce the repetition of tokens from the input. A higher value makes the model less likely to repeat tokens", default=1.0, ge=0.00, le=2.0),
        max_tokens: int = Input(description="Maximum number of tokens it is allowed to generate", default=512, ge=1, le=8192),
        seed: int = Input(description="0 for Random seed", default=42)
    ) -> ConcatenateIterator[str]:
        """Run a single prediction on the model and stream the output"""
        if seed is None:
            seed = int.from_bytes(os.urandom(2), "big")
        print(f"Using seed: {seed}")

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": True,
            "options": {
                "top_p": top_p,
                "temperature": temperature,
                "repeat_penalty": repeat_penalty,
                "num_predict": max_tokens,
            }
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        with requests.post(
            OLLAMA_GENERATE,
            headers=headers,
            data=json.dumps(payload),
            stream=True,
            timeout=300
        ) as response:
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if 'response' in chunk:
                            yield chunk['response']
                    except json.JSONDecodeError:
                        print("Failed to parse response chunk as JSON")

