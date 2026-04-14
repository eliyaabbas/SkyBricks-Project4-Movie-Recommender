import pandas as pd
import pickle
import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")

def check_file(filename):
    if not os.path.exists(filename):
        print(f"[MISSING] {filename}")
        return False
    print(f"[OK] {filename} exists. Size: {os.path.getsize(filename) / (1024*1024):.2f} MB")
    return True

all_good = True

# Check CSVs
for f in ["tmdb_5000_movies.csv", "tmdb_5000_credits.csv"]:
    if check_file(f):
        try:
            df = pd.read_csv(f)
            print(f"   -> Successfully loaded {f}. Shape: {df.shape}")
        except Exception as e:
            print(f"   -> [ERROR] loading {f}: {e}")
            all_good = False
    else:
        all_good = False

# Check PKLs
for f in ["movie_dict.pkl", "similarity.pkl", "vectorizer.pkl"]:
    if check_file(f):
        try:
            with open(f, "rb") as file:
                obj = pickle.load(file)
            print(f"   -> Successfully loaded {f}.")
        except Exception as e:
            print(f"   -> [ERROR] loading {f}: {e}")
            all_good = False
    else:
        all_good = False

if all_good:
    print("\n[SUCCESS] All files have sound integrity!")
else:
    print("\n[WARNING] Summary: One or more files are corrupted or missing.")
