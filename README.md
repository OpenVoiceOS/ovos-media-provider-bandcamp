# ovos-media-provider-bandcamp

OVOS **MediaProvider** plugin for [Bandcamp](https://bandcamp.com). Replaces the
deprecated OCP search skill `ovos-skill-bandcamp`.

It wraps the [`py_bandcamp`](https://github.com/OpenJarbas/py_bandcamp) scraper
client, which emits [`mediavocab.Release`](https://github.com/TigreGotico/mediavocab)
objects directly, and exposes Bandcamp's public search to the OCP pipeline.

## Routing

| Axis | Value |
| --- | --- |
| `media` | `{MediaType.MUSIC}` |
| `playback_type` | `{PlaybackType.AUDIO}` |

The pipeline gates this provider out of non-music queries before paying for a
network search.

## Install

```bash
pip install ovos-media-provider-bandcamp
```

The plugin is registered under the `opm.media.provider` entry-point group as
`bandcamp` and is loaded in-process by the OCP pipeline; there is nothing to
configure.

### Configuration

| Key | Default | Description |
| --- | --- | --- |
| `max_pages` | `1` | Number of Bandcamp search-result pages to walk per query. |

## How it works

`BandcampMediaProvider.search(signals, lang)` builds a query from
`signals.artist` + `signals.title`, calls `py_bandcamp.BandCamp.search(...)`
(albums + tracks), and returns the resulting `mediavocab.Release` list. Artist
and label hits are dropped — a MediaProvider returns playables, not identities.
Ranking is carried per-result via `Release.match_confidence`; the OCP pipeline
filters and ranks across providers.

## License

Apache-2.0
