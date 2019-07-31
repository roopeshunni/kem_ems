


from model import *
from constants import *
from flask_restful import Resource, Api
import json
from flask import Flask,jsonify,request
from user_mngmnt import *
import re




#=========================================================#
#              RE EVALUATION STUDENT ADD STARTS           #
#=========================================================# 
class RevaluationAdd(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                    if STD_REG_NUM in requestData:
                        
                        cou_id=requestData[COURSE_ID]
                        prg_id=requestData[PRG_ID]
                        exam_id=requestData[EXAM_ID]
                        std_reg_num=requestData[STD_REG_NUM]
                        
                        rev_chk=Revaluation.query.filter_by(std_reg_num=std_reg_num).first()                        
                        if rev_chk==None:
                            stud_chk=StudentMark.query.filter_by(std_reg_num=std_reg_num).first()
                            if stud_chk==None:
                                return jsonify(revalInvalid)                            
                            rev_data=Revaluation(std_reg_num=std_reg_num,dfm_num=stud_chk.dfm_num,
                            cou_id=stud_chk.cou_id,prg_id=stud_chk.prg_id,exam_id=stud_chk.exam_id,
                            camp_id=stud_chk.camp_id,addl_id=stud_chk.addl_id,addl_mark=stud_chk.addl_mark,
                            chief_id=stud_chk.chief_id,chief_mark=stud_chk.chief_mark,
                            chairman_id=stud_chk.chairman_id,chairman_mark=stud_chk.chairman_mark,
                            co_id=stud_chk.co_id,co_mark=stud_chk.co_mark,first_rv_mark=0,
                            second_rv_mark=0,secured_mark=stud_chk.std_mark,final_mark=0,rv_status="")
                            db.session.add(rev_data)
                            db.session.commit()
                            revdic={COURSE_ID:cou_id,STD_REG_NUM:std_reg_num,EXAM_ID:exam_id}
                            rev_add_success.update({DATA:revdic})
                            return jsonify(rev_add_success)
                        else:
                            return jsonify(rev_exists_err)
                        
                    elif COURSE_ID in  requestData:
                        cou_id=requestData[COURSE_ID]
                        prg_id=requestData[PRG_ID]
                        exam_id=requestData[EXAM_ID]                       
                        single_reval=Revaluation.query.filter_by(cou_id= cou_id,prg_id=prg_id,exam_id=exam_id).all()
                        if single_reval!=[]:
                            listrev=[]
                        
                    
                            for i in single_reval:
                                student_rev=Student.query.filter_by(std_reg=i.std_reg_num,status=STATUS).first()
                                camp_rev=Center_det.query.filter_by(cen_id=i.camp_id,status=STATUS).first()
                                revaluationdata={STD_REG_NUM:i.std_reg_num,CAMP_NAME:camp_rev.cen_name}
                                listrev.append(revaluationdata)
                            rev_fetch_success.update({DATA:listrev})
                            return jsonify(rev_fetch_success)
                        else:
                            return jsonify(invalid_data)
            else:
                return session_invalid
        except Exception as e:
            print(e)
            return jsonify(error)

#=========================================================#
#              RE EVALUATION STUDENT ADD ENDS             #
#=========================================================#

#=========================================================#
#              RE EVALUATION LIST VIEW STARTS             #
#=========================================================#


class RevaluationListView(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                cou_id=requestData[COURSE_ID]
                prg_id=requestData[PRG_ID]
                exam_id=requestData[EXAM_ID]
                rev_list=Revaluation.query.filter_by(cou_id=cou_id,prg_id=prg_id,exam_id=exam_id).all()
                if rev_list!=[]:
                    revallist=[]
                    revallist1=[]
                    programRev=ProgramDet.query.filter_by(prg_id=prg_id,status=STATUS).first()
                    s =programRev.prg_name
                    regex = re.compile(r'[\t]')
                    s = regex.sub(" ", s)
                    
                   
                    exam=Exam.query.filter_by(exam_id=exam_id,status=STATUS).first()
                    course=Course.query.filter_by(cou_id=cou_id).first()
                    dic={PRG_ID:prg_id,PRG_NAME:s,EXAM_ID:exam_id,EXAM_NAME:exam.exam_name,COURSE_ID:cou_id,COURSE_NAME:course.cou_name}
                    revallist.append(dic)
                    
                    for i in rev_list:
                        reg=i.std_reg_num
                        user_chief=User_det.query.filter_by(user_id=i.chief_id,status=STATUS).first()
                        user_chair=User_det.query.filter_by(user_id=i.chairman_id,status=STATUS).first()
                        addlRev=User_det.query.filter_by(user_id=i.addl_id,status=STATUS).first()
                        studObj=Student.query.filter_by(std_reg=reg,status=STATUS).first()
                        revaluationList={STD_NAME:studObj.std_name,STD_REG_NUM:i.std_reg_num,FALSE_NUMBER:i.dfm_num,ADDITIONAL_MARK:i.addl_mark,
                        CHIEF_MARK:i.chief_mark,
                        CHAIRMAN_MARK:i.chairman_mark,SECURED_MARK:i.secured_mark}
                        revallist1.append(revaluationList)
                    dic2={STUDENT_LIST:revallist1}
                    revallist.append(dic2)
                    revListSuccess.update({DATA:revallist})
                    return jsonify(revListSuccess)
                else:
                    return jsonify(revErr)
            else:
                return session_invalid
        except Exception as e:
            print(e)
            return jsonify(error)




#=========================================================#
#              RE EVALUATION LIST VIEW ENDS               #
#=========================================================#


#=======================================================#
#       Revaluation student list view camp wise         #
#=======================================================#


class RevaluationStudentList(Resource):
    def post(self):
        try:
            data = request.get_json()
            session_token = data[SESSION_TOKEN]
            user_id = data[USER_ID]
            sess_res = checkSessionValidity(session_token, user_id)
            if(not sess_res):
                return session_invalid

            if EXAM_ID in data:
                exam_id = data[EXAM_ID]
                course_id = data[COURSE_ID]
                prg_id =data[PRG_ID]
              

                revalStudent =Revaluation.query.filter_by(
                    exam_id=exam_id,cou_id=course_id, prg_id=prg_id).all()
             
                if revalStudent ==[]:

                    return stu_rv_error
                stuList = []

                for i in revalStudent:
                   
                    centre = Center_det.query.filter_by(
                        cen_id=i.camp_id).first()
                    student = Student.query.filter_by(
                         std_reg=i.std_reg_num).first()
                    
                    course = Course.query.filter_by(
                        cou_id=i.cou_id).first()
                   
                   
                    NewstuList = {STUDREG: i.std_reg_num, STUDNAME: student.std_name,
                                  FALSENO: i.dfm_num, COURSE_NAME: course.cou_name, CAMP_NAME: centre.cen_name, MARK: i.secured_mark}
                               
                    stuList.append(NewstuList)
                    rv_stu_sucss_get[DATA] = stuList

                return rv_stu_sucss_get
        except Exception as e:
            print(e)
            return err_exception



#=======================================================#
#       Revaluation student list view camp wise  end    #
#=======================================================#



#=========================================================#
#           ANSWER SCRIPT VERIFICATION STARTS             #                           
#=========================================================#

class AnswerScriptVerification(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            false_num=requestData[FALSE_NUM]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                false_chk=FalseNumber.query.filter_by(dfm_num=false_num).first()
                
                if false_chk!=None:
                    exam_chk=Exam.query.filter_by(exam_id=false_chk.exam_id).first()
                    course_chk=Course.query.filter_by(cou_id=false_chk.cou_id).first()
                    std_chk=Student.query.filter_by(std_reg=false_chk.std_reg_num).first()
                    std_mark=StudentMark.query.filter_by(std_reg_num=std_chk.std_reg).first()
                    if std_chk==None or std_mark==None:
                        return jsonify(invalidfalse)
                    false_dic={EXAM_ID:false_chk.exam_id,REG_NUM:false_chk.std_reg_num,STUDNAME:std_chk.std_name,
                    EXAM_NAME:exam_chk.exam_name,COURSE_NAME:course_chk.cou_name,CHIEF_MARK:std_mark.chief_mark,
                    CHAIRMAN_MARK:std_mark.chairman_mark,ADDITIONAL_MARK:std_mark.addl_mark}
                    falseFetch.update({DATA:false_dic})
                    return falseFetch
                else:
                    return jsonify(invalidfalse)
            else:
                return jsonify(session_invalid)
        except Exception as e: 
            return jsonify(error)


#=========================================================#
#           ANSWER SCRIPT VERIFICATION ENDS               #                           
#=========================================================#


#=========================================================#
#         REVALUATION MARK ENTRY STARTS(LIST FOR RV2)     #                           
#=========================================================#
class RevaluationMarkEntry(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            false_no=requestData[FALSENO]
            rv_mark=requestData[RV_MARK]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                false_chk=Revaluation.query.filter_by(dfm_num=false_no).first()
                if false_chk!=None:
                    current_mark=false_chk.secured_mark
                    mark_dif=rv_mark-current_mark
                    if mark_dif ==0 or mark_dif <0:
                       false_chk.final_mark=current_mark
                       false_chk.rv_status=0
                       db.session.commit()
                       falseDic={FALSENO:false_no}
                       rvMarkUpdate.update({DATA:falseDic})
                       return rvMarkUpdate
                    else:
                        dif_pcntg=(mark_dif/current_mark)*100
                        if dif_pcntg <=30:
                            false_chk.first_rv_mark=rv_mark
                            false_chk.final_mark=rv_mark
                            false_chk.rv_status=0
                            db.session.commit()
                            falseDic={FALSENO:false_no}
                            rvMarkUpdate.update({DATA:falseDic})
                            return rvMarkUpdate
                        elif dif_pcntg>30:  
                            false_chk.first_rv_mark=rv_mark
                            false_chk.final_mark=rv_mark
                            false_chk.rv_status=1
                            db.session.commit()
                            falseDic={FALSENO:false_no}
                            rvMarkUpdate.update({DATA:falseDic})
                            return rvMarkUpdate
                else:
                    return invalidfalse
            else:
                return session_invalid
        except Exception as e:
            print(e)       
            return error
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                rev_type=request.headers[REV_TYPE]
                falseList=[]
                if rev_type=="2":
                    false_chk=Revaluation.query.filter_by(rv_status="1").all()
                    if false_chk!=[]:
                       
                        
                        for i in false_chk:
                            falseDic={STUDREG:i.std_reg_num,FALSENO:i.dfm_num,FIRST_RV_MARK:i.first_rv_mark,
                            SECURED_MARK:i.secured_mark}
                            falseList.append(falseDic)
                        rvListFetch.update({DATA:falseList})
                        return rvListFetch
                    else:
                        return noStudents    
                elif rev_type=="1":
                    false_chk=Revaluation.query.filter_by().all()
                    if false_chk!=[]:

                        for i in false_chk:
                            falseDic={STUDREG:i.std_reg_num,FALSENO:i.dfm_num,
                            FIRST_RV_MARK:i.first_rv_mark,RV_STATUS:i.rv_status,
                            SECURED_MARK:i.secured_mark}
                            falseList.append(falseDic)
                        rvListFetch.update({DATA:falseList})
                        return rvListFetch
                    else:
                        return noStudents      
            else:
                return session_invalid
        except Exception as e:    
            return error
   


#=========================================================#
#         REVALUATION MARK ENTRY ENDS                     #                           
#=========================================================#

#=========================================================#
#  REVALUATION MARK LIST STARTS (AFTER RV1 AND RV2)       #                           
#=========================================================#
class RevaluationMarkList(Resource):
    
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            rev_type=requestData[REV_TYPE]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if rev_type=="1":
                    cou_id=requestData[COURSE_ID]
                    prg_id=requestData[PRG_ID]
                    exam_id=requestData[EXAM_ID]
                    rvmResponse=Revaluation.query.filter_by(exam_id=exam_id,cou_id=cou_id,prg_id=prg_id).all()
                    if rvmResponse!=[]:
                        rvmList=[]
                        rvmlist1=[]
                        exam=Exam.query.filter_by(exam_id=exam_id).first()
                        program=ProgramDet.query.filter_by(prg_id=prg_id).first()
                        course=Course.query.filter_by(cou_id=cou_id).first()
                        rvmdic={EXAM_ID:exam_id,EXAM_NAME:exam.exam_name,PROGRAM_ID:program.prg_id,PROGRAM_NAME:program.prg_name,COURSE_ID:course.cou_id,COURSE_NAME:course.cou_name}
                        rvmList.append(rvmdic)
                        for i in rvmResponse:
                            rvmdic1={REG_NUM:i.std_reg_num,FALSE_NUM:i.dfm_num,CURRENT_MARK:i.secured_mark,
                            FIRST_RV_MARK:i.first_rv_mark,FINAL_MARK:i.final_mark}
                            rvmlist1.append(rvmdic1)
                            dic2={RESULT:rvmlist1}
                        rvmList.append(dic2)
                        rvm_fetch.update({DATA:rvmList})
                        return jsonify(rvm_fetch)
                    else:
                        return revErr
                elif rev_type=="2":
                    cou_id=requestData[COURSE_ID]
                    prg_id=requestData[PRG_ID]
                    exam_id=requestData[EXAM_ID]
                    rvmResponse=Revaluation.query.filter_by(exam_id=exam_id,cou_id=cou_id,prg_id=prg_id).all()
                    if rvmResponse!=[]:
                        rvmList=[]
                        rvmlist1=[]
                        exam=Exam.query.filter_by(exam_id=exam_id).first()
                        program=ProgramDet.query.filter_by(prg_id=prg_id).first()
                        course=Course.query.filter_by(cou_id=cou_id).first()
                        rvmdic={EXAM_ID:exam_id,EXAM_NAME:exam.exam_name,PROGRAM_ID:program.prg_id,PROGRAM_NAME:program.prg_name,COURSE_ID:course.cou_id,COURSE_NAME:course.cou_name}
                        rvmList.append(rvmdic)
                        for i in rvmResponse:
                            if i.rv_status=="1":    
                                rvmdic1={REG_NUM:i.std_reg_num,FALSE_NUM:i.dfm_num,CURRENT_MARK:i.secured_mark,
                                FIRST_RV_MARK:i.first_rv_mark,SECOND_RV_MARK:i.second_rv_mark,FINAL_MARK:i.final_mark}
                                rvmlist1.append(rvmdic1)
                            dic2={RESULT:rvmlist1}
                        rvmList.append(dic2)
                        rvm_fetch.update({DATA:rvmList})
                        return jsonify(rvm_fetch)  
                    else:
                          return revErr
            else:
                return jsonify(session_invalid)
        except Exception as e:       
            return jsonify(error)

#=========================================================#
#       REVALUATION MARK LIST ENDS (AFTER  RV1 AND RV2)   #                           
#=========================================================#



#=========================================================#
#      SECOND RE EVALUATION MARK ENTRY STARTS             #
#=========================================================#

class SecondRevaluationMarkEntry(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            revallist=[]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                false_num=requestData[FALSE_NUM]
                mark=requestData[MARK]
                sec_rev=Revaluation.query.filter_by(dfm_num=false_num).first()                
                if sec_rev!=None:
                    sec_rev.second_rv_mark=mark
                    first_rv=sec_rev.first_rv_mark
                    final_rv=(first_rv+mark)/2
                    sec_rev.final_mark=final_rv
                    sec_rev.rv_status="2"
                    db.session.commit()
                    revobj=Revaluation.query.filter_by(dfm_num=false_num).first()
                    r_list={FALSE_NUM:revobj.dfm_num,FINALMARK:revobj.final_mark}
                    revallist.append(r_list)
                    secondRevalSuccess.update({DATA:revallist})
                    return jsonify(secondRevalSuccess)
                else:
                    return jsonify(secondRevalerr)
            else:
                return session_invalid
        except Exception as e:     
            return jsonify(error)
#=========================================================#
#      SECOND RE EVALUATION MARK ENTRY ENDS               #
#=========================================================#

#=========================================================#
#             REVALUATION MARK FINALIZE STARTS            #
#=========================================================#
class RevaluationMarkFinalize(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id)
            if sess_res:
                
                cou_id=requestData[COURSE_ID]
                prg_id=requestData[PRG_ID]
                exam_id=requestData[EXAM_ID]
                rvmResponse=Revaluation.query.filter_by(exam_id=exam_id,cou_id=cou_id,prg_id=prg_id).all()
                rvmList=[]
                rvmlist1=[]
                if  rvmResponse!=None:
                    
                    exam=Exam.query.filter_by(exam_id=exam_id).first()
                    program=ProgramDet.query.filter_by(prg_id=prg_id).first()
                    course=Course.query.filter_by(cou_id=cou_id).first()
                    rvmdic={EXAM_ID:exam_id,EXAM_NAME:exam.exam_name,PROGRAM_ID:program.prg_id,PROGRAM_NAME:program.prg_name,COURSE_ID:course.cou_id,COURSE_NAME:course.cou_name}
                    rvmList.append(rvmdic)
                    for i in rvmResponse:
                        rvmdic1={REG_NUM:i.std_reg_num,FALSE_NUM:i.dfm_num,CURRENT_MARK:i.secured_mark,FIRST_RV_MARK:i.first_rv_mark,SECOND_RV_MARK:i.second_rv_mark,FINAL_MARK:i.final_mark}
                        rvmlist1.append(rvmdic1)
                    dic2={RESULT:rvmlist1}
                    rvmList.append(dic2)
                    rvm_fetch.update({DATA:rvmList})
                    return jsonify(rvm_fetch)

                else:
                    return jsonify(invalid_id)    
                
            else:
                return jsonify(session_invalid)
        except Exception as e:
            print(e)
            return jsonify(err_exception)

#=========================================================#
#              REVALUATION MARK FINALIZE ENDS             #
#=========================================================#