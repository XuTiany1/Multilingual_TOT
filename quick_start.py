import argparse
from src.methods.bfs_tot import solve, naive_solve
from src.tasks.MGSM import MgsmTask
import re

# languages = ['en', 'es', 'fr', 'de', 'ru', 'zh', 'ja', 'th', 'sw', 'bn', 'te']

args = argparse.Namespace( 
    task='MGSM', 
    lang='en',
    naive_run=False, 
    prompt_sample='cot', 
    method_generate='propose', 
    method_evaluate='value', 
    method_select='greedy', 
    n_generate_sample=1, 
    n_evaluate_sample=3, 
    n_select_sample=2)



idx = 1
task = MgsmTask(args)
ys, infos, final_answers, model_output = solve(args, task, idx)

ground_truth_answer = task.ground_truth_answer(idx)
model_answer = task.model_answer(model_output)

print(f"ground truth answer is {ground_truth_answer}")
print(f"model prediction is {model_output}")
correct_count = (model_answer == ground_truth_answer)
print(f"model is correct: {correct_count}")