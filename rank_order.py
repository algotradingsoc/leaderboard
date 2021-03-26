import pandas as pd
from config import *
import math

pd.options.display.max_columns = None
pd.options.display.max_rows = None


def rank_order():
    df = pd.read_csv(CSV_FILE_NAME)
    total_public_scores = []

    for challenge in PUBLIC_CHALLENGES:
        if challenge == "ESG" or challenge == "Data Cleaning":
            df[f"{challenge} - rank"] = df[f"{challenge} - public"].rank(ascending=True).apply(lambda x: round(x))
        else:
            df[f"{challenge} - rank"] = df[f"{challenge} - public"].rank(ascending=False).apply(lambda x: round(x))

        df[f"{challenge} - rank_score"] = df[f"{challenge} - rank"].apply(lambda x: math.log(x**2))

    df["Execution - rank"] = df["Execution"].rank().apply(lambda x: round(x))
    df["Execution - rank_score"] = df["Execution - rank"].apply(lambda x: math.log(x**2))

    for i in range(len(df)):
        curr_row = df.loc[i]
        total_rank_scores = 0
        for challenge in CHALLENGES:
            total_rank_scores += curr_row[f"{challenge} - rank_score"]
        total_rank_scores = round(total_rank_scores, 2)
        total_public_scores.append(total_rank_scores)

    df['public'] = total_public_scores
    df.sort_values('public', ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)
    public_challenges = list(map(lambda x: f"{x} - public", PUBLIC_CHALLENGES))
    public_challenges += ["Execution", "team", "public"]
    challenges_ranked = list(map(lambda x: f"{x} - rank", CHALLENGES))
    public_challenges += challenges_ranked
    return df[:50][public_challenges]


# def create_csv():
#     df = pd.DataFrame([("hello", 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1)], columns=COLUMNS)
#     df.to_csv(CSV_FILE_NAME)


if __name__ == "__main__":
    print(rank_order())
