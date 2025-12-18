"""
Demo: Annotate code with risk scores and prioritize review
"""

from datasets import load_dataset
from dataset_risk_decorator.core import (
    DatasetRiskDecorator,
    DebertaRiskScorer,
)

# 1. Scorer (loaded once)
scorer = DebertaRiskScorer("durinn/data-eval")

# 2. Risk decorator
risk_guard = DatasetRiskDecorator(
    scorer=scorer,
    threshold=0.5,        # kept for metadata, not filtering
    filter_mode="none",   # always annotate
    max_rows=2000,        # speed knob
)

# 3. Dataset loader (decorated)
@risk_guard
def load_data():
    return load_dataset("CyberNative/Code_Vulnerability_Security_DPO")

# 4. Run annotation
ds = load_data()
train = ds["train"]

print("Total rows annotated:", len(train))

# 5. Inspect score distribution (THIS is the signal)
scores = train["risk_score"]
print("Min score:", min(scores))
print("Mean score:", sum(scores) / len(scores))
print("Max score:", max(scores))

# 6. Prioritize highest-risk samples (always works)
top_risky = train.sort("risk_score", reverse=True).select(range(10))

print("\nTop risky samples:")
for row in top_risky:
    print("---")
    print("risk_score:", row["risk_score"])
    print(row["chosen"][:200])
