from flask import Flask,jsonify,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from model import *
from user_mngmnt import*
from pre_exam import *
from atm import *
from exam import *
from evm import *
from rvm import *



CORS(application)
api = Api(application)



#=================================================#
#             USER MANAGEMENT MODULE              #
#=================================================#
api.add_resource(UserLogin, '/api/v1/user_login')
api.add_resource(UserLogout, "/api/v1/logout")
api.add_resource(Forgotpassword, "/api/v1/forgotpassword")
api.add_resource(Newpassword, "/api/v1/newpassword")
api.add_resource(Changepassword, "/api/v1/changepassword")
api.add_resource(AdditionalExaminerLogin, "/api/v1/additional_examiner_login")
api.add_resource(CacheClear, "/api/v1/cache_clear")


#=================================================#
#             PRE EXAMINATION MODULE              #
#=================================================#
api.add_resource(ExamCenter_Add, '/api/v1/examcenter_add')
api.add_resource(Designation_Add,"/api/v1/designation_add")
api.add_resource(Role_Add, '/api/v1/role_add')
api.add_resource(Action_Add, '/api/v1/action_add')
api.add_resource(Addegree,"/api/v1/degree_add")
api.add_resource(Addbranch,"/api/v1/branch_det")
api.add_resource(Addsection,"/api/v1/section_det")
api.add_resource(ProgramDetails, "/api/v1/pgmdetails")
api.add_resource(AddUser, '/api/v1/user_add')
api.add_resource(ChiefSuperintendent,'/api/v1/chiefsuptd')
api.add_resource(CSOrderGeneration,"/api/v1/order_generation")
api.add_resource(TeacherList, '/api/v1/teacher_list')
api.add_resource(AddInvigilator, '/api/v1/invigilator_add')
api.add_resource(ExamRoomDetails, "/api/v1/roomdetails")
api.add_resource(ExamHallAllotment, "/api/v1/hall_allotment")
api.add_resource(HallAllot, "/api/v1/allot_student")
api.add_resource(CourseAdd, "/api/v1/course_list")
api.add_resource(CenterExam, "/api/v1/center_exam")
api.add_resource(CenterCamp, "/api/v1/center_camp")
api.add_resource(ExamHallAllotmentView,"/api/v1/hall_allotment_view")
api.add_resource(GetExamCourse, "/api/v1/exam_course")
api.add_resource(BranchSection, "/api/v1/branch_section")
api.add_resource(UserRole, "/api/v1/user_role")
api.add_resource(HallwiseStudentList, "/api/v1/hallwise_stud_list")
api.add_resource(StudentHallAllotmentList,"/api/v1/stud_hall_alloted_list")



#=================================================#
#             ARTICLE TRACKING MANAGEMENT         #
#=================================================#
api.add_resource(Article_Add,"/api/v1/articlelist")
api.add_resource(RouteofficerLogin, "/api/v1/routeofficer_login")
api.add_resource(RouteofficerLogout, "/api/v1/routeofficer_logout")
# api.add_resource(RouteOfficerForgotpassword, "/api/v1/ro_forgot_password")
api.add_resource(CodeVerification,"/api/v1/code_verify")
api.add_resource(RouteOfficerNewpassword, "/api/v1/new_password")
api.add_resource(RouteOfficerChangePassword, "/api/v1/ro_change_password")
api.add_resource(ApprovalCodeverify,"/api/v1/approval_verify")



#=================================================#
#              EXAM MANAGEMENT MODULE             #
#=================================================#
    
api.add_resource(ExamAdd, "/api/v1/exam_add")
api.add_resource(Camp_Add,"/api/v1/camp_det")
api.add_resource(InvigilatorLogin, "/api/v1/invigilator_login")
api.add_resource(General_infoList, "/api/v1/generalinfo_list")
api.add_resource(AccessKeyGeneration, "/api/v1/accesskey_generation")
api.add_resource(AccessKeyVerification, "/api/v1/accesskey_verification")
api.add_resource(AccessKeyListing, "/api/v1/accesskey_listing")
api.add_resource(StudentTempMapp, "/api/v1/temp_map")
api.add_resource(TempMapp, "/api/v1/temp_map_confirm")
api.add_resource(StudentMapp, "/api/v1/std_map")
api.add_resource(MappingView, "/api/v1/mapping_view")
api.add_resource(FetchingAllAccessKey, "/api/v1/fetching_all_accesskey")
api.add_resource(InvigilatorASGeneration, "/api/v1/inv_as_generation")
api.add_resource(InvigilatorASSubmit, "/api/v1/inv_as_submit")
api.add_resource(CSAbsenteeGeneration,"/api/v1/cs_as_generation")
api.add_resource(CSAbsenteeSubmit,"/api/v1/cs_as_submit")
api.add_resource(ASOAbsenteeGeneration, "/api/v1/aso_as_generation")
api.add_resource(ASOAbsenteeVerification, "/api/v1/aso_as_verify")
api.add_resource(SOAbsenteeGeneration,"/api/v1/so_as_generation")
api.add_resource(SOAbsenteeApprove,"/api/v1/so_as_verify")
api.add_resource(AnswerScriptDispatchAdd,"/api/v1/as_dispatch")
api.add_resource(ExamProgram,"/api/v1/exam_program") 
api.add_resource(ProgramCourse,"/api/v1/program_course") 
api.add_resource(ExamCamp,"/api/v1/exam_camp")
api.add_resource(TodayExamList,"/api/v1/today_exam_list")
api.add_resource(AsExamList,"/api/v1/as_exam_list")
api.add_resource(ExamCenter,"/api/v1/exam_center")













#=================================================#
#              EVALUATION MODULE                  #
#=================================================#
api.add_resource(Chairman_Add,"/api/v1/chairman_det")
api.add_resource(ChairmanList,"/api/v1/chairman_list")
api.add_resource(ChiefExaminerAdd,"/api/v1/chiefexam_add")
api.add_resource(ChiefExaminerList,"/api/v1/chiefexam_list")
api.add_resource(CampOfficerAdd,"/api/v1/campofficer_add")    
api.add_resource(AdditionalExaminer_Add,"/api/v1/additionalexaminer_det")
api.add_resource(AdditionalExaminerList,"/api/v1/additionalexaminerlist")
api.add_resource(UniversityOfficialList,"/api/v1/campofficer_list")
api.add_resource(AnsScriptDistribution,"/api/v1/ans_script_distn")
api.add_resource(AnsScriptDistributionView,"/api/v1/ans_script_distn_view")
api.add_resource(MarkFinalizeView,"/api/v1/mark_finalize_view")
api.add_resource(AnsScriptReturn,"/api/v1/ans_script_return")
api.add_resource(AddAdditionalMark,"/api/v1/additnl_mark_add")
api.add_resource(AddChiefMark,"/api/v1/chief_mark_add")
api.add_resource(AddChairmanMark,"/api/v1/chairman_mark_add")
api.add_resource(AdditionalMarkList,"/api/v1/additional_mark_list")







#=================================================#
#              RE EVALUATION MODULE               #
#=================================================#
api.add_resource(RevaluationAdd,"/api/v1/rev_add")
api.add_resource(RevaluationListView,"/api/v1/rev_list_view")
api.add_resource(RevaluationStudentList, "/api/v1/student_rv_list")
api.add_resource(AnswerScriptVerification, "/api/v1/answerscript_verification") 
api.add_resource(RevaluationMarkEntry, "/api/v1/revaluation_markentry")
api.add_resource(RevaluationMarkList,"/api/v1/rvm_marklist") 
api.add_resource(SecondRevaluationMarkEntry, "/api/v1/sec_rev_markentry")
api.add_resource(RevaluationMarkFinalize,"/api/v1/rvm_mark_finalize") 




# logging.basicConfig(filename="logfilename.log", level=logging.ERROR)
# ipaddress=get_my_ip()
# req_url=request.url                
# application.logger.error("User with id  access the  "+ req_url)


if __name__ == "__main__":
    application.debug = True                 
    application.run()


