# YouTube Downloader CLI

Enjoying my project? Please show your appreciation by starring it on GitHub! ⭐

## Description

This command-line tool downloads YouTube videos from the `Terminal`, written under [Pytube](https://pytube.io/).

it is cross-platform (Windows, Mac, Linux) and can be used in any terminal.

> **Note:** This project is still in development.

## Inspiration

This project was inspired by [Utube](https://github.com/omer73364/uTube/) by [omer73364](https://github.com/omer73364) 🤩

## Features

- User-friendly CLI interface.
- Download a single YouTube video format or audio.
- Download YouTube shorts.
- Download YouTube playlists.

## TODO

- [x] Publish on PyPI.
- [x] Support downloading sounds (mp3 format).
- [x] Supports all available video resolutions.
- [x] Support shorts.
- [x] Supports downloading playlists.
- [ ] Playlists are organized into folders by their names.
- [ ] GUI app (not yet).
- [ ] Are there any features that you/I can think of?

## Upgrade

All the latest updates will be posted on [GitHub](https://github.com/Hetari/pyutube), you can also upgrade the tool via [PyPI](https://pypi.org/project/pyutube/) with this command:

```bash
pip install --upgrade pyutube
```

## Installation

Make sure that you have [Python](https://www.python.org) installed. To check if you have it installed, type `python --version` in your terminal. You should see something like `Python 3. x `

### Method 1: Using Pip

```bash
pip install --upgrade pip
pip install pyutube
```

### Method 2: Building the project from the source

Clone the repository:

```bash
git clone https://github.com/Hetari/pyutube.git
```

Change to the directory:

```bash
cd pyutube
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Build the package:

```bash
python setup.py sdist bdist_wheel
```

Install the package via pip:

```bash
pip3 install dist/*
```

> **Warning:**
>
> In some cases, the package will not install. You may have to run superuser in your **OS**, for MacOS and Linux, you can write `sudo` with pip command like `sudo pip3 install dist/*`.

Then you can use it in your `Terminal` 🥳.

## Usage

Pyutube is very easy to use, here are examples of its uses:

```bash
pyutube YOUTUBE_LINK [PATH]
```

> **Note:** `[PATH]` is an optional input, the default value is the `terminal` path where the CLI is running (the current working directory).

#### Arguments

| Arguments | Description                                                                                                          |
| --------- | -------------------------------------------------------------------------------------------------------------------- |
| `URL`     | The `URL` of the YouTube video. This argument is <span style="color:red">[Required]</span>.                          |
| `PATH`    | The `path` to save the video. Defaults to the current working directory. <span style="color:green">[Optional]</span> |

#### Options

| Option                                              | Description                                                      |
| --------------------------------------------------- | ---------------------------------------------------------------- |
| `-v` <span style="color:cyan">or</span> `--version` | Show the version number.                                         |
| `-a` <span style="color:cyan">or</span> `--audio`   | Download only audio immediately without asking (video or audio). |
| `-f` <span style="color:cyan">or</span> `--footage` | Download only video immediately without asking (video or audio). |

## Examples

### **- Show version:**

```bash
pyutube -v
```

### **- Download playlists:**

1. `pyutube <YOUTUBE_PLAYLIST_LINK | PLAYLIST_ID> [the_download_path*]`

   > Don't forget, the path is optional.

2. Then choose the format of the download, video or audio.
3. Choose the resolution if it is a video you want to download, otherwise, choose audio and it will download it all immediately 🔥.
   > It will check all resolutions available in the first video in the playlist, then it will download all of them in the same resolution 👍.

### **- Download shorts, videos, or audio:**

1. `pyutube <YOUTUBE_LINK | VIDEO_ID | SHORT_LINK> [the_download_path*]`

   > Don't forget, the path is optional.

2. Then choose the format of the download, video or audio.
3. Choose the resolution if it is a video you want to download, otherwise, choose audio and it will download it immediately 🔥.

```bash
pyutube cMPnY7EuZvo
pyutube youtu.be/cMPnY7EuZvo
pyutube https://youtube.com/watch?v=cMPnY7EuZvo
```

### **- Download audio immediately:**

1. `pyutube <YOUTUBE_LINK | VIDEO_ID | SHORT_LINK> [the_download_path*] -a`

```bash
pyutube cMPnY7EuZvo -a
```

or

```bash
pyutube -a youtu.be/cMPnY7EuZvo
```

and that's it 🎉.

### **- Download videos immediately:**

1. `pyutube <YOUTUBE_LINK | VIDEO_ID | SHORT_LINK> [the_download_path*] -f`
2. Choose the resolution.

```bash
pyutube cMPnY7EuZvo -f
```

or

```bash
pyutube -f youtu.be/cMPnY7EuZvo
```

see the video and relax 🎉.

<div style="text-align: center;">
   <a href="https://ibb.co/LhT6r3r">
      <img src="https://i.ibb.co/WprF0L0/image5.png" alt="image5">
   </a>
   <a href="https://ibb.co/7ymCS79">
      <img src="https://i.ibb.co/h8z9gpq/image4.png" alt="image4">
   </a>
   <a href="https://ibb.co/9sVDxbh">
      <img src="https://i.ibb.co/pJR7HfQ/image3.png" alt="image3">
   </a>
   <a href="https://ibb.co/Kb6qjmg">
      <img src="https://i.ibb.co/sbjwvt4/image2.png" alt="image2">
   </a>
   <a href="https://ibb.co/0JkdkQy">
      <img src="https://i.ibb.co/7yH6Hbt/image1.png" alt="image1">
   </a>
</div>

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you want to change.
please follow the [contributing guidelines](https://github.com/Hetari/pyutube/blob/main/CONTRIBUTING.md)

## License

This project is licensed under the [MIT License](https://github.com/Hetari/pyutube/blob/main/LICENSE.md).
