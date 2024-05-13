from ocr_error_filtering.filter_transcript import update_csv_files

def test_update_csv_files():
    transcript_dir = "./tests/test_data/transcript"
    page_ids = ['I1KG155250419', 'I3CN46890016']
    save_error_transcript_path = "./tests/test_data/error_transcript.csv"
    page_id_to_batch = update_csv_files(transcript_dir, page_ids, save_error_transcript_path)
    expected_page_id_to_batch = {'I3CN46890016': ['batch_1'], 'I1KG155250419': ['batch_2']}
    assert page_id_to_batch == expected_page_id_to_batch


