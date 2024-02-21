# PyTuneSmith

PyTuneSmith is a Python library designed for creating and manipulating music. It provides tools for generating musical compositions, applying audio effects, and synthesizing audio from musical scores.

## Features

- **Musical Composition:** Create musical compositions with ease, defining melodies, harmonies, and rhythms programmatically.
- **Audio Effects:** Apply various audio effects to your compositions, such as convolution and gain adjustments, to enhance the sound.
- **Lyrics Synthesis:** Integrate lyrics into your compositions with adjustable playback speeds and apply effects to the vocal tracks.
- **MIDI Synthesis:** Convert your compositions into MIDI format for further processing or playback using external synthesizers.

## Installation

PyTuneSmith can be installed using Poetry:

```bash
poetry add pytunesmith
```

Usage
Here's a simple example of how to create a song with PyTuneSmith:

```python
import pytunesmith

# Define the song structure
song = pytunesmith.Song(tempo=120)

# Add a piano track
piano_track = pytunesmith.InstrumentTrack(
    name="Acoustic Grand Piano",
    melody=[('C4', 0, 1), ('E4', 1, 2), ('G4', 2, 3)]
)
song.add_instrument_track(piano_track)

# Add lyrics
lyrics_track = pytunesmith.LyricsTrack(
    lyrics=[("Hello", 1), ("world", 2)]
)
song.set_lyrics_track(lyrics_track)

# Export the song to a WAV file
song.export("hello_world_song.wav")
```

## Collaboration with an LLM
PyTuneSmith is not just a library; it's a testament to the power of collaboration between humans and AI. A significant portion of this project was authored and constructed with the help of a Large Language Model (LLM), with guidance and direction provided by a human developer. This unique collaboration has allowed for the rapid development and refinement of the library, showcasing the potential of AI-assisted programming.

## Contributing
Contributions to PyTuneSmith are welcome! If you have ideas for new features, improvements, or bug fixes, feel free to open an issue or submit a pull request.

## License
PyTuneSmith is released under the MIT License. See the LICENSE file for more details.