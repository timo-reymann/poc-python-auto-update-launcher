Proof of Concept - Python Auto Updater
===

Graphical Auto Updater with QT 6 (pyside6).

- Get version of currently installed software from VERSION file
- Assumes files for application itself are in same folder
- Simple checksum check for downloaded files

## Limitations

- No signing of checksums, which would be strongly advisable for any real world use case to ensure the archive has not
  been changed in transfer.
- Error handling and UI is very basic and limited
