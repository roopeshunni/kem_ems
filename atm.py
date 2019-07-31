
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
import smtplib
from cachetools import cached, LRUCache, TTLCache
import random
from datetime import date
from user_mngmnt import *






#=========================================================#
#                  ARTICLE ASSIGN STARTS                  #                           
#=========================================================#

class Article_Add(Resource):
    def post(self):
        try:
            
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if CEN_ID  in requestData and ART_CODE in requestData:
                    artlist=[]
                    art_code1=requestData[ART_CODE]
                    articlelist= ARTDIC.get(str(art_code1))
                    articlename=articlelist
                    cen_id1=requestData[CEN_ID]
                    exam_id1=requestData[EXAM_ID]
                    status1=SEND
                    centrechk=Center_det.query.filter_by(cen_id=cen_id1,).first()
                    centrecode= centrechk.cen_code
                    random_generatecode=generate_code()
                    approvalcode=centrecode +'|'+ random_generatecode
                    crr_date=datetime.date(datetime.now())
                    cenid_exist=ArticleDistribution.query.filter_by(cen_id=cen_id1,exam_id=exam_id1).first()
                    datechk=crr_date.strftime('%Y-%m-%d')
                    artdic={ART_CODE:articlename,CEN_ID: cen_id1,EXAM_ID:exam_id1,DATE_SEND:datechk}
                    artlist.append(artdic)
                    if cenid_exist!=None:
                        return jsonify(cen_exist_id)
                    else:
                        new_artlist=ArticleDistribution(cen_id=cen_id1,exam_id=exam_id1,art_code=art_code1,art_approval_key=approvalcode,date_send=crr_date,art_status=status1,date_received="")
                        db.session.add(new_artlist)
                        db.session.commit()
                        csInfo=ChiefSuptd.query.filter_by(cen_id=cen_id1,pgm_id="-1").first()
                        userInfo=User_det.query.filter_by(user_id=csInfo.user_id).first()
                        csEmail=userInfo.usr_email
                        number=centrecode+" "+random_generatecode
                        send_email(csEmail,number)
                        art_success_add.update({DATA:artlist})
                        return jsonify(art_success_add)
                elif CEN_ID in requestData:
                    cen_id1=requestData[CEN_ID]
                    
                    artlist=[]
                    singlearticle=ArticleDistribution.query.filter_by(cen_id=cen_id1).all()
                    if singlearticle!=None:
                        for i in singlearticle:
                            exam=Exam.query.filter_by(exam_id=i.exam_id).first()
                            artcode=i.art_code
                            articlelist= ARTDIC.get(str(artcode))
                            articlename=articlelist
                            date_send=i.date_send
                            datechk=date_send.strftime('%m/%d/%Y')
                            d={ART_ID:i.art_id,CEN_ID:i.cen_id,EXAM_ID:i.exam_id,DATE_SEND:datechk,EXAM_NAME:exam.exam_name,ART_CODE:articlename,ART_STATUS:i.art_status}
                            artlist.append(d)
                        art_success_single_fetch.update({DATA:artlist})
                        return jsonify(art_success_single_fetch)
                    else:
                        return jsonify(cen_invalid_id)
                elif ART_ID in requestData:
                    art_id1=requestData[ART_ID]
                    singlearticle=ArticleDistribution.query.filter_by(art_id=art_id1).first()
                    if singlearticle!=None:
                        artcode=singlearticle.art_code
                        articlelist= ARTDIC.get(str(artcode))
                        articlename=articlelist
                        d={ART_ID:singlearticle.art_id,CEN_ID:singlearticle.cen_id,EXAM_ID:singlearticle.exam_id,ART_CODE:articlename,ART_STATUS:singlearticle.art_status}
                        art_success_single_fetch.update({DATA:d})
                        return jsonify(art_success_single_fetch)
                    else:
                        return jsonify(art_invalid_id)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            
            return jsonify(br_bad_request)  

    def get(self):
        try:
            
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            
            art_fetch1 ={"status":"Success","message":"Successfully fetched test"} 
            
            if sess_res:
                
                artResponse=ArticleDistribution.query.all()
                
                artlist=[]
                for i in artResponse:
                    
                    exam=Exam.query.filter_by(exam_id=i.exam_id).first()
                    centre=Center_det.query.filter_by(cen_id=i.cen_id).first()
                    singlearticle=ArticleDistribution.query.filter_by(art_id=i.art_id).first()
                    artcode=singlearticle.art_code
                    articlelist= ARTDIC.get(str(artcode))
                    articlename=articlelist
                    crr_date=datetime.date(datetime.now())
                    datechk=crr_date.strftime('%m/%d/%Y')
                    newartlist={ART_ID:i.art_id,ART_CODE:articlename,CEN_ID:i.cen_id,CEN_NAME:centre.cen_name,EXAM_ID:i.exam_id,EXAM_NAME:exam.exam_name,DATE_SEND:datechk,ART_STATUS:i.art_status}
                    artlist.append(newartlist)
                    art_fetch1.update({DATA:artlist})       
                
                return jsonify(art_fetch1)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(br_bad_request)  

    def put(self):
        try:
            
            requestData=request.get_json()
            art_id1=requestData[ART_ID]
            cen_id1=requestData[CEN_ID]
            exam_id1=requestData[EXAM_ID]
            art_code1=requestData[ART_CODE]
            articlelist= ARTDIC.get(str(art_code1))
            articlename=articlelist
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                artlist=[]
                artcodechk=ArticleDistribution.query.filter(ArticleDistribution.art_id !=art_id1,ArticleDistribution.art_code==art_code1)
                artcodecount=(artcodechk.count())
                if artcodecount>0:
                    return art_exist_code
                else:
                    singlearticleid=ArticleDistribution.query.filter_by(art_id=art_id1).first()
                   
                    singlecentreid=Center_det.query.filter_by(cen_id=cen_id1).first()
                    singleexamid=Exam.query.filter_by(exam_id=exam_id1).first()
                    if singlearticleid!=None:
                        singlearticleid.art_code=art_code1
                        db.session.commit()
                        artdic={ART_ID: art_id1,CEN_ID:cen_id1,EXAM_ID:exam_id1,ART_CODE: articlename}
                        artlist.append(artdic)
                        art_success_edit.update({DATA:artlist})
                        return art_success_edit
                    elif singlecentreid==None:
                        return cen_invalid_id
                    elif singleexamid==None:
                        return exam_invalid_id
                    else:
                        return art_invalid_id
            else:
                return session_invalid
        except Exception as e:
           return br_bad_request


    def delete(self):
        try:
            
            requestData=request.get_json()
            art_id1=requestData[ART_ID]
           
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                artlist=[]
                singlearticle=ArticleDistribution.query.filter_by(art_id= art_id1).first() 
                
                artcode=singlearticle.art_code
                articlelist= ARTDIC.get(str(artcode))
                articlename=articlelist
                artdic={ART_ID:singlearticle.art_id,ART_CODE:articlename,CEN_ID:singlearticle.cen_id,EXAM_ID:singlearticle.exam_id,ART_STATUS:singlearticle.art_status}
                if singlearticle!=None:
                    db.session.delete(singlearticle)
                    db.session.flush()
                    db.session.commit()
                    artlist.append(artdic)
                    art_success_delete.update({DATA:artdic})
                    return art_success_delete
                else:
                    return art_invalid_id
            else:
                return session_invalid
        except Exception as e:
            return art_bad_request
def generate_code():
    return str(random.randrange(10000, 99999))

def send_email(username,art_key):

    host='smtp.gmail.com'
    port=587
    email='smashx2018@gmail.com'
    password="tedaaststewbwlhk"
    subject="Article approval code"
    mail_to=username
    mail_from=email
    body="Hi CS, \n Article list is sent to your college.Your approval code is {id}. \n Store Officer ".format(id=art_key)

    # return u_id

    message = """From: %s\nTo:
    %s\nSubject:
    %s\n\n%s""" % (mail_from, mail_to, subject, body)

    try:

        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(email, password)
        server.sendmail(mail_from, mail_to, message)
        server.close()
        return 1
    except Exception as e:
            return art_bad_request



#=========================================================#
#                  ARTICLE ASSIGN ENDS                    #                           
#=========================================================#






#=========================================================#
#                  ROUTEOFFICER LOGIN STARTS              #                           
#=========================================================#


class RouteofficerLogin(Resource):    
    def post(self):
        try:
            requestData=request.get_json()            
            u_name=requestData[USER_NAME]
            u_pswd=requestData[USER_PSWD]
            ses_devtype=requestData[SES_DEVTYPE]            
            user_chk=User_det.query.filter_by(usr_email=u_name,usr_pswd=u_pswd).first()            
            if user_chk!=None:                
                role_chk=RoleDet.query.filter_by(role_id=user_chk.role_id,role_meta=ROUTE_OFFICER).first()
                if role_chk:
                    role_name=role_chk.role_name
                    ipaddress=get_my_ip()
                    curr_time=datetime.now()
                    session_token = token_urlsafe(64)
                    addsession=Session(user_id=user_chk.user_id,ses_devtype=ses_devtype,ses_token=session_token,ses_logintime=curr_time,ses_ip=ipaddress,ses_mac=ipaddress,ses_logouttime="",status=STATUS)
                    db.session.add(addsession)
                    db.session.commit()
                
                    r={ROLE_NAME:role_chk.role_name,SESSION_TOKEN:session_token,USER_ID:user_chk.user_id,USER_NAME:user_chk.name}
                    loginSuccess.update({DATA:r})
                    return loginSuccess
                else:
                    return invalid
            else:
                return invalidUser
        except Exception as e:
            print(e)
            return error  

def get_my_ip():
    return  request.remote_addr

#=========================================================#
#                  ROUTEOFFICER LOGIN ENDS                #                           
#=========================================================#

#=========================================================#
#                  ROUTEOFFICER LOGOUT STARTS             #                           
#=========================================================#
def checkSessionValidity(session_token,user_id): 
    chk_user=Session.query.filter_by(ses_token=session_token,user_id=user_id,status=STATUS).first()
    if chk_user!=None:
        return True
    else:
        return False

class RouteofficerLogout(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
          
            result=checkSessionValidity(session_token,user_id) 
            
            if result:
                sess_chk=Session.query.filter_by(ses_token=session_token,user_id=user_id).first()
                sess_chk.status=INACTIVE
                timestamp1 = datetime.now()
                sess_chk.ses_logouttime=timestamp1
                db.session.commit()
                return logoutSuccess
            else:
                return session_invalid
        except Exception as e:
            return error    



#=========================================================#
#                  ROUTEOFFICER LOGOUT ENDS               #                           
#=========================================================#



#=========================================================#
#                 FORGOT PASSWORD STARTS                  #                           
#=========================================================#



class CodeVerification(Resource):
    def post(data):
        content=request.get_json()
        emailid=content.get(EMAIL_ID)
        code=content.get(CODE)
        datas=cache_code(emailid)
        if datas != None:
            datas=int(datas)
        else:
            return emailcodeexpired
        if datas==int(code):
            return emailcodeverified            
        else:
            return emailcodeinvalid
      

class RouteOfficerForgotpassword(Resource):
    def post(self):
        requestData=request.get_json()
        emailid=requestData[EMAIL_ID]            
        chk_user=User_det.query.filter_by(usr_email=emailid).first()
        if chk_user!=None:
            number=cache_code(emailid)
            print(number)
            response=send_email(emailid,number)
            if response==0:
                return invalidEmail
            else:
                return mailSent
        else:
            return invalidEmail

#=========================================================#
#            NEW PASSWORD STARTS                          #                           
#=========================================================#

class RouteOfficerNewpassword(Resource):
    def post(data):
            requestData=request.get_json()
            emailid=requestData[EMAIL_ID]
            password=requestData[PASSWORD]
            chk_user=User_det.query.filter_by(usr_email=emailid).first()
            if chk_user!=None:                
                chk_user.usr_pswd=password
                db.session.commit()
                return passwdUpdate
            else:
                return invalidEmail


#=========================================================#
#           CHANGE PASSWORD STARTS                        #                           
#=========================================================#

class RouteOfficerChangePassword(Resource):
    def post(data):
        try:          
            requestData=request.get_json()
            emailid=requestData[EMAIL_ID]
            oldpassword=requestData[OLD_PASSWORD]
            newpassword=requestData[NEW_PASSWORD]
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            result=checkSessionValidity(session_token,user_id)
            if result:
                chk_user=User_det.query.filter_by(usr_email=emailid,usr_pswd=oldpassword,user_id=user_id).first()
                if chk_user!=None:
                    chk_user.usr_pswd=newpassword
                    db.session.commit()                    
                    return passwdUpdate1
                else:
                    return invalidEmail
            else:
                return session_invalid                
        except Exception as e:
            print(e)
            return error
        

#=========================================================#
#                  APPROVAL CODE VERIFY STARTS            #
#=========================================================#

#=========================================================#
#                  APPROVAL CODE VERIFY STARTS            #
#=========================================================#

class ApprovalCodeverify(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            art_approval_key=requestData[APPROVE_KEY]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                apprv_chk=ArticleDistribution.query.filter_by(art_approval_key=art_approval_key).first()
                print(apprv_chk)
              
                if apprv_chk!=None:
                    crr_date=datetime.date(datetime.now())
                    d_received=crr_date.strftime('%Y-%m-%d')
                    apprv_chk.art_status=RECIEVED
                    apprv_chk.date_received=d_received
                    exam_chk=Exam.query.filter_by(exam_id=apprv_chk.exam_id).first()
                    center_chk=Center_det.query.filter_by(cen_id=apprv_chk.cen_id).first()

                    
                    art_list=ARTDIC.get(apprv_chk.art_code)
                    article_list=art_list.split('|')
                    db.session.commit()
                    r={"exam_id":apprv_chk.exam_id,"exam_name":exam_chk.exam_name,"center_name":center_chk.cen_name,"cen_id":apprv_chk.cen_id,"art_data":article_list}
                    approveSuccess.update({DATA:r})
                    return approveSuccess
                else:
                    return invalidDet
            else:
                return session_invalid
        except Exception as e:
            return error



#=========================================================#
#                APPROVAL CODE VERIFY ENDS                #
#=========================================================#
