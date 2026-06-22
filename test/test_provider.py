"""Unit tests for BandcampMediaProvider (network mocked)."""
from unittest.mock import patch

from mediavocab import MediaType, Release, Signals, Work, Entity, EntityKind
from mediavocab.taxonomy import PlaybackType

from ovos_media_provider_bandcamp import BandcampMediaProvider


def _make_release(title):
    return Release(work=Work(title=title, media_type=MediaType.MUSIC),
                   uri=f"https://acme.bandcamp.com/album/{title}")


def test_instantiation():
    prov = BandcampMediaProvider()
    assert prov.name == "bandcamp"
    assert prov.media == {MediaType.MUSIC}
    assert prov.playback_type == {PlaybackType.AUDIO}
    assert prov.is_available() is True


def test_matches_music_true():
    prov = BandcampMediaProvider()
    assert prov.matches(Signals(medium=MediaType.MUSIC)) is True


def test_matches_movie_false():
    prov = BandcampMediaProvider()
    assert prov.matches(Signals(medium=MediaType.MOVIE)) is False


def test_search_returns_releases():
    prov = BandcampMediaProvider()
    fake = [
        _make_release("foo"),
        _make_release("bar"),
        Entity(name="some artist", kind=EntityKind.GROUP),  # must be dropped
    ]
    with patch("ovos_media_provider_bandcamp.BandCamp.search",
               return_value=iter(fake)) as mocked:
        results = prov.search(Signals(medium=MediaType.MUSIC,
                                      title="foo", artist="acme"))
    mocked.assert_called_once()
    assert isinstance(results, list)
    assert len(results) == 2
    assert all(isinstance(r, Release) for r in results)


def test_search_empty_query():
    prov = BandcampMediaProvider()
    with patch("ovos_media_provider_bandcamp.BandCamp.search") as mocked:
        results = prov.search(Signals(medium=MediaType.MUSIC))
    mocked.assert_not_called()
    assert results == []
