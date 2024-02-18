from pathlib import Path
from unittest import TestCase, mock

from sigal.gallery import Gallery
from sigal.settings import read_settings

from theme_153957 import full_menu


class TestFullMenu(TestCase):
    def get_demo_gallery(self) -> Gallery:
        demo_settings = str(Path(__file__).parent.parent / 'demo/sigal.conf.py')
        settings = read_settings(demo_settings)
        return Gallery(settings, ncpu=1)

    def test_path_to_root(self) -> None:
        gallery = self.get_demo_gallery()

        with self.subTest('Top level', album='.'):
            album = gallery.albums['.']
            full_menu.path_to_root(album)
            self.assertEqual('', album.path_to_root)

        with self.subTest('First level subalbum', album='Poles'):
            album = gallery.albums['Poles']
            full_menu.path_to_root(album)
            self.assertEqual('../', album.path_to_root)

        with self.subTest('Over nine levels deep'):
            album = gallery.albums['Nine levels deep/Limbo/Lust/Gluttony/Greed/Wrath/Heresy/Violence/Fraud/Treachery']
            full_menu.path_to_root(album)
            self.assertEqual('../' * 10, album.path_to_root)

    def test_path_from_root(self) -> None:
        gallery = self.get_demo_gallery()

        with self.subTest('Top level', album='.'):
            album = gallery.albums['.']
            full_menu.path_from_root(album)
            self.assertEqual(album.path, album.path_from_root)

        with self.subTest('First level subalbum', album='Poles'):
            album = gallery.albums['Poles']
            full_menu.path_from_root(album)
            self.assertEqual(album.path, album.path_from_root)

        with self.subTest('Over nine levels deep'):
            album = gallery.albums['Nine levels deep/Limbo/Lust/Gluttony/Greed/Wrath/Heresy/Violence/Fraud/Treachery']
            full_menu.path_from_root(album)
            self.assertEqual(album.path, album.path_from_root)

    def test_title_from_metadata(self) -> None:
        gallery = self.get_demo_gallery()

        with self.subTest('Use directory name as title', album='Poles'):
            album = gallery.albums['Poles']
            self.assertEqual('Poles', album.title)

        with self.subTest('Custom title', album='Nine levels deep'):
            album = gallery.albums['Nine levels deep']
            self.assertEqual('Inferno', album.title)

    def test_sorted_using_meta(self) -> None:
        gallery = self.get_demo_gallery()

        with self.subTest('Sorted by name'):
            self.assertEqual(
                [gallery.albums['Sequences/Tree'], gallery.albums['Sequences/Candle']],
                gallery.albums['Sequences'].albums,
            )

        with self.subTest('Custom order via metadata'):
            self.assertEqual(
                [
                    gallery.albums['Long menu'],
                    gallery.albums['Nine levels deep'],
                    gallery.albums['Poles'],
                    gallery.albums['Sequences'],
                    gallery.albums['Time-Lapse'],
                ],
                gallery.albums['.'].albums,
            )

    @mock.patch('theme_153957.full_menu.signals')
    def test_register(self, mock_signals: mock.MagicMock) -> None:
        full_menu.register({})

        mock_signals.album_initialized.connect.assert_any_call(full_menu.path_to_root)
        mock_signals.album_initialized.connect.assert_any_call(full_menu.path_from_root)
