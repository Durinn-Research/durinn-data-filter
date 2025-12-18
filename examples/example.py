"""
Demo: Annotate code with risk scores and prioritize review
"""

from datasets import load_dataset
from dataset_risk_decorator.core import risk_guard

# Dataset loader (decorated with defaults + overrides)
@risk_guard(
    threshold=0.5,      # metadata only
    filter_mode="none", # always annotate
    max_rows=2000,      # speed knob
)
def load_data():
    return load_dataset("CyberNative/Code_Vulnerability_Security_DPO")

# Run annotation
ds = load_data()
train = ds["train"]

print("Total rows annotated:", len(train))

# Inspect score distribution (this is the signal)
scores = train["risk_score"]
print("Min score:", min(scores))
print("Mean score:", sum(scores) / len(scores))
print("Max score:", max(scores))

# Prioritize highest-risk samples
top_risky = train.sort("risk_score", reverse=True).select(range(10))

print("\nTop risky samples:")
for row in top_risky:
    print("---")
    print("risk_score:", row["risk_score"])
    print(row["chosen"][:200])
