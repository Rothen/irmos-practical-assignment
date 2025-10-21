import requests
from datetime import datetime
from typing import List, TypedDict
import matplotlib.pyplot as plt

class MidspanRow(TypedDict):
    _time: List[datetime]
    stress_cycle: List[float]
    pos_na: List[float]

def visualize(data: MidspanRow):
    plt.figure(figsize=(14, 6))
    plt.subplot(2, 1, 1)
    plt.plot(data['_time'], data['stress_cycle'], label='Stress Cycle', color='blue')
    plt.xlabel('Time')
    plt.ylabel('stress_cycle')
    plt.title('stress_cycle over Time')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(data['_time'], data['pos_na'], label='Pos_na', color='orange')
    plt.xlabel('Time')
    plt.ylabel('Pos_na')
    plt.title('Pos_na over Time')
    plt.legend()
    plt.tight_layout()
    plt.show()

try:
    get_midspan = requests.get('http://localhost:8000/bridge-data')
    midspan_data: MidspanRow = get_midspan.json()

    print("Data retrieved successfully:")
    for i in range(len(midspan_data['_time'])):
        midspan_data['_time'][i] = datetime.fromisoformat(midspan_data['_time'][i])

    visualize(midspan_data)
except Exception as e:
    print("Error retrieving data:", str(e))