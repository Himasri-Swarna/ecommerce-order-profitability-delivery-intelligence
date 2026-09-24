import pandas as pd
from pathlib import Path

data_folder = Path("01_data/01_raw")

for file in data_folder.glob("*.csv"):
    df = pd.read_csv(file)

    missing = df.isna().sum()
    missing = missing[missing > 0]

    print("\n" + "=" * 60)
    print("FILE:", file.name)

    if len(missing) == 0:
        print("No missing values.")
    else:
        print("Missing values by column:")
        print(missing)