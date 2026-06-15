import pickle


def load_transaction():
    data = b"malicious_data"
    return pickle.loads(data)


def process_payment(amount):
    print(f"Processing payment: {amount}")


if __name__ == "__main__":
    process_payment(100)
