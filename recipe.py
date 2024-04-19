"""
modified from https://gist.github.com/wesslen/940da012837dda5d125e35e6a97f82ec
"""
import prodigy
import re
from prodigy.components.loaders import JSONL

@prodigy.recipe(
    "textcat_feedback",
    dataset=("Dataset to save answers to", "positional", None, str),
    examples=("Examples to load from disk", "positional", None, str),
)
def textcat_topic(dataset, examples):
    # set up stream; may want get_stream() instead to hash/avoid dedup
    stream = JSONL(examples)
    # Render highlight of each sentence 
    def add_html(examples):
        for ex in examples:
            summary_highlight = f"<b style='background-color: cyan;'> Code = {ex['meta']['theme']} </b> \n "
            summary_highlight += f"<b style='background-color: yellow;'> Defendant = {ex['meta']['defendant']} </b> \n "
            summary_highlight += ex["paragraph"]
            summary_highlight = re.sub("<p score=(.*?)>", "<b>", summary_highlight)
            summary_highlight = summary_highlight.replace(
                "</p>", "</b>"
            )
            ex["html"] = f"{summary_highlight}"
            ex['options'] = [
                {"id": "accept", "text": "Accept"},
                {"id": "reject", "text": "Reject"},
                {"id": "unsure", "text": "Unsure"},
            ]   
            yield ex

    # delete html key in output data
    def before_db(examples):
        for ex in examples:
            del ex["html"]
            del ex["options"]
        return examples
    
    return {
        "before_db": before_db,
        "dataset": dataset,
        "stream": add_html(stream),
        "view_id": "blocks",
        "config": {
            "blocks": [
                {"view_id": "choice"},
                {
                    "view_id": "text_input", 
                    "field_id": "reasons", 
                    "field_placeholder": "Reasons for reject or unsure.",
                    "field_suggestions": [
                        "not on topic", 
                        "wrong valence", 
                        "wrong person", 
                        "need context", 
                        "crime facts"
                                        ]
                },
            ]
    }
    }