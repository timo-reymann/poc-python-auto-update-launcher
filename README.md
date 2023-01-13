Proof of Concept - Python Auto Updater
===

Graphical Auto Updater with QT 6 (pyside6).

- Get version of currently installed software from VERSION file
- Assumes files for application itself are in same folder

## Features

- Checksum check after download
- Verification of integrity for checksum file using RSA

## Limitations

- Version checking is based on basic VERSION file, in demo delivered with application
- Error handling and UI is very basic and limited

## Run it

```shell
cd .server
docker compose up -d

cd ..
pip3 install -r requirements.txt
python3 main.py
```

## Publish new version

1. Create new folder with version number in `.server/web-root`
2. Zip each platform, make sure the file contains a VERSION file and the application entrypoint
3. Create checksums of files: `sha256sum .server/web-root/<version>/*.zip > .server/web-root/<version>/checksums.txt`
4. Create signature with private
   key: `openssl dgst -sign key/private_key.pem -out .server/web_root/0.0.0/checksums.sig -sha256 .server/web_root/0.0.0/checksums.txt`
