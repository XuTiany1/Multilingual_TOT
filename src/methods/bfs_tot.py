import itertools
import numpy as np
from functools import partial
from src.tasks.MGSM import MgsmTask
from src.models.gemma import *




##########################################################################
# EVALUATIVE PROMPTS
def get_value(task, x, y, n_evaluate_sample, cache_value=True):
    """
    task - task object
    x - input
    y - current solution candidate
    n_evaluate_sample - number of evaluations for y
    cache_value - boolean to store value
    """
    value_prompt = task.value_prompt_wrap(x, y)
    
    # Cache check
    if cache_value and value_prompt in task.value_cache:
        return task.value_cache[value_prompt]
    
    # Generate evaluation response using Gemma
    value_outputs = gemma_generate(prompt=value_prompt, max_tokens=50)
    value = task.value_outputs_unwrap(x, y, value_outputs)
    
    # Cache result
    if cache_value:
        task.value_cache[value_prompt] = value

    return value


def get_values(task, x, ys, n_evaluate_sample, cache_value=True):
    """
    task - task object
    x - input
    ys - all solution candidates
    n_evaluate_sample - number of evaluations to be generated
    cahce_value - boolean to store value
    
    """
    values = []
    local_value_cache = {}

    for y in ys:  # Iterate over each solution candidate
        if y in local_value_cache:  # Avoid duplicate evaluation
            value = 0
        else:
            value = get_value(task, x, y, n_evaluate_sample, cache_value=cache_value)
            local_value_cache[y] = value
        values.append(value)
    
    return values


def get_votes(task, x, ys, n_evaluate_sample):
    """
    task - task object
    x - input
    ys - all solution candidates
    n_evaluate_sample - number of evaluations to be generated
    
    """


##########################################################################
# GENERATIVE PROMPTS
def get_proposals(task, x, y):
    """
    task - task object
    x - input
    y - current unfinished solution from last step

    this function should continue the solution
    """
    propose_prompt = task.propose_prompt_wrap(x, y)
    
    # Generate proposals using Gemma
    proposals = gemma_generate(prompt=propose_prompt, max_tokens=100)
    
    # Split into multiple steps if necessary
    proposals = proposals.split("\n")

    return [y + _ + '\n' for _ in proposals]


def get_samples(task, x, y, n_generate_sample, prompt_sample, stop):
    """
    task - task object
    x - input
    y - current unfinished solution 
    n_generate_sample - number of samples to be generated
    prompt_sample 
    stop - stopping condition 
    """

    if prompt_sample == 'standard':
        prompt = task.standard_prompt_wrap(x)
    elif prompt_sample == 'cot':
        prompt = task.cot_prompt_wrap(x)
    else:
        raise ValueError(f'prompt_sample {prompt_sample} not recognized')

    # Generate samples using Gemma
    answer = gemma_generate(prompt=prompt, max_tokens=500)

    return answer



##########################################################################
# SOLVE
def solve(args, task, idx, to_print=True):


    # Setup model

    # Setup environment
    x = task.get_input(idx) # input
    ys = ['']               # current output candidates
    infos = []

    for step in range (task.steps):
        
        ############################
        # Generation Step
        # standard or CoT
        if args.method_generate == 'sample':
            # prompt_sample = either 'standard or cot'
            new_ys = [get_samples(task, 
                                  x, 
                                  y, 
                                  args.n_generate_sample, 
                                  prompt_sample=args.prompt_sample, 
                                  stop=task.stops[step]) for y in ys]
        # ToT
        elif args.method_generate == 'propose':
            new_ys = [get_proposals(task, x, y) for y in ys]
        
        new_ys = list(itertools.chain(*new_ys))
        ids = list(range(len(new_ys)))


        ############################
        # Evaluation Step
        if args.method_evaluate == 'vote':
            values = get_votes(task, x, new_ys, args.n_evaluate_sample)
        elif args.method_evaluate == 'value':
            values = get_values(task, x, new_ys, args.n_evaluate_sample)
        elif args.method_evaluate == 'bypass':
            continue


        ############################
        # Selection Step
        # Sample top k by probability
        if args.method_select == 'sample':
            probabilities = np.array(values)/sum(values)
            selected_ids = np.random.choice(ids, size=args.n_select_sample, p=probabilities).tolist()

        # Sample top k by greedy
        elif args.method_select == 'greedy':
            select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:args.n_select_sample]
        
        elif args.method_select == 'bypass':
            continue
        

        select_new_ys = [new_ys[select_id] for select_id in select_ids]


    
        

        ############################
        # Logging Step
        if to_print: 
            sorted_new_ys, sorted_values = zip(*sorted(zip(new_ys, values), key=lambda x: x[1], reverse=True))
            print(f'-- new_ys --: {sorted_new_ys}\n-- sol values --: {sorted_values}\n-- choices --: {select_new_ys}\n')
        
        infos.append({'step': step, 'x': x, 'ys': ys, 'new_ys': new_ys, 'values': values, 'select_new_ys': select_new_ys})
        ys = select_new_ys



    if to_print: 
        print(ys)

    return ys, {'steps': infos}







def naive_solve(args, task, idx, to_print=True):
    """
    A simple solver using Gemma to generate responses.

    Args:
        args - argument object containing method configurations
        task - the problem-solving task instance
        idx - index of the input in the dataset
        to_print - whether to print the results

    Returns:
        Generated response and metadata
    """
    # Get the input for the given index
    x = task.get_input(idx)

    # Generate samples using Gemma
    ys = get_samples(task, x, '', args.n_generate_sample, args.prompt_sample, stop=None)

    if to_print:
        print(f"Generated response: {ys}")

    return ys, {}



























































