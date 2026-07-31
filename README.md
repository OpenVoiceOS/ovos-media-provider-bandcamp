# ovos-media-provider-bandcamp

This is an OVOS **MediaProvider** plugin for [Bandcamp](https://bandcamp.com). It replaces the deprecated OCP search skill `ovos-skill-bandcamp`.

The plugin wraps the [`py_bandcamp`](https://github.com/OpenJarbas/py_bandcamp) scraper client. `py_bandcamp` returns [`mediavocab.Release`](https://github.com/TigreGotico/mediavocab) objects directly. The plugin exposes Bandcamp's public search to the OCP pipeline.

## Routing

| Axis | Value |
| --- | --- |
| `media` | `{MediaType.MUSIC}` |
| `playback_type` | `{PlaybackType.AUDIO}` |

The pipeline uses this routing to filter out non-music queries before it runs a network search.

## Install

```bash
pip install ovos-media-provider-bandcamp
```

The plugin registers under the `opm.media.provider` entry-point group as `bandcamp`. The OCP pipeline loads it in-process. There is nothing to configure.

### Configuration

| Key | Default | Description |
| --- | --- | --- |
| `max_pages` | `1` | Number of Bandcamp search-result pages to walk per query. |

## How it works

`BandcampMediaProvider.search(signals, lang)` builds a query from `signals.artist` and `signals.title`. It calls `py_bandcamp.BandCamp.search(...)` for albums and tracks, and returns the resulting list of `mediavocab.Release` objects.

The provider drops artist and label hits. A MediaProvider returns playables, not identities. Each result carries its own rank in `Release.match_confidence`. The OCP pipeline filters and ranks results across all providers.

## Related projects

This plugin is one of several OCP MediaProvider plugins in the [OpenVoiceOS](https://github.com/OpenVoiceOS) org:

- [ovos-media-provider-youtube](https://github.com/OpenVoiceOS/ovos-media-provider-youtube)
- [ovos-media-provider-youtube-music](https://github.com/OpenVoiceOS/ovos-media-provider-youtube-music)
- [ovos-media-provider-soundcloud](https://github.com/OpenVoiceOS/ovos-media-provider-soundcloud)
- [ovos-media-provider-spotify](https://github.com/OpenVoiceOS/ovos-media-provider-spotify)
- [ovos-media-provider-tunein](https://github.com/OpenVoiceOS/ovos-media-provider-tunein)
- [ovos-media-provider-somafm](https://github.com/OpenVoiceOS/ovos-media-provider-somafm)
- [ovos-media-provider-pyradios](https://github.com/OpenVoiceOS/ovos-media-provider-pyradios)
- [ovos-media-provider-news](https://github.com/OpenVoiceOS/ovos-media-provider-news)
- [ovos-media-provider-mass](https://github.com/OpenVoiceOS/ovos-media-provider-mass)

## License

Apache-2.0
