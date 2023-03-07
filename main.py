import socket
import subprocess
import signal
import time
import sys
import yaml
import os

CONFIG_PATH = os.environ.get("RTP2FILE_CONFIG_PATH")

with open(CONFIG_PATH, "r") as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)

print(
    "Listening on port %s and %s on %s"
    % (config["video_port"], config["audio_port"], config["ip"])
)
print("GStreamer pipeline: %s" % config["pipeline"])

while True:
    try:
        video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        audio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        video.bind((config["ip"], config["video_port"]))
        audio.bind((config["ip"], config["audio_port"]))
        video_data, _ = video.recvfrom(1)
        audio_data, _ = audio.recvfrom(1)
        video.close()
        audio.close()

        if video_data and audio_data:
            date = time.strftime("%Y%m%d-%H%M%S")
            print("Creating a backup of a stream that started on %s" % date)
            process = subprocess.Popen(
                config["pipeline"]
                .format(
                    port1=config["video_port"],
                    port2=config["audio_port"],
                    path=config["save_path"],
                    date=date,
                )
                .split(),
                stdout=subprocess.PIPE,
                preexec_fn=os.setsid,
            )
            while process.poll() is None:
                output = process.stdout.readline()
                if "GstUDPSrcTimeout" in output.decode("UTF-8"):
                    time.sleep(2)
                    os.killpg(os.getpgid(process.pid), signal.SIGINT)
                    process.wait()
                    print(
                        "End of the creation of a backup of a stream that started on %s"
                        % date
                    )

    except socket.timeout:
        pass
    except KeyboardInterrupt:
        try:
            while process.poll() is None:
                process.send_signal(signal.SIGINT)
                process.wait()
            sys.exit()
        except:
            sys.exit()
