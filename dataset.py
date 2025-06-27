import os

def get_dataset_path():
    """Download the dataset and return the path to the CSV file"""
    # Download latest version
    dataset_dir = kagglehub.dataset_download("wilomentena/lgbt-rights-worldwide")
    
    # Get the path to the CSV file
    csv_path = os.path.join(dataset_dir, "lgbtq_rights_by_country.csv")
    return csv_path

# Example usage
def main():
    path = get_dataset_path()
    print("Path to dataset file:", path)
    return path

if __name__ == "__main__":
    main()