import pandas as pd
from config import *


def rank_order():
    df = pd.read_csv(CSV_FILE_NAME)
    total_public_scores = []
    for i in range(len(df)):
        curr_row = df.loc[i]
        curr_public_score = 0
        for challenge in PUBLIC_CHALLENGES:
            curr_public_score += curr_row[f"{challenge} - public"]
        curr_public_score += curr_row["Execution"]
        total_public_scores.append(curr_public_score)

    df['public'] = total_public_scores
    print(df)
    df.sort_values('public', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    public_challenges = list(map(lambda x: f"{x} - public", PUBLIC_CHALLENGES)) + ["team", "public"]
    print(public_challenges)
    public_challenges += ["Execution"]
    return df[:50][public_challenges]

# def create_csv():
#     df = pd.DataFrame([("hello", 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1)], columns=COLUMNS)
#     df.to_csv(CSV_FILE_NAME)


if __name__ == "__main__":
    print(rank_order())
