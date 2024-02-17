# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['readmeProcess']

package_data = \
{'': ['*']}

install_requires = \
['easy-fossy>=2.0.11,<3.0.0']

entry_points = \
{'console_scripts': ['getfr = readmeProcess:main']}

setup_kwargs = {
    'name': 'getfr',
    'version': '0.1.2',
    'description': 'get fossology report for a given folder id',
    'long_description': '# getfr\n\nFossology report generater\n\n## Description\n\nThis is intended for generating the reports(readmeoss,spdx2,spdx2tv,dep5,unifiedreport) using folder_id in fossology.\n\n## Getting Started\n\n### Dependencies\n\n- easy_fossy\n\n### Installing\n\n- pip install dist/getfr-v.v.v.tar.gz\n\n### Executing program\n\n- How to run the program\n\n```\npip install getfr\n\nCOMMAND FORMAT:\ngetfr [-h] folder_id clearing_status userid since_yyyy_mm_dd report_format\n\nexample command:\ngetfr 107 closed all 2024-02-01 readmeoss\n\n\n```\n\n## Help\n\nAny advise for common problems or issues.\n\n```\n>getfr -h\nusage: getfr [-h] folder_id clearing_status userid since_yyyy_mm_dd report_format\n\npositional arguments:\n  folder_id         get the folder id from the fossology. organize > folders > Edit properties > select the folder to edit >check the folder    \n                    id form url\n  clearing_status   closed , open, inprogress, rejected\n  userid            all, or give single specific user id\n  since_yyyy_mm_dd  files uploaded date from 2024-02-01s\n  report_format     readmeoss,spdx2,spdx2tv,dep5,unifiedreport\n\noptions:\n  -h, --help        show this help message and exit\n\n```\n\n## Authors\n\nDinesh Ravi\n\n## Version History\n\n- 0.1.0\n  - Initial Release\n\n## License\n\nThis project is licensed under the MIT License - see the [MIT](LICENSE) file for details\n\n## Acknowledgments\n\n- [easy_fossy](https://pypi.org/project/easy-fossy)\n',
    'author': 'dineshr93gmail.com',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
