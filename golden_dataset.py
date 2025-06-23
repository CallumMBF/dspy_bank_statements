import dspy
import pandas as pd
def get_golden_dataset():
    # This is a sample of the bank statement provided by the user.
    # In a real-world scenario, this would be loaded from a file.
    bank_statement = pd.read_table("test.txt", sep = "|")
    print(bank_statement)
    bs = """
| 0 | 1  | 2   | 3     | 4 | 5 | 6 | 7                                            | 8      | 9   | 10 | 11 | 12 | 13                 | 14 | 15 | 16        | 17 | 18  | 19 |
|---+----+-----+-------+---+---+---+----------------------------------------------+--------+-----+----+----+----+--------------------+----+----+-----------+----+-----+----|
|   | 29 | Oct |       |   |   |   | BP Classified Hertfordshire GBRCard          |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | xx7831 AUD 1.00                              |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Value Date: 26/10/2021                       | 1.00   |     |    |    |    |                    |    |    | $1,079.10 |    | CR  |    |
|   | 29 | Oct |       |   |   |   | WORLDREMIT LTD LONDON W14 8U GB GBR          |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Card xx7831 AUD 294.34                       |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Value Date: 26/10/2021                       | 294.34 |     |    |    |    |                    |    |    | $784.76   |    | CR  |    |
|   | 30 | Oct |       |   |   |   | COTTON ON BRISBANE CBD BRISBANE QL AUS       |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Card xx7831                                  |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Value Date: 28/10/2021                       | 116.80 |     |    |    |    |                    |    |    | $667.96   |    | CR  |    |
|   | 30 | Oct |       |   |   |   | Transfer to CBA A/c CommBank app             |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Bill                                         | 100.00 |     |    |    |    |                    |    |    | $567.96   |    | CR  |    |
|   | 30 | Oct |       |   |   |   | TAP AND PAY FEES NetBank BPAY 333138         |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | 438225770 CommBank PayTag order              | 2.99   |     |    |    |    |                    |    |    | $564.97   |    | CR  |    |
|   | 30 | Oct |       |   |   |   | Direct Credit 128594 martin                  |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | payment                                      |        |     |    |    |    | 1,200.00           |    |    | $1,764.97 |    | CR  |    |
|   | 31 | Oct |       |   |   |   | BP Classified Hertfordshire GBR              |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Card xx7831 AUD 1.00                         |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Value Date: 28/10/2021                       | 1.00   |     |    |    |    |                    |    |    | $1,763.97 |    | CR  |    |
|   | 31 | Oct |       |   |   |   | OPTUS PRE PAID MELBOURNE VI AUS              |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Card xx7831                                  |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Value Date: 29/10/2021                       | 130.00 |     |    |    |    |                    |    |    | $1,633.97 |    | CR  |    |
|   | 31 | Oct |       |   |   |   | Direct Credit 037819 MR PETER STARK          |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | PETER                                        |        |     |    |    |    | 250.00             |    |    | $1,883.97 |    | CR  |    |
|   | 01 | Nov |       |   |   |   | Debit Excess Interest                        | 1.86   |     |    |    |    |                    |    |    | $1,882.11 |    | CR  |    |
|   | 01 |     | NovBP |   |   |   | Classified Hertfordshire GBR                 |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Card xx7831 AUD 1.00                         |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Value Date: 29/10/2021                       | 1.00   |     |    |    |    |                    |    |    | $1,881.11 |    | CR  |    |
|   |    |     |       |   |   |   |                                              | 02     | Nov |    |    |    | Transfer to xx8459 |    |    | CommBank  |    | app |    |
|   |    |     |       |   |   |   | Savings                                      |        |     |    |    |    |                    |    |    | $1,681.11 |    | CR  |    |
|   | 03 | Nov |       |   |   |   | Cash Dep Branch F'titude Valley              |        |     |    |    |    | 4,700.00           |    |    | $6,381.11 |    | CR  |    |
|   | 03 | Nov |       |   |   |   | Transfer to other Bank CommBank app          |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Gift                                         | 300.00 |     |    |    |    |                    |    |    | $6,081.11 |    | CR  |    |
|   | 03 | Nov |       |   |   |   | TG CNR PHARMACY BRISBANE AU                  | 234.95 |     |    |    |    |                    |    |    | $5,846.16 |    | CR  |    |
|   | 03 | Nov |       |   |   |   | TG CNR PHARMACY BRISBANE AU                  | 80.00  |     |    |    |    |                    |    |    | $5,766.16 |    | CR  |    |
|   | 04 | Nov |       |   |   |   | WORLDREMIT LTD LONDON W14 8U GB GBR          |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Card xx7831 AUD 84.30                        |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Value Date: 31/10/2021                       | 84.30  |     |    |    |    |                    |    |    | $5,681.86 |    | CR  |    |
|   | 04 | Nov |       |   |   |   | WORLDREMIT LTD LONDON W14 8U GB GBR          |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Card xx7831 AUD 267.70                       |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Value Date: 31/10/2021                       | 267.70 |     |    |    |    |                    |    |    | $5,414.16 |    | CR  |    |
|   | 04 | Nov |       |   |   |   | OPTUS BILLING PAY MY B MACQUARIE PAR NS      |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Card xx7831                                  |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Value Date: 30/10/2021                       | 440.36 |     |    |    |    |                    |    |    | $4,973.80 |    | CR  |    |
|   |    |     |       |   |   |   | 04 Nov Direct Credit 141000 MATTHEW PATRIC O |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Bris physio                                  |        |     |    |    |    | 300.00             |    |    | $5,273.80 |    | CR  |    |
|   | 05 | Nov |       |   |   |   | BP Classified Hertfordshire GBR              |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Card xx7831 AUD 5.00                         |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Value Date: 02/11/2021                       | 5.00   |     |    |    |    |                    |    |    | $5,268.80 |    | CR  |    |
|   |    |     |       |   |   |   | WORLDREMIT LTD LONDON W114 8U GB GBRCard     |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | xx7831 AUD 633.82                            |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Value Date: 02/11/2021                       | 633.82 |     |    |    |    |                    |    |    | $4,634.98 |    | CR  |    |
|   | 05 | Nov |       |   |   |   | BP Classified Hertfordshire GBR              |        |     |    |    |    |                    |    |    |           |    |     |    |
|   |    |     |       |   |   |   | Card xx7831 AUD 5.00                         |        |     |    |    |    |                    |    |    |           |    |     |    |
"""
    
    golden_dataset = [
        dspy.Example(bank_statement=bank_statement, target_date="29 Oct", expected_balance="$784.76").with_inputs("bank_statement", "target_date"),
        dspy.Example(bank_statement=bank_statement, target_date="30 Oct", expected_balance="$1,764.97").with_inputs("bank_statement", "target_date"),
        dspy.Example(bank_statement=bank_statement, target_date="31 Oct", expected_balance="$1,883.97").with_inputs("bank_statement", "target_date"),
        dspy.Example(bank_statement=bank_statement, target_date="01 Nov", expected_balance="$1,881.11").with_inputs("bank_statement", "target_date"),
        dspy.Example(bank_statement=bank_statement, target_date="02 Nov", expected_balance="$1,681.11").with_inputs("bank_statement", "target_date"),
        dspy.Example(bank_statement=bank_statement, target_date="03 Nov", expected_balance="$5,766.16").with_inputs("bank_statement", "target_date"),
        dspy.Example(bank_statement=bank_statement, target_date="04 Nov", expected_balance="$5,273.80").with_inputs("bank_statement", "target_date"),
        dspy.Example(bank_statement=bank_statement, target_date="05 Nov", expected_balance="$4,634.98").with_inputs("bank_statement", "target_date"),
    ]
    
    return golden_dataset

if __name__ == '__main__':
    dataset = get_golden_dataset()
    print(f"Loaded {len(dataset)} examples into the golden dataset.")
    print("First example:")
    print(dataset[0])
