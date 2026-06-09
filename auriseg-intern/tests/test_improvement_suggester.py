import json

from src.tools.improvement_suggester import improvement_suggester


TEST_CASES = {
    "List Comprehension Opportunity": """
result = []
for x in nums:
    result.append(x * 2)
""",

    "Context Manager Opportunity": """
file = open("data.txt")
content = file.read()
file.close()
""",

    "Missing Type Hints": """
def calculate_total(price, tax):
    return price + tax
""",

    "Long Conditional Chain": """
if role == "admin":
    access = True
elif role == "manager":
    access = True
elif role == "staff":
    access = True
else:
    access = False
""",

    "Class Modernization": """
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
"""
}


def run_verification_suite():
    print("=" * 60)
    print("RUNNING IMPROVEMENT SUGGESTER VERIFICATION SUITE")
    print("=" * 60 + "\\n")

    for case_name, code_snippet in TEST_CASES.items():
        print(f"Testing Category: [ {case_name} ]")
        print("-" * 50)

        tool_output = improvement_suggester.invoke(
            {"code_chunk": code_snippet}
        )

        print(json.dumps(tool_output, indent=4))

        print("\\n" + "=" * 60 + "\\n")


if __name__ == "__main__":
    run_verification_suite()
