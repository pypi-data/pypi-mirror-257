__version__ = "0.1.0"



import argparse

from easy_fossy import easy_fossy as fossy
from easy_fossy import (ClearingStatus,ReportFormat)
import os
if not os.path.exists("reports"):
    os.makedirs("reports")
# pip install easy-fossy==2.0.10


def main():
    this_package = __package__
    parser = argparse.ArgumentParser()
    # parser.add_argument("api_url")
    # parser.add_argument("token")
    parser.add_argument("folder_id",help="get the folder id from the fossology. organize > folders > Edit properties > select the folder to edit >check the folder id form url")
    parser.add_argument("clearing_status",help="closed , open, inprogress, rejected")
    parser.add_argument("userid",help="all, or give single specific user id")
    parser.add_argument("since_yyyy_mm_dd",help="files uploaded date from 2024-02-01s ")
    parser.add_argument("report_format",help="readmeoss,spdx2,spdx2tv,dep5,unifiedreport")
    # parser.add_argument("output_folder")
    args = parser.parse_args()


    # api_url = args.api_url
    # token = args.token
    folder_id = args.folder_id
    clearing_status = args.clearing_status
    since_yyyy_mm_dd = args.since_yyyy_mm_dd
    report_format = args.report_format
    # output_folder = args.output_folder
    userid = args.userid
    print("Arguments offered are")
    # print(api_url)
    # print(token)
    print(f"{folder_id=}")
    # print(f"{output_folder=}")
    print(f"{clearing_status=}")
    print(f"{userid=}")
    print(f"{since_yyyy_mm_dd=}")
    print(f"{report_format=}")

    # if not os.path.isdir(output_folder):
    #     sys.exit(0)
    
    f = fossy("config.ini", "prod")

    # class ClearingStatus(Enum):
    # Open = 'Open'
    # InProgress = 'InProgress'
    # Closed = 'Closed'
    # Rejected = 'Rejected'

    users=f.get_all_users()
    # print('==============================start')
    users = [ user.name  for user in users if user is not None ]
    # print(users_filt)
    # print('==============================')
    # users
    #    [
    #   {
    #     "id": 0,
    #     "name": "string",
    #     "description": "string",
    #     "email": "string",
    #     "accessLevel": "none",
    #     "rootFolderId": 0,
    #     "emailNotification": true,
    #     "defaultGroup": 0,
    #     "agents": {
    #       "bucket": true,
    #       "copyright_email_author": true,
    #       "ecc": true,
    #       "keyword": true,
    #       "mime": true,
    #       "monk": true,
    #       "nomos": true,
    #       "ojo": true,
    #       "package": true,
    #       "reso": true,
    #       "heritage": true
    #     },
    #     "defaultBucketpool": 0
    #   }
    # ]     



    clearing_status=clearing_status.lower()
    if clearing_status == 'inprogress':
        clearing_status = 'inProgress'

    if userid == 'all':
        for user in users:
            # , -unassigned-
            #     def get_all_uploads_based_on(
            #     self,
            #     folder_id: int,
            #     is_recursive: bool,
            #     search_pattern_key: str,
            #     clearing_status: ClearingStatus,
            #     assignee: str,
            #     since_yyyy_mm_dd: str,
            #     page: int,
            #     limit: int,
            # ) -> List[Upload]:
            uploads=f.get_all_uploads_based_on(folder_id,True,'',ClearingStatus[capitalize(clearing_status)],user,since_yyyy_mm_dd,1,1000)
            for upload in uploads:
                print("downloading readmeoss with status "+clearing_status+" for "+upload.uploadname + " done by "+f.get_user_by_id(upload.assignee).email)
                f.generate_and_get_desired_report_for_uploadid(upload_id=upload.id, report_format=ReportFormat(report_format.lower()))
        print("======================================================================================================")
        for user in users: # , -unassigned-
            uploads=f.get_all_uploads_based_on(folder_id,True,'',ClearingStatus[capitalize('open')],user,since_yyyy_mm_dd,1,1000)
            for upload in uploads:
                print("Pending readmeoss with status "+'open'+" for "+upload.uploadname + " to be done by "+f.get_user_by_id(upload.assignee).email)
        print("======================================================================================================")
        for user in users:# , -unassigned-
            uploads=f.get_all_uploads_based_on(folder_id,True,'',ClearingStatus[capitalize('InProgress')],user,since_yyyy_mm_dd,1,1000)
            for upload in uploads:
                print("Pending readmeoss with status "+'InProgress'+" for "+upload.uploadname + " to be done by "+f.get_user_by_id(upload.assignee).email)
    
    else:
        uploads=f.get_all_uploads_based_on(folder_id,True,'',ClearingStatus[capitalize(clearing_status)],userid,since_yyyy_mm_dd,1,1000)
        for upload in uploads:
            print("downloading readmeoss with status "+clearing_status+" for "+upload.uploadname + " done by "+f.get_user_by_id(upload.assignee).email)
            f.generate_and_get_desired_report_for_uploadid(upload_id=upload.id, report_format=ReportFormat(report_format.lower()))

def capitalize(line):
    return ' '.join(s[:1].upper() + s[1:] for s in line.split(' '))

if __name__ == "__main__":
    main()
