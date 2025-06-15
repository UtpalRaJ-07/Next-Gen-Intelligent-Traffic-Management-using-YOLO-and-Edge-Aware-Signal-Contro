import random

def update_intersection_traffic(current=None, green_dir=None):
    directions = ['North', 'East', 'South', 'West']
    if current is None:
        traffic = {}
        for dir in directions:
            traffic[dir] = random.choices(['normal', 'priority'], weights=[0.7, 0.3], k=random.randint(2, 6))
        return traffic

    for dir in directions:
        if dir != green_dir:
            if random.random() < 0.8:
                extra = random.choices(['normal', 'priority'], weights=[0.6, 0.4], k=random.randint(1, 3))
                current[dir].extend(extra)
        else:
            drain = min(len(current[dir]), random.randint(1, 4))
            current[dir] = current[dir][drain:]
    return current
