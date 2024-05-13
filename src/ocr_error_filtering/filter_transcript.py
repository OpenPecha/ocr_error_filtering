import os
from typing import Dict, List

import pandas as pd


def save_error_data_to_csv(error_data, save_error_transcript_path):
    """
    Saves error data to a specified CSV file path.

    Parameters:
    - error_data (DataFrame): Data to be saved that includes errors.
    - save_error_transcript_path (str): Path where the error data will be saved.
    """
    if not error_data.empty:
        # Append data if file exists, otherwise create and write headers
        error_data.to_csv(
            save_error_transcript_path,
            mode="a",
            header=not os.path.exists(save_error_transcript_path),
            index=False,
        )


def update_csv_files(transcript_dir, page_ids, save_error_transcript_path):
    """
    Update CSV files to remove entries based on page IDs and log errors in a separate CSV.

    Parameters:
    - transcript_dir (str): Directory path to the transcript CSV files (locally).
    - page_ids (list): List of page IDs to filter out.
    - save_error_transcript_path (str): Path where the error data will be saved.

    Returns:
    - dict: Mapping of page IDs to their corresponding batch folders.
    """
    page_id_to_batch: Dict[str, List[str]] = {}

    # Iterate over each CSV file in the local directory
    for batch_csv_file in os.listdir(transcript_dir):
        csv_path = os.path.join(transcript_dir, batch_csv_file)
        csv_data = pd.read_csv(csv_path)

        # Update mapping and filter out the data
        for idx, row in csv_data.iterrows():
            page_id = row["line_image_id"].split("_")[0]
            if page_id in page_ids:
                if page_id not in page_id_to_batch:
                    page_id_to_batch[page_id] = []
                page_id_to_batch[page_id].append(batch_csv_file.replace(".csv", ""))

        # Identify and save error data
        error_data = csv_data[
            csv_data["line_image_id"].apply(lambda x: x.split("_")[0] in page_ids)
        ]
        save_error_data_to_csv(error_data, save_error_transcript_path)

        # Filter out rows where the page_id is in the list and save
        filtered_data = csv_data[
            ~csv_data["line_image_id"].apply(lambda x: x.split("_")[0] in page_ids)
        ]
        filtered_data.to_csv(csv_path, index=False)

    # Remove duplicates from the mapping
    for key, value in page_id_to_batch.items():
        page_id_to_batch[key] = list(set(value))

    return page_id_to_batch
