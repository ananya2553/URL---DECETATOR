import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from extractor import get_url_features
import joblib

# 1. Dataset Load karein (Aapki file ka naam check kar lena)
print("Loading dataset...")
df = pd.read_csv('malicious_phish.csv')

# Training fast karne ke liye hum sirf pehli 50,000 rows lenge
df = df.head(100000)

# 2. Features Extract karein (URLs ko numbers mein badalna)
print("Extracting features... Please wait.")
feature_list = []
for url in df['url']:
    feature_list.append(get_url_features(url))

X = pd.DataFrame(feature_list)
y = df['type'] # Yahan 'type' hi likhna kyunki Excel mein yahi naam hai

# 3. Model Training
print("Training PhishGuard Antigravity AI...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100 max_depth=10,random_state=42)
model.fit(X_train, y_train)

# 4. Save the model
joblib.dump(model, 'phish_model.pkl')
print(f"Success! Accuracy: {model.score(X_test, y_test)*100:.2f}%")