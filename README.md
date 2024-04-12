# 📹 YouTube Downloader CLI

## Enjoying my project? Please show your appreciation by starring it on GitHub! ⭐

[![Version](https://img.shields.io/pypi/v/pyutube.svg?style=flat)](https://pypi.org/project/pyutube/)
[![Downloads](https://static.pepy.tech/badge/pyutube)](https://pepy.tech/project/pyutube)

> [!NOTE]
> Help me to improve this tool!
> I tested it on Windows, Mac, and Linux, and it works fine, but if there is any issue, please open an issue on [GitHub](https://github.com/Hetari/pyutube/issues/new) and I'll fix it.
>
> Have a new feature? Please don't hesitate to [tell me](https://github.com/Hetari/pyutube/issues/new)!

<a href="https://ibb.co/27wcFYN">
   <img src="images/pyutube.png" alt="Pyutube" style="width: 100%;">
</a>

## 📓 Description

This command-line tool downloads YouTube videos from the `Terminal`, written under [Pytube](https://pytube.io/).

it is cross-platform (Windows, Mac, Linux) and can be used in any terminal.

## 💎 Features

- User-friendly CLI interface.
- Download a single YouTube video format or audio.
- Download YouTube shorts.
- Download YouTube playlists.

## 📈 Upgrade

All the latest updates will be posted on [GitHub](https://github.com/Hetari/pyutube), you can also upgrade the tool via [PyPI](https://pypi.org/project/pyutube/) with this command:

```bash
pip install --upgrade pyutube
```

## 🛠️ Installation

it is easy to install Pyutube, make sure that you have [Python](https://www.python.org) installed. To check if you have it installed, type `python --version` in your terminal. You should see something like `Python 3. x ` otherwise, download and install it from [Python](https://www.python.org/downloads/).

after that, you can install it with the following command:

```bash
pip install pyutube
```

Then you can use it in your `Terminal` 🥳.

## 🦸 Usage

Pyutube is very easy to use, here are examples of its uses:

```bash
pyutube YOUTUBE_LINK [PATH]
```

> [!NOTE] > `[PATH]` is an optional input, the default value is the `terminal` path where the CLI is running (the current working directory).

<div style="text-align: center;">
   <p>Download video with specify the save location</p>
   <a href="https://ibb.co/0JkdkQy">
      <img src="images/image1.png" alt="Download video with specify the save location">
   </a>

   <p>Chose what type you want to download</p>
   <a href="https://ibb.co/Kb6qjmg">
      <img src="images/image2.png" alt="Chose what type you want to download">
   </a>

   <p>Chose what what resolution you want to download(if the type is video)</p>
   <a href="https://ibb.co/7ymCS79">
      <img src="images/image3.png" alt="Chose what what resolution you want to download">
   </a>

   <p>If you download a playlist, you can chose what video you want to download, or even all of them</p>
   <a href="https://ibb.co/0qwkQNm">
      <img src="images/image4.png" alt="If you download a playlist, you can chose what video you want to download, or even all of them"/>
   </a>

<br /><br />

 <p>Do not know how to use it? just type <code>pyutube --help</code></p>
  <a href="https://ibb.co/LhT6r3r">
      <img src="images/image5.png" alt="image5">
   </a>
</div>

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

## 🕵️‍♂️ Examples

### **- Show version:**

```bash
pyutube -v
```

### **- Download playlists:**

1. `pyutube <YOUTUBE_PLAYLIST_LINK | PLAYLIST_ID> [the_download_path*]`

   > [!NOTE]
   > Don't forget, the path is optional.

2. Then choose the format of the download, video or audio.
3. Choose the resolution if it is a video you want to download, otherwise, choose audio and it will download it all immediately 🔥.
   > [!NOTE]
   > It will check all resolutions available in the first video in the playlist, then it will download all of them in the same resolution 👍.

### **- Download shorts, videos, or audio:**

1. `pyutube <YOUTUBE_LINK | VIDEO_ID | SHORT_LINK> [the_download_path*]`

   > [!NOTE]
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

## 🥰 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you want to change.
please follow the [contributing guidelines](https://github.com/Hetari/pyutube/blob/main/CONTRIBUTING.md)

## 📎 License

This project is licensed under the [MIT License](https://github.com/Hetari/pyutube/blob/main/LICENSE.md).
