import pickle

# Load the trained model (green_predictor.pkl must be in the same directory)
with open("green_predictor.pkl", "rb") as f:
    clf = pickle.load(f)

def predict_green_direction(traffic):
    dirs = ['North', 'East', 'South', 'West']
    counts = [len(traffic[d]) for d in dirs]
    prios = [1 if 'priority' in traffic[d] else 0 for d in dirs]
    features = counts + prios
    result = clf.predict([features])[0]
    return dirs[result]
