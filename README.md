# Short Drama Audio Library

Curated background music and sound effects for short dramas, organized by English mood tags.

This private library contains **1,284 unique audio assets**: **1,217 BGM tracks** and **67 sound effects**, totaling about **8.79 GiB**. Only recordings with explicit mood labels are included. Another 445 BGM tracks and 110 effects without supported mood labels remain local and are not included in this repository.

## Browse

- `bgm/<mood>/`: background music, organized by English mood.
- `sfx/<mood>/`: sound effects, organized by English mood.
- `catalog.json`: full metadata, English moods and function/style tags, original titles, source paths, duration, codec, and SHA-256.
- `catalog.csv`: searchable spreadsheet-friendly catalog.
- `import-report.json`: source accounting, exclusions, deferred unlabeled counts, and validation results.
- `tools/find_audio.py`: dependency-free catalog search and integrity checks (Python 3.11+).

Examples of mood tags include `suspense`, `tense`, `sad`, `warm`, `romantic`, `cheerful`, `calm`, `epic`, and `horror`. Function/style tags include `riser`, `whoosh`, `impact`, `transition`, `battle`, and `chinese_traditional`.

An asset can have multiple moods. The directory uses its alphabetically first mood; the catalog lists all moods. Filenames contain a stable ID derived from the original file hash and up to three English mood tags. Original titles and every retained source path remain searchable in the catalog.

## Download

Audio files are stored with Git LFS. Install Git LFS, then:

```sh
git lfs install
git clone https://github.com/instl999/short-drama-audio-library.git
cd short-drama-audio-library
git lfs pull
```

For a lightweight checkout, set the `GIT_LFS_SKIP_SMUDGE` environment variable to `1` in your shell before cloning. Fetch only a folder when needed:

```sh
git lfs pull --include="bgm/sad/**"
```

Selective folder downloads include only files physically stored there. A catalog search for a mood can also match assets in other folders. Git LFS storage and downloads count toward the owner's account quota.

## Search

Run from the library root:

```sh
python tools/find_audio.py --kind bgm --mood suspense
python tools/find_audio.py --kind bgm --mood warm
python tools/find_audio.py --kind sfx --tag riser
python tools/find_audio.py "Merry Christmas"
python tools/find_audio.py --mood sad --json
python tools/find_audio.py --verify
```

Use `--limit 100` to show more matches. `--verify` checks every matching file's SHA-256, including detection of unhydrated LFS pointers.

## Use with sheelshort

Keep this repository separate from the sheelshort application repository. In your project's `sheelshort.toml`, set the `[edit]` music file to an absolute path from this library:

```toml
[edit]
music = "E:/path/to/short-drama-audio-library/bgm/<mood>/<filename>.mp3"
```

Replace placeholders with an existing catalog path. The episode JSON's `music` field contains music-generation prompts and is separate from this setting.

For effects, copy a selected asset into the project's `inputs/sfx/` and register it in the project's bible:

```json
{
  "sfx": {
    "custom_reveal": {
      "file": "inputs/sfx/reveal.wav",
      "sync": 0.0,
      "level": -4,
      "what": "Suspense accent on a reveal"
    }
  }
}
```

Keep the correct file extension. Reference the cue in a cut with `"sfx": "custom_reveal"`. Audition the clip to set `sync`; onset/peak timing has not been measured by this import.

## Import and quality

The source collection contained 2,268 files. This repository represents 1,602 usable source files after merging 318 byte-identical copies into 1,284 assets. The remaining collection consists of 625 source files deferred for lack of mood labels, 13 non-media/incomplete files, and 28 copies of 20 recordings that failed audio decoding.

Every included asset passed a complete FFmpeg audio decode and SHA-256 verification. Audio was preserved byte-for-byte except for video containers: their first audio stream was extracted, with AAC copied directly and other codecs decoded to lossless FLAC. Separate encodings/edits remain separate unless their original bytes match exactly.

Mood tags translate existing source labels and descriptive filename/folder keywords. A matching labeled title may supply missing tags. These are source-derived labels, not a claim that each recording was auditioned for emotion, vocals, or production suitability. Original source files remain untouched.

## Provenance and rights

Recordings were supplied by the repository owner from third-party sources. No redistribution or commercial-use license was supplied or inferred. They are not represented as CC0 and are not covered by any software license of sheelshort. Original artist/title information remains in the catalog. Confirm the necessary rights before using a recording in a published production.
