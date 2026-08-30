from querypilot.dataset import create_dataset


if __name__ == "__main__":
    path = create_dataset("data/querypilot.db")
    print(f"Created {path}")
