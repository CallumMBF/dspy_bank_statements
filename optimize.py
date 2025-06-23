import dspy
from dspy.teleprompt import MIPROv2, BootstrapFewShot
from dspy.evaluate import Evaluate

from balance_extractor import BankStatementBalanceExtractor
from golden_dataset import get_golden_dataset
from evaluation import combined_metric, exact_match_metric
import os
import sys
import io

# Configure the language model
# gemini_api_key = os.getenv('GEMINI_API_KEY')
# lm = dspy.LM('gemini/gemini-2.5-flash', api_key=gemini_api_key, temperature=1, max_tokens=10000)
lm = dspy.LM('azure/gpt-4o-mini-global', api_key = os.getenv('AZURE_OPENAI_API_KEY'), api_base=os.getenv('AZURE_API_BASE'), api_version='2024-12-01-preview')
dspy.configure(lm=lm)

def main():
    # 1. Load the dataset
    dataset = get_golden_dataset()
    trainset = dataset[:5]  # Using a smaller subset for training
    devset = dataset[5:]    # Using the rest for development/validation

    # 2. Instantiate the program
    extractor = BankStatementBalanceExtractor()

    # 3. Set up the evaluator
    evaluator = Evaluate(
        devset=devset,
        metric=combined_metric,
        num_threads=1,
        display_progress=True,
        display_table=5
    )

    # 4. Evaluate the un-optimized program
    print("--- Evaluating Un-optimized Program ---")
    evaluator(extractor)

    # Save the un-optimized prompt
    print("\n--- Saving Un-optimized Prompt ---")
    os.makedirs("saved_prompts", exist_ok=True)
    # Capture the output of inspect_history
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    with dspy.settings.context(lm=lm):
        dspy.inspect_history(n=1)
    sys.stdout = old_stdout
    
    with open("saved_prompts/unoptimized_prompt.txt", "w") as f:
        f.write(captured_output.getvalue())
    print("Un-optimized prompt saved to saved_prompts/unoptimized_prompt.txt")


    # 5. Set up the optimizer (MIPROv2)
    optimizer_mipro = MIPROv2(
        metric=combined_metric,
        auto="medium",
        num_threads=1
    )

    print("\n--- Optimizing with MIPROv2 ---")
    optimized_extractor_mipro = optimizer_mipro.compile(
        extractor,
        trainset=trainset,
        max_bootstrapped_demos=2,
        max_labeled_demos=1,
        requires_permission_to_run=False
    )

    # 6. Evaluate the MIPROv2-optimized program
    print("\n--- Evaluating MIPROv2-Optimized Program ---")
    evaluator(optimized_extractor_mipro)

    # Save the MIPROv2-optimized model and prompt
    os.makedirs("optimized_models", exist_ok=True)
    optimized_extractor_mipro.save("optimized_models/mipro_extractor.json")
    print("\n--- Saving MIPROv2-Optimized Prompt ---")
    # Capture the output of inspect_history
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    with dspy.settings.context(lm=lm):
        dspy.inspect_history(n=1)
    sys.stdout = old_stdout

    with open("saved_prompts/mipro_optimized_prompt.txt", "w") as f:
        f.write(captured_output.getvalue())
    print("MIPROv2-optimized prompt saved to saved_prompts/mipro_optimized_prompt.txt")


    # 7. Set up another optimizer (BootstrapFewShot)
    optimizer_bootstrap = BootstrapFewShot(
        metric=combined_metric,
        max_bootstrapped_demos=2,
        max_labeled_demos=1
    )

    print("\n--- Optimizing with BootstrapFewShot ---")
    optimized_extractor_bootstrap = optimizer_bootstrap.compile(
        extractor,
        trainset=trainset
    )

    # 8. Evaluate the BootstrapFewShot-optimized program
    print("\n--- Evaluating BootstrapFewShot-Optimized Program ---")
    evaluator(optimized_extractor_bootstrap)

    # Save the BootstrapFewShot-optimized model and prompt
    optimized_extractor_bootstrap.save("optimized_models/bootstrap_extractor.json")
    print("\n--- Saving BootstrapFewShot-Optimized Prompt ---")
    # Capture the output of inspect_history
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    with dspy.settings.context(lm=lm):
        dspy.inspect_history(n=1)
    sys.stdout = old_stdout

    with open("saved_prompts/bootstrap_optimized_prompt.txt", "w") as f:
        f.write(captured_output.getvalue())
    print("BootstrapFewShot-optimized prompt saved to saved_prompts/bootstrap_optimized_prompt.txt")


if __name__ == '__main__':
    main()
