from flask import Flask, request, jsonify, render_template
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import random


app = Flask(__name__)

# Load your trained model and tokenizer
model = GPT2LMHeadModel.from_pretrained('./trained_model')
tokenizer = GPT2Tokenizer.from_pretrained('./trained_model', padding_side='left')  # Set padding side to left
model.eval()  # Set model to evaluation mode

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    keywords = data['keywords']
    num_suggestions = int(data['num_suggestions'])

    prompt_text = f"{keywords} ->"
    suggestions = generate_names(prompt_text, num_suggestions)

    return jsonify(suggestions)


def generate_names(prompt, num_suggestions):
    original_keywords = prompt.split('->')[0].split(',')

    output_list = []
    for _ in range(num_suggestions):
        # Shuffle keywords and select a random subset each time to vary the input
        keywords = random.sample(original_keywords, k=len(original_keywords))  # Shuffle the keywords
        subset_keywords = keywords[:random.randint(1, len(keywords))]  # Select a random number of keywords

        # Further modify keywords by splitting or truncating randomly
        modified_keywords = []
        for keyword in subset_keywords:
            action = random.choice(['split', 'truncate', 'original'])
            if action == 'split' and len(keyword) > 2:
                split_index = random.randint(1, len(keyword) - 1)
                modified_keywords.append(keyword[:split_index])  # Take the first part
            elif action == 'truncate' and len(keyword) > 1:
                modified_keywords.append(keyword[:-1])  # Remove the last character
            else:
                modified_keywords.append(keyword)  # Use the original keyword

        # Construct a new prompt from these modified keywords
        new_prompt = ', '.join(modified_keywords) + ' ->'
        encoding = tokenizer(new_prompt, return_tensors='pt', padding='max_length', truncation=True, max_length=50)
        input_ids = encoding['input_ids']
        attention_mask = encoding['attention_mask']

        # Generate text from the uniquely altered prompt
        outputs = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=100,  # Ensure the generated text is not too long
            pad_token_id=tokenizer.eos_token_id,
            num_return_sequences=1
        )
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True).split('->')[-1].strip()
        output_list.append(generated_text)

    return output_list

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
