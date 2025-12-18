"""
Demo: Filter risky code and surface it for prioritization
"""

from datasets import load_dataset
from dataset_risk_decorator.core import (
    DatasetRiskDecorator,
    HeuristicCodeColumnDetector,
    DebertaRiskScorer,
)

# 1. Components
detector = HeuristicCodeColumnDetector()
scorer = DebertaRiskScorer("durinn/data-eval")

# 2. Risk decorator
risk_guard = DatasetRiskDecorator(
    detector=detector,
    scorer=scorer,
    threshold=0.5,              # policy knob
    filter_mode="none",          # annotate only
)

# 3. Dataset loader
@risk_guard
def load_data():
    return load_dataset("CyberNative/Code_Vulnerability_Security_DPO")

# 4. Run
ds = load_data()
train = ds["train"]

# 5. Split by risk
problematic = train.filter(lambda r: r["is_problematic"])
safe = train.filter(lambda r: not r["is_problematic"])

print("Total:", len(train))
print("Problematic:", len(problematic))
print("Safe:", len(safe))

# 6. Prioritize new data collection
top_risky = problematic.sort("risk_score", reverse=True).select(range(10))

for row in top_risky:
    print("---")
    print("risk_score:", row["risk_score"])
    print(row.get("output", "")[:200])
