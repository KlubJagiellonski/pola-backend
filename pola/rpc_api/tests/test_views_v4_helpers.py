from pola.rpc_api.views_v4 import _extract_barcode_from_query_source


def test_extract_barcode_from_alt_prefix_returns_suffix():
    assert _extract_barcode_from_query_source('alt_5901234567890') == '5901234567890'


def test_extract_barcode_from_non_alt_returns_none():
    assert _extract_barcode_from_query_source('scanner') is None
