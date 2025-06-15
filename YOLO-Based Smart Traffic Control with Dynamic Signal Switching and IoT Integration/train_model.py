import random
import pickle
from sklearn.tree import DecisionTreeClassifier

X = []
y = []

directions = ['North', 'East', 'South', 'West']

# Generate synthetic training data
for _ in range(5000):
    features = []
    priority = []
    for d in directions:
        count = random.randint(0, 50)
        features.append(count)
        priority.append(random.choice([0, 1]))  # 0 = normal, 1 = priority
    X.append(features + priority)
    # Label: pick direction with highest (priority or volume)
    priority_dirs = [i for i in range(4) if priority[i]]
    if priority_dirs:
        y.append(priority_dirs[0])
    else:
        y.append(max(range(4), key=lambda i: features[i]))

clf = DecisionTreeClassifier(max_depth=5)
clf.fit(X, y)

with open("green_predictor.pkl", "wb") as f:
    pickle.dump(clf, f)

print("✅ Model saved as green_predictor.pkl")
