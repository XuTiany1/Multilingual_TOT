USER_CHAT_TEMPLATE = "<start_of_turn>user\n{prompt}<end_of_turn><eos>\n"
MODEL_CHAT_TEMPLATE = "<start_of_turn>model\n"

# standard prompt
standard_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Answer the following mathematical question. Just input the final answer as a number and nothing else.\n"
) + "{question}\nAnswer: " + MODEL_CHAT_TEMPLATE





# cot prompt
cot_prompt = '''
Answer the following mathematical question. 
Think this through step by step and leave your thought process below. 
The last line should be of the form "The answer is xxx" where xxx is a number. 
Question: {question}
Step-by-step Answer:
'''




# propose_prompt
propose_prompt = '''
Imagine that you are composed of {n} independent mathematicians speaking {lang}, each with a unique perspective on how to tackle a multi-step math problem.

Based on the given question and the current thought process, each mathematician will independently generate one unique, creative, and valid next step** toward solving the problem. Each step should differ in approach, leveraging different mathematical methods, problem breakdowns, or alternative representations.

Each mathematician will explain their reasoning clearly and concisely before proposing their next step. They will only append their first step, allowing further discussion and refinement later.

If no previous context exists, this marks the start of the thought process, and mathematicians will propose different ways to begin solving the problem.

This process continues step by step until a definitive answer is reached.

---
Question: {question}

Context (previous thought process, if any):  
{current_thought_process}

List of potential future steps (each line represents the perspective of a single mathematician):
'''



# value_prompt
value_prompt = '''
Evaluate whether the given reasoning step contributes meaningfully to solving the problem. Assign one of the following judgments:
- sure: The step is correct and a logical progression toward the solution.
- likely: The step is plausible but may need further refinement or is missing key details.
- impossible: The step is incorrect, irrelevant, or contradicts known facts.

---
Question: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?

Proposed Next Step: Compute the difference: 20 - 12.
Evaluation: sure

Proposed Next Step: Express the problem as an equation: 20 - x = 12.
Evaluation: sure

Proposed Next Step: Assume that Jason gave away 15 lollipops and verify by subtracting: 20 - 15 = 5.
Evaluation: impossible

Proposed Next Step: Represent the relationship as a fraction: 12 / 20.
Evaluation: impossible

Proposed Next Step: Consider that Jason's remaining lollipops should be doubled: 12 × 2.
Evaluation: impossible

Proposed Next Step: Reverse the reasoning by assuming the answer is x and checking if 12 + x = 20.
Evaluation: sure

---
Question: {question}

Proposed Next Step: {curr_candidate}

Evaluation:
'''


# value_last_step_prompt
value_last_step_prompt = '''
Evaluate whether the given reasoning chain and final answer correctly solve the problem. The answer must be mathematically valid, use correct logical steps, and reach the correct final result.

---
Question: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?

Step-by-Step Answer: Jason started with 20 lollipops. He now has 12 lollipops. The difference between the starting amount and the current amount is 20 - 12 = 8. The answer is 8.
Judgment: sure

Step-by-Step Answer: Jason started with 20 lollipops. He assumes that he gave away 10 lollipops, so 20 - 10 = 10. The answer is 10.
Judgment: impossible

Step-by-Step Answer: Jason had 20 lollipops. We assume the remaining lollipops were 5, so we calculate the difference: 20 - 5 = 15. The answer is 15.
Judgment: impossible

Step-by-Step Answer: Jason started with 20 lollipops. He gave away x lollipops, so we set up the equation 20 - x = 12. Solving for x, we get x = 8. The answer is 8.
Judgment: sure

---
Question: {question}

Step-by-Step Answer: {answer}

Judgment:
'''






























































































