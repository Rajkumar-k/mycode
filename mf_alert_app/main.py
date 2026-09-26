from mftool import Mftool
import pandas as pd


scheme_codes = {

    "Motilal Oswal Midcap Fund Direct Growth": {
        "frequency": "Monthly",
        "fund_type": "India",
        "code": "127042",
        "type": "Mid Cap"
    },

    "Canara Robeco Small Cap Fund Direct": {
        "frequency": "Monthly",
        "fund_type": "India",
        "code": "146130",
        "type": "Small Cap"
    },

    "Motilal Oswal Infra Fund": {
        "frequency": "Adhoc",
        "fund_type": "Adhoc",
        "code": "153484",
        "type": "Sectoral"
    },

    "Ivesco India Pharma and Healthcare Fund": {
        "frequency": "Adhoc",
        "fund_type": "Adhoc",
        "code": "154547",
        "type": "Sectoral"
    },
}

mf = Mftool()

# ---------------------------------------
# Fetch NAV history
# ---------------------------------------

all_data = []

for fund_name, details in scheme_codes.items():

    code = details["code"]

    nav_data = mf.get_scheme_historical_nav(code)

    if nav_data and "data" in nav_data:

        temp = pd.DataFrame(nav_data["data"])

        temp["date"] = pd.to_datetime(
            temp["date"],
            format="%d-%m-%Y"
        )

        temp["nav"] = pd.to_numeric(temp["nav"])

        # From 01-Jan-2026
        temp = temp[temp["date"] >= "2026-01-01"]

        # Add your fund information
        temp["Fund"] = fund_name
        temp["Code"] = code
        temp["Frequency"] = details["frequency"]
        temp["Fund_Type"] = details["fund_type"]
        temp["Type"] = details["type"]

        all_data.append(temp)


# ---------------------------------------
# Combine all funds
# ---------------------------------------

df = pd.concat(all_data, ignore_index=True)

# Sort
df = df.sort_values(
    ["Fund", "date"]
).reset_index(drop=True)


# ---------------------------------------
# Final columns
# ---------------------------------------

df = df[
    [
        "date",
        "Fund",
        "nav"
    ]
]

df['Week_Number'] = df['date'].dt.isocalendar().week

df = df.groupby(
    ["Fund", "Week_Number"],
    as_index=False
).agg(
    avg_nav=("nav", "mean"),
    min_date=("date", "min")
)

# Sort before calculating previous row
df = df.sort_values(
    ["Fund", "Week_Number"]
).reset_index(drop=True)



# Final columns
df = df[
    [
        "Fund",
        "avg_nav",
        "min_date"
    ]
]
df["Date_Rank"] = (
    df.groupby("Fund")["min_date"]
      .rank(method="dense", ascending=False)
      .astype(int)
)

latest = df[df["Date_Rank"] == 1].set_index("Fund")["avg_nav"]

result = df[df["Date_Rank"].isin([3, 5, 7, 12, 15])].pivot(
    index="Fund",
    columns="Date_Rank",
    values="avg_nav"
)

for r in [3, 5, 7, 12, 15]:
    result[f"W1 vs W{r}"] = (
        (latest - result[r]) / result[r] * 100
    )

result = result[
    [f"W1 vs W{r}" for r in [3, 5, 7, 12, 15]]
].round(2).reset_index()

result.to_csv("mf_alert_app/output.csv", index=False)
