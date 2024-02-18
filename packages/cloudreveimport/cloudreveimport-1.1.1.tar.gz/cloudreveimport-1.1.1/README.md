# cloudreveimport

Import your existing files into [Cloudreve](https://github.com/cloudreve/Cloudreve)!

## Install

### Build executable file

```sh
git clone https://github.com/yindaheng98/cloudreveimport
cd cloudreveimport
go build
```

Then you shall get an executable file `cloudreveimport`, you can try it:

```sh
./cloudreveimport -h
Usage of D:\Documents\MyPrograms\cloudreveimport\cloudreveimport.exe:
  -c string
        Path to the config file. (default "D:\\Documents\\MyPrograms\\cloudreveimport\\conf.ini")
  -m string
        Map of files to be imported.
  -u string
        Email of the target user. (default "admin@cloudreve.org")
```

### Install Python package

```sh
pip install cloudreveimport
```

## Usage

```python
import time
from cloudreveimport import Invoker
invoker = Invoker(
    execuable="path to executable file you just built",
    config="path to your conf.ini for your cloudreve",
    email="your email in cloudreve"
)
invoker.start()
invoker.import_file(
    source_name="path to the file on your disk",
    dst_path=["path", "you", "want", "to", "import", "to", "in", "cloudreve"],
    size=100, # Bytes
)
invoker.update_file_stat(
    dst_path=["path", "to", "file", "in", "cloudreve"],
    ctime=int(time.time()), # created time
    mtime=int(time.time()), # updated time
    size=100, # Bytes
)
invoker.delete_file(
    dst_path=["path", "to", "file", "in", "cloudreve"],
)
invoker.update_folder_time(
    dst_path=["path", "to", "folder", "in", "cloudreve"],
    ctime=int(time.time()), # created time
    mtime=int(time.time()), # updated time
)
```