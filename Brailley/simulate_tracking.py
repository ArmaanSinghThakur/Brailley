import time

locations = ["Entrance", "Grocery", "Dairy", "Cosmetics", "Pharmacy", "Clothing"]

for loc in locations:
    with open("current_location.txt", "w") as f:
        f.write(loc)
    time.sleep(5)
