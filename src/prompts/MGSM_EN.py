USER_CHAT_TEMPLATE = "<start_of_turn>user\n{prompt}<end_of_turn><eos>\n"
MODEL_CHAT_TEMPLATE = "<start_of_turn>model\n"

# standard prompt
standard_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Answer the following mathematical question. Just input the final answer as a number and nothing else.\n"
) + "{question}\nAnswer: " + MODEL_CHAT_TEMPLATE





# cot prompt
cot_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Answer the following mathematical question. "
           "Think this through step by step and leave your thought process below. "
           "The last line should be of the form 'The answer is xxx' where xxx is a number.\n"
) + "Question: {question}\nStep-by-step Answer:\n" + MODEL_CHAT_TEMPLATE



# propose_prompt
propose_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Imagine that you are composed of {n} independent mathematicians speaking {lang}, "
           "each with a unique perspective on how to tackle a multi-step math problem.\n\n"
           "Before responding with your thought process, each mathematician should begin their response with "
           "'Mathematician i: ', where 'i' can be 1, 2, or 3.\n\n"
           "Based on the given question and the current thought process, each mathematician will independently "
           "generate one unique, creative, and valid next step toward solving the problem. "
           "Each step should differ in approach, leveraging different mathematical methods, problem breakdowns, "
           "or alternative representations.\n\n"
           "Each mathematician will explain their reasoning clearly and concisely before proposing their next step. "
           "They will only append their first step, allowing further discussion and refinement later.\n\n"
           "If no previous context exists, this marks the start of the thought process, and mathematicians will propose "
           "different ways to begin solving the problem.\n\n"
           "This process continues step by step until a definitive answer is reached.\n\n"
) + "---\n" \
    "Question: {question}\n\n" \
    "Context (previous thought process, if any):\n{current_thought_process}\n\n" \
    "List of potential future steps (each line represents the perspective of a single mathematician):\n" \
    + MODEL_CHAT_TEMPLATE



# value_prompt
value_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Evaluate whether the given reasoning step contributes meaningfully to solving the problem. "
           "Answer with just 'Evaluation: sure', 'Evaluation: likely', or 'Evaluation: impossible'. "
           "Do not include explanations or any additional text.\n\n"
           "Assign one of the following judgments:\n"
           "- sure: The step is correct and a logical progression toward the solution.\n"
           "- likely: The step is plausible but may need further refinement or is missing key details.\n"
           "- impossible: The step is incorrect, irrelevant, or contradicts known facts.\n\n"
           "---\n"
           "Question: A train departs from Station A with 50 passengers. At the next stop, 15 passengers get off, "
           "and 30 new passengers board. How many passengers are now on the train?\n\n"
           "Proposed Next Step: Compute the net change: -15 + 30.\nEvaluation: sure\n\n"
           "Proposed Next Step: Express the situation as an equation: 50 - 15 + 30 = x.\nEvaluation: sure\n\n"
           "Proposed Next Step: Assume that the train lost 20 passengers at the next stop and check if the total matches.\nEvaluation: impossible\n\n"
           "Proposed Next Step: Represent the relationship as a percentage: (50 - 15) / 50.\nEvaluation: impossible\n\n"
           "Proposed Next Step: Consider doubling the number of passengers at each stop.\nEvaluation: impossible\n\n"
           "Proposed Next Step: Reverse the reasoning by assuming the final count is x and working backward.\nEvaluation: sure\n\n"
           "---\n"
           "Question: There were nine computers in the server room. Five more computers were installed each day from Monday to Thursday. "
           "How many computers are now in the server room?\n\n"
           "Proposed Next Step: Compute the total computers added: 5 × 4.\nEvaluation: sure\n\n"
           "Proposed Next Step: Represent the change as an arithmetic sequence: 9 + (5 × n) where n is the number of days.\nEvaluation: sure\n\n"
           "Proposed Next Step: Consider that the computers were removed instead of added: 9 - (5 × 4).\nEvaluation: impossible\n\n"
           "Proposed Next Step: Convert the problem into a ratio: (9 / 5) × 4.\nEvaluation: impossible\n\n"
           "Proposed Next Step: Assume an exponential growth pattern instead of linear addition.\nEvaluation: impossible\n\n"
           "Proposed Next Step: Check if reversing the calculation still results in 9 initial computers.\nEvaluation: sure\n\n"
) + "---\n" \
    "{question}\n\n" \
    "Proposed Next Step: {curr_candidate}\n\n" \
    "Evaluation:" \
    + MODEL_CHAT_TEMPLATE


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






























































































