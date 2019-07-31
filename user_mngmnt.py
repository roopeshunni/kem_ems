
from model import *
from constants import *
from flask_restful import Resource, Api
import json
from flask import Flask,jsonify,request
from datetime import *
import datetime
from secrets import token_urlsafe
from  datetime import datetime,timedelta
import time
from datetime import date
import smtplib
from cachetools import cached, LRUCache, TTLCache
from random import randint


code_cache=TTLCache(maxsize=1024, ttl=600)
#=========================================================#
#             FUNCTION FOR CHECKING SESSION               #                           
#=========================================================#
def checkSessionValidity(session_token,user_id): 
    # print(session_token)
    chk_user=Session.query.filter_by(ses_token=session_token,user_id=user_id,status="active").first()
    if chk_user!=None:
        return True
    else:
        return False
#=========================================================#
#                      USER LOGIN STARTS                  #                           
#=========================================================#
class UserLogin(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            u_name=requestData[USER_NAME]
            u_pswd=requestData[PASSWORD]
            ses_devtype=requestData[SES_DEVTYPE]
            user_chk=User_det.query.filter_by(usr_email=u_name,usr_pswd=u_pswd).first()
            
            if user_chk!=None:
                role_chk=RoleDet.query.filter_by(role_id=user_chk.role_id).first()
                role_permission=role_chk.role_permission
                role_len=len(role_permission)
                permissionlist=actionlist(role_len,role_permission)
                ipaddress=get_my_ip()
                cs_chk=ChiefSuptd.query.filter_by(user_id=user_chk.user_id,status=STATUS).first()
                print(cs_chk)
                if cs_chk!=None:
                    print("dshfhf")
                    curr_time=datetime.now()
                    session_token = token_urlsafe(64)
                    addsession=Session(user_id=user_chk.user_id,ses_devtype=ses_devtype,ses_token=session_token,ses_logintime=curr_time,
                    ses_ip=ipaddress,ses_mac=ipaddress,ses_logouttime="",status=STATUS)
                    db.session.add(addsession)
                    db.session.commit()
                    log_dic={ROLE_NAME:role_chk.role_name,USER_NAME:user_chk.name,USER_ID:user_chk.user_id,CEN_ID:user_chk.cen_id,
                    SESSION_TOKEN:session_token,ACTION_LIST:permissionlist}
                    loginSuccess.update({DATA:log_dic})
                    return loginSuccess
                else:
                    curr_time=datetime.now()
                    session_token = token_urlsafe(64)
                    addsession=Session(user_id=user_chk.user_id,ses_devtype=ses_devtype,ses_token=session_token,ses_logintime=curr_time,
                    ses_ip=ipaddress,ses_mac=ipaddress,ses_logouttime="",status=STATUS)
                    db.session.add(addsession)
                    db.session.commit()
                    log_dic={ROLE_NAME:role_chk.role_name,USER_NAME:user_chk.name,USER_ID:user_chk.user_id,
                    CEN_ID:user_chk.cen_id,SESSION_TOKEN:session_token,ACTION_LIST:permissionlist}
                    loginSuccess.update({DATA:log_dic})
                    return loginSuccess
            else:
                return invalid
        except Exception as e:
            print(e)          
            return error

#=========================================================#
#    FUNCTION FOR GETTING IP ADDRESS                      #                           
#=========================================================#

def get_my_ip():
    return  request.remote_addr 


#=========================================================#
#              ACTION LIST FUNCTION                       #                           
#=========================================================#

def actionlist(role_len,role_permission):
    permissionlist=[]
    if role_len>3:
        role_permission_split=(role_permission.split('|'))

        for i in role_permission_split:
            action_chk=ActionDet.query.filter_by(act_code=i,act_status=STATUS).first()
            if action_chk==None:
                continue            
            permissionlist.append({"action_name":action_chk.act_name})
            # permissionlist.append({"action_name":action_chk.act_name,"action_code":action_chk.act_code,"module":action_chk.mod_id,'card_name':action_chk.act_card})
        
        # print(permissionlist)

        return permissionlist
    else:
        action_chk=ActionDet.query.filter_by(act_code=role_permission,act_status=STATUS).first()
        if action_chk!=None:        
            permissionlist.append({"action_name":action_chk.act_name})       
        return permissionlist 

#=========================================================#
#              CARD VISIBILITY                       #                           
#=========================================================#

def cardList(permissionList):
    preExam=[i for i in permissionList if i.get('module')==1]
    permissionResultList=[]

    permissionlist=[]
    if role_len>3:
        role_permission_split=(role_permission.split('|'))

        for i in role_permission_split:
            action_chk=ActionDet.query.filter_by(act_code=i,act_status=STATUS).first()
            if action_chk==None:
                continue            
            permissionlist.append({"action_name":action_chk.act_name,"action_code":action_chk.act_code,"module":action_chk.mod_id})
        

        return permissionlist
    else:
        action_chk=ActionDet.query.filter_by(act_code=role_permission,act_status=STATUS).first()        
        permissionlist.append(action_chk.act_name)       
        return permissionlist   

#=========================================================#
#            USER LOGOUT                                  #                           
#=========================================================#
class UserLogout(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
          
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                chk_ses=Session.query.filter_by(ses_token=session_token,user_id=user_id).first()

                chk_ses.status=INACTIVE
                timestamp1 = datetime.now()
                chk_ses.ses_logouttime=timestamp1
                db.session.commit()
                return logoutsuccess
            else:
                return session_invalid
        except Exception as e:
            return error
#=========================================================#
#   FUNCTIONS FOR FORGOT PASSWORD                         #                           
#=========================================================#

@cached(cache=code_cache)
def cache_code(email_id):
    range_start = 10**(4-1)
    range_end = (10**4)-1
    return randint(range_start, range_end)

def send_email(username,number):
    host='smtp.gmail.com'
    port=587
    email='smashx2018@gmail.com'
    password="tedaaststewbwlhk"
    subject="Verification "
    mail_to=username
    mail_from=email
    body="YOUR VERIFICATION CODE IS {id}.".format(id=number)
    # return u_id
    message = """From: %s\nTo:  %s\nSubject: %s\n\n%s""" % (mail_from, mail_to,  subject, body)
    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(email, password)
        server.sendmail(mail_from, mail_to, message)
        server.close()
        return 1
    except Exception as ex:
        return 0

def emailcodeverification(data):

        emailid=data.get(EMAIL_ID)
        code=data.get(CODE)
        datas=cache_code(emailid)
        if datas != None:
            datas=int(datas)
        else:
            return emailcodeexpired
        if datas==int(code):
            return emailcodeverified            
        else:
            return emailcodeinvalid
      

#=========================================================#
#    USER FORGOT PASSWORD STARTS                          #                           
#=========================================================#
class Forgotpassword(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            emailid=requestData[EMAIL_ID]            
            chk_user=User_det.query.filter_by(usr_email=emailid).first()
            if chk_user!=None:
                code_cache.clear()
                number=cache_code(emailid)
                print(number)
                response=send_email(emailid,number)
                if response==0:
                    return invalidemail
                else:
                    return mailsent
            else:
                return invalidemail
        except Exception as e:         
            return error

class Newpassword(Resource):
    def post(data):
        try:
            requestData=request.get_json()
            emailid=requestData[EMAIL_ID]
            password=requestData[PASSWORD]
            code=requestData[CODE]
            chk_user=User_det.query.filter_by(usr_email=emailid).first()
            if chk_user!=None:
                verify_code_data={EMAIL_ID:emailid,CODE:code}
                code_response=emailcodeverification(verify_code_data)
                if(code_response.get("status")!="Success"):
                    return emailcodeinvalid
                chk_user.usr_pswd=password
                db.session.commit()
                return pwdupdated
            else:
                return invalidemail
        except Exception as e:           
            return error

#=========================================================#
#    USER CHANGE PASSWORD                                 #                           
#=========================================================#
class Changepassword(Resource):
    def post(data):
        try:
            requestData=request.get_json()
            emailid=requestData[EMAIL_ID]
            oldpassword=requestData[OLD_PASSWORD]
            newpassword=requestData[NEW_PASSWORD]
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                chk_user=User_det.query.filter_by(usr_email=emailid,usr_pswd=oldpassword,user_id=user_id).first()
                if chk_user!=None:
                    
                    chk_user.usr_pswd=newpassword
                    db.session.commit()
                
                    return pwdupdated
                else:
                    return invalidemail
            else:
                return session_invalid
        except Exception as e:       
            return error

#=========================================================#
#   MOBILE LOGIN  FOR INVIGILATOR                         #                           
#=========================================================#
class InvigilatorLogin(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            print(requestData)
            u_name=requestData[USER_NAME]
            u_pswd=requestData[PASSWORD]
            ses_devtype=requestData[SES_DEVTYPE]
            user_chk=User_det.query.filter_by(usr_email=u_name,usr_pswd=u_pswd,status=STATUS).first()
            print(user_chk)
            if user_chk!=None:
                invg_chk=ExamInvigilator.query.filter_by(user_id=user_chk.user_id,invig_status=STATUS).first()
                if invg_chk!=None:
                    center_chk=Center_det.query.filter_by(cen_id=user_chk.cen_id,status=STATUS).first()
                    ipaddress=get_my_ip()
                    curr_time=datetime.now()
                    session_token = token_urlsafe(64)
                    addsession=Session(user_id=user_chk.user_id,ses_devtype=ses_devtype,ses_token=session_token,ses_logintime=curr_time,
                    ses_ip=ipaddress,ses_mac=ipaddress,ses_logouttime="",status=STATUS)
                    db.session.add(addsession)
                    db.session.commit()
                    log_dic={"user_name":user_chk.name,"user_id":user_chk.user_id,
                    "cen_id":user_chk.cen_id,"session_token":session_token,"center_name":center_chk.cen_name}
                    loginSuccess.update({DATA:log_dic})
                    return loginSuccess
                else:
                    return invalidInvg
            else:
                return invalid
        except Exception as e: 
            print(e)          
            return error



#=========================================================#
#   ADDITIONAL EXAMINER LOGIN                             #                           
#=========================================================#

class AdditionalExaminerLogin(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            u_name=requestData[USER_NAME]
            u_pswd=requestData[PASSWORD]
            ses_devtype=requestData[SES_DEVTYPE]
            user_chk=User_det.query.filter_by(usr_email=u_name,usr_pswd=u_pswd,status=STATUS).first()
            if user_chk!=None:
                role_chk=RoleDet.query.filter_by(role_id=user_chk.role_id,role_status=STATUS).first()
                addlExaminer_chk=AdditionalExaminer.query.filter_by(addl_id=user_chk.user_id,status=STATUS).first()
                chiefExaminer_chk=ChiefExaminer.query.filter_by(chief_id=user_chk.user_id,status=STATUS).first()
                if addlExaminer_chk!=None:
                    center_chk=Center_det.query.filter_by(cen_id=addlExaminer_chk.cen_id,status=STATUS).first()
                    exam_chk=Exam.query.filter_by(exam_id=addlExaminer_chk.exam_id,status=STATUS).first()
                    camp_chk=Camp.query.filter_by(cen_id=addlExaminer_chk.cen_id).first()
                    if camp_chk==None:
                        return jsonify(invalid_data)
                    prm_chk=ProgramDet.query.filter_by(prg_id=camp_chk.prg_id).first()
                    ipaddress=get_my_ip()
                    curr_time=datetime.now()
                    session_token = token_urlsafe(64)
                    addsession=Session(user_id=user_chk.user_id,ses_devtype=ses_devtype,ses_token=session_token,ses_logintime=curr_time,
                    ses_ip=ipaddress,ses_mac=ipaddress,ses_logouttime="",status=STATUS)
                    db.session.add(addsession)
                    db.session.commit()
                    userdic={USER_NAME:user_chk.name,USER_ID:user_chk.user_id,CENTER_NAME:center_chk.cen_name,
                    EXAM_NAME:exam_chk.exam_name,PRG_NAME:prm_chk.prg_name,
                    ROLE_NAME:role_chk.role_name,CEN_ID:user_chk.cen_id,SESSION_TOKEN:session_token}
                    loginSuccess.update({DATA:userdic})
                    return loginSuccess
                elif chiefExaminer_chk!=None:
                    center_chk=Center_det.query.filter_by(cen_id=chiefExaminer_chk.camp_id,status=STATUS).first()
                    exam_chkChief=Exam.query.filter_by(exam_id=chiefExaminer_chk.exam_id,status=STATUS).first()
                    camp_chk=Camp.query.filter_by(cen_id=chiefExaminer_chk.camp_id).first()
                    if camp_chk==None:
                        return jsonify(invalid_data)
                    prm_chk=ProgramDet.query.filter_by(prg_id=camp_chk.prg_id).first()
                    
                    ipaddress=get_my_ip()
                    curr_time=datetime.now()
                    session_token = token_urlsafe(64)
                    addsession=Session(user_id=user_chk.user_id,ses_devtype=ses_devtype,ses_token=session_token,ses_logintime=curr_time,
                    ses_ip=ipaddress,ses_mac=ipaddress,ses_logouttime="",status=STATUS)
                    db.session.add(addsession)
                    db.session.commit()

                    userdic={USER_NAME:user_chk.name,USER_ID:user_chk.user_id,CENTER_NAME:center_chk.cen_name,
                    EXAM_NAME:exam_chkChief.exam_name,PRG_NAME:prm_chk.prg_name,
                    ROLE_NAME:role_chk.role_name,CEN_ID:user_chk.cen_id,SESSION_TOKEN:session_token}
                    loginSuccess.update({DATA:userdic})
                    return jsonify(loginSuccess)
            else:
                return invalid
        except Exception as e:         
            return jsonify(error)




#=========================================================#
#   MOBILE LOGIN  FOR INVIGILATOR                         #                           
#=========================================================#

#=========================================================#
#           CACHE CLEAR API STARTS                        #                           
#=========================================================#
class CacheClear(Resource):
    def get(self):
        code_cache.clear()
        return jsonify({"status":"Success"})

#=========================================================#
#           CACHE CLEAR API ENDS                          #                           
#=========================================================#