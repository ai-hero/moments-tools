from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import pandas as pd


HF_MODEL = "danielv835/PF_Coach"

model = AutoModelForCausalLM.from_pretrained(HF_MODEL)

# this line needed for now, probably a config issue.
tokenizer = AutoTokenizer.from_pretrained(HF_MODEL)
df = pd.read_csv("../from-personal_finance.csv", nrows=99)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# This is currently taking 30s per answer
for idx, conv in df.head(1).itertuples():
    print(f"Input:\n{conv}")
    print(f"Generated:\n{generator(conv, max_new_tokens=150)}\n" + ("#" * 80))
