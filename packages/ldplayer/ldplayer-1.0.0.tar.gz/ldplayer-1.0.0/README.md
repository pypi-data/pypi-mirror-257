LDPlayer
==========
This is package for LDPlayer emulator control software. (unofficial)

LDPlayer CLI details can be found in [here]("https://www.ldplayer.net/blog/introduction-to-ldplayer-command-line-interface.html")

#### Table of contents

- [LDPlayer](#ldplayer)
- [Install](#install)
- [Usage](#usage)
- [Environments](#environments)
- [License](#license)


Install
==========
```shell
pip install git+https://github.com/sinmentis/ldplayer.git
```

Usage
==========
```python
from ldplayer import LDPlayer
ldplayer = LDPlayer(r"D:\LDPlayer\LDPlayer9\ldconsole.exe")
print(ldplayer.list_instances())
```


Environments
============
* [LDPlayer 9.0.66](https://www.ldplayer.net/)
* Python 3.11

License
==========
MIT