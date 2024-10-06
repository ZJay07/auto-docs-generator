from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

app = Flask(__name__)

model_name = "Salesforce/codegen-350M-multi"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# pipeline
hf_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Define a function to generate documentation using the chain
def generate_documentation(code: str) -> str:
    prompt = f"""
    You are an expert code analyzer and documenter. Given a function, your job is to provide a clear, concise, and accurate description of what the function does, in less than 10 words. Here is the function:

    {code}

    Description of the function:
    """
    response = hf_pipeline(prompt, max_length=150, num_return_sequences=1)
    return response[0]['generated_text'].strip()

@app.route('/generate-docs', methods=['POST'])
def generate_docs():
    if request.is_json:
        content = request.get_json()
        code = content.get("code", "")
        documentation = generate_documentation(code)
        return jsonify({"documentation": documentation})
    else:
        return jsonify({"error": "Invalid request format, expected JSON"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
