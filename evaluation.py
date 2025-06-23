import dspy
import re

def normalize_balance(balance_str):
    """Removes currency symbols, commas, and whitespace from a balance string."""
    if balance_str is None:
        return ""
    return re.sub(r'[$,\s]', '', balance_str)

def exact_match_metric(example: dspy.Example, prediction: dspy.Prediction, trace=None) -> bool:
    """Checks if the extracted balance exactly matches the expected balance."""
    expected = normalize_balance(example.expected_balance)
    predicted = normalize_balance(prediction.balance)
    return expected == predicted

def numerical_proximity_metric(example: dspy.Example, prediction: dspy.Prediction, trace=None) -> float:
    """Measures how close the predicted balance is to the expected balance."""
    try:
        expected = float(normalize_balance(example.expected_balance))
        predicted = float(normalize_balance(prediction.balance))
        # Return a score between 0 and 1 based on proximity
        return max(0, 1 - min(1, abs(expected - predicted) / expected))
    except (ValueError, TypeError, ZeroDivisionError):
        return 0.0

def combined_metric(example: dspy.Example, prediction: dspy.Prediction, trace=None) -> float:
    """Combines multiple metrics with appropriate weights."""
    exact_score = 1.0 if exact_match_metric(example, prediction, trace) else 0.0
    proximity_score = numerical_proximity_metric(example, prediction, trace)
    
    # Weighted combination (prioritizing exact match)
    return 0.7 * exact_score + 0.3 * proximity_score

if __name__ == '__main__':
    # Example usage for testing the metrics
    sample_example = dspy.Example(expected_balance="$1,079.10")
    
    # Test case 1: Exact match
    prediction1 = dspy.Prediction(balance="$1,079.10")
    print(f"Exact match (test 1): {exact_match_metric(sample_example, prediction1)}")
    print(f"Proximity (test 1): {numerical_proximity_metric(sample_example, prediction1)}")
    print(f"Combined (test 1): {combined_metric(sample_example, prediction1)}")

    # Test case 2: Different formatting
    prediction2 = dspy.Prediction(balance="1079.10")
    print(f"Exact match (test 2): {exact_match_metric(sample_example, prediction2)}")
    print(f"Proximity (test 2): {numerical_proximity_metric(sample_example, prediction2)}")
    print(f"Combined (test 2): {combined_metric(sample_example, prediction2)}")

    # Test case 3: Incorrect value
    prediction3 = dspy.Prediction(balance="$1,079.11")
    print(f"Exact match (test 3): {exact_match_metric(sample_example, prediction3)}")
    print(f"Proximity (test 3): {numerical_proximity_metric(sample_example, prediction3)}")
    print(f"Combined (test 3): {combined_metric(sample_example, prediction3)}")
