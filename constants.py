
#=========================================================#
#                      FIXED                              #                           
#=========================================================#

SESSION_TOKEN="session_token"
USER_ID="user_id"




#=========================================================#
#                      EXAM CENTER ADD                    #                           
#=========================================================#

Govt=1
Aided=2
Un_Aided=3

error={'status':"Fail",'message':'Bad request','data':[]}
emailExist={'status':"Fail","message":"Email already exists","data":[]}
codeExist={'status':"Fail","message":"Exam code already exists","data":[]}
invalid={'status':"Fail","message":"Invalid user","data":[]}
examcenterExist={'status':"Fail","message":"Exam_center already exists","data":[]}
empidExist={'status':"Fail","message":"Employee id already exist","data":[]}
deleteError={'status':"Fail","message":"Can't be deleted,exam center is already mapped","data":[]}
centerFetch={"status":"Success","message":"Successfully fetched"}
centerAdd={"status":"Success","message":"Successfully added new center"}
centerAllFetch={"status":"Success","message":"Successfully fetched"}
centerDelete={"status":"Success","message":"Successfully Deleted the exam center"}
centerUpdate={"status":"Success","message":"Successfully updated"}
codeExist_exam={'status':"Fail","message":"Exam code already exists","data":[]}

#=========================================================#
#                      DESIGNATION ADD                    #                           
#=========================================================#
desExist={"status":"Fail","message":"Designation details already exists","data":[]}
codeExist_des={"status":"Fail","message":" Designation code already exists","data":[]}
nameExist_des={"status":"Fail","message":" Designation name already exists","data":[]}
successDes={"status":"Success","message":"Designation details successfully added"}
des_update_success ={"status":"Success","message":"Successfully updated the designation details"}
successDet={"status":"Success","message":"Successfully deleted the designation details"}
desdeleteError={'status':"Fail","message":"Can't be deleted,designation details is already mapped","data":[]}


#=========================================================#
#                      DEGREE ADD                         #                           
#=========================================================#
degdeleteError={"status":"Fail","message":"Can't be deleted,degree details is already mapped","data":[]}
success={"status":"Success","message":"successfull"}
successDeg={"status":"Success","message":"Degree details successfully added"}
fetch={"status":"Success","message":"Successfully fetched data"}
degExist={"status":"Fail","message":"Degree details already exists","data":[]}
invalid={"status":"Fail","message":"Invalid id","data":[]}
error={"status":"Fail","message":"Bad gateway","data":[]}
codeExist={"status":"Fail","message":" code already exists","data":[]}
delete_success={"status":"Success","message":"Successfully deleted the degree details"}
successUpd ={"status":"Success","message":"Successfully updated the degree details"}
nameExist={"status":"Fail","message":" Degree name already exist","data":[]}
#=========================================================#
#                      PROGRAM ADD                        #                           
#=========================================================#
PRG_ID="prg_id"
PRG_NAME="prg_name"
PRG_CODE ="prg_code"
DEG_ID="deg_id"
PRG_STATUS ="status"

prg_err_post_id = {"status": "Fail","message": "Invalid program id", "data": []}
prg_err_post_add = {"status": "Fail","message": "Program with the given details already exist", "data":[]}
Prg_exist_err={"status": "Fail","message": "Program with the same name already exist", "data": []}
prg_code_exist_err={"status": "Fail","message": "Program with the same code already exist", "data": []}
err_exception = {"status": "Fail", "message": "Bad request","data":[]}
prg_err_put ={"status": "Fail","message": "Invalid Program id or degree id", "data":[]}
prg_err_delete = {"status": "Fail","message": "Invalid program id", "data":[]}

prg_sucss_post_id ={"status": "Success", "message": "Successfull","data":[]}
prg_sucss_post = {"status": "Success","message": "Program details successfully added","data":[]}
prg_sucss_get = {"status": "Success","message": "Program details fetch successfully", "data": []}
prg_sucss_put = {"status": "Success","message": "Successfully updated the program details", "data": []}
prg_sucss_delete = {"status": "Success","message":"Successfully deleted the program details","data":[]}

#=========================================================#
#                      BRANCH ADD                         #                           
#=========================================================#

BRANCH_ID="branch_id"
BRANCH_NAME="branch_name"
BRANCH_CODE="branch_code"
DEGREE_ID="degree_id"
DEGREE_NAME="degree_name"
BRANCH_STATUS="status"
br_success_single_fetch ={"status":"Success","message":"Successfull"}
br_invalid_id ={"status":"Fail","message":"Invalid branch id","data":[]}
br_exist_name ={"status":"Fail","message":"Branch name already exists","data":[]}
br_exist_code ={"status":"Fail","message":"Branch code already exists","data":[]}
br_success_add ={"status":"Success","message":"Branch details successfully added"}
br_bad_request ={"status":"Fail","message":"Bad request","data":[]}  
brdeleteError={"status":"Fail","message":"Can't be deleted,branch details is already mapped","data":[]}
br_success_edit ={"status":"Success","message":"Successfully updated the branch details"}
br_fetch ={"status":"Success","message":"Successfully fetched"}
br_success_delete={ "status":"Success","message":"Successfully deleted the branch details"}



#=========================================================#
#                      SECTION ADD                        #                           
#=========================================================#

SECTION_ID="section_id"
SECTION_NAME="section_name"
SECTION_CODE="section_code"


sec_success_single_fetch={"status":"Success","message":"Successfull"}
sec_invalid_id={"status":"Fail","message":"Invalid section id","data":[]}
sec_exist_name={"status":"Fail","message":"Section name already exists","data":[]}
sec_exist_code={"status":"Fail","message":"Section code already exists","data":[]}
sec_success_add={"status":"Success","message":"Section details successfully added"}
sec_fetch={"status":"Success","message":"Successfully fetched"}  
sec_success_edit= { "status":"Success","message":"Successfully updated the section details"}
sec_bad_request ={"status":"Fail","message":"Bad request","data":[]}
sec_success_delete={ "status":"Success","message":"Successfully deleted the section details"}

#=========================================================#
#                      ACTION ADD                         #                           
#=========================================================#
DATA="data"
ACTION_CODE="action_code"
ACTION_NAME="action_name"
action_fetch={"status":"Success","message":"Successfully fetched data"}
action_bad_request={"status":"Fail","message":"Bad request","data":[]}

#=========================================================#
#                      ROLE ADD                           #                           
#=========================================================#
DATA="data"
ROLE_ID="role_id"
ROLE_NAME="role_name"
ROLE_STATUS='role_status'
ROLE_PERMISSION="role_permission"
ROLE_META="role_meta"
STATUS="active"
role_fetch={"status":"Success","message":"Successfully fetched data"}
role_add={"status":"Success","message":"New role details successfully added "}
role_update={"status":"Success","message":"Successfully updated the role details"}
role_delete={"status":"Success","message":"Successfully deleted the role details"}
role_delete_fail={"status":"Success","message":"Sorry can't delete the role","data":[]}
role_invalid_id={"status":"Fail","message":"Invalid id"}
role_bad_request={"status":"Fail","message":"Bad request","data":[]}
role_exist_err={"status":"Fail","message":"Role already exist","data":[]}

#=========================================================#
#                      USER ADD                           #                           
#=========================================================#
userSingleFetch={"status":"Success","message":"Successfully fetched"}
adduserSuccess={"status":"Success","message":"Successfully added new user"}
userUpdate={"status":"Success","message":"Successfully updated the user details"}
userAdd={"status":"Success","message":"Successfully added"}
userFetch={"status":"Success","message":"Successfully fetched"}
userdeleteSuccess={"status":"Success","message":"Successfully deleted the user details"}
userdeleteError={"status":"Fail","message":"Can't Deleted","data":[]}

#=========================================================#
#                      INVIGILATOR ADD                    #                           
#=========================================================#
CENTER_ID='center_id'
TEACH_CAT='001'

INV_NAME="invigilator_name"
EMPLOYEE_ID="emp_id"
EXAM_NAME="exam_name"
TEACHER_ROLE="teacher"
TEACHER_ID="teacher_id"
TEACHER_NAME="teacher_name"


msg_400 = {'status':"Fail",'message':'Bad request', 'data':[]}
success = {"status":"Success","message":"Successfully fetched"}
success1 = {"status":"Success","message":"Successfully added"}
deleted = {"status":"Success","message":"Successfully deleted"}
inv_invalid_id = {'status':"Fail","message":"Invalid id",'data':[]}
no_invegilator = {'status':"Fail","message":"No Invigilator"}
invg_delete_error={"status":"Fail","message":"Can't delete the invigilator"}
no_exist = {"status":"Fail","message":"Can't be deleted,degree details is already mapped"}
already_exists = {"status":"Fail","message":"Already Exists"}

invig_not_exist={"status":"Success","message":"No invigilator exist","data":[]}
teacher_fetch={"status":"Success","message":"Successfully fetched"}
teacher_fetch_empty={"status":"Success","message":"Successfully fetched",DATA:[]}
invig_already_exists = {"status":"Fail","message":"Sorry invigilator already assigned"}

invdeleteError={"status":"Fail","message":"Can't be deleted, is already mapped","data":[]}


#=========================================================#
#                      EXAM HALL ADD                      #                           
#=========================================================#
ROOM_ID="room_id"
CEN_ID="cen_id"
ROOM_NO="room_no"
ROOM_CAPACITY="room_capacity"
BUILDING_NAME="building_name"
ROOM_ALLOTED="room_alloted"
ROOM_FREE="room_free"
ROOM_STATUS="status"


room_err_post_id = {"status": "Fail", "message": "Invalid room id"}
room_err_post_add = {"status": "Fail","message": "Exam hall already exists", "data": []}
room_err_put = {"status": "Fail","message": "Invalid room id or center id", "data":[]}
room_err_delete = {"status": "Fail","message": "Invalid room id or centre id", "data":[]}

room_sucss_post_id = {"status": "Success", "message": "Successfull", "data": []}
room_sucss_post = {"status": "Success","message": "Exam room  details successfully added", "data":[]}
room_sucss_get = {"status": "Success","message": "Exam room details fetch successful", "data":[]}
room_sucss_put = {"status": "Success","message": "Successfully updated the exam room details", "data":[]}
room_sucss_delete = {"status": "Success","message": "Successfully deleted the exam room details", "data":[]}

#=========================================================#
#                     EXAM HALL ALLOTMENT ADD             #                           
#=========================================================#
EXAM_HALL_ID="hall_id"
EXAM_ID="exam_id"
PROGRAM_ID="program_id"
COURSE_ID="course_id"
EXAM_DATE="exam_date"
STUDENT_COUNT="std_count"

EXAM_HALL_NAME="exam_hall_name"
EXAM_HALL_NUMBER="exam_hall_number"
EXAM_HALL_CAPACITY="exam_hall_capacity"
EXAM_HALL_ALLOTTED="exam_hall_allotted"
EXAM_HALL_FREE="exam_hall_free"
ALLOTED_STUDENT="alloted_student"

hall_allotment_invalid_data={"status": "Fail","message": "Invalid data", "data":[]}
hall_allotment_count_invalid={"status": "Fail","message": "Required student count is greater than free space try another hall", "data":[]}
hall_allotment_bad_request={"status":"Fail","message":"Bad request","data":[]}
hall_allotment_fetch={"status":"Success","message":"Successfully fetched data"}
hall_allotment_success={"status":"Success","message":"Successfully alloted students to the exam hall"}
hall_allotment_exist={"status": "Fail","message": "Students are already alloted for the selected hall", "data":[]}
no_inv_allot_err={"status": "Fail","message": "No hall is alloted for this invigilator", "data":[]}
no_student_err={"status": "Fail","message": "No student in the selected exam", "data":[]}
no_student_allot_err={"status": "Fail","message": "No students are alloted in the selected exam", "data":[]}


#=========================================================#
#      CHIEF SUPERINTENDENT ORDER GENERATION              #                           
#=========================================================#
ORDER_NUMBER="order_number"
ORDER_DATE="order_date"
EMP_ID_LIST="emp_id_list"
PRGID="-1"
ORDER_ID="order_id"
EMPLOYEE_NAME="employee_name"
EXAM_START_DATE="exam_start_date"
EXAM_END_DATE="exam_end_date"

exam_exist={'status':"Fail","message": "Order already generated for the selected exam","data":[]}
cs_not_exist={'status':"Fail","message": "There is no Chief Superintedent is appointed for the selected exam","data":[]}

csFetch={"status":"Success","message":"Successfully fetched data"}


#=========================================================#
#                      SESSION_CHECK                      #                           
#=========================================================#

session_invalid={"status":"Fail","message":"Unauthorised access","data":[]}
#=========================================================#
#                    USER LOGIN                           #                           
#=========================================================#
USER_NAME="user_name"
USER_PSWD="user_password"
SES_DEVTYPE="ses_devtype"
INACTIVE="inactive"
ACTION_LIST="action_list"
logoutsuccess={"status":"Success","message":"Logout successfully","data":[]}
loginSuccess={"status":"Success","message":"Successfully login"}
loginerror={"status":"Fail","message":"Invalid user","data":[]}
invalidInvg={"status":"Fail","message":"Invalid invigilator","data":[]}

#=========================================================#
#               FORGOT PASSWORD                           #                           
#=========================================================#
EMAIL_ID="email_id"
PASSWORD="password"
CODE="code"
NEW_PASSWORD="new_password"
OLD_PASSWORD="old_password"
emailcodeexpired={"status":"Fail","message":"Code expired","data":[]}
emailcodeverified={"status":"Success","message":"Code verified","data":[]}
emailcodeinvalid={"status":"Fail","message":"Invalid code","data":[]}
pwdupdated={"status":"Success","message":"Password updated","data":[]}
invalidemail={'status':"Fail","message": "Invalid Email","data":[]}
mailsent={"status":"Success","message":" Mail send","data":[]}




#=========================================================#
#                   COURSE                                #                           
#=========================================================#
COURSE_NAME="course_name"
bad_request={"status":"Fail","message":"Bad request","data":[]}
course_fetch_success={"status":"Success","message":"Successfully fetched"}

#=========================================================#
#                EXAM SPECIFIC COURSE                     #                           
#=========================================================#
exam_course_success={"status":"Success","message":"Successfully fetched"}


#=========================================================#
#         CENTER SPECIFIC CAMP LIST STARTS                #                           
#=========================================================#

cenfetch={"status":"Success","message":"Successfull"}



#=========================================================#
#                   USER ROLE                             #                           
#=========================================================#


cenfetch={"status":"Success","message":"Successfull"}



#========================================================#
#                    MODULE II                           #
#========================================================#
#========================================================#
#             ARTICLE TRACKING MANAGEMENT                #
#========================================================#

#=========================================================#
#         ARTICLE DISTRIBUTION ADD                        #                           
#=========================================================#

DATA="data"
ART_ID="art_id"
CEN_NAME="cen_name"
ART_CODE="art_code"
EXAM_ID="exam_id"
EXAM_NAME="exam_name"
ART_STATUS="art_status"
ART_APPROVAL_CODE="art_approval_key"
DATE_SEND="date_send"
DATA_RECEIVE="date_received"
SEND="send"



session_invalid={"status":"Fail","message":"Unauthorised access","data":[]}
ARTDIC={"1":'AnswerScript',"2":'Sticker',"3":'AnswerScript|Sticker',"4":'Forms',"5":'AnswerScript|Forms',
"6":'Sticker|Forms',"7":'AnswerScript|Sticker|Forms',"8":'Stationary',"9":'AnswerScript|Stationary',"10":'Sticker|Stationary',
"11":'AnswerScript|Sticker|Stationary',"12":'Forms|Stationary',"13":'AnswerScript|Forms|Stationary',"14":'Sticker|Forms|Stationary',
"15":'AnswerScript|Sticker|Forms|Stationary',"16":'Qpcover',"17":'AnswerScript|Qpcover',"18":'Sticker|Qpcover',
"19":'AnswerScript|Sticker|Qpcover',"20":'Forms|Qpcover',"21":'AnswerScript|Forms|Qpcover',"22":'Sticker|Forms|Qpcover',
"23":'AnswerScript|Sticker|Forms|Qpcover',"24":'Stationary|Qpcover',"25":'AnswerScript|Stationary|Qpcover',"26":'Sticker|Stationary|Qpcover',
"27":'AnswerScript|Sticker|Stationary|Qpcover',"28":'Forms|Stationary|Qpcover',"29":'AnswerScript|Forms|Stationary|Qpcover',
"30":'Sticker|Forms|Stationary|Qpcover',"31":'AnswerScript|Sticker|Forms|Stationary|Qpcover',"32":'NominalRole',"33":'AnswerScript|NominalRole',
"34":'Sticker|NominalRole',"35":'AnswerScript|Sticker|NominalRole',"36":'Forms|NominalRole',"37":'AnswerScript|Forms|NominalRole',
"38":'Sticker|Forms|NominalRole',"39":'AnswerScript|Sticker|Forms|NominalRole',"40":'Stationary|NominalRole',"41":'AnswerScript|Stationary|NominalRole',
"42":'Sticker|Stationary|NominalRole',"43":'AnswerScript|Sticker|Stationary|NominalRole',"44":'Forms|Sticker|Stationary|NominalRole',
"45":'AnswerScript|Forms|Sticker|Stationary|NominalRole',"46":'Sticker|Forms|Stationary|NominalRole',"47":'AnswerScript|Sticker|Forms|Stationary|NominalRole',
"48":'Qpcover|NominalRole',"49":'AnswerScript|Qpcover|NominalRole',"50":'Sticker|Qpcover|NominalRole',"52":'Forms|Qpcover|NominalRole',
"53":'AnswerScript|Forms|Qpcover|NominalRole',"54":'Sticker|Forms|Qpcover|NominalRole',"55":'AnswerScript|Sticker|Forms|Qpcover|NominalRole',
"56":'Stationary|Qpcover|NominalRole',"57":'AnswerScript|Stationary|Qpcover|NominalRole',"58":'Sticker|Stationary|Qpcover|NominalRole',
"59":'AnswerScript|Sticker|Stationary|Qpcover|NominalRole',"60":'Forms|Stationary|Qpcover|NominalRole',"61":'AnswerScript|Forms|Stationary|Qpcover|NominalRole',
"62":'Sticker|Forms|Stationary|Qpcover|NominalRole',"63":'AnswerScript|Sticker|Forms|Stationary|Qpcover|NominalRole' }

# ARTDIC={"1":'AnswerScript',"2":'Sticker',"3":'AnswerScript|Sticker',"4":'Forms',"5":'AnswerScript|Forms',
# "6":'Sticker|Forms',"7":'AnswerScript|Sticker|Forms',"8":'Stationary',"9":'AnswerScript|Stationary',"10":'Sticker|Stationary',
# "11":'AnswerScript|Sticker|Stationary',"12":'Forms|Stationary',"13":'AnswerScript|Forms|Stationary',"14":'Sticker|Forms|Stationary',
# "15":'AnswerScript|Sticker|Forms|Stationary',"16":'Qpcover',"17":'AnswerScript|Qpcover',"18":'Sticker|Qpcover',
# "19":'AnswerScript|Sticker|Qpcover',"20":'Forms|Qpcover',"21":'AnswerScript|Forms|Qpcover',"22":'Sticker|Forms|Qpcover',
# "23":'AnswerScript|Sticker|Forms|Qpcover',"24":'Stationary|Qpcover',"25":'AnswerScript|Stationary|Qpcover',"26":'Sticker|Stationary|Qpcover',
# "27":'AnswerScript|Sticker|Stationary|Qpcover',"28":'Forms|Stationary|Qpcover',"29":'AnswerScript|Forms|Stationary|Qpcover',
# "30":'Sticker|Forms|Stationary|Qpcover',"31":'AnswerScript|Sticker|Forms|Stationary|Qpcover',"32":'NominalRole' }



art_success_single_fetch={"status":"Success","message":"Successfull"}
cen_invalid_id={"status":"Fail","message":"Invalid centre id","data":[]}
cen_exist_id ={"status":"Fail","message":"For selected center,article is already assign","data":[]}
exam_exist_id ={"status":"Fail","message":"Exam id already exists","data":[]}
art_success_add ={"status":"Success","message":"Article list successfully added"}
art_fetch ={"status":"Success","message":"Successfully fetched"} 
art_fetch1 ={"status":"Success","message":"Successfully fetched test"} 
art_exist_code ={"status":"Fail","message":"Article code already exists","data":[]}
art_success_edit ={"status":"Success","message":"Successfully updated the article list"}
art_invalid_id={"status":"Fail","message":"Invalid article id","data":[]}
exam_invalid_id={"status":"Fail","message":"Invalid exam id","data":[]}
art_success_delete={ "status":"Success","message":"Successfully deleted the article list"}
art_bad_request ={"status":"Fail","message":"Bad request","data":[]} 
art_success_mail={ "status":"Success","message":"Mail successfully send"}  
invalid_id={"status":"Fail","message":"Invalid id","data":[]}


#=========================================================#
#                      Routeofficer Login                 #                           
#=========================================================#

USERNAME="username"
# PASSWORD="password"
ROLE_ID="role_id"
SES_DEVTYPE="ses_devtype"
RECIEVED="received"
ROUTE_OFFICER="routeofficer"
loginSuccess={"status":"Success","message":"Login successful"}
invalidUser={"status": "Fail", "message": "Invalid username or password"}
error={"status":"Fail","message":"Bad request","data":[]}


#=========================================================#
#                      Routeofficer Logout                #                           
#=========================================================#


logoutSuccess={"status":"Success","message":"Logout successful"}


#=========================================================#
#                      Forgot Password                    #                           
#=========================================================#


EMAIL_ID="email_id"
PASSWORD="password"
CODE="code"
emailcodeexpired={"status":"Fail","message":"code expired"}
emailcodeverified={"status":"Success","message":"code verified","data":[]}
emailcodeinvalid={"status":"Fail","message":"invalid code"}
invalidEmail={"status": "Fail", "message": "Invalid email"}
mailSent={"status":"Success","message":"Mail successfully send"}
passwdUpdate={"status":"Success","message":"Password updated successfully","data":[]}
passwdUpdate1={"status":"Success","message":"Password updated successfully","data":[]}
OLD_PASSWORD="old_password"
NEW_PASSWORD="new_password"


#=========================================================#
#                  APPROVAL CODE VERIFY                   #                           
#=========================================================#

EXAM_ID="exam_id"
CENTER_ID="center_id"
APPROVE_KEY="art_approval_key"
approveSuccess={"status":"Success","message":"Successfully received the article"}
invalidDet={"status": "Fail", "message": "Not successfully received the article"}



#========================================================#
#                    MODULE III                          #
#========================================================#
#========================================================#
#                 EXAMINATION MANAGEMENT                 #
#========================================================#


#=========================================================#
#                        EXAM ADD                         # 
#=========================================================#

EXAM_ID="exam_id"
EXAM_CODE="exam_code"
EXAM_NAME="exam_name"
START_DATE="start_date"
END_DATE="end_date"
STATUS1="status"
examNameError={'status':"Fail","message":"Please enter the exam_name","data":[]}
examName={'status':"Fail","message":"Exam_name already exists","data":[]}
examCode={'status':"Fail","message":"Exam_code already exists","data":[]}
examSuccess = {"status": "Success", "message":"Successfully added"}
examFetch= {"status": "Success", "message": "Successfully fetched"}
examSingleFetch= {"status": "Success", "message": "Successfull fetched"}
invalidexam = {"status": "Fail", "message": "Invalid exam_id","data":[]}
examDeleted = {"status":"Success","message":"Successfully deleted"}
examUpdate={"status":"Success","message":"Successfully updated"}
examDeleteError={'status':"Fail","message":"Can't delete","data":[]}

#=========================================================#
#                 CAMP ADD                                #             
#=========================================================#

CAMP_ID="camp_id"
CAMP_NAME="camp_name"
CENTRE_ID="centre_id"
EXAM_ID="exam_id"
EXAM_NAME="exam_name"
PRG_ID="prg_id"
PRG_NAME="prg_name"
DEG_ID="deg_id"
DEG_NAME="deg_name"
START_DATE="start_date"
END_DATE="end_date"
CAMP_STATUS="camp_status"
CEN_DISTRICT="cen_dist"


camp_success_single_fetch={"status":"Success","message":"Successfull"}
invalid_id={"status":"Fail","message":"Invalid data","data":[]}
camp_invalid_id={"status":"Fail","message":"Invalid camp id","data":[]}
cen_invalid_id={"status":"Fail","message":"Invalid centre id","data":[]}
prg_invalid_id={"status":"Fail","message":"Invalid program id","data":[]}
cen_exist_id ={"status":"Fail","message":"Centre id already exists","data":[]}
camp_success_add ={"status":"Success","message":"Camp details successfully added"}
cen_exam_prg_exist_id ={"status":"Fail","message":"Centre id or Exam id or Program id already exists","data":[]}
exam_exist_id ={"status":"Fail","message":"Exam id already exists","data":[]}
prg_exist_id ={"status":"Fail","message":"program id already exists","data":[]}
camp_success_edit ={"status":"Success","message":"Successfully updated the camp details"}
camp_fetch ={"status":"Success","message":"Successfully fetched"} 
camp_success_delete={ "status":"Success","message":"Successfully deleted the camp details"}
camp_date_err={ "status":"Fail","message":"Start date of camp is before the end date of the exam","data":[]}


#=========================================================#
#              GENERAL INFO                               #                           
#=========================================================#
# INVIG_ID="invigilator_id"
nocs={"status":"Fail","message":"There is no chief superintendent for this invigilator","data":[]}
CHIEFSUPERINTENDENT="chiefsuperintendent"
generalinfoFetch= {"status": "Success", "message": "Successfully fetched"}
invaliddata={"status":"Fail","message":"Invalid data","data":[]}
generalInfoUnavilable= {"status": "Fail", "message": "General information is not avilable","data":[]}
RESULT_DATA="resultData"
FN="FN"
AN="AN"

# generalinfoFetch= {"status": "Success", "message": "Successfully fetched"}
#=========================================================#
#      ACCESS KEY GENERATION                              #                           
#=========================================================#
EXAM_ID="exam_id"
COURSE_ID="course_id"
CEN_ID="cen_id"
DATE="date"
ACCESS_CODE="access_code"
EXAM_SECTION="exam_section"

emptyStudents={"status":"Fail","message":"There is no  students for this selected exam ","data":[]}
noAccesskey={"status":"Fail","message":"There is no access key is generated for the selected center","data":[]}
invalidcs={"status":"Fail","message":"Invalid cs_id","data":[]}
noExam={"status":"Fail","message":"There is no exam on this date","data":[]}
accesskeysuccess= {"status": "Success", "message":"Successfully added"}
accessCenter={'status':"Fail","message":"Access_code  already generated"}
accesscodeexpired={"status":"Fail","message":"code expired","data":[]}
codeVsuccess={"status":"Success","message":"Successfully verified","data":[]}
incorrectcode={"status":"Fail","message":"Incorrect access_code","data":[]}
accesskeyFetch={"status": "Success", "message":"Successfully fetched"}

CENTER_NAME="center_name"
INVIG_ID="invigilator_id"
INVIG_NAME="invigilator_name"
COURSE_NAME="course_name"
CENTER_NAME="center_name"
CS_ID="cs_id"
CS_NAME="cs_name"

#=========================================================#
#     INVIGILATOR ABSENTEE STATEMENT GENERATION           #                           
#=========================================================#
PROGRAM_ID="program_id"
CENTER_ID="center_id"
COURSE_ID="course_id"
STUDREG="student_reg"
STUDNAME="student_name"
FALSENO="false_number"
ABSENTEE_LIST="absentee_list"
PRESENT_LIST="present_list"
SMP_STATUS="smp_status"
STUDENT_ID="student_id"
INVIG_STATUS=1
CS_STATUS=2
COMPLETE_STUD_LIST="complete_stud_list"
PROGRAM_NAME="program_name"
MAPPED_LIST="mapped_list"
ALLOTED_STUD_LIST="allotted_stud_list"
absenteeUpdate={"status":"Success","message":"Successfully updated"}
falseFetch={"status":"Success","message":"Successfully fetched data"}
invData={"status":"Fail","message":"Invalid data",DATA:{RESULT_DATA:[]}}
invDataAdditional={"status":"Fail","message":"Invalid user",DATA:{RESULT_DATA:[]}}
sessioninvalid={"status":"Fail","message":"Unauthorised access",DATA:{RESULT_DATA:[]}}
errorResponse={'status':"Fail",'message':'Bad request',DATA:{RESULT_DATA:[]}}
ASerror={'status':"Fail",'message':'Absentee statement already generated',DATA:{RESULT_DATA:[]}}
ASinvalidInvg={"status":"Fail","message":"Invalid invigilator",DATA:{RESULT_DATA:[]}}

# PROGRAM_ID="program_id"
# CENTER_ID="center_id"
# COURSE_ID="course_id"
# STUDREG="student_reg"
# STUDNAME="student_name"
# FALSENO="false_number"
# ABSENTEE_LIST="absentee_list"
# PRESENT_LIST="present_list"
# SMP_STATUS="smp_status"
# INVIG_STATUS=1
# CS_STATUS=2

# absenteeUpdate={"status":"Success","message":"Successfully updated"}
# falseFetch={"status":"Success","message":"Successfully fetched data"}
# invData={"status":"Fail","message":"Invalid data",DATA:{RESULT_DATA:[]}}
# invDataAdditional={"status":"Fail","message":"Invalid user",DATA:{RESULT_DATA:[]}}
# sessioninvalid={"status":"Fail","message":"Unauthorised access",DATA:{RESULT_DATA:[]}}
# errorResponse={'status':"Fail",'message':'Bad request',DATA:{RESULT_DATA:[]}}


#=========================================================#
#              CS ABSENTEE SUBMIT                         #
#=========================================================#
STUDREG="student_reg"
STUDNAME="student_name"
FALSENO="false_number"
PRESENT_LIST="present_list"
ABSENTEE_LIST="absentee_list"
SMP_STATUS="smp_status"
CS_STATUS=2
falseFetch={"status":"Success","message":"Successfully fetched data"}
cs_update={"status":"Success","message":"Successfully updated"}
smp_status_none={"status":"Fail","message":"No smp_list","data":[]}
invalid_data={"status":"Fail","message":"No data is available for selected examination","data":[]}
invSubmitError={"status":"Fail","message":"For this selected examination invigilator is not submit the absentee statement","data":[]}
CSerror={"status":"Fail","message":"Absentee statement already generated","data":[]}
invalid_data_err={"status":"Fail","message":"There is no student in selected exam","data":[]}


#=================================================#
#       ASO AS GENERATE                           #
#=================================================#


invalidData={"status":"Fail","message":"Invalid Credentials"}

asoUpdate = {"status": "Success","message": "Absentee statement verified"}
falseFetch = {"status": "Success", "message": "Successfully fetched data"}
noSmp = {"status": "Success", "message": "No smp_list"}
csSubmitError={"status":"Fail","message":"For the selected examination chief superintendent is not submit the absentee statement","data":[]}


#=================================================#
#           ASO ABSENTEE STATEMENT APPROVE        #
#=================================================#

ASO_STATUS = 3
DFM_STATUS = "aso_status"
ASO_VERIFIED_DATE = "aso_verified_date"

absenteeerror={"status":"Fail","message":"There is no absentee statement to the given data" }
falseFetch = {"status": "Success", "message": "Successfully fetched data"}




#=========================================================#
#          SO ABSENTEE STATEMENT GENERATE                 #             
#=========================================================#

SO_STATUS=4
PROGRAM_ID="program_id"
CENTER_ID="center_id"
STUDREG="student_reg"
STUDNAME="student_name"
FALSENO="false_number"
ABSENTEE_LIST="absentee_list"
PRESENT_LIST="present_list"
SMP_STATUS="smp_status"
SO_APPROVED_DATE="so_approved_date"


soUpdate={"status":"Success","message":"Successfully approved"}

soSubmitError={"status":"Fail","message":"For this selected examination Assistant section officer is not submit the absentee statement","data":[]}
falseFetch={"status":"Success","message":"Successfully fetched data"}
noSmp={"status":"Success","message":"No smp_list"}
so_error={"status":"Fail","message":"Absentee statement already generated","data":[]}





#=========================================================#
#                    STUDENT  MAPPING                     #                           
#=========================================================#
EXAM_ID="exam_id"
PAIRED_DATA="paired_data"
STUDENT_REGISTER_NUMBER="student_register_number"
STUDENT_FALSE_NUMBER="student_false_number"
STUDENT_SMP_STATUS="student_smp_status"
STUDENT_NAME="student_name"
UPDATE_DATE="0000-00-00"
UPDATE_ID=0


tmp_map_err={"status":"Fail","message":"You don't have the permission to do the task","data":[]}
tmp_map_exist={"status":"Fail","message":"Already exist","data":[]}
tmp_map_confirm={"status":"Success","message":"Please confirm"}
tmp_map_success={"status": "Success", "message":"Successfully mapped",DATA:{"resultData":[]}}

std_map_success={"status":"Success","message":"Successfully mapped"}

false_already_exist_err={"status":"Fail","message":"Data already exist",DATA:{RESULT_DATA:[]}}

# COURSE_ID="course_id"
# CEN_ID="cen_id"
# DATE="date"
# ACCESS_CODE="access_code"
# accesskeysuccess= {"status": "Success", "message":"Successfully added"}
# accessCenter={'status':"Fail","message":"Access_code  already generated","data":[]}
# accesscodeexpired={"status":"Fail","message":"code expired","data":[]}
# codeVsuccess={"status":"Success","message":"Successfully verified","data":[]}
# incorrectcode={"status":"Fail","message":"Incorrect access_code","data":[]}
# accesskeyFetch={"status": "Success", "message":"Successfully fetched"}
# CENTER_ID="center_id"
# CENTER_NAME="center_name"
# INVIGILATOR_ID="invigilator_id"
# INVIG_NAME="invigilator_name"
# COURSE_NAME="course_name"
# CENTER_NAME="center_name"
# CS="cs_name"

#=========================================================#
#    MAPPING VIEW                                         #                           
#=========================================================#
CHIEF_MARK="chief_mark"
CHAIRMAN_MARK="chairman_mark"
ADDITIONAL_MARK="additional_mark"
STUDENT_DETAILS="student_details"
EXAM_DETAILS="exam_details"
invalidRegnum={"status":"Fail","message":"Invalid register number","data":[]}
noFlaseNumber={"status":"Fail","message":"There is no student mapped for selected exam","data":[]}

#=========================================================#
#             ANSWER SCRIPT DISPATCH                      #
#=========================================================#
ABSENTEE_COUNT="absentee_count"
SMP_COUNT="smp_count"
TOTAL_COUNT="total_count"
ANS_DISPATCH_COUNT="ans_dispatch_count"
ANS_DISPATCH_DATE="ans_dispatch_date"
ANS_DISPATCH_STATUS="ans_dispatch_status"
ans_add_success={"status":"Success","message":"Successfully added","data":[]}
ans_exists_err={"status":"Fail","message":"Data exists","data":[]}
ans_fetch_success={"status":"Success","message":"Successfully fetched data","data":[]}
ans_invalid={"status":"Fail","message":"Invalid id","data":[]}
ansDispatcherr={"status":"Fail","message":"Dispatch count is not equal","data":[]}


#=========================================================#
#          EXAM SPECIFIC PROGRAM LIST                     #                           
#=========================================================#

examfetch={"status":"Success","message":"Successfull"}

#=========================================================#
#          PROGRAM SPECIFIC COURSE STARTS                 #                           
#=========================================================#

prgfetch={"status":"Success","message":"Successfull"}


#========================================================#
#                    MODULE IV                           #
#========================================================#
#========================================================#
#                 EVALUATION MODULE                      #
#========================================================#


#=========================================================#
#                 CHAIRMAN ADD                            #             
#=========================================================#

CHAIRMAN_ID="chairman_id"
CHAIRMAN_NAME="chairman_name"
EXAM_ID="exam_id"
CEN_ID="cen_id"
PGM_ID="pgm_id"
EXPIRE_DATE="expire_date"
CHAIRMAN_STATUS="status"
CHAIRMAN="chairman"
PASS="pass"

cen_exam_prg_exist_id_err={"status":"Success","message":" Chairman already assigned to the selected camp"}
chairman_success_single_fetch={"status":"Success","message":"Successfull"}
chairman_invalid_id={"status":"Fail","message":"Invalid chairman id","data":[]}
chairman_success_add ={"status":"Success","message":"Chairman details successfully added"}
chairman_fetch ={"status":"Success","message":"Successfully fetched"} 
chairman_none={"status":"Fail","message":"No chairman ","data":[]}
chief_exist_id ={"status":"Fail","message":"Can't deleted,There is an chief examiner subordinate under the chairman","data":[]}
addl_exist_id ={"status":"Fail","message":"Additional examiner id exists","data":[]}
chairman_success_delete={ "status":"Success","message":"Successfully deleted the chairman details"}


#=========================================================#
#                  CHIEF EXAMINER ADD                    #                           
#=========================================================#



STAT="status"
CEN_NAME="cen_name"
CAMP_ID="camp_id"
CHIEF_ID="chief_id"
CHIEF_NAME="chief_name"
CHAIRMAN_ID="chairman_id"
CHIEFEXAM_ID="chiefexam_id"
END_DATE="end_date"
CHAIRMAN="chairman"
INACTIVE="inactive"
exists_chiefid={"status":"Fail","message":" Chief is already assigned under selected chairman","data":[]}
addl_exist_error={"status":"Fail","message":"Can't deleted,there is an additional examiner subordinate under the chief examiner","data":[]}
exists_chair={"status":"Fail","message":"chairman exists","data":[]}
chief_single_fetch={"status":"Success","message":"Successfully fetched data"}
chief_invalid_id={"status":"Fail","message":"Invalid chief id","data":[]}
chief_success={"status":"Success","message":"Chief examiner details successfully added"}
chief_fetch={"status":"Success","message":"Successfully fetched data","data":[]}
chief_success_delete={"status":"Success","message":"Successfully deleted the chief examiner details","data":[]}
chief_invalid={"status":"Success","message":"No data","data":[]}
chief_chairman_err={"status":"Fail","message":"Can't Assign Chairman as Chief","data":[]}


#=========================================================#
#                       CAMP OFFICER ADD                                 
#=========================================================#
USERNAME="campofficer_name"
CO_STATUS="status"
CAMP_OFFI_ID="co_id"
CAMPOFFICER="campofficer"
CAMP_OFFICER="camp officer"
CHIEF_SUPTD_ID = "chief_suptd_id"
EXP_DATE ="exp_date"
campofficer_exist={"status": "Fail", "message": "Already assigned camp officer in the camp"}
campofficer_err_post_id = {"status": "Fail", "message": "Invalid Camp Officer id"}
campofficer_exist_err = {"status": "Fail","message": "The Role Already Assigned"}
campofficer_err_post_add = {"status": "Fail","message": "Camp Officer details addition fail", "data": []}
campofficer_err_put = {"status": "Fail","message": "Invalid Camp Officerid", "data": []}
campofficer_err_delete = {"status": "Fail","message": "Invalid Credentials", "data": []}
campofficer_err_exist_delete = {"status": "Fail","message": "The role assigned", "data": []}
camp_not_exist={"status":"FAIL","message":"Camp not exist"}
campofficer_sucss_post_co_id = {"status": "Success","message": "Camp Officer Single Fetch Successful", "data": []}
campofficer_error_post_co_id = {"status": "Fail","message": "Invalid Camp Officer ID", "data": []}
campofficersucss_post = {"status": "Success","message": "Camp officer details successfully added", "data": []}
campofficer_sucss_get = {"status": "Success","message": "Camp Officer details fetch successful", "data": []}
campofficer_sucss_put = {"status": "Success","message": "Successfully updated the camp officer details", "data": []}
campofficer_sucss_delete = {"status": "Success","message": "Successfully deleted the camp officer details", "data": []}
campofficer_error_delete = {"status": "Fail","message": "Invalid Credentials", "data": []}
campofficerError={"status": "Fail", "message": "There is no camp officer in this table", "data": []}
#=========================================================#
#                ADDITIONAL EXAMINER ADD                  #             
#=========================================================#

CHIEF_NAME="chief_name"
CHAIRMAN_NAME="chairman_name"
STAT="status"
EXAM_ID="exam_id"
EXAM_NAME="exam_name"
CEN_NAME="cen_name"
END_DATE="end_date"
INACTIVE="inactive"
CHIEF_ID="chief_id"
ADDITIONAL_ID="additional_id"
ADDITIONAL_NAME="additional_name"
ADDITIONALEXAM_ID="additionalexam_id"
CHIEFEXAMINER="chiefexaminer"
ADDITIONALEXAMINER="additionalexaminer"
TEACHER='teacher'



invalid_addlexam_id={"status":"Fail","message":"Invalid additional exam id","data":[]}
exists_additional={"status":"Fail","message":"Additional examiner exists","data":[]}
exists_chief={"status":"Fail","message":"Invalid chief id","data":[]}
additional_single_fetch={"status":"Success","message":"Successful"}
additional_invalid_id={"status":"Fail","message":"Invalid additional id","data":[]}
additional_success={"status":"Success","message":"Additional examiner added successfully"}
additional_fetch={"status":"Success","message":"Successfully fetched","data":[]}
additional_success_delete={"status":"Success","message":"Successfully deleted the additional examiner details","data":[]}
additional_no_data={"status":"Fail","message":"No data","data":[]}
addl_chief_err={"status":"Fail","message":"Can't Assign Chief examiner as additional examiner","data":[]}

#=========================================================#
#                UNIVERSITY OFFICIALS LIST ADD            #             
#=========================================================#
NON_TEACH="002"
UNIVER_CAT="101"
PUBLIC="public"
uni_fetch={"status":"Success","message":"Successfully fetched"}
#=========================================================#
#                UNIVERSITY OFFICIALS LIST ENDS           #             
#=========================================================#

#=========================================================#
#          ANSWER SCRIPT DISTRIBUTION                     #                           
#=========================================================#
ADDITIONAL_EX_ID="additional_ex_id"
FALSE_NO_LIST="false_no_list"
duplicate_error={"status":"Fail","message":"Duplicate element present.Please scan again","data":[]}
campnotexist_error={"status":"Fail","message":"Camp does not exist","data":[]}
ans_script_dis_success={"status":"Success","message":"Answer script successfully distributed"}
usernotexist={"status":"Fail","message":"No such user exist","data":[]}

#=========================================================#
#      	ANSWER SCRIPT DISTRIBUTION VIEW                   # 
#=========================================================#

ANSWER_DISTRIBUTION_COUNT="answer_distribution_count"
ANSWER_DISTRIBUTION_DATE="answer_distribution_date"
answerScriptfetch={"status":"Success","message":"Successfully fetched","data":[]}
answerScriptfetchErr={"status":"Fail","message":"Not successfully fetched the data","data":[]}


#=========================================================#
#          ANSWER SCRIPT RETURN                           #                           
#=========================================================#
DATA_LIST="data_list"
CONF_DATA="conflicted_data"
OLD_DATA="old_data"
marknotexist_error={"status":"Fail","message":"Mark entry cannot possible.Scan again","data":[]}
ans_script_return_success={"status":"Success","message":"Successfully added mark"}
ans_script_return_conflict={"status":"Fail","message":"conflict occur"}
#=========================================================#
#         ADDITIONAL EXAMINER MARK ADD                    #                           
#=========================================================#
RESULT_DATA="resultData"
session_invalid_msg={"status":"Fail","message":"Unauthorised access",DATA:{RESULT_DATA:[]}}
error_msg={'status':"Fail",'message':'Bad request',DATA:{RESULT_DATA:[]}}
false_no_exist={"status":"Fail","message":"False number already exist",DATA:{RESULT_DATA:[]}}
campnot_exist_error={"status":"Fail","message":"Camp does not exist",DATA:{RESULT_DATA:[]}}
falseno_not_exist={"status":"Fail","message":"False number not exist",DATA:{RESULT_DATA:[]}}
stud_mark_exist={"status":"Fail","message":"Already exists",DATA:{RESULT_DATA:[]}}
add_astnl_mark_success={"status":"Success","message":"Successfully added mark"}
notExists={"status":"Fail","message":"Not exist",DATA:{RESULT_DATA:[]}}

#=========================================================#
#              CHIEF EXAMINER MARK ADD                    #                           
#=========================================================#
stud_mark_not_exist={"status":"Fail","message":"Could not enter mark.Try again",DATA:{RESULT_DATA:[]}}

chief_exist_error={"status":"fail","message":"There is no chief examiner under the chairman","data":[]}
ROLE_TYPE="role_type"
#=========================================================#
#                 ADD MARK BY CHAIRMAN                    #                           
#=========================================================#
chairman_error={"status":"Fail","message":"This user is not a chairman",DATA:[]}
mark_exist_error={"status":"Fail","message":"Mark already assign",DATA:[]}
exam_existing_error={"status":"Fail","message":"Exam does not exist",DATA:[]}

#========================================================#
#          MARK FINALIZE VIEW                            #
#========================================================#
RESULT="result"
ADDITIONAL_MARK="additional_mark"
CHIEF_MARK="chief_mark"
CHAIRMAN_MARK="chairman_mark"
CAMP_OFFICER_MARK="camp_officer_mark"
STUDENT_MARK="student_mark"
DFM_NUMBER="dfm_no"
mark_fetch={"status":"Success","message":"Successfully fetched the mark"}
mark_no_data={"status":"Fail","message":"There is no mark for the selected exam",DATA:[]}
invalid_data_error={"status":"Fail","message":"Exam is not done","data":[]}


#=========================================================#
#    ADDITIONAL MARK LIST                                 #                           
#=========================================================#
ADDITIONAL_ID="additional_id"
NoAdditional={"status":"Fail","message":"No additional examiner",DATA:{RESULT_DATA:[]}}
NoMarkEntry={"status":"Fail","message":"No mark entry",DATA:{RESULT_DATA:[]}}
additionalMarkFetch={"status":"Success","message":"Successfully fetched data"}
MARK_DETAILS="mark_details"


#========================================================#
#                    MODULE V                            #
#========================================================#
#========================================================#
#                 RE EVALUATION MODULE                   #
#========================================================#

#========================================================#
#                 RE EVALUATION STUDENT ADD              #
#========================================================#
STD_REG_NUM="std_reg_num"
# rev_reg_num_not_exist={}
rev_add_success={"status":"Success","message":"Successfully added","data":[]}
revalInvalid={"status":"Fail","message":"Invalid Register Number","data":[]}
rev_exists_err={"status":"Fail","message":"Register Number exists","data":[]}
rev_fetch_success={"status":"Success","message":"Successfully fetched","data":[]}

#=========================================================#
#              RE EVALUATION LIST VIEW STARTS             #
#=========================================================#
SECURED_MARK="secured_mark"
FALSE_NUMBER="false_number"
STUDENT_LIST="student_list"
STD_NAME="std_name"
revListSuccess={"status":"Success","message":"Successfully fetched","data":[]}
revErr={"status":"Fail","message":"There is no student for the given list","data":[]}

#=======================================================#
#       Revaluation student list view camp wise         #
#=======================================================#
MARK="mark"
rv_stu_sucss_get ={"status": "Success","message": "Student revaluation list details fetched successfully", "data": []}
stu_rv_error = {"status": "Fail","message": "There is no student list to the given data"}


#=========================================================#
#     ANSWERSCRIPT VERIFICATION                           #                           
#=========================================================#
FALSE_NUM="false_num"
REG_NUM="reg_num"
invalidfalse={"status":"Fail","message":"Incorrect false number","data":[]}

#=========================================================#
#    REVALUATION MARK ENTRY                               #                           
#=========================================================#
RV_MARK="rv_mark"
REV_TYPE="rev_type"
FIRST_RV_MARK="first_rv_mark"
SECURED_MARK="secured_mark"
RV_STATUS="rev_status"
rvMarkUpdate={"status":"Success","message":"Successfully updated"}
rvListFetch={"status":"Success","message":"Successfully fetched students for second revaluation  "}
noStudents={"status":"Fail","message":"No students"}


#=========================================================#
#          REVALUATION MARK LIST STARTS                   #                           
#=========================================================#

CURRENT_MARK="current_mark"
FIRST_RV_MARK="first_rv_mark"
SECOND_RV_MARK="second_rv_mark"
FINAL_MARK="final_mark"
REV_TYPE="rev_type"
rvm_fetch={"status":"Success","message":"Successfull"}


#=========================================================#
#           SECOND   RE EVALUATION                        #
#=========================================================#

secondRevalSuccess={"status":"Success","message":"Successfully updated"}
secondRevalerr={"status":"Fail","message":"Invalid","data":[]}
MARK="mark"
FINALMARK="final_mark"
