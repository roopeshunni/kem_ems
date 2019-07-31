from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

application = Flask(__name__)
# application.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root1234@dastp.cq9dav1ixlfr.ap-southeast-1.rds.amazonaws.com/ems_dev'
# application.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root1234@dastp.cq9dav1ixlfr.ap-southeast-1.rds.amazonaws.com/ems_uat'
# application.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root1234@dastp.cq9dav1ixlfr.ap-southeast-1.rds.amazonaws.com/ems_qa'
application.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root1234@dastp.cq9dav1ixlfr.ap-southeast-1.rds.amazonaws.com/kem_ems'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(application)


#========================================================#
#                    MODULE I                            #
#========================================================#
#========================================================#
#              PRE EXAMINATION MANAGEMENT                #
#========================================================#
class Center_det(db.Model):
    cen_id=db.Column(db.Integer,primary_key=True)
    cen_name=db.Column(db.String(200),nullable=False)
    cen_code=db.Column(db.String(200),nullable=False)
    cen_addr=db.Column(db.String(200),nullable=False)
    cen_loc=db.Column(db.String(200),nullable=False)
    cen_dist=db.Column(db.String(200),nullable=False)
    cen_pin=db.Column(db.String(200),nullable=False)
    cen_city=db.Column(db.String(200),nullable=False)
    cen_phone_num=db.Column(db.String(200),nullable=False)
    cen_mobile=db.Column(db.String(200),nullable=False)
    cen_email=db.Column(db.String(200),unique=True,nullable=False)
    cen_type=db.Column(db.String(200),nullable=False)
    status=db.Column(db.String(200),nullable=False)
class designation_det(db.Model):
    des_id=db.Column(db.Integer,primary_key=True)
    des_name=db.Column(db.String(200),nullable=False)
    des_code=db.Column(db.String(200),nullable=False)
    status=db.Column(db.String(200),nullable=False)
class ProjectModule(db.Model):
    mod_id=db.Column(db.Integer,primary_key=True)
    mod_name=db.Column(db.String(200),nullable=False)
    mod_status=db.Column(db.String(200),nullable=False)
class ActionDet(db.Model):
    act_id=db.Column(db.Integer,primary_key=True)
    act_name=db.Column(db.String(200),nullable=False)
    act_code=db.Column(db.String(10),nullable=False)
    act_status=db.Column(db.String(200),nullable=False)
    act_card=db.Column(db.String(200),nullable=False)
    mod_id=db.Column(db.Integer,db.ForeignKey('project_module.mod_id'),nullable=False)
class RoleDet(db.Model):
    role_id=db.Column(db.Integer,primary_key=True)
    role_name=db.Column(db.String(200),nullable=False)
    role_permission=db.Column(db.String(20000),nullable=False)
    role_meta=db.Column(db.String(50),nullable=False)
    role_status=db.Column(db.String(200),nullable=False)
class ProgramDet(db.Model):
    prg_id = db.Column(db.Integer, primary_key=True,autoincrement=True, nullable=False)
    prg_name = db.Column(db.String(200), nullable=False)
    prg_code = db.Column(db.String(200), nullable=False)
    prg_meta = db.Column(db.String(200),nullable=False)
    deg_id = db.Column(db.Integer, db.ForeignKey('degree_det.deg_id'), nullable=False)
    status = db.Column(db.String(200))
class degree_det(db.Model):
    deg_id=db.Column(db.Integer,primary_key=True)
    deg_name=db.Column(db.String(250),nullable=False)
    deg_code=db.Column(db.String(100),nullable=False)
    status =db.Column(db.String(100),nullable=False)
class branch_det(db.Model):
    br_id=db.Column(db.Integer,primary_key=True)
    br_name=db.Column(db.String(100),nullable=False)
    br_code=db.Column(db.String(20),nullable=False)
    deg_id=db.Column(db.Integer,db.ForeignKey('degree_det.deg_id'),nullable=False)
    br_status=db.Column(db.String(50),nullable=False)
class Section_det(db.Model):
    sec_id=db.Column(db.Integer,primary_key=True)
    sec_name=db.Column(db.String(100),nullable=False)
    br_id=db.Column(db.Integer,db.ForeignKey('branch_det.br_id'),nullable=False)
    sec_code=db.Column(db.String(20),nullable=False)
    sec_status=db.Column(db.String(50),nullable=False)
class User_det(db.Model):
    user_id=db.Column(db.Integer,primary_key=True)
    emp_id=db.Column(db.String(200),unique=True,nullable=False)
    name=db.Column(db.String(200),nullable=False)
    usr_add=db.Column(db.String(200),nullable=False)
    usr_loc=db.Column(db.String(200),nullable=False)
    usr_city=db.Column(db.String(256),nullable=False)
    usr_pin=db.Column(db.Integer,nullable=False)
    cen_id=db.Column(db.Integer,nullable=False)
    usr_mobile=db.Column(db.String(256),nullable=False)
    usr_phone=db.Column(db.String(15),nullable=False)
    usr_email=db.Column(db.String(256),unique=True,nullable=False)
    usr_uname=db.Column(db.String(256),nullable=False)
    usr_pswd=db.Column(db.String(256),nullable=False)
    role_id=db.Column(db.Integer,db.ForeignKey('role_det.role_id'),nullable=False)
    des_id=db.Column(db.Integer,db.ForeignKey('designation_det.des_id'),nullable=False)
    usr_cat1=db.Column(db.String(256),nullable=False)
    usr_cat2=db.Column(db.String(256),nullable=False)
    usr_cat3=db.Column(db.String(256),nullable=False)
    status=db.Column(db.String(256),nullable=False)
class BranchMapping(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    emp_id=db.Column(db.String(200),nullable=False)
    br_id=db.Column(db.Integer,db.ForeignKey('branch_det.br_id'),nullable=False)
    sec_id=db.Column(db.Integer,db.ForeignKey('section_det.sec_id'),nullable=False)
    joining_date=db.Column(db.DateTime,nullable=False)
    rel_date=db.Column(db.DateTime,nullable=False)
    status=db.Column(db.String(200),nullable=False)
class ChiefSuptd(db.Model):
    chief_suptd_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user_det.user_id'),nullable=False)
    cen_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
    role_id=db.Column(db.Integer,db.ForeignKey('role_det.role_id'),nullable=False)
    pgm_id = db.Column(db.Integer,nullable=False)
    exp_date = db.Column(db.String(200),nullable=False)
    status = db.Column(db.String(200),nullable=False)
class ExamRole(db.Model):
    exam_role_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user_det.user_id'),nullable=False)
    cen_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
    role_id=db.Column(db.Integer,db.ForeignKey('role_det.role_id'),nullable=False)
    pgm_id = db.Column(db.Integer,db.ForeignKey('program_det.prg_id'),nullable=False)
    exp_date = db.Column(db.String(200),nullable=False)
    exam_role_status = db.Column(db.String(200),nullable=False)
class OrderGeneration(db.Model):
    order_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    order_number = db.Column(db.String(200),nullable=False)
    order_date = db.Column(db.String(200),nullable=False)
    emp_id_list = db.Column(db.String(200),nullable=False)
    status = db.Column(db.String(200),nullable=False)
    exam_id=db.Column(db.Integer,nullable=False)
class ExamInvigilator(db.Model):
    invig_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user_det.user_id'),nullable=False)
    cen_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
    invig_status = db.Column(db.String(200),nullable=False)
class ExamHall(db.Model):
    hall_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    cen_id = db.Column(db.Integer, db.ForeignKey('center_det.cen_id'), nullable=False)
    hall_no = db.Column(db.Integer,nullable=False)
    hall_capacity = db.Column(db.Integer,nullable=False)
    hall_alloted = db.Column(db.Integer,nullable=False)
    hall_free = db.Column(db.Integer,nullable=False)
    hall_name= db.Column(db.String(200))
    hall_status = db.Column(db.String(200))
class HallAllotment(db.Model):
    hall_allot_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False) 
    std_id=db.Column(db.Integer,db.ForeignKey('student.std_id'),nullable=False)
    cen_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
    hall_id=db.Column(db.Integer,db.ForeignKey('exam_hall.hall_id'),nullable=False)
    hall_allot_date = db.Column(db.String(200),nullable=False)
    exam_date=db.Column(db.DateTime,nullable=False)
    hall_allot_status = db.Column(db.String(200),nullable=False)
    prg_id=db.Column(db.Integer,db.ForeignKey('program_det.prg_id'),nullable=False)
    cou_id=db.Column(db.Integer,db.ForeignKey('course.cou_id'),nullable=False)
class HallExamMapping(db.Model):
    h_map_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    hall_id=db.Column(db.Integer,db.ForeignKey('exam_hall.hall_id'),nullable=False)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
    hall_capacity = db.Column(db.Integer,nullable=False)
    hall_alloted = db.Column(db.Integer,nullable=False)
    hall_free = db.Column(db.Integer,nullable=False)
class HallCapacity(db.Model):
    h_map_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    hall_id=db.Column(db.Integer,db.ForeignKey('exam_hall.hall_id'),nullable=False)
    hall_capacity = db.Column(db.Integer,nullable=False)
    hall_alloted = db.Column(db.Integer,nullable=False)
    hall_free = db.Column(db.Integer,nullable=False)
    exam_date=db.Column(db.DateTime,nullable=False)
class Session(db.Model):
    ses_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user_det.user_id'),nullable=False)
    ses_devtype=db.Column(db.String(1),nullable=False)
    ses_token=db.Column(db.String(200),nullable=False)
    ses_logintime=db.Column(db.DateTime,nullable=False)
    ses_ip=db.Column(db.String(256),nullable=False)
    ses_mac=db.Column(db.String(256),nullable=False)
    ses_logouttime=db.Column(db.DateTime,nullable=False)
    status=db.Column(db.String(200),nullable=False)
#========================================================#
#                    MODULE II                           #
#========================================================#
#========================================================#
#             ARTICLE TRACKING MANAGEMENT                #
#========================================================#
class ArticleDistribution(db.Model):
    art_id=db.Column(db.Integer,primary_key=True)
    cen_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
    art_code=db.Column(db.String(20),nullable=False)
    art_approval_key=db.Column(db.String(20),nullable=False)
    date_send=db.Column(db.Date,nullable=False)
    date_received=db.Column(db.Date,nullable=False)
    art_status=db.Column(db.String(50),nullable=False)
#========================================================#
#                    MODULE III                          #
#========================================================#
#========================================================#
#                    EXAM MODULE                         #
#========================================================#
class Exam(db.Model):
    exam_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    exam_name = db.Column(db.String(500),nullable=False)
    exam_code = db.Column(db.String(500),nullable=False)
    start_date =db.Column(db.Date,nullable=False)
    end_date = db.Column(db.Date,nullable=False)
    status = db.Column(db.String(500),nullable=False)
class Student(db.Model):
    std_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
    cen_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
    prg_id=db.Column(db.Integer,db.ForeignKey('program_det.prg_id'),nullable=False)
    std_reg = db.Column(db.String(500),nullable=False)
    std_name = db.Column(db.String(500),nullable=False)
    std_dob = db.Column(db.String(500),nullable=False)
    std_mobile = db.Column(db.String(500),nullable=False)
    std_email = db.Column(db.String(500),nullable=False)
    std_addr = db.Column(db.String(5000),nullable=False)
    status = db.Column(db.String(200),nullable=False)
class Syllabus(db.Model):
    syl_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    pgm_id = db.Column(db.Integer,db.ForeignKey('program_det.prg_id'),nullable=False)
    semester = db.Column(db.String(200),nullable=False)
    syl_year = db.Column(db.String(200),nullable=False)
    syl_status = db.Column(db.String(200),nullable=False)
class Course(db.Model):
    cou_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    pgm_id = db.Column(db.Integer,db.ForeignKey('program_det.prg_id'),nullable=False)
    semester = db.Column(db.String(200),nullable=False)
    cou_name = db.Column(db.String(500),nullable=False)
    cou_code = db.Column(db.String(500),nullable=False)
    syl_id = db.Column(db.Integer,db.ForeignKey('syllabus.syl_id'),nullable=False)
    cou_status = db.Column(db.String(200),nullable=False)
class ExamTimetable(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    cou_id=db.Column(db.Integer,db.ForeignKey('course.cou_id'),nullable=False)
    prg_id=db.Column(db.Integer,db.ForeignKey('program_det.prg_id'),nullable=False)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
    date=db.Column(db.DateTime,nullable=False)
    section=db.Column(db.String(200),nullable=False)
    status=db.Column(db.String(200),nullable=False)
class Camp(db.Model):
    camp_id=db.Column(db.Integer,primary_key=True)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
    cen_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
    prg_id=db.Column(db.Integer,db.ForeignKey('program_det.prg_id'),nullable=False)
    start_date=db.Column(db.Date,nullable=False)
    end_date=db.Column(db.Date,nullable=False)
    camp_status=db.Column(db.String(50),nullable=False)
class AccessKeyGen(db.Model):
    key_id=db.Column(db.Integer,primary_key=True)
    cen_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
    inv_id=db.Column(db.Integer,db.ForeignKey('exam_invigilator.user_id'),nullable=False)
    access_code=db.Column(db.String(200),nullable=False)
    examSection=db.Column(db.String(200),nullable=False)
    exp_date=db.Column(db.DateTime,nullable=False)
    key_status=db.Column(db.String(200),nullable=False)
class StudTempMapp(db.Model):
    std_tmp_map_id=db.Column(db.Integer,primary_key=True)
    std_reg_num=db.Column(db.String(500),nullable=False)
    std_false_num=db.Column(db.String(500),nullable=False)
    smp_status=db.Column(db.Boolean,default=False)
    std_temp_status=db.Column(db.String(50),nullable=False)
    inv_id=db.Column(db.Integer,db.ForeignKey('user_det.user_id'),nullable=False)
class InvigilatorExamHall(db.Model):
    inv_hall=db.Column(db.Integer,primary_key=True)
    # exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
    cen_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
    inv_id=db.Column(db.Integer,db.ForeignKey('exam_invigilator.user_id'),nullable=False)
    hall_id=db.Column(db.Integer,db.ForeignKey('exam_hall.hall_id'),nullable=False)
    exam_date=db.Column(db.DateTime,default=datetime.datetime.utcnow)

class FalseNumber(db.Model):
    dfm_id=db.Column(db.Integer,primary_key=True)
    std_reg_num=db.Column(db.String(500),nullable=False)
    dfm_num=db.Column(db.String(500),nullable=False)
    cen_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
    cou_id=db.Column(db.Integer,db.ForeignKey('course.cou_id'),nullable=False)
    inv_id=db.Column(db.Integer,db.ForeignKey('user_det.user_id'),nullable=False)
    dfm_date=db.Column(db.Date,nullable=False)
    cs_id=db.Column(db.Integer,nullable=False)
    cs_submit_date=db.Column(db.Date,nullable=False)
    aso_id=db.Column(db.Integer,nullable=False)
    aso_verify_date=db.Column(db.Date,nullable=False)
    so_id=db.Column(db.Integer,nullable=False)
    so_approved_date=db.Column(db.Date,nullable=False)
    smp_status=db.Column(db.Boolean,default=False)
    dfm_status=db.Column(db.String(50),nullable=False)
    dfm_flag=db.Column(db.Boolean,default=False)
class AnswerScriptDispatch(db.Model):
    ans_dispatch_id=db.Column(db.Integer,primary_key=True)
    cen_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
    cou_id=db.Column(db.Integer,db.ForeignKey('course.cou_id'),nullable=False)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
    exam_date=db.Column(db.Date,nullable=False)
    ans_dispatch_date=db.Column(db.Date,nullable=False)
    ans_dispatch_count=db.Column(db.Integer,nullable=False) 
    smp_count=db.Column(db.Integer)
    total_count=db.Column(db.Integer)
    absentee_count=db.Column(db.Integer)
    ans_dispatch_status=db.Column(db.String(50),nullable=False)
#========================================================#
#                    MODULE IV                           #
#========================================================#
#========================================================#
#                EVALUATION MODULE                       #
#========================================================#
class ChiefExaminer(db.Model):
    chiefexam_id=db.Column(db.Integer,primary_key=True)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
    camp_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
    chief_id=db.Column(db.Integer,db.ForeignKey('user_det.user_id'),nullable=False)
    chairman_id=db.Column(db.Integer,db.ForeignKey('user_det.user_id'),nullable=False)
    end_date = db.Column(db.DateTime,nullable=False)
    status=db.Column(db.String(200),nullable=False)
class AdditionalExaminer(db.Model):
    addlexam_id=db.Column(db.Integer,primary_key=True)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
    cen_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
    addl_id=db.Column(db.Integer,db.ForeignKey('user_det.user_id'),nullable=False)
    chief_id=db.Column(db.Integer,db.ForeignKey('user_det.user_id'),nullable=False)
    status=db.Column(db.String(200),nullable=False)
class AnswerScriptDistribution(db.Model):
    ans_distribution_id=db.Column(db.Integer,primary_key=True)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
    camp_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
    addl_id=db.Column(db.Integer,db.ForeignKey('user_det.user_id'),nullable=False)
    ans_distribution_date=db.Column(db.DateTime,nullable=False)
    ans_distribution_count=db.Column(db.DateTime,nullable=False)
    ans_distribution_flase_num_list=db.Column(db.String(500),nullable=False)
class StudentMark(db.Model):
    std_mark_id=db.Column(db.Integer,primary_key=True)
    std_reg_num=db.Column(db.String(500),nullable=False)
    dfm_num=db.Column(db.String(500),nullable=False)
    cou_id=db.Column(db.Integer,db.ForeignKey('course.cou_id'),nullable=False)
    prg_id=db.Column(db.Integer,db.ForeignKey('program_det.prg_id'),nullable=False)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
    camp_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
    addl_id=db.Column(db.Integer,db.ForeignKey('user_det.user_id'),nullable=False)
    addl_mark=db.Column(db.Integer,nullable=False)
    addl_date=db.Column(db.DateTime,nullable=False)
    chief_id=db.Column(db.Integer,nullable=False) 
    chief_mark=db.Column(db.Integer,nullable=False)
    chief_date=db.Column(db.DateTime,nullable=False)
    chairman_id=db.Column(db.Integer,nullable=False) 
    chairman_mark=db.Column(db.Integer,nullable=False)
    chairman_date=db.Column(db.DateTime,nullable=False)
    co_id=db.Column(db.Integer,nullable=False) 
    co_mark=db.Column(db.Integer,nullable=False)
    co_date=db.Column(db.DateTime,nullable=False)
    std_mark=db.Column(db.String(20),nullable=False)
    smp_status=db.Column(db.Boolean,default=False)

# class StudentMark(db.Model):
#     std_mark_id=db.Column(db.Integer,primary_key=True)
#     std_reg_num=db.Column(db.String(500),nullable=False)
#     dfm_num=db.Column(db.String(500),nullable=False)
#     cou_id=db.Column(db.Integer,db.ForeignKey('course.cou_id'),nullable=False)
#     prg_id=db.Column(db.Integer,db.ForeignKey('program_det.prg_id'),nullable=False)
#     exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
#     camp_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
#     addl_id=db.Column(db.Integer,db.ForeignKey('user_det.user_id'),nullable=False)
#     addl_mark=db.Column(db.Integer,nullable=False)
#     addl_date=db.Column(db.DateTime,nullable=False)
#     chief_id=db.Column(db.Integer,nullable=False) 
#     chief_mark=db.Column(db.Integer,nullable=False)
#     chief_date=db.Column(db.DateTime,nullable=False)
#     chairman_id=db.Column(db.Integer,nullable=False) 
#     chairman_mark=db.Column(db.Integer,nullable=False)
#     chairman_date=db.Column(db.DateTime,nullable=False)
#     co_id=db.Column(db.Integer,nullable=False) 
#     co_mark=db.Column(db.Integer,nullable=False)
#     co_date=db.Column(db.DateTime,nullable=False)
#     std_mark=db.Column(db.String(20),nullable=False)
#     smp_status=db.Column(db.Boolean,default=False)



#========================================================#
#                    MODULE V                            #
#========================================================#
#========================================================#
#               RE EVALUATION MODULE                     #
#========================================================#
class Revaluation(db.Model):
    rv_id=db.Column(db.Integer,primary_key=True)
    std_reg_num=db.Column(db.String(500),nullable=False)
    dfm_num=db.Column(db.String(500),nullable=False)
    cou_id=db.Column(db.Integer,db.ForeignKey('course.cou_id'),nullable=False)
    prg_id=db.Column(db.Integer,db.ForeignKey('program_det.prg_id'),nullable=False)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.exam_id'),nullable=False)
    camp_id=db.Column(db.Integer,db.ForeignKey('center_det.cen_id'),nullable=False)
    addl_id=db.Column(db.Integer,nullable=False)
    addl_mark=db.Column(db.Integer,nullable=False)    
    chief_id=db.Column(db.Integer,nullable=False)
    chief_mark=db.Column(db.Integer,nullable=False)
    chairman_id=db.Column(db.Integer,nullable=False)
    chairman_mark=db.Column(db.Integer,nullable=False)
    co_id=db.Column(db.Integer,nullable=False)
    co_mark=db.Column(db.Integer,nullable=False)
    first_rv_mark=db.Column(db.Integer,nullable=False)
    second_rv_mark=db.Column(db.Integer,nullable=False)
    secured_mark=db.Column(db.Integer,nullable=False)
    final_mark=db.Column(db.Integer,nullable=False)
    rv_status=db.Column(db.String(200),nullable=False)