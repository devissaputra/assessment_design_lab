"""Reproduce the labeled worked example; this is not an empirical study."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from assessment_design_lab import core
outputs={'proportion correct': core.item_difficulty([1,1,0,0]), 'Cronbach alpha': core.cronbach_alpha([[1,1,0],[1,1,1],[0,0,0],[0,1,0]])}
result={'kind':'illustrative_calculation','note':'Tiny synthetic response examples; not a psychometric validation.','outputs':outputs}
(ROOT/'results/review_examples.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
