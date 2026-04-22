import google.generativeai as genai

# Your API Key
GEMINI_API_KEY = "AIzaSyDjmE7tHOBa16iDq-pOmhbbbJwFz39TCsY"
genai.configure(api_key=GEMINI_API_KEY)

print("\n🔍 CHECKING AVAILABLE MODELS FOR YOUR ENVIRONMENT...")
print("-" * 50)

try:
    models = list(genai.list_models())
    if not models:
        print("⚠️ No models found. Check your API key permissions.")
    else:
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ SUPPORTED: {m.name}")
except Exception as e:
    print(f"❌ CRITICAL ERROR: {e}")
    print("\nPRO TIP: Ensure you have the latest library by running: pip install -U google-generativeai")

print("-" * 50)
