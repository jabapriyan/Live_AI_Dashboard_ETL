import pandas as pd


def clean_traffic_data(data):

    # Convert list of dictionaries into DataFrame
    df = pd.DataFrame(data)

    # Convert Rank from string to integer
    df["Rank"] = pd.to_numeric(df["Rank"])

    # Convert MoM from string percentage to numeric
    df["MoM"] = df["MoM"].str.replace("%", "", regex=False)
    df["MoM"] = pd.to_numeric(df["MoM"])

    # Convert Monthly Visits
    def convert_visits(value):

        value = str(value).strip()

        if value.endswith("B"):
            return float(value[:-1]) * 1_000_000_000

        elif value.endswith("M"):
            return float(value[:-1]) * 1_000_000

        elif value.endswith("K"):
            return float(value[:-1]) * 1_000

        else:
            return float(value)

    df["Monthly_Visits"] = df["Monthly_Visits"].apply(convert_visits)

    # Convert Monthly Visits to integer
    df["Monthly_Visits"] = df["Monthly_Visits"].astype("int64")

    return df

