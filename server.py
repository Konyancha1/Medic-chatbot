import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from flask import Flask, jsonify, request
from flask_cors import CORS

# Initialize Flask application
app = Flask(__name__)
CORS(app)
model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2, from_tf=True)
model.load_state_dict(torch.load('model.pth', map_location=torch.device('cpu')))

tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

def preprocess(input_message):
    # Tokenize the input message
    input_tokens = tokenizer.encode(input_message, add_special_tokens=True, truncation=True, max_length=128, return_tensors='pt')
    input_ids = input_tokens[0].tolist()
    attention_mask = [1] * len(input_ids)
    # Return the input tokens
    return {
        'input_ids': input_ids,
        'attention_mask': attention_mask
    }

def postprocess(output_tensor):
    probabilities = torch.softmax(output_tensor, dim=1)[0].tolist()
    predicted_label = int(torch.argmax(output_tensor, dim=1))
    # Determine the confidence score for the predicted label
    confidence_score = probabilities[predicted_label]
    # Map the predicted label to the appropriate response
    if predicted_label == 0:
        response = "I'm sorry, I'm not qualified to provide medical advice. Please consult a licensed healthcare professional."
    else:
        response = "Hello! How can I help you today?"
    # Return the response and confidence score as a dictionary
    return {'response': response, 'confidence_score': confidence_score}

def generate_response(input_message):
    preprocessed_input = preprocess(input_message)
    input_tensor = torch.tensor([preprocessed_input['input_ids']])
    attention_mask = torch.tensor([preprocessed_input['attention_mask']])
    output_tensor = model(input_ids=input_tensor, attention_mask=attention_mask)[0]
    postprocessed_output = postprocess(output_tensor)
    response = postprocessed_output['response']
    confidence_score = postprocessed_output['confidence_score']
    return {'response': response, 'confidence_score': confidence_score}

# Define an API endpoint for chatbot
@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    message = request.json.get('message')
    response = generate_response(message)['response']
    return jsonify({'response': response})

# Define an API endpoint for prediction
@app.route('/predict', methods=['POST'])
def predict():
    message = request.json.get('message')
    response = generate_response(message)['response']
    return jsonify(response)

# Run the Flask application
if __name__ == '__main__':
    app.run()
