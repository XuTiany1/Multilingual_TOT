import itertools
import re
import numpy as np
from functools import partial
from src.tasks.MGSM import MgsmTask
from src.models.gemma import *



##########################################################################
# EXTRACT thoughts from tot

def extract_thoughts(response):
    """
    Extracts only the generated thought process from Gemma's output.
    Filters out empty lines and unwanted generic responses.
    """

    # Remove "<start_of_turn>model" and special tokens
    response = response.replace("<start_of_turn>model\n", "").strip()

    # Remove any "<end_of_turn><eos>" if accidentally generated
    response = re.sub(r"<end_of_turn><eos>", "", response)

    thought_lines = []
    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("Mathematician "):  # Ensure it's a valid response
            thought_lines.append(line)

    return "\n".join(thought_lines).strip()  # Return only valid thoughts



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
    value = task.value_outputs_unwrap(value_outputs)
    
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
def get_proposals(task, x, y, num_generate_sample, language):
    """
    task - task object
    x - input
    y - current unfinished solution from last step

    this function should continue the solution
    """
    propose_prompt = task.propose_prompt_wrap(num_generate_sample, language, x, y)
    
    # Generate proposals using Gemma
    proposals = gemma_generate(prompt=propose_prompt, max_tokens=500)
    
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
# FORCE OUTPUT PROMPT
def get_answers(task, x, ys):
    """
    task - task object
    x - input
    y - current unfinished solution from last step

    this function should continue the solution
    """


    answers = []
    local_answer_cache = {}


    for y in ys:  # Iterate over each solution candidate

        if y in local_answer_cache:  # Avoid duplicate evaluation
            continue
        else:
            final_answer_prompt = task.force_output_prompt_wrap(x, y)
            answer = gemma_generate(prompt=final_answer_prompt, max_tokens=500)
            local_answer_cache[y] = answer
        answers.append(answer)
    
    return answers

def finalize_answer(task, x, ys):

    final_judgement_prompt = task.final_judgement_wrap(x, ys)
    answer = gemma_generate(prompt=final_judgement_prompt, max_tokens=100)

    return answer


##########################################################################
# SOLVE
def solve(args, task, idx, to_print=True):


    # Setup model

    # Setup environment
    x = task.get_input(idx) # input
    ys = ['']               # current output candidates
    infos = []

    for step in range (task.steps - 1):
        
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

            new_ys = []

            for y in ys:
                proposals = get_proposals(task, 
                                    x,
                                    y,
                                    args.n_generate_sample,
                                    args.lang)
            
                # Each new thought should build on the previous one
                for thought in proposals:
                    if thought.strip():  # Ignore empty lines
                        new_ys.append(y + "\n" + thought)
        
        new_ys = new_ys
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


    ######################
    # Force the final output
    final_answers = get_answers(task, x, ys)

    if to_print: 
        print(ys)
        print(f"final candidates: {final_answers}")
    
    model_output = finalize_answer(task, x, final_answers)

    return ys, {'steps': infos}, final_answers, model_output







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

    if args.prompt_sample == 'cot':
        match = re.search(r'The answer is (\d+)', ys)
        ys = int(match.group(1)) if match else None

    if to_print:
        print(f"Generated response: {ys}")

    return ys, {}



























































