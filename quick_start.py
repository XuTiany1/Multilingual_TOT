import argparse
from src.methods.bfs_tot import solve, naive_solve
from src.tasks.MGSM import MgsmTask
import re


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


task = MgsmTask(args)
ys, infos = solve(args, task, 1)