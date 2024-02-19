# getfr

Fossology combined Notice report generater for all pkgs in a specified folder

## Description

This is intended for generating the reports(readmeoss,spdx2,spdx2tv,dep5,unifiedreport) using folder_id in fossology.

## Getting Started

### Dependencies

- easy_fossy

### Installing

- pip install dist/getfr-v.v.v.tar.gz

### Executing program

- How to run the program

```
pip install getfr

COMMAND FORMAT:
getfr [-h] [--sbom | --no-sbom] folder_id clearing_status userid since_yyyy_mm_dd report_format

example command:
getfr 107 closed all 2024-02-01 readmeoss --sbom


```

## configure your server in config.ini

- (config.ini file with below contents is essential & effortless kickstart)

```
[prod]
url = http://fossology.com:port/repo/api/v1/
uname =
pwd =
access = write
bearer_token = Bearer OHNSUFaI6OtoFNz
token_valdity_days = 365
token_expire = 2022-10-29
reports_location = reports/
group_name = fossy
```

## Help


```
>getfr -h
usage: getfr [-h] [--sbom | --no-sbom] folder_id clearing_status userid since_yyyy_mm_dd report_format

positional arguments:
  folder_id          get the folder id from the fossology. organize > folders > Edit properties > select the folder to edit
                     >check the folder id form url
  clearing_status    closed , open, inprogress, rejected
  userid             all, or give single specific user id
  since_yyyy_mm_dd   files uploaded date from 2024-02-01s
  report_format      readmeoss,spdx2,spdx2tv,dep5,unifiedreport

options:
  -h, --help         show this help message and exit
  --sbom, --no-sbom  create sbom

```

## Authors

Dinesh Ravi

## Version History

- 0.1.0
  - Initial Release

## License

This project is licensed under the MIT License - see the [MIT](LICENSE) file for details

## Acknowledgments

- [easy_fossy](https://pypi.org/project/easy-fossy)
