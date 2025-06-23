import dspy
import os
from golden_dataset import get_golden_dataset

gemini_api_key = os.getenv('GEMINI_API_KEY')

# --- 1. LM Configuration ---
# Configure the language model
lm = dspy.LM('gemini/gemini-2.5-flash', api_key=gemini_api_key, temperature=1, max_tokens=10000)
dspy.configure(lm=lm)

# --- 2. Signature Definition ---
class BalanceExtractionSignature(dspy.Signature):
    """
    Extract the balance for a specific date from a bank statement.
    If there are multiple transactions on the same date, the balance to extract is the final balance of that date.
    Logically this is the bottom most balance in the vertical structure for that date.
    """
    bank_statement = dspy.InputField(desc="The bank statement in markdown format")
    target_date = dspy.InputField(desc="The date to find the balance for (format: DD MMM)")
    balance = dspy.OutputField(desc="The account balance on the target date")
    reasoning = dspy.OutputField(desc="Step-by-step reasoning for how the balance was determined")

# --- 3. Core Program ---
class BankStatementBalanceExtractor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.extract_balance = dspy.ChainOfThought(BalanceExtractionSignature)
        
    def forward(self, bank_statement, target_date):
        result = self.extract_balance(bank_statement=bank_statement, target_date=target_date)
        return result

if __name__ == '__main__':
    # This section is for basic validation and demonstration if the script is run directly.
    print("--- Bank Statement Balance Extractor ---")

    # Instantiate the extractor
    extractor = BankStatementBalanceExtractor()
    print("BankStatementBalanceExtractor instantiated successfully.")

    target_date = "02 Nov"

    # In a real scenario, this would make an LLM call
    # prediction = extractor(bank_statement=sample_statement, target_date=target_date)
    prediction = extractor(bank_statement=get_golden_dataset(), target_date=target_date)
    print(f"Prediction for {target_date}:")
    print(f"  Balance: {prediction.balance}")
    print(f"  Reasoning: {prediction.reasoning}")

    print("\nScript structure is valid.")
