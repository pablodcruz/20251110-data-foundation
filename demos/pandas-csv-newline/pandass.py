import pandas as pd

# Load the CSV
df = pd.read_csv("products.csv")

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
df.to_csv("products_with_images.csv", index=False)

df.head()
