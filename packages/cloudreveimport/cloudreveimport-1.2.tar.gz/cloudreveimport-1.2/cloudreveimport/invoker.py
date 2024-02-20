import json
import time
import subprocess
from threading import Thread


def stdout_reader(process: subprocess.Popen):
    while True:
        output = process.stdout.readline().decode('utf-8')
        if not output and process.poll() is not None:
            break
        if len(output.strip()) <= 0:
            continue
        print("stdout", output.strip())


def stderr_reader(process: subprocess.Popen):
    while True:
        output = process.stderr.readline().decode('utf-8')
        if not output and process.poll() is not None:
            break
        if len(output.strip()) <= 0:
            continue
        print("stderr", output.strip())


class Invoker:
    def __init__(self, executable, config, email, restart_interval=None):
        self.executable = executable
        self.config = config
        self.email = email
        self.process = None
        self.stdout_reader = None
        self.stderr_reader = None
        self.restart_interval = restart_interval
        self._current_time = 0

    def start(self):
        self.process = subprocess.Popen(
            args=[self.executable, "-c", self.config, "-u", self.email, "-m", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.stdout_reader = Thread(target=stdout_reader, args=(self.process,))
        self.stderr_reader = Thread(target=stderr_reader, args=(self.process,))
        self.stdout_reader.start()
        self.stderr_reader.start()
        self._current_time = time.time()

    def invoke(self, command, **kwargs):
        if not self.process:
            print("not started")
            return
        data = json.dumps({
            **{k: v for k, v in kwargs.items() if v},
            "command": command
        })
        self.process.stdin.write((data + "\n").encode("utf8"))
        if self.restart_interval:
            current_time = time.time()
            if current_time-self._current_time > self.restart_interval:
                self.join()
                self.start()

    def import_file(self, dst_path, source_name, size=0):
        self.invoke(command="ImportFile", dst_path=dst_path, source_name=source_name, size=size)

    def delete_file(self, dst_path):
        self.invoke(command="DeleteFile", dst_path=dst_path)

    def update_file_stat(self, dst_path, mtime=None, ctime=None, size=0):
        mtime = int(mtime) if mtime else mtime
        ctime = int(ctime) if ctime else ctime
        self.invoke(command="UpdateFileStat", dst_path=dst_path, updated_at=mtime, created_at=ctime, size=size)

    def update_folder_time(self, dst_path, mtime=None, ctime=None):
        mtime = int(mtime) if mtime else mtime
        ctime = int(ctime) if ctime else ctime
        self.invoke(command="UpdateFolderTime", dst_path=dst_path, updated_at=mtime, created_at=ctime)

    def join(self):
        self.process.stdin.close()
        self.stdout_reader.join()
        self.stderr_reader.join()
        self.process.kill()
        self.process = None
        self.stdout_reader = None
        self.stderr_reader = None
