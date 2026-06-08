import json

from src.tools.bug_detector import bug_detector


TEST_CASES = {
    "Null Pointer / NoneType Dereference": """
def get_user_length(user_profile):
    name = user_profile.get("name")
    return len(name)

user = None
print(get_user_length(user))
""",

    "Off-by-One Error (Loop & Indexing)": """
def calculate_average(scores):
    total = 0
    for i in range(0, len(scores) + 1):
        total += scores[i]
    return total / len(scores)
""",

    "Unhandled Exception": """
import json

def parse_config_file(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data
""",

    "Logic Error": """
def check_admission(age, paid_fee):
    if age >= 18 or paid_fee == True:
        return "Allowed"
    return "Denied"
""",

    "Mixed Errors (Null Pointer + Unhandled Exception)": """
import requests

def fetch_and_parse_api(url):
    response = requests.get(url)
    data = response.json()
    return data["items"][0]
"""
}


def run_verification_suite():
    print("=" * 60)
    print("RUNNING BUG DETECTOR TOOL VERIFICATION SUITE")
    print("=" * 60 + "\n")

    for case_name, code_snippet in TEST_CASES.items():
        print(f"Testing Category: [ {case_name} ]")
        print("-" * 50)

        tool_output = bug_detector.invoke(
            {"code_chunk": code_snippet}
        )

        print(json.dumps(tool_output, indent=4))

        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    run_verification_suite()
