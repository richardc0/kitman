import requests
import json

# --- Configuration (REPLACE THESE PLACEHOLDERS) ---
BASE_URL = "https://api.kitmanlabs.com/iP/v1"  # Hypothetical base URL
API_TOKEN = "YOUR_SECURE_API_TOKEN" # Your actual API token/key

# Hypothetical Endpoints (REPLACE IF YOU HAVE THE EXACT DOCS)
TEMPLATES_ENDPOINT = "/questionnaires/templates"
ANSWERS_BY_TEMPLATE_ENDPOINT = "/questionnaires/templates/{template_id}/answers"

def get_templates():
    """
    Fetches all available templates from the Kitman Labs API.
    """
    url = f"{BASE_URL}{TEMPLATES_ENDPOINT}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept": "application/json"
    }
    
    print(f"-> Fetching templates from: {url}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching templates: {e}")
        return None

def get_answers_by_template_id(template_id):
    """
    Fetches all answers associated with a specific template ID.
    """
    # Replace the placeholder in the URL with the actual template_id
    endpoint = ANSWERS_BY_TEMPLATE_ENDPOINT.format(template_id=template_id)
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept": "application/json"
    }

    print(f"-> Fetching answers for template ID {template_id} from: {url}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching answers for template {template_id}: {e}")
        return None

def main():
    """
    Main function to execute the steps: get templates and then get answers for each.
    """
    # 1. Get all templates
    templates_data = get_templates()

    if templates_data and isinstance(templates_data, list):
        print(f"\nSuccessfully retrieved {len(templates_data)} templates.")
        
        # Assume the template ID field is called 'id'
        for template in templates_data:
            template_id = template.get('id') 
            template_name = template.get('name', 'Unknown Name') # Use a fallback name
            
            if template_id:
                print(f"\n--- Processing Template: {template_name} (ID: {template_id}) ---")
                
                # 2. Use the template ID to list all answers
                answers_data = get_answers_by_template_id(template_id)
                
                if answers_data:
                    # Depending on the API's response structure, you might need to adjust this
                    # For example, if the result is a list of answers under a key like 'data'
                    # num_answers = len(answers_data.get('data', [])) 
                    
                    # Assuming the answers_data is a list of answers:
                    num_answers = len(answers_data)
                    print(f"Found {num_answers} answers for template '{template_name}'.")
                    
                    # Optional: Print the first few answers for verification
                    if num_answers > 0:
                        print("Sample answer data:", answers_data[0]) 
                else:
                    print(f"No answers found or error occurred for template '{template_name}'.")
            else:
                print("Warning: Template found with no 'id' field. Skipping.")

    elif templates_data:
         print("\nTemplates data retrieved but not in expected list format. Check API docs.")
         print(templates_data) # Print the raw data for debugging
    else:
        print("\nFailed to retrieve templates. Script aborted.")

if __name__ == "__main__":
    main()
