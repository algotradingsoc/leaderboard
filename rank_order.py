import pandas as pd
from config import *
import math
import numpy as np

pd.options.display.max_columns = None
pd.options.display.max_rows = None


def rank_order():
    df = pd.read_csv(CSV_FILE_NAME)
    total_public_scores = []
    total_private_scores = []

    for challenge in PUBLIC_CHALLENGES:
        if challenge == "ESG" or challenge == "Data Cleaning":
            df[f"{challenge} - public"] = df[f"{challenge} - public"].apply(lambda x: np.round(x, 7))
            df[f"{challenge} - rank"] = df[f"{challenge} - public"].rank(ascending=True).apply(lambda x: int(x) if not np.isnan(x) else 50)
        else:
            df[f"{challenge} - public"] = df[f"{challenge} - public"].apply(lambda x: np.round(x, 7))
            df[f"{challenge} - rank"] = df[f"{challenge} - public"].rank(ascending=False).apply(lambda x: int(x) if not np.isnan(x) else 50)

        df[f"{challenge} - rank_score"] = df[f"{challenge} - rank"].apply(lambda x: np.round(math.log(x**2), 3) if x <= 50 else np.round(math.log(50**2), 3))

    df["Execution"] = df["Execution"].apply(lambda x: x)
    df["Execution - rank"] = df["Execution"].rank(ascending=True).apply(lambda x: int(x) if not np.isnan(x) else 50)
    df["Execution - rank_score"] = df["Execution - rank"].apply(lambda x: np.round(math.log(x**2), 3) if x <= 50 else np.round(math.log(50**2), 3))

    for challenge in PUBLIC_CHALLENGES:
        if challenge == "ESG" or challenge == "Data Cleaning":
            df[f"{challenge} - private"] = df[f"{challenge} - private"].apply(lambda x: np.round(x, 7))
            df[f"{challenge} - rank(private)"] = df[f"{challenge} - private"].rank(ascending=True).apply(lambda x: int(x) if not np.isnan(x) else 50)
        else:
            df[f"{challenge} - private"] = df[f"{challenge} - private"].apply(lambda x: np.round(x, 7))
            df[f"{challenge} - rank(private)"] = df[f"{challenge} - private"].rank(ascending=False).apply(lambda x: int(x) if not np.isnan(x) else 50)

        df[f"{challenge} - rank_score(private)"] = df[f"{challenge} - rank(private)"].apply(lambda x: np.round(math.log(x**2), 3) if x <= 50 else np.round(math.log(50**2), 3))

    df["Execution"] = df["Execution"].apply(lambda x: x)
    df["Execution - rank(private)"] = df["Execution"].rank(ascending=True).apply(lambda x: int(x) if not np.isnan(x) else 50)
    df["Execution - rank_score(private)"] = df["Execution - rank(private)"].apply(lambda x: np.round(math.log(x**2), 3) if x <= 50 else np.round(math.log(50**2), 3))

    for i in range(len(df)):
        curr_row = df.loc[i]
        total_rank_scores = 0
        for challenge in CHALLENGES:
            total_rank_scores += curr_row[f"{challenge} - rank_score"]
        total_rank_scores = np.round(total_rank_scores, 3)
        total_public_scores.append(total_rank_scores)

    df['public'] = total_public_scores

    for i in range(len(df)):
        curr_row = df.loc[i]
        total_rank_scores = 0
        for challenge in CHALLENGES:
            total_rank_scores += curr_row[f"{challenge} - rank_score(private)"]
        total_rank_scores = np.round(total_rank_scores, 3)
        total_private_scores.append(total_rank_scores)

    df['private'] = total_private_scores
    df.sort_values('private', ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df = df.replace(np.nan, -1)
    public_challenges = list(map(lambda x: f"{x} - public", PUBLIC_CHALLENGES))
    public_challenges += ["Execution", "team", "public", "private"]
    challenges_ranked = list(map(lambda x: f"{x} - rank", CHALLENGES))
    adjusted_ranked = list(map(lambda x: f"{x} - rank_score", CHALLENGES))
    private_challenges = list(map(lambda x: f"{x} - private", PUBLIC_CHALLENGES))
    private_challenges_ranked = list(map(lambda x: f"{x} - rank(private)", CHALLENGES))
    private_adjusted_ranked = list(map(lambda x: f"{x} - rank_score(private)", CHALLENGES))
    public_challenges += challenges_ranked + adjusted_ranked + private_challenges + private_challenges_ranked + private_adjusted_ranked
    return df[public_challenges]


# def create_csv():
#     df = pd.DataFrame([("hello", 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1)], columns=COLUMNS)
#     df.to_csv(CSV_FILE_NAME)


if __name__ == "__main__":
    print(rank_order())
