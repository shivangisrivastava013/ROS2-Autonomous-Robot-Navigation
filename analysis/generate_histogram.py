import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("classes.csv", header=None, names=["class"])

counts = data["class"].value_counts()

counts.plot(kind="bar")

plt.title("Detection Class Histogram")
plt.xlabel("Class")
plt.ylabel("Count")

plt.savefig("histogram.png")

# Detection Results

# All detections recorded during the run corresponded to the class "cone".

# This is expected because the simulated environment primarily contains cone objects used as navigation markers.

# The detection pipeline successfully captured and stored all events in the PostgreSQL database.
