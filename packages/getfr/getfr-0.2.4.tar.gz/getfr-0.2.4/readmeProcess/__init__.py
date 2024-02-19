__version__ = "0.1.0"

from pydantic import BaseModel
import re
import argparse
from easy_fossy import easy_fossy as fossy
from easy_fossy import (ClearingStatus,ReportFormat)
import os
from datetime import datetime
import shutil



# pip install easy-fossy==2.0.10

MAIN_LICENSES="MAIN LICENSES"
COPYRIGHT_NOTICES="Copyright notices"
ACKNOWLEDGEMENTS="ACKNOWLEDGEMENTS"
OTHER_LICENSES="OTHER LICENSES"

end_text = "------------------------------------------------------------------------------------------------------------------------"

start_text = "========================================================================================================================"

class License(BaseModel):
    name: str = "" 
    text: str = "" 

class BOM(BaseModel):
    name: str = "" 
    main_lic: list[License] = None 
    other_lic: list[License] = None 
    ack: list[License] = None 
    copyright: list[str] = None 
class SBOM(BaseModel):
    boms: list[BOM] = None 

def sbomFunc() -> SBOM:
    dir="reports"
    sbom=SBOM()
    sbom.boms=list()
    # file="reports/ReadMe_OSS_acl_2.3.1.orig.tar.xz_1708078729.txt"
    # file="reports/ReadMe_OSS_sed_4.8.orig.tar.xz_1708078724.txt"
    # file="reports/ReadMe_OSS_libxcrypt_4.4.27.orig.tar.xz_1708078747.txt"
    # file="reports/ReadMe_OSS_systemd_249.11.orig.tar.gz_1708088069.txt"

    files = [f for f in os.listdir(dir) if re.match(r'ReadMe_OSS_.*\.txt', f)]
    for count,file in enumerate(files):
        f = open(os.path.join(dir,file), 'r')
        lines = f.readlines()
        total_len = len(lines)
        bom=BOM()
        
        is_ack_present, is_main_lic_present,is_other_lic_present,is_copyright_present=False,False,False,False
        for line in lines:
            line_trimmed = line.strip()
            if line_trimmed == "":
                continue
            if line_trimmed == MAIN_LICENSES:
                is_main_lic_present=True
                continue
            if line_trimmed == OTHER_LICENSES:
                is_other_lic_present=True
                continue
            if line_trimmed == ACKNOWLEDGEMENTS:
                is_ack_present=True
                continue
            if line_trimmed == COPYRIGHT_NOTICES:
                is_copyright_present=True
                continue

        # TITLE SECTION
        name=""
        is_start=True
        license_heading=False
        master_line_count=-1
        while True :
            master_line_count = master_line_count + 1
            stripped_line=lines[master_line_count].strip()
            if stripped_line == "":
                continue
            if stripped_line == start_text or stripped_line == COPYRIGHT_NOTICES:
                if is_start:
                    is_start=False
                    continue
                else:
                    break
            if stripped_line == end_text:
                continue
            name=stripped_line
        bom.name=name
        print(str(count+1)+": ==============processing "+bom.name)



        # MAIN LICENSE SECTION
        if is_main_lic_present:
            main_lic=list()
            is_start=True
            license_heading=False
            license=License()
            master_line_count=master_line_count-3
            while True:
                master_line_count = master_line_count + 1
                stripped_line=lines[master_line_count].strip()
                if stripped_line == "":
                    continue
                if stripped_line == start_text or stripped_line == COPYRIGHT_NOTICES:
                    if is_start:
                        is_start=False
                        continue
                    else:
                        break
                # print(stripped_line)
                if stripped_line == MAIN_LICENSES:
                    continue

                if stripped_line == end_text:
                    main_lic.append(license)
                    license_heading = True
                    license=License()
                    continue
                
                if license_heading:
                    license.name=stripped_line
                    license_heading = False

                if not license_heading:
                    license.text+=stripped_line+'\n'
            bom.main_lic=main_lic[2:]
            # print(bom.main_lic)
        else:
            print(bom.name+": Main license section is not Present")

        # OTHER LICENSES SECTION
        if is_other_lic_present:
            other_lic=list()
            is_start=True
            license_heading=False
            license=License()
            master_line_count=master_line_count-3
            while True:
                master_line_count = master_line_count + 1
                stripped_line=lines[master_line_count].strip()
                if stripped_line == "":
                    continue
                if stripped_line == start_text or stripped_line == COPYRIGHT_NOTICES:
                    if is_start:
                        is_start=False
                        continue
                    else:
                        break
                if stripped_line == OTHER_LICENSES:
                    continue
                if stripped_line == end_text:
                    other_lic.append(license)
                    license_heading = True
                    license=License()
                    continue
                if license_heading:
                    license.name=stripped_line
                    license_heading = False
                if not license_heading:
                    license.text+=stripped_line+'\n'
            bom.other_lic=other_lic[2:]
            # print(bom.other_lic)
        else:
            print(bom.name+": Other license section is not Present")

        # ack SECTION
        if is_ack_present:
            ack=list()
            is_start=True
            license_heading=False
            license=License()
            master_line_count=master_line_count-3
            while True:
                master_line_count = master_line_count + 1
                stripped_line=lines[master_line_count].strip()
                if stripped_line == "":
                    continue
                if stripped_line == start_text or stripped_line == COPYRIGHT_NOTICES:
                    if is_start:
                        is_start=False
                        continue
                    else:
                        break
                if stripped_line == ACKNOWLEDGEMENTS:
                    continue
                if stripped_line == end_text:
                    ack.append(license)
                    license_heading = True
                    license=License()
                    continue
                if license_heading:
                    license.name=stripped_line
                    license_heading = False
                if not license_heading:
                    license.text+=stripped_line+'\n'
            bom.ack=ack[2:]
            # print(bom.ack)
        else:
            print(bom.name+": Ack license section is not Present")


        # COPYRIGHT SECTION
        if is_copyright_present:
            copyright=list()
            is_start=True
            license_heading=False
            license=License()
            master_line_count=master_line_count-1
            while master_line_count < total_len-1 :
                master_line_count = master_line_count + 1
                stripped_line=lines[master_line_count].strip()
                if stripped_line == "":
                    continue
                if stripped_line == start_text or stripped_line == COPYRIGHT_NOTICES:
                    if is_start:
                        is_start=False
                        continue
                    else:
                        break
                if stripped_line == COPYRIGHT_NOTICES:
                    continue
                copyright.append(stripped_line)
            bom.copyright=copyright
            # print(bom.copyright)
        else:
            print(bom.name+": Copyright section is not Present")

        sbom.boms.append(bom)

    print(len(sbom.boms))
    return sbom



def main():
    this_package = __package__

    if os.path.exists("reports"):
        shutil.rmtree("reports", ignore_errors=True)


    if not os.path.exists("reports"):
        os.makedirs("reports")

    parser = argparse.ArgumentParser()
    # parser.add_argument("api_url")
    # parser.add_argument("token")
    parser.add_argument("folder_id",help="get the folder id from the fossology. organize > folders > Edit properties > select the folder to edit >check the folder id form url")
    parser.add_argument("clearing_status",help="closed , open, inprogress, rejected")
    parser.add_argument("userid",help="all, or give single specific user id")
    parser.add_argument("since_yyyy_mm_dd",help="files uploaded date from 2024-02-01s ")
    parser.add_argument("report_format",help="readmeoss,spdx2,spdx2tv,dep5,unifiedreport")
    parser.add_argument('--sbom', action=argparse.BooleanOptionalAction,help='create sbom')
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
                if args.sbom and report_format.lower() != "readmeoss":
                    f.generate_and_get_desired_report_for_uploadid(upload_id=upload.id, report_format=ReportFormat("readmeoss"))
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
            if args.sbom and report_format.lower() != "readmeoss":
                f.generate_and_get_desired_report_for_uploadid(upload_id=upload.id, report_format=ReportFormat("readmeoss"))

    sbom = SBOM()
    if args.sbom:
        sbom=sbomFunc()
        current_directory = os.getcwd()
        sbom_file_location = os.path.join(current_directory,"NOTICE-SBOM.txt")
        if os.path.exists(sbom_file_location):
            os.remove(sbom_file_location)
        f = open(sbom_file_location, "a")
        current_year = datetime.now().year
        f.write("Copyright @ "+str(current_year)+"\n")
        f.write("\n")
        f.write("Project Name:\n")
        f.write("Project Version:\n")

        # components section
        f.write("\n")
        f.write("Components:\n")
        f.write("\n")

        for count,bom in enumerate(sbom.boms,1):
            name = bom.name
            main_lic = ""
            m_lics = bom.main_lic
            firsttime=True
            if m_lics is not None:    
                for lic in m_lics:
                    if firsttime:
                        firsttime=False
                        main_lic=lic.name
                    main_lic=main_lic+", "+lic.name
                f.write(str(count)+" "+name+" ["+main_lic+"]\n")

# Other license section
        f.write("\n")
        f.write("Other licenses:\n")
        f.write("\n")

        for count,bom in enumerate(sbom.boms,1):
            name = bom.name
            other_lic = ""
            o_lics = bom.other_lic
            firsttime=True
            if o_lics is not None:        
                for lic in o_lics:
                    if firsttime:
                        firsttime=False
                        other_lic=lic.name
                    other_lic=other_lic+", "+lic.name
                f.write(str(count)+" "+name+" ["+other_lic+"]\n")

        # Acknowledgement section
        f.write("\n")
        f.write("Acknowledgements:\n")
        f.write("\n")

        for count,bom in enumerate(sbom.boms,1):
            name = bom.name
            ack = ""
            ack_lics = bom.ack
            firsttime=True
            if ack_lics is not None:    
                for lic in ack_lics:
                    if firsttime:
                        firsttime=False
                        ack=lic.name
                    ack=ack+", "+lic.name
                f.write(str(count)+" "+name+" ["+ack+"]\n")

        # copyright section
        f.write("\n")
        f.write("Copyrights:\n")
        f.write("\n")
        for count,bom in enumerate(sbom.boms,1):
            name = bom.name
            f.write(str(count)+" "+name+":\n")
            copyrights = bom.copyright
            for copyright in copyrights:
                f.write("   "+copyright+"\n")

        # License section
        f.write("\n")
        f.write("LICENSES:\n")
        f.write("\n")

        for count,bom in enumerate(sbom.boms,1):
            name = bom.name
            f.write(str(count)+" "+name+":\n")
            n=len(str(count)+" "+name)
            line="="*n
            f.write(line+"\n")

            main_lics = bom.main_lic
            if main_lics is not None:
                for c_m_lic,m_lic in enumerate(main_lics,1):
                    f.write(str(count)+"."+str(1)+"."+str(c_m_lic)+" "+m_lic.name+"\n")
                    f.write(m_lic.text+"\n")
                    f.write("---\n")
                    f.write("\n")
            othr_lics = bom.other_lic
            if othr_lics is not None:
                for c_o_lic,o_lic in enumerate(othr_lics,1):
                    f.write(str(count)+"."+str(2)+"."+str(c_o_lic)+" "+o_lic.name+"\n")
                    f.write(o_lic.text+"\n")
                    f.write("---\n")
                    f.write("\n")
            acks = bom.ack
            if acks is not None:
                for c_ack,ack in enumerate(acks,1):
                    f.write(str(count)+"."+str(3)+"."+str(c_ack)+" "+ack.name+"\n")
                    f.write(ack.text+"\n")
                    f.write("---\n")
                    f.write("\n")
            f.write("------------\n")
            f.write("\n")
        f.close()


def capitalize(line):
    return ' '.join(s[:1].upper() + s[1:] for s in line.split(' '))

if __name__ == "__main__":
    main()
