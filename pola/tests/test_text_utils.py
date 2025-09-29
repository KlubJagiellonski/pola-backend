from pola.text_utils import _shorten_txt, strip_dbl_spaces, strip_urls_newlines


def test_strip_dbl_spaces_basic():
    assert strip_dbl_spaces("  Ala   ma   kota  ") == "Ala ma kota"


def test_strip_urls_newlines_removes_urls_and_trims():
    s = "Visit https://example.com/page?q=1 and www.example.org/test\n"
    # URLs are removed, double spaces may remain, trailing newline trimmed
    assert strip_urls_newlines(s) == "Visit  and"


def test_strip_urls_newlines_collapses_double_newlines():
    s = "A\n\nB\r\n\r\nC"
    assert strip_urls_newlines(s) == "A\nB\r\nC"


def test_strip_urls_newlines_only_url_results_in_empty_string():
    s = "   http://example.com   "
    assert strip_urls_newlines(s) == ""


def test_shorten_txt_no_change_when_short_or_equal():
    assert _shorten_txt("abc", 3) == "abc"
    assert _shorten_txt("short") == "short"


def test_shorten_txt_truncates_and_adds_ellipsis():
    assert _shorten_txt("abcdefghijklmnopqrstuvwxyz012345", 10) == "abcdefghij..."
