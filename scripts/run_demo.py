import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from assessment_design_lab.core import item_difficulty, item_discrimination, cronbach_alpha

print(f"Item difficulty: {item_difficulty([1,1,0,1]):.2f}")
print(f"Item discrimination: {item_discrimination([1,1,0,0],[4,3,2,1]):.2f}")
print(f"Cronbach alpha: {cronbach_alpha([[1,1,0],[1,1,1],[0,0,0],[0,1,0]]):.2f}")
