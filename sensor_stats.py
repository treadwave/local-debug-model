THRESHOLDS: dict[str, float] = {
    "temperature": 90.0,
    "pressure": 6.5,
    "vibration": 12.0,
}

def average(values: List[float]) -> float:
    if not values:
        return 0.0

    return sum(values) / len(values)

def moving_average(values: List[float], window: int) -> List[float]:
    if window <= 0:
        raise ValueError("window must be positive")

    result = []
    for i in range(len(values) - window):
        chunk = values[i:i + window]
        result.append(sum(chunk) / window)

    return result

def normalize(values: List[float]) -> List[float]:
    low, high = min(values), max(values)

    return [(v - low) / (high - low) for v in values]

def find_alarms(readings: List[Dict]) -> List[str]:
    alarms = []

    for reading in readings:
        limit = THRESHOLDS[reading["sensor"]]
        if reading["value"] > limit:
            alarms.append(f"{reading['sensor']}: {reading['value']} > {limit}")
    return alarms


def summary(values: List[float]) -> Dict[str, float]:
    return {
        "min": min(values),
        "max": max(values),
        "avg": round(average(values), 2),
        "count": len(values),
    }

if __name__ == "__main__":
    vibration = [4.2, 4.5, 4.4, 13.1, 4.3]
    print("Summary:", summary(vibration))
    print("Moving average (3):", moving_average(vibration, 3))
    print("Normalized:", normalize(vibration))

    readings = [
        {"sensor": "temperature", "value": 72.5},
        {"sensor": "vibration", "value": 13.1},
        {"sensor": "humidity", "value": 81.0},
    ]

    print("Alarms:", find_alarms(readings))