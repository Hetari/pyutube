# Pyutube Changelog

## 1.1.8

- Fix: Cancel the download process.
- Modify: Documentation, and code style that made it easier to understand (using `pylint`).

## 1.1.7

- Added: Display the video size next to the resolution.
  For example:

```
  ✅ There is internet connection

  [?] Choose the file type you want to download:
  Audio

  > Video
  > Cancel the download

  Title: Write an Incredible Resume: 5 Golden Rules!

  [?] Choose the resolution you want to download:
    144p ~= 10.91 MB
    240p ~= 15.17 MB
    360p ~= 21.62 MB
    480p ~= 38.37 MB
  > 720p ~= 70.31 MB
    1080p ~= 128.81 MB
    Cancel the download
```

> **Note:** The video size is approximate, that's mean it's not exact 100%.

## 1.1.6

- Added: Ability to show the tool version with the `-v` or `--version` option.
- Added: Support only downloading audio with the `-a` or `--audio` option.
- Added: Support only downloading video with the `-f` or `--footage` option.
- Changed: Updated the documentation

## 1.1.5

- Fix: big resolution fixing

  Now you can download any resolution you want from all available resolution.

- Fix: Speed up the download process.

## 1.1.4

- Edit filename template

  the new default filename template is:
  `%name% - %resolution% _-_%video_id%.%ext%`

  > Note: This is the only filename template in the moment, we consider to add more in the future. (but not now)

## 1.1.3

- Add New feature:

  1. Allow downloading by video ID without whole link, for example:

  ```bash
  pyutube cMPnY7EuZvo
  pyutube youtu.be/cMPnY7EuZvo
  pyutube https://youtube.com/watch?v=cMPnY7EuZvo
  ```

````

```

- Fix: Enhanced Output Representation when using `--help`

## 1.1.2

- Fix: Show only available resolutions.

## 1.1.0

- Add: New feature:

  - Download the youtube shorts by one click

- Fix: big fixing

## 1.0.1

- Fix: big fixing and update the endpoints

## 1.0.0

- Initial release
```
````
