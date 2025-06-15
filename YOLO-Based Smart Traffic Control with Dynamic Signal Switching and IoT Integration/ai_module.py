def predict_congestion(total_vehicles):
    if total_vehicles < 10:
        return 'Low'
    elif total_vehicles < 25:
        return 'Medium'
    else:
        return 'High'
