# File_uploader
This project is for uploading files from devices to the laptop using wifi hotspot

## Running on different systems

### Linux
Run the `run_script.sh` file
### Windows
Run the `ENV.cmd` file
### Dockerfile
Build image from `Dockerfile` and run the container (don't forget to link the expose container to host 😜)


#### Exposed APIS

- /

    Homepage to upload files

- /upload

    Handles uploading files on POST and sends report on GET
- /files

    Shows files uploaded to the server

- /download/<filename>

    Download <filename> from the uploaded server

- /delete

    Delete all uploaded files from the server.