from pathlib import Path

import pandas as pd

exercise_dir = Path(__file__).resolve().parent

# Load the CSV
df = pd.read_csv(exercise_dir / "products.csv")

# Create image filenames from the title column
df["image"] = (
    df["title"]
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace(r"[^a-z0-9_]", "", regex=True)  # remove special characters
    + ".png"
)

# Save new CSV
df.to_csv(exercise_dir / "products_with_images.csv", index=False)

df.head()
