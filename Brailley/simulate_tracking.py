import time

locations = [
    ("Entrance", 12.000, 12.000),
    ("Grocery", 12.005, 12.010),
    ("Dairy", 12.008, 12.014),
    ("Cosmetics", 12.006, 12.007),
    ("Pharmacy", 12.012, 12.010),
    ("Clothing", 12.015, 12.015)
]

for name, lat, lon in locations:

    with open("current_location.txt", "w") as f:
        f.write(name)

    with open("current_gps.txt", "w") as f:
        f.write(f"{lat}, {lon}")

    print(f"Moved to: {name}")
    time.sleep(5)
