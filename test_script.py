import requests
from datetime import datetime
from typing import List, TypedDict
import matplotlib.pyplot as plt

class MidspanRow(TypedDict):
    time: datetime
    Fat_cycle_bot: float
    Pos_na: float

def visualize(data: List[MidspanRow]):
    timestamps = [row['time'] for row in data]
    fat_cycle_bot_values = [row['Fat_cycle_bot'] for row in data]
    pos_na_values = [row['Pos_na'] for row in data]
    
    plt.figure(figsize=(14, 6))
    plt.subplot(2, 1, 1)
    plt.plot(timestamps, fat_cycle_bot_values, label='Fat_cycle_bot', color='blue')
    plt.xlabel('Time')
    plt.ylabel('Fat_cycle_bot')
    plt.title('Fat_cycle_bot over Time')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(timestamps, pos_na_values, label='Pos_na', color='orange')
    plt.xlabel('Time')
    plt.ylabel('Pos_na')
    plt.title('Pos_na over Time')
    plt.legend()
    plt.tight_layout()
    plt.show()

try:
    get_midspan = requests.get('http://localhost:8000/midspan')
    midspan_data = get_midspan.json()
except Exception as e:
    midspan_data = {"status": "error", "message": str(e)}

if midspan_data["status"] == "ok":
    print("Data retrieved successfully:")
    for row in midspan_data["data"]:
        row['time'] = datetime.fromisoformat(row['time'])

    for row in midspan_data["data"][:5]:
        print(row)

    visualize(midspan_data["data"])
else:
    print("Failed to retrieve data.")