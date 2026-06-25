"""Bandcamp MediaProvider plugin for OVOS.

Wraps the :mod:`py_bandcamp` scraper client and exposes Bandcamp search to the
OCP pipeline as a :class:`~ovos_plugin_manager.templates.media_provider.MediaProvider`.
Replaces the deprecated OCP search skill ``ovos-skill-bandcamp``.

``py_bandcamp`` already emits :class:`mediavocab.Release` objects directly from
``BandCamp.search`` (and the per-type ``search_albums`` / ``search_tracks``
helpers), so this provider is a thin routing/filtering shim over the public
search API.
"""
from typing import ClassVar, List, Optional, Set

from ovos_utils.log import LOG

from mediavocab import Release, Signals, Entity

from ovos_plugin_manager.templates.media_provider import MediaProvider

from py_bandcamp import BandCamp


class BandcampMediaProvider(MediaProvider):
    """Search Bandcamp's public catalog and return playable music releases."""

    name: ClassVar[str] = "bandcamp"

    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)
        self.max_pages = self.config.get("max_pages", 1)

    def search(self, signals: Signals, lang: str = "en-us", *,
               supported_playback_types: Optional[Set[str]] = None,
               blocked_genres: Optional[Set[str]] = None,
               region: Optional[str] = None,
               session_id: Optional[str] = None) -> List[Release]:
        """Search Bandcamp for ``signals.title`` (optionally scoped by
        ``signals.artist``) and return candidate music :class:`Release` objects.

        Albums and tracks are returned as ``Release`` objects by py_bandcamp;
        artist/label hits (yielded as :class:`mediavocab.Entity`) are dropped —
        a MediaProvider returns playables, not identities.
        """
        title = (signals.title or "").strip()
        artist = (signals.artist or "").strip()
        query = " ".join(p for p in (artist, title) if p).strip()
        if not query:
            return []

        results: List[Release] = []
        try:
            for item in BandCamp.search(query, albums=True, tracks=True,
                                        artists=False, labels=False,
                                        max_pages=self.max_pages):
                if isinstance(item, Release):
                    results.append(item)
                elif isinstance(item, Entity):
                    # artist/label identity hits are not playable
                    continue
        except Exception:
            LOG.exception("Bandcamp search failed")
            return []
        return results
