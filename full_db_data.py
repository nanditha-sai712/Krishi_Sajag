import os
import json
import sqlite3
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("FATAL: GEMINI_API_KEY not found. Please set it in your .env file.")
    exit()

client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"
DATABASE_NAME = 'knowledge.db'

# --- 1. DEFINE TARGETS ---
# List of diseases/problems you want to research and translate
TARGET_PROBLEMS = [
    {"disease_key": "Rice Blast", "crop": "Rice"},
    {"disease_key": "Wheat Rust", "crop": "Wheat"},
    {"disease_key": "Cotton Bollworm", "crop": "Cotton"},
    {"disease_key": "Potato Late Blight", "crop": "Potato"},
    {"disease_key": "Zinc Deficiency", "crop": "General Crops"}
]

TARGET_LANGUAGES = [
    {"code": "en", "name": "English"},
    {"code": "hi", "name": "Hindi"},
    {"code": "te", "name": "Telugu"}
]

# --- 2. PROMPT TEMPLATE ---
SYSTEM_PROMPT = """
You are an expert agricultural researcher specializing in low-cost, organic solutions for Indian farmers.
Your task is to provide a structured diagnosis and remedy plan for a specific crop disease.
You MUST provide the response as a single, valid JSON object that matches the provided JSON schema.
Ensure all translations are in simple, farmer-friendly language.
"""

JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "disease_name": {"type": "string", "description": "The localized name of the disease/deficiency."},
        "cause": {"type": "string", "description": "The cause (fungus, pest, deficiency, etc.) and its ideal conditions."},
        "symptoms": {"type": "string", "description": "Key visual symptoms described simply."},
        "remedies": {"type": "string", "description": "Specific, low-cost organic treatment suggestions (e.g., neem oil, buttermilk)."},
        "preventive": {"type": "string", "description": "Future steps and cultural practices for prevention."}
    },
    "required": ["disease_name", "cause", "symptoms", "remedies", "preventive"]
}

# --- 3. DATABASE FUNCTIONS ---

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diseases (
            id INTEGER PRIMARY KEY,
            disease_key TEXT NOT NULL,
            lang_code TEXT NOT NULL,
            disease_name TEXT NOT NULL,
            cause TEXT,
            symptoms TEXT,
            remedies TEXT,
            preventive TEXT,
            UNIQUE(disease_key, lang_code)
        );
    """)
    conn.commit()
    print("Database table 'diseases' checked/created successfully.")


# --- 4. CORE GENERATION AND INSERTION LOGIC ---

def generate_and_insert_data(conn):
    """Generates data for all target diseases in all target languages and inserts them."""
    cursor = conn.cursor()
    total_records_inserted = 0

    for problem in TARGET_PROBLEMS:
        disease_key = problem["disease_key"]
        crop = problem["crop"]

        print(f"\n--- Generating content for: {disease_key} ({crop}) ---")

        for lang in TARGET_LANGUAGES:
            lang_code = lang["code"]
            lang_name = lang["name"]

            # Skip generation if record already exists (prevents accidental duplication)
            cursor.execute("SELECT 1 FROM diseases WHERE disease_key = ? AND lang_code = ?", (disease_key, lang_code))
            if cursor.fetchone():
                print(f"  [SKIPPING] {lang_name} for {disease_key} already exists.")
                continue

            user_query = f"Provide a complete agricultural advisory for '{disease_key}' affecting '{crop}'. Translate the entire JSON response into simple, localized {lang_name}."
            
            try:
                # 4.1. CALL THE GEMINI API
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=user_query,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        response_schema=JSON_SCHEMA,
                    )
                )

                # 4.2. PARSE AND VALIDATE RESPONSE
                generated_json = json.loads(response.text)
                
                # 4.3. INSERT INTO DATABASE
                cursor.execute("""
                    INSERT INTO diseases (disease_key, lang_code, disease_name, cause, symptoms, remedies, preventive)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    disease_key,
                    lang_code,
                    generated_json['disease_name'],
                    generated_json['cause'],
                    generated_json['symptoms'],
                    generated_json['remedies'],
                    generated_json['preventive']
                ))
                conn.commit()
                total_records_inserted += 1
                print(f"  [SUCCESS] Inserted {disease_key} in {lang_name}.")
                
            except genai.errors.APIError as e:
                 print(f"  [ERROR] API failed for {disease_key} in {lang_name}: {e}")
            except json.JSONDecodeError:
                print(f"  [ERROR] API returned invalid JSON for {disease_key} in {lang_name}.")
            except Exception as e:
                print(f"  [ERROR] An unknown error occurred: {e}")
            
            # 4.4. Throttle the requests to respect API rate limits and avoid errors
            time.sleep(2) 

    print(f"\n--- Data Generation Complete ---")
    print(f"Total new records inserted: {total_records_inserted}")


def main():
    conn = create_connection(DATABASE_NAME)
    if conn is not None:
        create_table(conn)
        generate_and_insert_data(conn)
        conn.close()
    
    print(f"\n✅ You can now run the Streamlit app: 'streamlit run krishi_sajag_db.py'")

if __name__ == '__main__':
    main()
