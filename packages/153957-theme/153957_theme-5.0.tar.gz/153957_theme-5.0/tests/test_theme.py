from pathlib import Path
from unittest import TestCase, mock

from sigal.gallery import Gallery
from sigal.settings import read_settings

from theme_153957 import theme


class TestTheme(TestCase):
    def get_demo_gallery(self) -> Gallery:
        demo_settings = str(Path(__file__).parent.parent / 'demo/sigal.conf.py')
        settings = read_settings(demo_settings)
        return Gallery(settings, ncpu=1)

    def test_get_path(self) -> None:
        self.assertEqual(
            str(Path(__file__).resolve().parent.parent / 'theme_153957'),
            theme.get_path(),
        )

    def test_theme(self) -> None:
        gallery = self.get_demo_gallery()
        theme.theme(gallery)

        self.assertEqual(
            str(Path(__file__).resolve().parent.parent / 'theme_153957'),
            gallery.settings['theme'],
        )

    @mock.patch('theme_153957.theme.signals')
    def test_register(self, mock_signals: mock.MagicMock) -> None:
        theme.register({})
        mock_signals.gallery_initialized.connect.assert_called_once_with(theme.theme)
        mock_signals.gallery_build.connect.assert_called_once_with(theme.remove_leaflet)
