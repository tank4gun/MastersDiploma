import os

print(sorted([path for path in os.listdir("./../data") if path.startswith("Linear")])[-1].split("_")[1].split(".")[0])
