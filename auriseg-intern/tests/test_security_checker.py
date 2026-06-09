import json

from src.tools.security_checker import security_checker


TEST_CASES = {
    "Vulnerable Code": """
import os
import pickle

API_KEY = "sk-secret-key-123"
PASSWORD = "admin123"

username = input("Username: ")

query = "SELECT * FROM users WHERE name = '" + username + "'"

data = input("Enter data: ")
eval(data)

obj = pickle.loads(user_input)

os.system("rm -rf " + username)
"""
}


def run_verification_suite():
    print("=" * 60)
    print("RUNNING SECURITY CHECKER VERIFICATION SUITE")
    print("=" * 60 + "\\n")

    for case_name, code_snippet in TEST_CASES.items():
        print(f"Testing Category: [ {case_name} ]")
        print("-" * 50)

        tool_output = security_checker.invoke(
            {"code_chunk": code_snippet}
        )

        print(json.dumps(tool_output, indent=4))

        print("\\n" + "=" * 60 + "\\n")


if __name__ == "__main__":
    run_verification_suite()
