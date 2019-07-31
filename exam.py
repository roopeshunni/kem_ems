
from model import *
from constants import *
from flask_restful import Resource, Api
import json
from flask import Flask,jsonify,request
from  pre_exam import  *
from datetime import *
from user_mngmnt import *
import random
import string
from sqlalchemy.sql import func
import smtplib
#=========================================================#
#                  EXAM ADD STARTS                        #                           
#=========================================================#
class ExamAdd(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if EXAM_ID in requestData:
                    exam_id=requestData[EXAM_ID]
                    examname_chk=Exam.query.filter_by(exam_id=exam_id,status=STATUS).first()
                  
                    if examname_chk !=None:
                        s_date=examname_chk.start_date
                        s_date=s_date.strftime('%Y-%m-%d')
                        e_date=examname_chk.end_date
                        e_date=e_date.strftime('%Y-%m-%d')
                        examdic={EXAM_ID:examname_chk.exam_id,EXAM_NAME:examname_chk.exam_name,
                        EXAM_CODE:examname_chk.exam_code,
                        START_DATE:s_date,END_DATE:e_date,STATUS1:examname_chk.status}
                    
                        examSingleFetch.update({DATA:examdic})                
                        return  jsonify(examSingleFetch)
                    else:
                        return invalidexam
                elif EXAM_CODE in requestData:
                    exam_name=requestData[EXAM_NAME]
                    exam_code=requestData[EXAM_CODE]
                    start_date=requestData[START_DATE]
                    end_date=requestData[END_DATE]
                    ex_name=exam_name.replace(" ","")
                    if len(ex_name)==0:
                        return jsonify(examNameError)
                    examname_chk=Exam.query.filter_by(exam_name=exam_name).first()
                    examcode_chk=Exam.query.filter_by(exam_code=exam_code).first()
                    if examname_chk !=None:
                        return jsonify(examName)
                    elif examcode_chk !=None:
                        return jsonify(examCode)
                    else:
                        addexam=Exam(exam_name=exam_name,exam_code=exam_code,start_date=start_date,end_date=end_date,status=STATUS)
                        db.session.add(addexam)
                        db.session.commit()
                        examdic={EXAM_NAME:exam_name,EXAM_CODE:exam_code,
                        START_DATE:start_date,END_DATE:end_date}
                        examSuccess.update({DATA:examdic})
                        return jsonify(examSuccess)
                else:
                    pass
            else:
                return session_invalid
        except Exception as e:
            return error

    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                examname_chk=Exam.query.filter_by(status=STATUS).all()
                examlist=[]
                for i in examname_chk:                    
                    s_date=i.start_date
                    s_date=s_date.strftime("%Y-%m-%d")
                    
                    e_date=i.end_date
                    e_date=e_date.strftime("%Y-%m-%d")
                    examdic={EXAM_ID:i.exam_id,EXAM_NAME:i.exam_name,EXAM_CODE:i.exam_code,
                    START_DATE:s_date,END_DATE:e_date,STATUS1:i.status}
                    examlist.append(examdic)
                    examFetch.update({DATA:examlist})  
                             
                return  examFetch
            else:
                return session_invalid
        except Exception as e:
            return error


    
    def put(self):
        try:
            requestdata=request.get_json()
            session_token=requestdata[SESSION_TOKEN]
            user_id=requestdata[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                exam_id=requestdata[EXAM_ID]
                exam_name=requestdata[EXAM_NAME]
                exam_code=requestdata[EXAM_CODE]
                start_date=requestdata[START_DATE]
                end_date=requestdata[END_DATE]
                namechk=Exam.query.filter(Exam.exam_id !=exam_id,Exam.exam_name ==exam_name,Exam.status==STATUS)
                codechk=Exam.query.filter(Exam.exam_id !=exam_id,Exam.exam_code ==exam_code,Exam.status==STATUS)
                namecount=(namechk.count())
                codecount=(codechk.count())
                if namecount>0:
                    return examName
                elif codecount>0:
                    return examCode
                else:
                    exam_chk=Exam.query.filter_by(exam_id=exam_id,status=STATUS).first()
                    if exam_chk!=None:
                        exam_chk.exam_name=exam_name
                        exam_chk.exam_code=exam_code
                        exam_chk.start_date=start_date
                        exam_chk.end_date=end_date
                        db.session.commit()
                        examdic={EXAM_ID:exam_id,EXAM_NAME:exam_name,EXAM_CODE:exam_code,
                        START_DATE:start_date,END_DATE:end_date}
                        examUpdate.update({DATA:examdic})
                        return examUpdate
                    else:
                        return invalidexam
            else:
                return session_invalid
        except Exception as e:           
            return error
            

    def delete(self):
        try:
            requestdata=request.get_json()
            session_token=requestdata[SESSION_TOKEN]
            user_id=requestdata[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                exam_id=requestdata[EXAM_ID]  
                invigilator_chk=ExamInvigilator.query.filter_by(exam_id=exam_id).first()
                cs_chk=ChiefSuptd.query.filter_by(exam_id=exam_id).first()
                article_chk=ArticleDistribution.query.filter_by(exam_id=exam_id,art_status=STATUS).first()  
                stud_chk=Student.query.filter_by(exam_id=exam_id,status=STATUS).first()   
                hall_chk=HallAllotment.query.filter_by(exam_id=exam_id).first()               
                exam_chk=Exam.query.filter_by(exam_id=exam_id,status=STATUS).first()
                camp_chk=Camp.query.filter_by(exam_id=exam_id,camp_status=STATUS).first()
                asd_chk=AnswerScriptDispatch.query.filter_by(exam_id=exam_id,ans_dispatch_status=STATUS).first()
                chief_chk=ChiefExaminer.query.filter_by(exam_id=exam_id,status=STATUS).first()
                if invigilator_chk!=None or article_chk!=None or stud_chk!=None or hall_chk!=None:
                    return examDeleteError
                if camp_chk!=None or  asd_chk!=None or chief_chk!=None or cs_chk!=None:
                    return examDeleteError
                if exam_chk!= None:
                    db.session.delete(exam_chk)
                    db.session.commit()
                    examdic={EXAM_ID:exam_id,EXAM_NAME:exam_chk.exam_name,EXAM_CODE:exam_chk.exam_code}
                    examDeleted.update({DATA:examdic})
                    return examDeleted
                else:
                    return invalidexam
            else:
                return session_invalid
        except Exception as e:         
            return error



#=========================================================#
#                  EXAM ADD ENDS                          #                           
#=========================================================#



#=========================================================#
#                  CAMP ADD STARTS                        #                           
#=========================================================#
def mapfunc(n):
    dict1=n._asdict()
    dict1["end_date"]=dict1["end_date"].strftime("%Y-%m-%d")
    dict1["start_date"]=dict1["start_date"].strftime("%Y-%m-%d")
    return dict1

class Camp_Add(Resource):
    
    def post(self):
        try:
            requestData=request.get_json()            
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
           
            if sess_res:
                if CAMP_ID in  requestData:
                    
                    camp_id1=requestData[CAMP_ID]
                    singlecamp=Camp.query.filter_by(camp_id=camp_id1,camp_status=STATUS).first()                   
                    
                    if singlecamp!=None:
                        cenchk=Center_det.query.filter_by(cen_id=singlecamp.cen_id).first()
                        prgchk=ProgramDet.query.filter_by(prg_id=singlecamp.prg_id).first()
                        examchk=Exam.query.filter_by(exam_id=singlecamp.exam_id).first()
                        # examend_date=examchk.end_date
                        
                        s_date=singlecamp.start_date
                        s_date=s_date.strftime("%Y-%m-%d")
                       

                        e_date=singlecamp.end_date
                        e_date=e_date.strftime("%Y-%m-%d")
                        # if(examend_date>datetime.strptime(s_date, '%Y-%m-%d').date()):
                        #     return camp_date_err
                        
                       
                        d={CAMP_ID:singlecamp.camp_id,CENTRE_ID:singlecamp.cen_id,CEN_NAME:cenchk.cen_name,CEN_DISTRICT:cenchk.cen_dist,
                        PRG_ID:singlecamp.prg_id,PRG_NAME:prgchk.prg_name,EXAM_ID:singlecamp.exam_id,EXAM_NAME:examchk.exam_name,START_DATE:s_date,END_DATE:e_date}
                        camp_success_single_fetch.update({DATA:d})
                        return camp_success_single_fetch
                    else:
                        return camp_invalid_id

                elif CENTRE_ID in requestData and EXAM_ID in requestData:
                   
                    
                    camplist=[]
                    cen_id1=requestData[CENTRE_ID]
                    exam_id1=requestData[EXAM_ID]
                    prg_id1=requestData[PRG_ID]
                    start_date1=requestData[START_DATE]
                    end_date1=requestData[END_DATE]
                    status1=STATUS
                    # if(start_date1>end_date1):
                    #     return ""
                    camp_exist=Camp.query.filter_by(cen_id=cen_id1,exam_id= exam_id1,prg_id= prg_id1).first()
                    
                    exam=Exam.query.filter_by(exam_id=exam_id1).first()
                    examend_date=exam.end_date
                    
                    if(examend_date>datetime.strptime(start_date1, '%Y-%m-%d').date()):
                        return camp_date_err
                    # examend_date=examend_date.strftime("%Y%m%d")
                   
                    # print(examend_date)
                    # s_date=camp_exist.start_date
                    # s_date=s_date.strftime("%Y%m%d")
                    # st_date=int(examend_date)<int(s_date)

                    # e_date=singlecamp.end_date
                    # e_date=e_date.strftime("%Y%m%d")
                    # ed_date=int(s_date)<int(e_date)    


                    campdic={CENTRE_ID:cen_id1,EXAM_ID:exam_id1,PRG_ID:prg_id1,START_DATE:start_date1,END_DATE:start_date1}
                    
                    camplist.append(campdic)
                    if camp_exist!=None:

                        return cen_exam_prg_exist_id
                    else:
                        new_camptlist=Camp(cen_id=cen_id1,exam_id=exam_id1,prg_id=prg_id1,start_date=start_date1,end_date=end_date1,camp_status=status1)
                        db.session.add(new_camptlist)
                       
                        db.session.commit()
                        camp_success_add.update({DATA:camplist})
                        return camp_success_add
            else:
                session_invalid
        except Exception as e:
           
            return sec_bad_request


    def get(self):
        try:
            
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:                
                cur_time=datetime.now()
                c_date=cur_time.strftime("%Y-%m-%d")
                campData=db.session.query(Camp,Exam,Center_det,ProgramDet).with_entities(Camp.camp_id,Exam.exam_id,Exam.exam_name,Center_det.cen_id.label("centre_id"),Center_det.cen_name,Center_det.cen_dist,Camp.end_date,Camp.start_date,ProgramDet.prg_id,ProgramDet.prg_name).filter(Camp.end_date>c_date,Exam.exam_id==Camp.exam_id,Center_det.cen_id==Camp.cen_id,ProgramDet.prg_id==Camp.prg_id,Camp.camp_status==STATUS).all()               
                campRes=list(map(mapfunc,campData))
                camp_fetch.update({DATA:campRes}) 
                return jsonify(camp_fetch)                
            else:
                return jsonify(session_invalid)        
        except Exception as e:
            return br_bad_request  

    def put(self):
        try:
            requestData=request.get_json()
            camp_id1=requestData[CAMP_ID]
            cen_id1=requestData[CENTRE_ID]
            exam_id1=requestData[EXAM_ID]
            prg_id1=requestData[PRG_ID]
            start_date1=requestData[START_DATE]
            end_date1=requestData[END_DATE]
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                camplist=[]
                singlecampid=Camp.query.filter_by(camp_id=camp_id1).first()
                singlecentreid=Center_det.query.filter_by(cen_id=cen_id1).first()
                singleprogramid=ProgramDet.query.filter_by(prg_id=prg_id1).first()
                singleexamid=Exam.query.filter_by(exam_id=exam_id1).first()
                if singlecentreid==None:
                    return invalid_id
                elif singleexamid==None:
                    return invalid_id
                elif singleprogramid==None:
                    return invalid_id
                elif singlecampid!=None:
                    singlecampid.cen_id=cen_id1
                    singlecampid.exam_id=exam_id1

                    

                    singlecampid.prg_id=prg_id1
                    singlecampid.start_date=start_date1
                    singlecampid.end_date=end_date1

                    examend_date=singleexamid.end_date
                    
                    if(examend_date>datetime.strptime(start_date1, '%Y-%m-%d').date()):
                        return camp_date_err

                    db.session.commit()
                    campdic={CAMP_ID:camp_id1,CENTRE_ID:cen_id1,EXAM_ID:exam_id1,PRG_ID:prg_id1,START_DATE:start_date1,END_DATE:end_date1}
                    camplist.append(campdic)
                    camp_success_edit.update({DATA:camplist})
                    single=RoleDet.query.filter_by(role_meta=CHAIRMAN).first()
                    roleid=single.role_id
                    singlechairman=ChiefSuptd.query.filter_by(cen_id=cen_id1,exam_id=exam_id1,role_id=roleid).first()
                    if singlechairman!=None:
                        singlechairman.exp_date=end_date1
                    db.session.commit()
                    
                    return camp_success_edit
                else:
                    return camp_invalid_id
            else:
                return session_invalid
        except Exception as e:
            return jsonify(br_bad_request)


    def delete(self):
        try:            
            requestData=request.get_json()
            camp_id1=requestData[CAMP_ID]
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                camplist=[]
                singlecamp=Camp.query.filter_by(camp_id=camp_id1).first() 
                if singlecamp!=None:
                    campdic={CAMP_ID:singlecamp.camp_id,CENTRE_ID:singlecamp.cen_id,EXAM_ID:singlecamp.exam_id,CAMP_STATUS:singlecamp.camp_status}
                    db.session.delete(singlecamp)
                    db.session.commit()
                    camplist.append( campdic)
                    camp_success_delete.update({DATA:campdic})
                    return camp_success_delete
                else:
                    return camp_invalid_id
            else:
                return session_invalid
        except Exception as e:
            return art_bad_request


#=========================================================#
#                  CAMP ADD ENDS                          #                           
#=========================================================#

#=========================================================#
#          ACCESS KEY GENERATION STARTS                   #                           
#=========================================================#

class AccessKeyGeneration(Resource):
    def post(self):
            try:
                requestData=request.get_json()
                session_token=requestData[SESSION_TOKEN]
                user_id=requestData[USER_ID]
                invList=[]
                list1=[]
                # listCount = False
                sess_res=checkSessionValidity(session_token,user_id) 
                if sess_res:
                    cur_time=datetime.now()
                    role_chk=RoleDet.query.filter_by(role_meta=CHIEFSUPERINTENDENT).first()
                    cs_chk=ChiefSuptd.query.filter_by(user_id=user_id,role_id=role_chk.role_id).first()
                    if cs_chk==None:
                        return invalidcs
                    start_date=datetime.now().strftime("%Y-%m-%d 00:00:00")
                    end_date=datetime.now().strftime("%Y-%m-%d 23:59:59")
                    c_date=cur_time.strftime("%Y-%m-%d")
                    c_time=cur_time.strftime("%H%M")
                    if int(c_time)<1230:
                        section=FN
                    elif int(c_time)>1230:
                        section=AN 
                    if section==FN:
                        expire_date="1:00 PM"
                    elif section==AN:
                        expire_date="5:30 PM"
                    examDate=ExamTimetable.query.filter(ExamTimetable.date>=start_date,ExamTimetable.date<=end_date,ExamTimetable.section==section).all()
                    if examDate!=[]:
                        
                        for i in examDate:
                            stud_chk=Student.query.filter_by(exam_id=i.exam_id,cen_id=cs_chk.cen_id,status=STATUS).first()
                            
                            if stud_chk!=None:
                                invg_chk=ExamInvigilator.query.filter_by(cen_id=cs_chk.cen_id,exam_id=i.exam_id,invig_status=STATUS).all()
                                for j in invg_chk:
                                    invList.append(j.user_id)
                            else:
                                return emptyStudents
                    else:
                        return noExam
                    for i in invList:
                        
                        access_chk=AccessKeyGen.query.filter(AccessKeyGen.exp_date>=start_date,AccessKeyGen.exp_date<=end_date,
                        AccessKeyGen.examSection==section,AccessKeyGen.cen_id==cs_chk.cen_id,AccessKeyGen.inv_id==i,AccessKeyGen.key_status==STATUS).first()
                        
                        user_chk=User_det.query.filter_by(user_id=i,status=STATUS).first()
                        
                        if access_chk==None:
                            listCount = False

                            access_code=generate_code()
                            access_keyadd=AccessKeyGen(cen_id=cs_chk.cen_id,examSection=section,
                            access_code=access_code,inv_id=i,exp_date=cur_time,key_status=STATUS)
                            db.session.add(access_keyadd)
                            db.session.commit()
                            userInfo=User_det.query.filter_by(user_id=i).first()
                            email=userInfo.usr_email
                            name=userInfo.name
                            send_mail(email,access_code,name)
                            dic={CEN_ID:cs_chk.cen_id,USER_ID:i,USER_NAME:user_chk.name,ACCESS_CODE:access_code,EXP_DATE:expire_date,EXAM_SECTION:section}
                            
                            list1.append(dic)
                            resultList=sorted(list1, key = lambda k:k[USER_NAME])
                        else:
                            dic={CEN_ID:cs_chk.cen_id,USER_ID:i,USER_NAME:user_chk.name,ACCESS_CODE:access_chk.access_code,
                            EXP_DATE:expire_date,EXAM_SECTION:access_chk.examSection} 
                            list1.append(dic)
                            resultList=sorted(list1, key = lambda k:k[USER_NAME])
                            accessCenter.update({DATA:resultList})
                            listCount = True
                    accesskeysuccess.update({DATA:resultList})
                    if listCount:
                        return accessCenter
                    else:
                        return accesskeysuccess
                    
                else:
                    return session_invalid
            except Exception as e: 
                return error


def generate_code():
    char_set = string.ascii_uppercase + string.digits
    return ''.join(random.sample(char_set*6, 6))


def send_mail(username,art_key,name):

    host='smtp.gmail.com'
    port=587
    email='smashx2018@gmail.com'
    password="tedaaststewbwlhk"
    subject="Access code"
    mail_to=username
    mail_from=email
    body="Hi {name}, \n Your access code is {id}. \n\n Chief Superintendent ".format(name=name,id=art_key)
    
    # return u_id

    message = """From: %s\nTo:
    %s\nSubject:
    %s\n\n%s""" % (mail_from, mail_to, subject, body)
    

    # try:

    server = smtplib.SMTP(host, port)
    server.ehlo()
    server.starttls()
    server.login(email, password)
    server.sendmail(mail_from, mail_to, message)
    server.close()
    #     return 1
    # except Exception as e:
    #         return art_bad_request

#=========================================================#
#          ACCESS KEY GENERATION ENDS                     #                           
#=========================================================#

#=========================================================#
#                ACCESS KEY LISTING STARTS                #                           
#=========================================================#

class AccessKeyListing(Resource):
    def post(self):
            try:
                requestData=request.get_json()
                session_token=requestData[SESSION_TOKEN]
                user_id=requestData[USER_ID]
                exam_id=requestData[EXAM_ID]
                course_id=requestData[COURSE_ID]
                cen_id=requestData[CEN_ID]
                sess_res=checkSessionValidity(session_token,user_id) 
                if sess_res:
                    access_chk=AccessKeyGen.query.filter_by(cen_id=cen_id,exam_id=exam_id,course_id=course_id,key_status=STATUS).all()
                    accessList=[]
                    if access_chk!=[]:
                        for i in access_chk:
                            user_chk=User_det.query.filter_by(user_id=i.inv_id,status=STATUS).first()
                            exam_chk=Exam.query.filter_by(exam_id=i.exam_id,status=STATUS).first()
                            center_chk=Center_det.query.filter_by(cen_id=i.cen_id,status=STATUS).first()
                            course_chk=Course.query.filter_by(cou_id=i.course_id,cou_status=STATUS).first()
                            accessdtl={INVIG_ID:user_chk.user_id,INVIG_NAME:user_chk.name,
                            EXAM_ID:i.exam_id,EXAM_NAME:exam_chk.exam_name,CENTER_ID:i.cen_id,CENTER_NAME:center_chk.cen_name,
                            COURSE_ID:i.course_id,COURSE_NAME:course_chk.cou_name,ACCESS_CODE:i.access_code}
                            accessList.append(accessdtl)
                        accesskeyFetch.update({DATA:accessList})
                        return accesskeyFetch
                    else:
                        return invalidInvg

                else:
                    return session_invalid
            except Exception as e:         
                return error

#=========================================================#
#                ACCESS KEY LISTING ENDS                  #                           
#=========================================================#

#=========================================================#
#                FETCHING ALL ACCESS KEY STARTS           #                           
#=========================================================#
class FetchingAllAccessKey(Resource):
    def get(self):
            try:
                session_token=request.headers[SESSION_TOKEN]
                user_id=request.headers[USER_ID]
                sess_res=checkSessionValidity(session_token,user_id) 
                if sess_res:
                    start_date=datetime.now().strftime("%Y-%m-%d 00:00:00")
                    cs_chk=ChiefSuptd.query.filter_by(user_id=user_id,status=STATUS).first()
                    if cs_chk==None:
                        return invalidcs
                    access_chk=AccessKeyGen.query.filter(AccessKeyGen.exp_date>=start_date,AccessKeyGen.cen_id==cs_chk.cen_id,AccessKeyGen.key_status==STATUS).all()
                    accessList=[]
                    if access_chk!=[]:
                        for i in access_chk:
                                date=i.exp_date
                                s_date=date.strftime("%Y-%m-%d")
                                user_chk=User_det.query.filter_by(user_id=i.inv_id,status=STATUS).first()
                                exam_chk=Exam.query.filter_by(exam_id=i.exam_id,status=STATUS).first()
                                center_chk=Center_det.query.filter_by(cen_id=i.cen_id,status=STATUS).first()
                                course_chk=Course.query.filter_by(cou_id=i.course_id,cou_status=STATUS).first()
                                accessdtl={INVIG_ID:user_chk.user_id,INVIG_NAME:user_chk.name,
                                EXAM_ID:i.exam_id,EXAM_NAME:exam_chk.exam_name,CENTER_ID:i.cen_id,CENTER_NAME:center_chk.cen_name,
                                COURSE_ID:i.course_id,COURSE_NAME:course_chk.cou_name,ACCESS_CODE:i.access_code,DATE:s_date}
                                accessList.append(accessdtl)
                        accesskeyFetch.update({DATA:accessList})
                        return accesskeyFetch
                    else:
                        return noAccesskey
                else:
                    return session_invalid
            except Exception as e:  
                  
                return error

#=========================================================#
#                FETCHING ALL ACCESS KEY ENDS             #                           
#=========================================================#


#========================================================#
#                    MOBILE                              #
#========================================================#



#=========================================================#
#           GENERAL INFO LIST STARTS                      #                           
#=========================================================#
class General_infoList(Resource):
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                invg_chk=ExamInvigilator.query.filter_by(user_id=user_id).first()
                if invg_chk!=None:
                    center_chk=Center_det.query.filter_by(cen_id=invg_chk.cen_id).first()
                    exam_chk=Exam.query.filter_by(exam_id=invg_chk.exam_id).first()
                    role_chk=RoleDet.query.filter_by(role_meta=CHIEFSUPERINTENDENT).first()
                    cs_chk=ChiefSuptd.query.filter_by(exam_id=invg_chk.exam_id,cen_id=invg_chk.cen_id,role_id=role_chk.role_id).first()
                    if cs_chk==None:
                        return nocs
                    if center_chk==None or exam_chk==None:
                        return invalid
                    cs_user_chk=User_det.query.filter_by(user_id=cs_chk.user_id).first()
                    if cs_user_chk==None:
                        return invalid
                    response=general_info(user_id,center_chk,cs_chk,cs_user_chk,invg_chk)
                    return jsonify(response)
                else:
                    return invalidInvg
            else:
                return session_invalid
        except Exception as e:        
            return error


def general_info(user_id,center_chk,cs_chk,cs_user_chk,invg_chk):
    start_date=datetime.now().strftime("%Y-%m-%d 00:00:00")    
    end_date=datetime.now().strftime("%Y-%m-%d 23:59:59")
    access_chk=AccessKeyGen.query.filter(AccessKeyGen.inv_id==user_id,AccessKeyGen.exp_date>=start_date,AccessKeyGen.exp_date<=end_date,AccessKeyGen.key_status==STATUS).all()
    cur_time=datetime.now()
    # c_date=cur_time.strftime("%Y-%m-%d")
    c_time=cur_time.strftime("%H%M")
    list1=[]
    if int(c_time)<1230:
        section=FN
    elif int(c_time)>1230:
        section=AN 
    if  access_chk!=[]:
        invg_chk=ExamInvigilator.query.filter_by(user_id=user_id).all()
        for i in invg_chk:
            exam_chk=Exam.query.filter_by(exam_id=i.exam_id).first()
            time_table_chk=ExamTimetable.query.filter(ExamTimetable.date>=start_date,ExamTimetable.date<=end_date,ExamTimetable.status==STATUS,
            ExamTimetable.exam_id==i.exam_id,ExamTimetable.section==section).first()
            if time_table_chk!=None:
                course_chk=Course.query.filter_by(cou_id=time_table_chk.cou_id).first()
                prm_chk=ProgramDet.query.filter_by(prg_id=time_table_chk.prg_id).first()
                generalInfo_dic={CENTER_ID:center_chk.cen_id,CENTER_NAME:center_chk.cen_name,COURSE_ID:course_chk.cou_id,
                COURSE_NAME:course_chk.cou_name,PROGRAM_ID:prm_chk.prg_id,PROGRAM_NAME:prm_chk.prg_name,
                EXAM_ID:exam_chk.exam_id,EXAM_NAME:exam_chk.exam_name,CS_ID:cs_chk.chief_suptd_id,CS_NAME:cs_user_chk.name}
                list1.append(generalInfo_dic)
        generalinfoFetch.update({DATA:list1})
        return generalinfoFetch
    else: 
        return generalInfoUnavilable 


         



#=========================================================#
#           GENERAL INFO LIST ENDS                        #                           
#=========================================================#



#=========================================================#
#      ACCESS KEY VERIFICATION STARTS                     #                           
#=========================================================#
class AccessKeyVerification(Resource):
    def post(self):
            try:
                requestData=request.get_json()
                session_token=requestData[SESSION_TOKEN]
                user_id=requestData[USER_ID]
                access_code=requestData[ACCESS_CODE]
                sess_res=checkSessionValidity(session_token,user_id) 
                if sess_res:
                    invg_chk=ExamInvigilator.query.filter_by(user_id=user_id).first()
                    if invg_chk==None:
                        return invalidInvg
                    cur_time=datetime.now()
                    # c_date=cur_time.strftime("%Y-%m-%d")
                    c_time=cur_time.strftime("%H%M")
                    if int(c_time)<1230:
                        section=FN
                    elif int(c_time)>1230:
                        section=AN     
                    access_chk=AccessKeyGen.query.filter_by(cen_id=invg_chk.cen_id,inv_id=user_id,key_status=STATUS,examSection=section).first()
                    if access_chk!=None:
                        if section==FN:
                            if access_chk.access_code==access_code:
                                ex_date=access_chk.exp_date
                                e_date=ex_date.strftime("%Y%m%d")
                                # exp_date=e_date+"180000"
                                
                                exp_date=e_date+"130000"
                                c_date=cur_time.strftime("%Y%m%d%H%M%S")
                                if int(c_date)>int(exp_date):
                                    return accesscodeexpired
                                else:
                                    return codeVsuccess
                            else:
                                return incorrectcode
                        elif section==AN:
                            if access_chk.access_code==access_code:
                                ex_date=access_chk.exp_date
                                e_date=ex_date.strftime("%Y%m%d")
                                
                                #for testing purpose
                                exp_date=e_date+"220000"
                                c_date=cur_time.strftime("%Y%m%d%H%M%S")
                                if int(c_date)>int(exp_date):
                                    return accesscodeexpired
                                else:
                                    return codeVsuccess
                            else:
                                return incorrectcode
                    else:
                        return invalidInvg
                else:
                    return session_invalid
            except Exception as e:            
                return error

#=========================================================#
#            ACCESS KEY VERIFICATION ENDS                 #                           
#=========================================================#

#=========================================================#
#              STUDENT TEMP MAP  STARTS                   #                           
#=========================================================#
class StudentTempMapp(Resource):
    def post(self):
            try:
                requestData=request.get_json()
                session_token=requestData[SESSION_TOKEN]
                user_id=requestData[USER_ID]                                
                sess_res=checkSessionValidity(session_token,user_id) 
                if sess_res:
                    # e_id=requestData[EXAM_ID]
                    s_reg_num=requestData[STUDENT_REGISTER_NUMBER]
                    s_false_num=requestData[STUDENT_FALSE_NUMBER]
                    s_smp_status=requestData[STUDENT_SMP_STATUS]
                    exam_date=datetime.now().strftime("%Y-%m-%d 23:59:59")
                    cur_time=datetime.now()
                    c_time=cur_time.strftime("%H%M")
                    if int(c_time)<1230:
                        
                        ex_date=cur_time.strftime("%Y-%m-%d 09:30:00")
                        
                    elif int(c_time)>1230:
                        ex_date=cur_time.strftime("%Y-%m-%d 13:30:00")
                    hallList=db.session.query(Student,ExamInvigilator,HallAllotment).with_entities(HallAllotment.hall_id.label(EXAM_HALL_ID),ExamInvigilator.cen_id.label(CENTER_ID)).filter(ExamInvigilator.user_id==user_id,Student.std_reg==s_reg_num,Student.std_id==HallAllotment.std_id,HallAllotment.prg_id==Student.prg_id).all()
                    # print(hallList)
                    resData=list(map(lambda n:n._asdict(),hallList))
                    # e_id=resData[0].get(EXAM_ID)
                    invHallExistance=InvigilatorExamHall.query.filter(InvigilatorExamHall.cen_id==resData[0].get(CENTER_ID),InvigilatorExamHall.hall_id==resData[0].get(EXAM_HALL_ID),
                    InvigilatorExamHall.inv_id==user_id,InvigilatorExamHall.exam_date<exam_date).first()
                    # First mapping of a student
                    if invHallExistance==None:
                        newInv=InvigilatorExamHall(cen_id=resData[0].get(CENTER_ID),hall_id=resData[0].get(EXAM_HALL_ID),inv_id=user_id,exam_date=ex_date)
                        db.session.add(newInv)
                        # db.session.commit()                    
                    tmp_mapp_obj=StudTempMapp(std_reg_num=s_reg_num,std_false_num=s_false_num,smp_status=s_smp_status,inv_id=user_id,std_temp_status=STATUS)
                    db.session.add(tmp_mapp_obj)
                    db.session.commit()
                    
                    return jsonify(tmp_map_success)
                else:
                    return session_invalid
            except Exception as e: 
                return jsonify(error)

class TempMapp(Resource):
    def post(self):
        requestData=request.get_json()
        session_token=requestData[SESSION_TOKEN]
        user_id=requestData[USER_ID]                                
        sess_res=checkSessionValidity(session_token,user_id) 
        if sess_res:
            s_reg_num=requestData[STUDENT_REGISTER_NUMBER]
            s_false_num=requestData[STUDENT_FALSE_NUMBER]
            s_smp_status=requestData[STUDENT_SMP_STATUS]
            # inv_existance=ExamInvigilator.query.filter_by(user_id=user_id,exam_id=e_id,invig_status=STATUS).first()
            # t_map_exist=StudTempMapp.query.filter_by(std_reg_num=s_reg_num,std_false_num=s_false_num,inv_id=user_id).first()
            # if t_map_exist!=None:
            #     return jsonify(tmp_map_exist)
            # if inv_existance==None:
            #     return jsonify(tmp_map_err)
            hallList=db.session.query(Student,ExamInvigilator,HallAllotment,ExamHall).with_entities(HallAllotment.hall_id.label(EXAM_HALL_ID),ExamHall.hall_no.label(EXAM_HALL_NUMBER),ExamHall.hall_name.label(EXAM_HALL_NAME),ExamInvigilator.cen_id.label(CENTER_ID),ExamInvigilator.exam_id.label(EXAM_ID),Student.std_name.label(STUDENT_NAME)).filter(ExamInvigilator.user_id==user_id,Student.std_reg==s_reg_num,Student.std_id==HallAllotment.std_id,HallAllotment.prg_id==Student.prg_id,ExamHall.hall_id==HallAllotment.hall_id).all()
            resData=list(map(lambda n:n._asdict(),hallList))
            tmp_map_confirm.update({DATA:{RESULT_DATA:resData}})
            return jsonify(tmp_map_confirm)
        else:
            return session_invalid
#=========================================================#
#              STUDENT TEMP MAP  ENDS                     #                           
#=========================================================#



#=========================================================#
#              STUDENT ALLOTMENT LIST STARTS              #                           
#=========================================================#

# class AllotementStudentList(Resource):
#     def get(self):
#         try:
#             session_token=request.headers[SESSION_TOKEN]
#             user_id=request.headers[USER_ID]
#             sess_res=checkSessionValidity(session_token,user_id) 
#             if sess_res:
#                 studentList=db.session.query()                
#                 else:
#                     return invalidInvg
#             else:
#                 return session_invalid
#         except Exception as e:          
#             return error


#=========================================================#
#              STUDENT ALLOTMENT LIST  ENDS               #                           
#=========================================================#





#=========================================================#
#            STUDENT  MAPPING  STARTS                     #                           
#=========================================================#
class StudentMapp(Resource):
    def post(self):
            try:
                requestData=request.get_json()
                session_token=requestData[SESSION_TOKEN]
                user_id=requestData[USER_ID]                                
                sess_res=checkSessionValidity(session_token,user_id) 
                if sess_res:
                    # e_id=requestData[EXAM_ID]
                    p_data=requestData[PAIRED_DATA]                    
                    c_id=requestData[CENTER_ID]
                    
                    e_date=datetime.now()
                    e_date=e_date.strftime("%Y-%m-%d")
                    for singleStudent in p_data:
                        
                        stud=Student.query.filter_by(std_reg=singleStudent.get(STUDENT_REGISTER_NUMBER)).first()
                        e_id=stud.exam_id
                        p_id=stud.prg_id
                        timeTableList=ExamTimetable.query.filter_by(exam_id=e_id,prg_id=p_id).all()                        
                        for firstCourse in timeTableList:
                            t_date=firstCourse.date
                            t_date=t_date.strftime("%Y-%m-%d")
                            if t_date==e_date:
                                cr_id=firstCourse.cou_id

                            
                            
                        # return stud.prg_id
                        # false_already_exist=FalseNumber.query.filter(or_(FalseNumber.dfm_num==singleStudent.get(STUDENT_FALSE_NUMBER),FalseNumber.std_reg_num==singleStudent.get(STUDENT_FALSE_NUMBER))).first()
                        false_already_exist=FalseNumber.query.filter_by(dfm_num=singleStudent.get(STUDENT_FALSE_NUMBER)).first()
                        student_already_exist=FalseNumber.query.filter_by(std_reg_num=singleStudent.get(STUDENT_REGISTER_NUMBER),exam_id=e_id,cou_id=cr_id).first()
                        if false_already_exist!=None :
                            return jsonify(false_already_exist_err)
                        if student_already_exist !=None:
                            return jsonify(false_already_exist_err)
                        new_student=FalseNumber(std_reg_num=singleStudent.get(STUDENT_REGISTER_NUMBER),dfm_num=singleStudent.get(STUDENT_FALSE_NUMBER),exam_id=e_id,cou_id=cr_id,inv_id=user_id,dfm_date=e_date,cs_id=UPDATE_ID,cs_submit_date=UPDATE_DATE,aso_id=UPDATE_ID,aso_verify_date=UPDATE_DATE,so_id=UPDATE_ID,so_approved_date=UPDATE_DATE,smp_status=singleStudent.get(STUDENT_SMP_STATUS),dfm_status=UPDATE_ID,dfm_flag=UPDATE_ID,cen_id=c_id)
                        db.session.add(new_student)
                        db.session.commit()                                           
                    return tmp_map_success                    
                else:
                    return session_invalid
            except Exception as e:        
                return jsonify(error)
#=========================================================#
#              STUDENT  MAPPING  ENDS                     #                           
#=========================================================#

#=========================================================#
#               STUDENT MAPPING VIEW STARTS               #                           
#=========================================================#
class MappingView(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            exam_id=requestData[EXAM_ID]
            center_id=requestData[CENTER_ID]
            course_id=requestData[COURSE_ID]
            hall_id=requestData[EXAM_HALL_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                hall_chk=HallAllotment.query.filter_by(cen_id=center_id,exam_id=exam_id,cou_id=course_id,hall_id=hall_id).all()
                
                if hall_chk!=[]:
                    student_details=[]
                    center_chk=Center_det.query.filter_by(cen_id=center_id).first()
                    exam_chk=Exam.query.filter_by(exam_id=exam_id).first()
                    course_chk=Course.query.filter_by(cou_id=course_id).first()
                    c=0
                    for i in hall_chk:
                        # print(i.std_id)
                        std_chk=Student.query.filter_by(std_id=i.std_id).first()
                        
                        false_chk=FalseNumber.query.filter_by(std_reg_num=std_chk.std_reg).first()
                        
                        # print(inv_id)
                        if false_chk!=None:
                            c=1
                            
                            # inv_id=false_chk.inv_id
                            inv_id=false_chk.inv_id
                            df_date=false_chk.dfm_date
                            dic={STUDREG:false_chk.std_reg_num,FALSENO:false_chk.dfm_num,STUDNAME:std_chk.std_name,
                            SMP_STATUS:false_chk.smp_status}
                            
                            student_details.append(dic)
                    if c==1:

                        user_chk=User_det.query.filter_by(user_id=inv_id).first()
                        
                        df_date=datetime.now()
                        exam_dt=df_date.strftime("%Y-%m-%d")
                        # exam_dt=df_date.strftime("%Y-%m-%d")
                        examDetails={CENTER_NAME:center_chk.cen_name,EXAM_NAME:exam_chk.exam_name,EXAM_DATE:exam_dt,
                        COURSE_NAME:course_chk.cou_name,INVIG_NAME:user_chk.name}
                        Dic={STUDENT_DETAILS:student_details,EXAM_DETAILS:examDetails}
                        falseFetch.update({DATA:Dic})
                        return falseFetch
                    else:
                        return noFlaseNumber
                else:
                    return invaliddata
            else:
                return session_invalid
        except Exception as e:  
            # print(e)         
            return error


#=========================================================#
#               STUDENT MAPPING VIEW ENDS                 #                           
#=========================================================#

#=========================================================#
#  INVIGILATOR ABSENTEE_STATEMENT GENERATION STARTS       #                           
#=========================================================#


class InvigilatorASGeneration(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            exam_id=requestData[EXAM_ID]
            cen_id=requestData[CENTER_ID]
            prg_id=requestData[PROGRAM_ID]
            cou_id=requestData[COURSE_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            absenteeList=[]
            resultList=[]
            mappedList=[]
            allotedList=[]
            if sess_res:
                inv_chk=FalseNumber.query.filter_by(inv_id=user_id).first()
                if inv_chk!=None:
                    dfm_chk=FalseNumber.query.filter(FalseNumber.inv_id==user_id,FalseNumber.dfm_status==1)
                    if dfm_chk.count()>0:
                        return ASerror
                    stud_chk=Student.query.filter_by(exam_id=exam_id,cen_id=cen_id,prg_id=prg_id).all()
                    if stud_chk!=[]:
                        completeStudList=[]
                        for i in stud_chk:
                            completeStudDic={STUDENT_ID:i.std_id,STUDREG:i.std_reg,STUDNAME:i.std_name}
                            completeStudList.append(completeStudDic)
                            false_chk=FalseNumber.query.filter_by(exam_id=exam_id,cen_id=cen_id,cou_id=cou_id,std_reg_num=i.std_reg,inv_id=user_id).first()
                            if false_chk==None:
                                continue
                            mapped_dic={STUDENT_ID:i.std_id,EXAM_ID:exam_id,CENTER_ID:cen_id,COURSE_ID:cou_id,STUDREG:i.std_reg,STUDNAME:i.std_name,
                            SMP_STATUS:false_chk.smp_status}
                            mappedList.append(mapped_dic)

                        for i in mappedList:
                            std_id=i.get(STUDENT_ID)
                        hall_chk=HallAllotment.query.filter_by(exam_id=exam_id,cen_id=cen_id,prg_id=prg_id,cou_id=cou_id,std_id=std_id).first()  
                        if hall_chk!=None:
                            hallStud_chk=HallAllotment.query.filter_by(exam_id=exam_id,cen_id=cen_id,prg_id=prg_id,cou_id=cou_id,hall_id=hall_chk.hall_id).all()
                            for j in hallStud_chk:
                                hallDic={STUDENT_ID:j.std_id}
                                allotedList.append(hallDic)
                        allotedIdList=[]
                        mappedIdList=[]
                        for i in allotedList:
                            allotedIdList.append(i.get(STUDENT_ID))
                        for j in mappedList:
                            mappedIdList.append(j.get(STUDENT_ID))
                        resultIdList=[elem for elem  in allotedIdList if elem not in mappedIdList]
                        for singleStudent in completeStudList:
                            for resId in resultIdList:
                                if resId==singleStudent.get(STUDENT_ID):
                                    absenteeDic={STUDENT_ID:singleStudent.get(STUDENT_ID),STUDREG:singleStudent.get(STUDREG),
                                    STUDNAME:singleStudent.get(STUDNAME)}
                                    absenteeList.append(absenteeDic)
                        resultList.append({PRESENT_LIST:mappedList})
                        resultList.append({ABSENTEE_LIST:absenteeList})
                        falseFetch.update({DATA:{RESULT_DATA:resultList}})
                        return jsonify(falseFetch)
                    else:
                        return jsonify(invData)
                else:
                    return jsonify(ASinvalidInvg)
                    
            else:
                return jsonify(sessioninvalid)
        except Exception as e: 
                 
            return jsonify(errorResponse)


#=========================================================#
#   INVIGILATOR ABSENTEE_STATEMENT GENERATION ENDS        #                           
#=========================================================#

#=========================================================#
#   INVIGILATOR ABSENTEE_STATEMENT SUBMITION STARTS       #                           
#=========================================================#

class InvigilatorASSubmit(Resource):
    def post(self):
            try:
                requestData=request.get_json()
                session_token=requestData[SESSION_TOKEN]
                user_id=requestData[USER_ID]
                exam_id=requestData[EXAM_ID]
                cen_id=requestData[CENTER_ID]
                cou_id=requestData[COURSE_ID]
                sess_res=checkSessionValidity(session_token,user_id) 
                if sess_res:
                    falseList=[]
                    false_chk=FalseNumber.query.filter_by(exam_id=exam_id,cen_id=cen_id,cou_id=cou_id,inv_id=user_id).all()
                    if false_chk!=[]:
                        for i in false_chk:
                            i.dfm_status=INVIG_STATUS
                            db.session.commit()
                            falsedic={EXAM_ID:exam_id,CENTER_ID:cen_id,COURSE_ID:cou_id,STUDREG:i.std_reg_num,
                            SMP_STATUS:i.smp_status}
                            falseList.append(falsedic)
                        absenteeUpdate.update({DATA:{RESULT_DATA:falseList}})
                        return absenteeUpdate
                    # std_chk=HallAllotment.query.filter_by(exam_id=exam_id,cen_id=cen_id,cou_id=cou_id).all()
                    # if std_chk!=[]:
                    #     return jsonify()
                    else:
                        return invData
                else:
                    return sessioninvalid
            except Exception as e:      
                return errorResponse

#=========================================================#
#   INVIGILATOR ABSENTEE_STATEMENT SUBMITION STARTS       #                           
#=========================================================#


#=========================================================#
#         CS ABSENTEE_STATEMENT GENERATION STARTS         #                           
#=========================================================#

class CSAbsenteeGeneration(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            exam_id=requestData[EXAM_ID]
            cen_id=requestData[CENTER_ID]
            prg_id=requestData[PROGRAM_ID]
            cou_id=requestData[COURSE_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            absenteeList=[]
            resultList=[]
            presentList=[]
            if sess_res:
                submitError=FalseNumber.query.filter_by(exam_id=exam_id,cen_id=cen_id,cou_id=cou_id,dfm_status="0").first()
                if submitError!=None:
                    return invSubmitError
                dfm_chk=FalseNumber.query.filter(FalseNumber.cs_id==user_id,FalseNumber.dfm_status=="2",FalseNumber.exam_id==exam_id,FalseNumber.cou_id==cou_id)
                
                if dfm_chk.count()>0:

                    return CSerror
               
                stud_chk=Student.query.filter_by(exam_id=exam_id,cen_id=cen_id,prg_id=prg_id).all()
                
                if stud_chk!=[]:
                    for i in stud_chk:
                        false_chk=FalseNumber.query.filter_by(exam_id=exam_id,cen_id=cen_id,cou_id=cou_id,std_reg_num=i.std_reg).first()
                        if false_chk==None:
                            studdic={EXAM_ID:exam_id,CENTER_ID:cen_id,PROGRAM_ID:prg_id,STUDREG:i.std_reg,STUDNAME:i.std_name}
                            absenteeList.append(studdic)
                        else:
                            falsedic={EXAM_ID:exam_id,CENTER_ID:cen_id,COURSE_ID:cou_id,STUDREG:i.std_reg,STUDNAME:i.std_name,
                            SMP_STATUS:false_chk.smp_status}
                            presentList.append(falsedic)
                    resultList.append({PRESENT_LIST:presentList})
                    resultList.append({ABSENTEE_LIST:absenteeList})
                    falseFetch.update({DATA:resultList})
                    return jsonify(falseFetch)
                else:
                    return jsonify(invalid_data)

            else:
                return session_invalid
        except Exception as e:
            return error




#=========================================================#
#         CS ABSENTEE_STATEMENT GENERATION ENDS           #                           
#=========================================================#



#=========================================================#
#              CS ABSENTEE SUBMIT STARTS                  #
#=========================================================#

class CSAbsenteeSubmit(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            exam_id=requestData[EXAM_ID]
            cen_id=requestData[CENTER_ID]
            cou_id=requestData[COURSE_ID]
            smp_status=requestData[SMP_STATUS]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                submitError=FalseNumber.query.filter_by(exam_id=exam_id,cen_id=cen_id,cou_id=cou_id,dfm_status="0").first()
                if submitError!=None:
                    return invSubmitError
                dfmUpdate=FalseNumber.query.filter_by(exam_id=exam_id,cen_id=cen_id,cou_id=cou_id).all()
                
                c_time=datetime.now()
                if dfmUpdate!=[]:
                    for i in dfmUpdate:
                        i.dfm_status=CS_STATUS
                        i.cs_submit_date=c_time
                        i.cs_id=user_id
                        db.session.commit()
                    if smp_status!=[]:
                        for i in smp_status:
                            false_chk=FalseNumber.query.filter_by(exam_id=exam_id,cen_id=cen_id,cou_id=cou_id,std_reg_num=i.get(STUDREG)).first()
                            if false_chk!=None:
                                
                                false_chk.dfm_status=CS_STATUS
                                false_chk.cs_submit_date=c_time
                                false_chk.smp_status=i.get(SMP_STATUS)
                                false_chk.cs_id=user_id
                                db.session.commit()
                    return jsonify(cs_update)
              
                else:
                    return jsonify(invalid_data_err)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            
            return jsonify(error)



#======================================================#
#              CS ABSENTEE SUBMIT ENDS                 #
#======================================================#

#======================================================#
#              ASO ABSENTEE GENERATION STARTS          #
#======================================================#
class ASOAbsenteeGeneration(Resource):
    def post(self):
        try:
            requestData = request.get_json()
            session_token = requestData[SESSION_TOKEN]
            user_id = requestData[USER_ID]
            exam_id = requestData[EXAM_ID]
            cen_id = requestData[CENTER_ID]
            prg_id = requestData[PROGRAM_ID]
            cou_id = requestData[COURSE_ID]
            sess_res = checkSessionValidity(session_token, user_id)
            absenteeList = []
            resultList = []
            presentList = []
            if sess_res:
              
                dfm_chk=FalseNumber.query.filter(FalseNumber.aso_id==user_id,FalseNumber.dfm_status=="3")
                if dfm_chk.count()>0:
                    return CSerror
                submitError=FalseNumber.query.filter_by(exam_id=exam_id,cen_id=cen_id,cou_id=cou_id,dfm_status="2").first()
                if submitError==None:
                    return csSubmitError
              
        
                
                stud_chk = Student.query.filter_by(exam_id=exam_id, cen_id=cen_id, prg_id=prg_id).all()
                if stud_chk != []:
                    for i in stud_chk:
                        false_chk = FalseNumber.query.filter_by(
                            exam_id=exam_id, cen_id=cen_id, cou_id=cou_id, std_reg_num=i.std_reg).first()
                        if false_chk == None:

                                studdic = {EXAM_ID: exam_id, CENTER_ID: cen_id,
                                           PROGRAM_ID: prg_id, STUDREG: i.std_reg, STUDNAME: i.std_name}
                                absenteeList.append(studdic)
                        else:
                            falsedic = {EXAM_ID: exam_id, CENTER_ID: cen_id, COURSE_ID: cou_id, STUDREG: i.std_reg, STUDNAME: i.std_name,
                                         SMP_STATUS: false_chk.smp_status}
                            presentList.append(falsedic)
                    resultList.append({PRESENT_LIST: presentList})
                    resultList.append({ABSENTEE_LIST: absenteeList})
                    falseFetch.update({DATA: resultList})
                    return jsonify(falseFetch)
                else:
                    return jsonify(invalid_id)
            else:
                return session_invalid
        except Exception as e:
            return jsonify(error)


#======================================================#
#              ASO ABSENTEE GENERATION ENDS            #
#======================================================#
#======================================================#
#            ASO ABSENTEE VERIFICATION STARTS          #
#======================================================#

class ASOAbsenteeVerification(Resource):
    def post(self):

        try:
            requestData = request.get_json()
            session_token = requestData[SESSION_TOKEN]
            user_id = requestData[USER_ID]
            exam_id = requestData[EXAM_ID]
            cen_id = requestData[CENTER_ID]
            cou_id = requestData[COURSE_ID]
            sess_res = checkSessionValidity(session_token, user_id)
            if sess_res:
                submitError=FalseNumber.query.filter_by(exam_id=exam_id,cen_id=cen_id,cou_id=cou_id,dfm_status="2").first()
                if submitError==None:
                    return csSubmitError
                # user_existence = AccessKeyGen.query.filter_by(
                #     exam_id=exam_id, cen_id=cen_id, course_id=cou_id).first()
                # if user_existence==None:
                #     return jsonify(absenteeerror)

                falseList = []
                false_chk = FalseNumber.query.filter_by(exam_id=exam_id, cen_id=cen_id, cou_id=cou_id).all()
                if false_chk != []:
                    curr_date = datetime.now()
                    datechk = curr_date.strftime('%Y-%m-%d')
                    for i in false_chk:
                        i.aso_id = user_id
                        i.dfm_status = ASO_STATUS
                        i.aso_verify_date = datechk
                        db.session.commit()
                    asoUpdate.update()
                    return jsonify(asoUpdate)
                else:
                    return jsonify(invalid_id)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(error)

    # def post(self):
    #     try:
    #         requestData = request.get_json()
    #         session_token = requestData[SESSION_TOKEN]
    #         user_id = requestData[USER_ID]
    #         exam_id = requestData[EXAM_ID]
    #         cen_id = requestData[CENTER_ID]
    #         cou_id = requestData[COURSE_ID]
    #         sess_res = checkSessionValidity(session_token, user_id)
    #         if sess_res:

    #             falseList = []

    #             false_chk = FalseNumber.query.filter_by(
    #                 exam_id=exam_id, cen_id=cen_id, cou_id=cou_id).all()

    #             print(false_chk)

    #             if false_chk != []:

    #                 curr_date = datetime.now()

    #                 print(curr_date)

    #                 datechk = curr_date.strftime('%Y-%m-%d')

    #                 for i in false_chk:

    #                     i.so_id = user_id

    #                     i.dfm_status = ASO_STATUS

    #                     i.so_approved_date = datechk

    #                     db.session.commit()

                        


    #                 absenteeUpdate.update()

    #                 return jsonify(absenteeUpdate)

    #             else:

    #                 return jsonify(invalid_id)

    #         else:

    #             return jsonify(session_invalid)

    #     except Exception as e:

    #         print(e)

    #         return jsonify(error)

#=========================================================#
#              ASO ABSENTEE VERIFICATION ENDS             #
#=========================================================#


#=========================================================#
#              SO ABSENTEE GENERATION STARTS              #
#=========================================================#


class SOAbsenteeGeneration(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            exam_id=requestData[EXAM_ID]
            cen_id=requestData[CENTER_ID]
            prg_id=requestData[PROGRAM_ID]
            cou_id=requestData[COURSE_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            absenteeList=[]
            resultList=[]
            presentList=[]
            if sess_res:
                submitError=FalseNumber.query.filter_by(exam_id=exam_id,cen_id=cen_id,cou_id=cou_id,dfm_status="3").first()
                stud_chk=Student.query.filter_by(exam_id=exam_id,cen_id=cen_id,prg_id=prg_id).all()
                if stud_chk!=[]:
                    dfm_chk=FalseNumber.query.filter(FalseNumber.so_id==user_id,FalseNumber.dfm_status=="4")
                    if dfm_chk.count()>0:
                        return so_error
                    if submitError==None:
                        return soSubmitError                
                    for i in stud_chk:
                        false_chk=FalseNumber.query.filter_by(exam_id=exam_id,cen_id=cen_id,cou_id=cou_id,std_reg_num=i.std_reg).first()
                        if false_chk==None:                            
                                studdic={EXAM_ID:exam_id,CENTER_ID:cen_id,PROGRAM_ID:prg_id,STUDREG:i.std_reg,STUDNAME:i.std_name}
                                absenteeList.append(studdic)
                        else:
                            falsedic={EXAM_ID:exam_id,CENTER_ID:cen_id,COURSE_ID:cou_id,STUDREG:i.std_reg,STUDNAME:i.std_name,
                            SMP_STATUS:false_chk.smp_status}
                            presentList.append(falsedic)
                    resultList.append({PRESENT_LIST:presentList})
                    resultList.append({ABSENTEE_LIST:absenteeList})
                    falseFetch.update({DATA:resultList})
                    return jsonify(falseFetch)
                else:
                    return jsonify(invalid_id)                    
            else:
                return session_invalid
        except Exception as e:  
            return jsonify(br_bad_request) 





#=========================================================#
#              SO ABSENTEE GENERATION ENDS                #
#=========================================================#

#=========================================================#
#              SO ABSENTEE APPROVAL STARTS                #
#=========================================================#
class SOAbsenteeApprove(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            exam_id=requestData[EXAM_ID]
            cen_id=requestData[CENTER_ID]
            cou_id=requestData[COURSE_ID]
            sess_res=checkSessionValidity(session_token,user_id)
            if sess_res:
                submitError=FalseNumber.query.filter_by(exam_id=exam_id,cen_id=cen_id,cou_id=cou_id,dfm_status="3").first()
                if submitError==None:
                    return soSubmitError
                falseList=[]
                false_chk=FalseNumber.query.filter_by(exam_id=exam_id,cen_id=cen_id,cou_id=cou_id).all()
                if false_chk!=[]:
                    curr_date=datetime.now()
                    datechk=curr_date.strftime('%Y-%m-%d')
                    for i in false_chk:
                        i.so_id=user_id
                        i.dfm_status=SO_STATUS
                        i.so_approved_date=datechk
                        db.session.commit()
                       
                        # falsedic={EXAM_ID:i.exam_id,CENTER_ID:i.cen_id,COURSE_ID:i.cou_id,STUDREG:i.std_reg_num,
                        # FALSENO:i.dfm_num,SO_APPROVED_DATE:datechk,STATUS:SO_STATUS}
                       
                        # falseList.append(falsedic)
                        # print(falseList)
                    soUpdate.update({DATA:falseList})
                    return jsonify(soUpdate)
                else:
                    return jsonify(invalid_id)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(br_bad_request)  

#=========================================================#
#              SO ABSENTEE APPROVAL ENDS                  #
#=========================================================#

#=========================================================#
#             ANSWER SCRIPT DISPATCH STARTS               #
#=========================================================#

class AnswerScriptDispatchAdd(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if ANS_DISPATCH_COUNT in requestData:
                    
                    cen_id=requestData[CENTER_ID]
                    cou_id=requestData[COURSE_ID]
                    exam_id=requestData[EXAM_ID]
                    ans_dispatch_count=requestData[ANS_DISPATCH_COUNT]
                    ans_chk=AnswerScriptDispatch.query.filter_by(cen_id=cen_id,cou_id=cou_id,exam_id=exam_id).first()
                    studentchk=db.session.query(Student,Course).with_entities(Student.std_id).filter(Student.prg_id==ExamTimetable.prg_id,ExamTimetable.cou_id==cou_id,Student.status==STATUS).all()
                    std_count=len(studentchk)
                    # ans_chk=1
                    if ans_chk==None:                                            
                        fls_chk=FalseNumber.query.filter(FalseNumber.cen_id==cen_id,FalseNumber.exam_id==exam_id,FalseNumber.cou_id==cou_id,FalseNumber.smp_status==0)
                        fls_count=fls_chk.count()
                        fls_count=True
                        if fls_count:

                        # if fls_count==ans_dispatch_count:
                            
                            smpchk=FalseNumber.query.filter(FalseNumber.cen_id==cen_id,FalseNumber.exam_id==exam_id,FalseNumber.cou_id==cou_id,FalseNumber.smp_status==1)
                            smp_count=smpchk.count()
                            present_count=fls_count + smp_count
                            absentee_count=std_count-present_count

                            curr_date=datetime.now()
                            datechk=curr_date.strftime('%Y-%m-%d')
                            data=AnswerScriptDispatch(cen_id=cen_id,cou_id=cou_id,exam_id=exam_id,exam_date=datechk,
                            ans_dispatch_date=datechk,ans_dispatch_count=ans_dispatch_count,absentee_count=absentee_count,smp_count=smp_count,total_count=std_count,ans_dispatch_status=STATUS)
                            db.session.add(data)
                            db.session.commit()
                            ansdic={CENTER_ID:cen_id,COURSE_ID:cou_id,EXAM_ID:exam_id}
                            ans_add_success.update({DATA:ansdic})
                            return jsonify(ans_add_success)
                        else:
                            return jsonify(ansDispatcherr)
                    else:
                        return jsonify(ans_exists_err)
                    
                
                elif CENTER_ID in  requestData:
                    cen_id=requestData[CENTER_ID]
                    single_ans=AnswerScriptDispatch.query.filter_by(cen_id= cen_id,ans_dispatch_status=STATUS).all()
                    if single_ans!=[]:
                        list1=[]
                        centre=Center_det.query.filter_by(cen_id=cen_id,status=STATUS).first()
                    
                        for i in single_ans:
                            exam=Exam.query.filter_by(exam_id=i.exam_id,status=STATUS).first()
                            course=Course.query.filter_by(cou_id=i.cou_id,cou_status=STATUS).first()
                            single_center={CENTER_ID:cen_id,CENTER_NAME:centre.cen_name,
                            COURSE_ID:i.cou_id,COURSE_NAME:course.cou_name,ANS_DISPATCH_COUNT:i.ans_dispatch_count,
                            EXAM_NAME:exam.exam_name,EXAM_ID:i.exam_id,ANS_DISPATCH_DATE:i.ans_dispatch_date,
                            ABSENTEE_COUNT:i.absentee_count,SMP_COUNT:i.smp_count,TOTAL_COUNT:i.total_count}
                            list1.append(single_center)

                        ans_fetch_success.update({DATA:list1})
                        return jsonify(ans_fetch_success)
                    else:
                        return jsonify(ans_invalid)
            else:
                return session_invalid
        except Exception as e:
            return jsonify(error) 



    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                answr_script=AnswerScriptDispatch.query.filter_by(ans_dispatch_status=STATUS).all()
                if answr_script!=[]:
                    anslist=[]
                    for i in answr_script:
                        exam=Exam.query.filter_by(exam_id=i.exam_id,status=STATUS).first()
                        course=Course.query.filter_by(cou_id=i.cou_id,cou_status=STATUS).first()
                        centre=Center_det.query.filter_by(cen_id=i.cen_id,status=STATUS).first()
                        fetch_ans={CENTER_ID:i.cen_id,CENTER_NAME:centre.cen_name,
                        COURSE_ID:i.cou_id,COURSE_NAME:course.cou_name,ANS_DISPATCH_COUNT:i.ans_dispatch_count,ABSENTEE_COUNT:i.absentee_count,SMP_COUNT:i.smp_count,TOTAL_COUNT:i.total_count,
                        EXAM_NAME:exam.exam_name,EXAM_ID:i.exam_id,ANS_DISPATCH_DATE:i.ans_dispatch_date}
                        anslist.append(fetch_ans)
                        ans_fetch_success.update({DATA:anslist})
                    return jsonify(ans_fetch_success)
                else:
                    return jsonify(ans_invalid)
            else:
                return session_invalid
        except Exception as e:
            return jsonify(error)




#=========================================================#
#             ANSWER SCRIPT DISPATCH ENDS                 #
#=========================================================#

       
#=========================================================#
#              EXAM SPECIFIC PROGRAM LIST STARTS          #                           
#=========================================================#


class ExamProgram(Resource):
    
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if EXAM_ID in requestData:
                    examlist=[]
                    result=[]
                    exam_id=requestData[EXAM_ID]
                    singleidchk=ExamTimetable.query.filter_by(exam_id=exam_id).all()
                    if  singleidchk!=None:
                        for i in singleidchk:
                            program=ProgramDet.query.filter_by(prg_id=i.prg_id).first()
                            examdic={EXAM_ID:i.exam_id,PROGRAM_ID:i.prg_id,PROGRAM_NAME:program.prg_name}
                            examlist.append(examdic)
                            result = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in examlist)]    
                        examfetch.update({DATA:result})
                        return jsonify(examfetch)
                    else:
                        return jsonify(invalid_id)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(err_exception)

#=========================================================#
#         EXAM SPECIFIC PROGRAM LIST ENDS                 #                           
#=========================================================#

#=========================================================#
#          PROGRAM SPECIFIC COURSE STARTS                 #                           
#=========================================================#



class ProgramCourse(Resource):
    
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if PROGRAM_ID in requestData:
                    prglist=[]
                    prg_id=requestData[PROGRAM_ID]
                    singleidchk=ExamTimetable.query.filter_by(prg_id=prg_id).all()
                    if  singleidchk!=None:
                        for i in singleidchk:
                            course=Course.query.filter_by(cou_id=i.cou_id).first()
                            programdic={PROGRAM_ID:i.prg_id,COURSE_ID:i.cou_id,COURSE_NAME:course.cou_name}
                            prglist.append(programdic)
                        prgfetch.update({DATA:prglist})
                        return jsonify(prgfetch)
                    else:
                        return jsonify(invalid_id)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(err_exception)

#=========================================================#
#         PROGRAM SPECIFIC COURSE ENDS                    #                           
#=========================================================#

#=========================================================#
#          EXAM SPECIFIC CAMP STARTS                      #                           
#=========================================================#

class ExamCamp(Resource):
    
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if PROGRAM_ID in requestData:
                    reslist=[]
                    prg_id=requestData[PROGRAM_ID]
                    exam_id=requestData[EXAM_ID]
                    singleidchk=Camp.query.filter_by(prg_id=prg_id,exam_id=exam_id).all()
                    if  singleidchk!=None:
                        for i in singleidchk:
                           
                            center=Center_det.query.filter_by(cen_id=i.cen_id).first()
                            newdic={CAMP_ID:i.cen_id,CAMP_NAME:center.cen_name}
                            reslist.append(newdic)
                        prgfetch.update({DATA:reslist})
                        return jsonify(prgfetch)
                    else:
                        return jsonify(invalid_id)
            else:
                return jsonify(session_invalid)
        except Exception as e:            
            return jsonify(err_exception)

#=========================================================#
#          EXAM SPECIFIC CAMP ENDS                        #                           
#=========================================================#


#=========================================================#
#               MAPPING EXAM STARTS                       #                           
#=========================================================#
class TodayExamList(Resource):
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                start_date=datetime.now().strftime("%Y-%m-%d 00:00:00")
                end_date=datetime.now().strftime("%Y-%m-%d 23:59:59")
                examlist=[]
                singleidchk=ExamTimetable.query.filter(ExamTimetable.date>start_date,ExamTimetable.date<end_date).all()                
                for i in singleidchk:
                    exam=Exam.query.filter_by(exam_id=i.exam_id).first()
                    examdic={EXAM_ID:i.exam_id,EXAM_NAME:exam.exam_name}
                    examlist.append(examdic)
                br_fetch.update({DATA:examlist})                
                return jsonify(br_fetch)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(error)
#=========================================================#
#               MAPPING EXAM ENDS                         #                           
#=========================================================#
class AsExamList(Resource):
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                cur_time=datetime.now().strftime("%Y-%m-%d 23:59:59")
                

                singleidchk=db.session.query(ExamTimetable,Exam).with_entities(Exam.exam_id.label("exam_id"),Exam.exam_name.label("exam_name")).filter(Exam.exam_id==ExamTimetable.exam_id,ExamTimetable.date<cur_time,ExamTimetable.status==STATUS).all()
                examlist=list(map(lambda n:n._asdict(),singleidchk))
                
                # return singleidchk
                
                # examlist=[]
                # singleidchk=ExamTimetable.query.filter(ExamTimetable.date>cur_time).all()                
                # for i in singleidchk:
                #     exam=Exam.query.filter_by(exam_id=i.exam_id).first()
                #     examdic={EXAM_ID:i.exam_id,EXAM_NAME:exam.exam_name}
                #     examlist.append(examdic)
                result = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in examlist)]
                
                # return result
                br_fetch.update({DATA:result})                
                return jsonify(br_fetch)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(error)


class ExamCenter(Resource):
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            exam_id=request.headers[EXAM_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
           
                # singleidchk=db.session.query(Center_det,Exam).with_entities(Center_det.cen_id.label("cen_id"),Center_det.cen_name.label("cen_name"),Center_det.cen_dist.label("cen_dist")).filter().all()
                # examlist=list(map(lambda n:n._asdict(),singleidchk)           
                 
                cenlist=[]
                singleidchk=Student.query.filter_by(exam_id=exam_id).all()
                if  singleidchk!=None:
                    for i in singleidchk:
                        center=Center_det.query.filter_by(cen_id=i.cen_id).first()
                        centerdic={CENTER_ID:i.cen_id,CENTER_NAME:center.cen_name,CEN_DISTRICT:center.cen_dist}
                        cenlist.append(centerdic)
                        result = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in cenlist)] 
                    prgfetch.update({DATA:result})
                    return jsonify(prgfetch)
                else:
                    return jsonify(invalid_id)                
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(error)