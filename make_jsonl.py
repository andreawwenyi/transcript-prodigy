import pandas as pd
import jsonlines
import sys

theme = sys.argv[1]
df = pd.read_excel(f"{theme}_pred_true_paragraph.xlsx", sheet_name=None)

with jsonlines.open(f'{theme}_fp.jsonl', mode='w') as writer:
    for defendant in df.keys():
        sheet = df[defendant]
        fp_sheet = sheet[sheet[theme] == 0]
        for row in fp_sheet.to_dict(orient='records'):
            if row['mean_score'] < 0.9: 
                continue
            writer.write({
                "paragraph": row["paragraph"],
                "meta":{
                    "defendant": defendant,
                    "score": round(row["mean_score"], 3),
                    "theme": theme
                }
            })

