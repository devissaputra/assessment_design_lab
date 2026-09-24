import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment_design_lab.core import analyze_assessment


matrix = [
    [1, 1, 1, 1],
    [1, 1, 1, 0],
    [1, 1, 0, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 0],
]

result = analyze_assessment(matrix)

print(f"Respondents: {result['respondent_count']}")
print(f"Items: {result['item_count']}")
print(
    "Cronbach alpha: "
    + (
        f"{result['cronbach_alpha']:.2f}"
        if result["cronbach_alpha"] is not None
        else "not estimable"
    )
)
print(f"Flagged items: {result['flagged_item_count']}")

for item in result["items"]:
    discrimination = (
        f"{item['discrimination']:.2f}"
        if item["discrimination"] is not None
        else "not estimable"
    )
    flags = ", ".join(item["review_flags"]) or "none"
    print(
        f"Item {item['item_index'] + 1}: "
        f"difficulty={item['difficulty']:.2f}, "
        f"discrimination={discrimination}, "
        f"flags={flags}"
    )
