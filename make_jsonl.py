import pandas as pd
import jsonlines

records = list()
for theme in ["Emotions", "Manipulative", "Cheating", "Parent"]:
    df = pd.read_excel(f"{theme}_pred_true_paragraph.xlsx", sheet_name=None)
    for defendant in df.keys():
        sheet = df[defendant]
        fp_sheet = sheet[sheet[theme] == 0]
        for row in fp_sheet.to_dict(orient='records'):
            if row['mean_score'] < 0.9: 
                continue
            records.append({
                    "paragraph_id": f"{defendant}-{row['value_grp']}",
                    "paragraph": row["paragraph"],
                        "defendant": defendant,
                        "score": round(row["mean_score"], 3),
                        "theme": theme
                })
            
with jsonlines.open(f'fp.jsonl', mode='w') as writer:
    for r in records:
        writer.write({
            "paragraph_id": r['paragraph_id'],
            "paragraph": r["paragraph"],
            "meta":{
                "defendant": r['defendant'],
                "score": r['score'],
                "theme": r['theme']
            }
        })

# stratified sampling
sampled = pd.DataFrame(records).groupby(['defendant', 'theme'], group_keys=False).apply(lambda x: x.sample(frac=0.2)).sort_values(["theme", "defendant"]).to_dict(orient='records')
with jsonlines.open(f'fp_andrea.jsonl', mode='w') as writer:
    for r in sampled:
        writer.write({
            "paragraph_id": r['paragraph_id'],
            "paragraph": r["paragraph"],
            "meta":{
                "defendant": r['defendant'],
                "score": r['score'],
                "theme": r['theme']
            }
        })


