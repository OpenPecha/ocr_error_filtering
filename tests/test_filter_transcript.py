import pandas as pd

from ocr_error_filtering.filter_transcript import update_csv_files


def test_update_csv_files():
    transcript_dir = "tests/test_data/transcript"
    page_ids = ["I1KG155250419", "I3CN46890016"]
    save_error_transcript_path = "tests/test_data/error_transcript.csv"
    update_csv_files(transcript_dir, page_ids, save_error_transcript_path)
    # Check that the error data was saved correctly
    error_data = pd.read_csv(save_error_transcript_path)
    expected_error_data = pd.read_csv("tests/test_data/expected_error_transcript.csv")
    pd.testing.assert_frame_equal(error_data, expected_error_data)
