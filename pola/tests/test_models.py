from pola.models import app_default_banner_upload_to


def test_app_default_banner_upload_to_returns_static_path():
    class Dummy:
        pass

    assert app_default_banner_upload_to(Dummy(), 'file.png') == 'main-banner.png'
