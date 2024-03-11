import pytest
from pyutube.utils import is_youtube_link


@pytest.mark.parametrize("link, expected_result", [
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ",
     (True, "video")),
    ("https://youtu.be/dQw4w9WgXcQ", (True, "video")),
    # ("https://www.youtube.com/playlist?list=PLynG8gQD-n8BMplEGyFBRVJFssMFo5x07",
    #  (True, "playlist")),
    ("https://www.youtube.com/shorts/dQw4w9WgXcQ",
     (True, "shorts")),


    ("", (False, "unknown")),
    ("https://www.youtube.com/", (False, "unknown")),
    ("https://www.youtube.com/watch?v=", (False, "unknown")),
    ("https://www.youtu.be/", (False, "unknown")),
    ("https://www.youtube.com/playlist?list=",
     (False, "unknown")),
    ("https://www.youtube.com/shorts/", (False, "unknown")),


    ("https://www.google.com", (False, "unknown")),
    ("https://www.youtube.com/watch?list=dQw4w9WgXcQ",
     (False, "unknown")),
    ("https://www.youtu.be/dQw4w9WgXcQ?list=PLynG8gQD-n8BMplEGyFBRVJFssMFo5x07",
     (True, "video")),
    ("https://www.youtube.com/shorts/dQw4w9WgXcQ?list=PLynG8gQD-n8BMplEGyFBRVJFssMFo5x07",
     (True, "shorts")),
])
def test_is_youtube_link_error_cases(link, expected_result):
    # Act
    result = is_youtube_link(link)

    # Assert
    assert result == expected_result
