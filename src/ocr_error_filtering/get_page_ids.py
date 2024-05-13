import pandas as pd

def extract_page_ids(file_path):
    """
    Load a CSV file and extract page IDs from a specified column containing file paths.

    Parameters:
    - file_path (str): Path to the CSV file.

    Returns:
    - list: A list of extracted page IDs.
    """
    # Load the CSV file using the provided path
    data = pd.read_csv(file_path, delimiter=',')

    # Extract page IDs from the 'file_path' column by splitting the string
    # Assumes the format is Windows path with backslashes and filename ending in '.json'
    data['page_id'] = data['file_path'].apply(lambda x: x.split('\\')[-1].split('.')[0])

    # Convert the page IDs to a list
    page_ids = data['page_id'].tolist()

    return page_ids
