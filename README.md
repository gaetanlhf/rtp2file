
<h2 align="center">rtp2file</h2>
<p align="center">Automatically save RTP streams as a file </p>
<p align="center">
    <a href="#about">About</a> •
    <a href="#features">Features</a> •
    <a href="#configuration">Configuration</a> •
    <a href="#run">Run</a> •
    <a href="#license">License</a>
</p>

## About

rtp2file is a small Python program designed to easily receive RTP streams and combine them into a file.  
When the program receives data on both ports, it triggers a GStreamer pipeline and listens to the pipeline to detect if a timeout (`GstUDPSrcTimeout`) has occurred.  
If so, an EOS signal is sent to GStreamer to stop the pipeline and the program is ready to receive new streams again.  
In this repository, the proposed version retrieves a video (e.g. from a camera) and audio (e.g. from a computer microphone) RTP stream and merges them into a .mp4 file (see also the GStreamer pipeline provided as an example below).  
This concept can be easily tailored to your needs.

## Features

- ✅ An **adaptable** concept
- ✅ Use of **standard tool** (GStreamer)
- ✅ Use any **GStreamer pipeline**
- ✅ An **easily configurable** tool
- ✅ Can operate effortlessly as a **daemon**

## Configuration

Here is an example of a configuration (YAML): 
```yaml
# IP to listen to
ip: 127.0.0.1
# RTP port used for video to listen to
video_port: 5100
# RTP port used for audio to listen to
audio_port: 5200
# Path where the saved files will be stored
save_path: ./
# GStreamer pipeline
pipeline: gst-launch-1.0 -em udpsrc port={port1} caps=application/x-rtp,media=video,encoding-name=H264,payload=96 timeout=2000000000 ! queue ! rtph264depay ! queue ! h264parse ! queue ! mp4mux name=mux ! queue ! filesink location={path}/{date}.mp4 udpsrc port={port2} caps=application/x-rtp,media=audio,encoding-name=OPUS,payload=96 timeout=2000000000 ! queue ! rtpopusdepay ! queue ! opusparse ! queue ! mux.
```

For the GStreamer pipeline :
- The `-e` option is used to receive the EOS signal from the Python program via a SIGINT
- The `-m` option is used to display the messages, important for the Python program to detect the timeout
- `{port1}` is the video RTP port
- `{port2}` is the audio RTP port
- `{path}` is the defined backup path
- `{date}` is the date which is a timestamp and serves as the file name
- `{port1}`, `{port2}`, `{path}` and `{date}` must be present in your pipeline as they are dynamic elements that are added by the Python program before GStreamer is launched
- Don't forget to give a timeout to the different `udpsrc`, otherwise the Python program won't be able to detect the end of a stream.

## Run
### Direct use

To be able to use rtp2file directly, you must set the environment variable `rtp2file_CONFIG_FILE_PATH` as the path to the configuration file.  
For example :rtp2file
```
export rtp2file_CONFIG_FILE_PATH=./config.yaml
```
Then you can run the program:
```
./rtp2file
```

### As a systemd service

It is possible to easily use rtp2file as a daemon with the provided systemd service.  
The systemd service provided can be adapted to your needs.

Steps to install rtp2file as a systemd service:

- Create a group:

```
groupadd rtp2file
```

 - Create an user:

```
useradd -r -s /sbin/nologin -g rtp2file rtp2file
```

- Copy the `rtp2file` binary to `/usr/bin/`

```
cp rtp2file /usr/bin/
```

- Create a `rtp2file` folder in `/etc/` for the configuration file

```
mkdir /etc/rtp2file
```

- Copy the `config.yaml` configuration file to `/etc/rtp2file/`

```
cp config.yaml /etc/rtp2file/
```

- Copy the `rtp2file.service` systemd service file to `/etc/systemd/system/`

```
cp rtp2file.service /etc/systemd/system/
```

- Start the systemd service

```
systemctl start rtp2file
```

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
