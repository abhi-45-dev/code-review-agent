import json

from src.tools.quality_checker import quality_checker


TEST_CASES = {
    "Messy Code": """
def f(x):
    if x > 5:
        return 42
    return 0
""",

    "Clean Code": """
def calculate_discount(price: float, discount_percentage: float) -> float:
    \"\"\"Calculate discounted price.\"\"\"

    return price * (1 - discount_percentage / 100)
"""
}


def run_verification_suite():
    print("=" * 60)
    print("RUNNING QUALITY CHECKER VERIFICATION SUITE")
    print("=" * 60 + "\\n")

    for case_name, code_snippet in TEST_CASES.items():
        print(f"Testing Category: [ {case_name} ]")
        print("-" * 50)

        tool_output = quality_checker.invoke(
            {"code_chunk": code_snippet}
        )

        print(json.dumps(tool_output, indent=4))

        print("\\n" + "=" * 60 + "\\n")


if __name__ == "__main__":
    run_verification_suite()
