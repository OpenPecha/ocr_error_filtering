from ocr_error_handling.get_page_ids import extract_page_ids
from ocr_error_handling.filter_transcript import update_csv_files
from ocr_error_handling.filter_image import setup_s3_client, copy_images_within_s3

if __name__ == "__main__":
    issue_file_path = "./data/google-ocr-issues.csv"
    page_ids = extract_page_ids(issue_file_path)
    save_error_transcript_path = "./data/error_transcript.csv"
    page_id_to_batch = update_csv_files("./data/transcript/", page_ids, save_error_transcript_path)

    s3_client = setup_s3_client()
    bucket_name = 'monlam.ai.ocr'
    source_prefix = 'norbuketaka/images/'
    destination_prefix = 'norbuketaka/error_images/images/'
    copy_images_within_s3(s3_client, bucket_name, source_prefix, destination_prefix, page_id_to_batch)