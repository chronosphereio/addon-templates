import re

def convert_path_to_title(path):
    # Step 1: Extract last segment
    last_part = path.split('/')[-1]
    
    # Step 2: Remove trailing dash and digits
    cleaned = re.sub(r'-\d+$', '', last_part)
    
    # Step 3: Convert camelCase or PascalCase to words
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', cleaned)
    
    # Step 4: Capitalize each word
    title = ' '.join(word.capitalize() for word in words.split())
    
    return title

def convert_kebab_to_title(text):
    # Define a set of known acronyms to keep fully uppercased
    acronyms = {'gcp', 'aws', 'api', 'cpu', 'gpu', 'ram', 'sql', 'json'}

    words = text.split('-')
    title = ' '.join(word.upper() if word.lower() in acronyms else word.capitalize() for word in words)
    return title
