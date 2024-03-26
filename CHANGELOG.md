# Pyutube Changelog

## 1.1.6

- Added: Ability to show the tool version with the `-v` or `--version` option.
- Added: Support for downloading only audio with the `-a` or `--audio` option.
- Added: Support for downloading only video with the `-f` or `--footage` option.
- Changed: Updated the documentation

## 1.1.5

- Fix: big resolution fixing

  Now you can download any resolution you want from all available resolution.

- Fix: Speed up the download process.

## 1.1.4

- Edit filename template

  the new defult filename template is:
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
