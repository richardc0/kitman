import requests
import json

# --- Configuration (REPLACE THESE WITH YOUR ACTUAL VALUES) ---
BASE_URL = "https://your-kitman-api-base-url.com"  # e.g., "https://api.kitmanlabs.com"
API_KEY = "YOUR_API_KEY"
ORG_ID = "YOUR_ORGANISATION_ID" # Required for both endpoints
SQUAD_ID = "YOUR_SQUAD_ID"       # Required for the 'list answers' endpoint

# --- API Headers ---
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_templates():
    """Fetches a list of all questionnaire templates."""
    url = f"{BASE_URL}/api/external/organisations/{ORG_ID}/questionnaire_templates"
    print(f"Fetching templates from: {url}")
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching templates: {e}")
        return None

def get_answers_by_template(template_id):
    """Fetches all answers associated with a specific template ID."""
    url = (
        f"{BASE_URL}/api/external/organisations/{ORG_ID}/squads/{SQUAD_ID}"
        f"/questionnaire_templates/{template_id}/answers"
    )
    print(f"  Fetching answers for template ID: {template_id}")

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"  Error fetching answers for template {template_id}: {e}")
        return None

def main():
    """Main function to run the process."""
    templates_data = get_templates()

    if templates_data and 'data' in templates_data:
        templates = templates_data['data']
        print(f"\nFound {len(templates)} questionnaire templates.")
        
        all_template_answers = {}
        
        for template in templates:
            template_id = template.get('id')
            template_name = template.get('name', 'N/A')
            
            if template_id:
                print(f"\n--- Processing Template: {template_name} (ID: {template_id}) ---")
                answers_data = get_answers_by_template(template_id)
                
                if answers_data and 'data' in answers_data:
                    # Store the template's answers, possibly using the name for better readability
                    all_template_answers[template_name] = answers_data['data']
                    print(f"  Successfully retrieved {len(answers_data['data'])} answers.")
                else:
                    print(f"  No answers found or error retrieving answers for {template_name}.")
            
        print("\n--- Summary of All Template Answers ---")
        for name, answers in all_template_answers.items():
            print(f"Template '{name}': {len(answers)} total answers.")
            # You can uncomment the line below to print all data
            # print(json.dumps(answers, indent=2))
    
    elif templates_data is None:
        print("Script failed to retrieve templates due to an API error.")
    else:
        print("No templates found or unexpected response format.")


if __name__ == "__main__":
    main()
