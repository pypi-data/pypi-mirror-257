# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dkp']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['dkp = dkp:main']}

setup_kwargs = {
    'name': 'dkp',
    'version': '0.1.0',
    'description': 'DocKer compose Packer',
    'long_description': "# DKP - DocKer compose Packer\n\n![PyPI - Version](https://img.shields.io/pypi/v/dkp)\n\nPacks existent docker-compose project in executable single encrypted (GPG\nAES256) archive (tar + gz). It means, that you don't need to install DKP or\nremember procedure details during restore which dramatically reduces stress and\nmake your life simpler. In the end - it's hard to remember how to restore backup\nmade by N generations of administrators years ago before you...\n\nThe pipeline is:\n\n```mermaid\nflowchart TD\n    A[tar volumes] -->B(tar images)\n    B --> C[add env files and manifests]\n    C --> D[add restore scripts]\n    D --> E[compress and encrypt]\n    E --> F[wrap to self-extracting file]\n```\n\nFor backup you need:\n\n- gpg\n- python3 3.8+ (see tests in workflow)\n- sh\n- tar\n- gzip\n- docker with compose plugin\n\nFor restore you need:\n\n- gpg\n- sed\n- tar\n- gzip\n\n## Installation\n\n**Recomended**\n\n    pip install dkp\n\nAlternative - just download [dkp/dkp.py](dkp/dkp.py) and make it executable.\n\n## Backward compatibility\n\nOnce backup created, the version of DKP doesn't matter anymore since archive is\nself-complete independent file.\n\nNew DKP versions may introduce more features as well as different layout of\nfinal archive, but it will not affect previous backups.\n\n## Usage\n\n### Create backup\n\n```\nusage: dkp [-h] [--output OUTPUT] [--skip-images] [--passphrase PASSPHRASE] [project]\n\nDocKer compose Packer - backup compose project with all batteries included\n\npositional arguments:\n  project               Compose project name. Default is docker-compose-pack\n\noptions:\n  -h, --help            show this help message and exit\n  --output OUTPUT, -o OUTPUT\n                        Output file. Default docker-compose-pack.bin\n  --skip-images, -S     Do not archive images\n  --passphrase PASSPHRASE, -p PASSPHRASE\n                        Passphrase to encrypt backup. Can be set via env PASSPHRASE\n```\n\n### Restore\n\n```\nUsage:\n\n./path/to/backup/file [--restore/-r] [-s/--start] [-h/--help] [passphrase]\n\n   passphrase      Key to decrypt archive. Can be set by env PASSPHRASE\n\n  -h, --help       Show this help\n  -r, --restore    Automatically restore project after unpacking\n  -s, --start      Automatically start project after unpacking. Implicitly enables --restore\n```\n",
    'author': 'Aleksandr Baryshnikov',
    'author_email': 'owner@reddec.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
