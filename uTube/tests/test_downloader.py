import pytest
from uTube.utils import is_youtube_link

# Parametrized test cases for happy path, edge cases, and error cases


@pytest.mark.parametrize("link, expected_result, test_id", [
    # Happy path tests
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", True, "happy_standard"),
    ("http://www.youtube.com/watch?v=dQw4w9WgXcQ", True, "happy_http"),
    ("https://youtube.com/watch?v=dQw4w9WgXcQ", True, "happy_no_www"),
    ("https://youtu.be/dQw4w9WgXcQ", True, "happy_short"),
    ("www.youtube.com/watch?v=dQw4w9WgXcQ", True, "happy_no_protocol"),
    ("youtube.com/watch?v=dQw4w9WgXcQ", True, "happy_no_protocol_www"),
    ("youtu.be/dQw4w9WgXcQ", True, "happy_short_no_protocol"),
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=100s",
     True, "happy_starts_at_100s"),
    ("https://www.youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj",
     True, "happy_playlist"),

    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", True, "video_id_standard"),
    ("https://youtu.be/dQw4w9WgXcQ", True, "video_id_short"),
    ("https://www.youtube.com/watch?list=PLA7no0L9zTk4Qp6LlDjFVCetW-sFw9r5I",
     True, "playlist_standard"),
    ("https://www.youtube.com/playlist?list=PLA7no0L9zTk4Qp6LlDjFVCetW-sFw9r5I",
     True, "playlist_full"),
    ("http://www.youtube.com/watch?v=dQw4w9WgXcQ", True, "video_id_http"),
    ("www.youtube.com/watch?v=dQw4w9WgXcQ", True, "video_id_no_protocol"),
    ("youtube.com/watch?v=dQw4w9WgXcQ", True, "video_id_no_subdomain"),
    ("https://www.youtube.com/embed/dQw4w9WgXcQ", True, "video_embed_standard"),
    ("https://www.youtube.com/v/dQw4w9WgXcQ", True, "video_v_standard"),

    # Edge cases
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtu.be",
     True, "edge_with_params"),
    ("", False, "edge_empty_string"),
    ("https://www.youtube.com/watch?v=", False, "edge_no_video_id"),
    ("https://www.youtu.be/", False, "edge_short_no_video_id"),
    ("https://www.youtube.com/watch?", False, "edge_no_query_string"),

    ("", False, "empty_string"),
    ("https://www.youtube.com/watch?v=", False, "video_id_empty"),
    ("https://www.youtube.com/playlist?list=", False, "playlist_id_empty"),
    ("https://www.youtu.be/", False, "short_domain_no_id"),
    ("https://youtube.com/watch?v=dQw4w9WgXcQ&feature=share",
     True, "video_id_with_query"),
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLA7no0L9zTk4Qp6LlDjFVCetW-sFw9r5I",
     True, "video_and_playlist"),

    # Error cases
    ("https://www.notyoutube.com/watch?v=dQw4w9WgXcQ", False, "error_wrong_domain"),
    ("https://www.youtube.com/watchv=dQw4w9WgXcQ",
     False, "error_missing_question_mark"),
    ("https://youtu.be/dQw4w9WgXcQextra", True, "error_extra_characters"),
    ("https://www.youtube.com/watch?time_continue=1&v=dQw4w9WgXcQ",
     True, "error_unexpected_params"),
    ("https://www.youtu.be/dQw4w9WgXcQ?list=PLA7dr9B2F8mN5WLzcpC3sB9YR_ATCf90F",
     True, "error_playlist_included"),

    ("https://example.com/watch?v=dQw4w9WgXcQ", False, "non_youtube_domain"),
    ("https://www.youtube.com/watchv=dQw4w9WgXcQ", False, "typo_in_query"),
    ("https://youtu.be/dQw4w9WgXcQ?list=PLA7no0L9zTk4Qp6LlDjFVCetW-sFw9r5I",
     True, "short_link_with_playlist"),
    ("https://www.youtub.com/watch?v=dQw4w9WgXcQ", False, "typo_in_domain"),
    ("https://www.youtube.com/watch?feature=share&v=dQw4w9WgXcQ",
     True, "video_id_with_other_query_first"),
    ("https://www.youtube.com/playlist?feature=share&list=PLA7no0L9zTk4Qp6LlDjFVCetW-sFw9r5I",
     True, "playlist_with_other_query_first"),

])
def test_is_youtube_link(link, expected_result, test_id):
    # Act
    result = is_youtube_link(link)

    # Assert
    assert result == expected_result, f"Test failed for test_id: {test_id}"
