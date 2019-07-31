

from model import *
from constants import *
from flask_restful import Resource, Api
import json
from flask import Flask,jsonify,request
from secrets import token_urlsafe
import random
from datetime import datetime,timedelta
from datetime import *
import time
from user_mngmnt import *
from itertools import chain

#=========================================================#
#                   CHAIRMAN ADD STARTS                   #                           
#=========================================================#

class Chairman_Add(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
               
                chairmanlist=[]
                cen_id1=requestData[CEN_ID]
                exam_id1=requestData[EXAM_ID]
                prg_id1=requestData[PRG_ID]
                user_id1=requestData[CHAIRMAN_ID]
                user_existence=User_det.query.filter_by(user_id=user_id1,status=STATUS).first()
                if user_existence!=None:
                    singleidchk=Camp.query.filter_by(cen_id=cen_id1,prg_id=prg_id1,exam_id=exam_id1).first() 
                    chairman_exist=ChiefSuptd.query.filter_by(cen_id=cen_id1,exam_id= exam_id1,pgm_id=prg_id1,status=STATUS).first()
                    # print(chairman_exist)
                    if singleidchk==None:
                        return invalid_id
                    # elif chairman_exist!=None:
                    #     return cen_exam_prg_exist_id_err
                    else:
                        single=RoleDet.query.filter_by(role_meta=CHAIRMAN).first()                       
                        status1=STATUS
                        singlecamp=Camp.query.filter_by(cen_id=cen_id1,exam_id=exam_id1).first()
                        campenddate=singlecamp.end_date
                        exp_date=campenddate
                        exp_date= exp_date.strftime("%Y-%m-%d")
                        # singleRole=RoleDet.query.filter_by(role_meta=CHAIRMAN).first()
                        
                        
                        role_id1=single.role_id
                        new_chairmanlist=ChiefSuptd(exam_id=exam_id1,user_id=user_id1,cen_id=cen_id1,role_id=role_id1,pgm_id=prg_id1,exp_date=exp_date,status=status1)
                        chairmandic={EXAM_ID:exam_id1,CHAIRMAN_ID:user_id,CEN_ID:cen_id1,ROLE_ID:role_id1,PGM_ID:prg_id1,EXPIRE_DATE:exp_date}
                        chairmanlist.append(chairmandic)
                        db.session.add(new_chairmanlist)
                        
                        # singlecamp.end_date=chairman_exist.exp_date
                        user_existence.role_id=single.role_id
                        db.session.commit()
                        chairman_success_add.update({DATA:chairmanlist})
                
                        return chairman_success_add
                else:
                    return invalid  
                    
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
                roleobj=RoleDet.query.filter_by(role_meta="chairman").first()
                chairmanResponse=ChiefSuptd.query.filter(ChiefSuptd.pgm_id!="-1",ChiefSuptd.role_id==roleobj.role_id,ChiefSuptd.status==STATUS).all()
                chairmanlist=[]
                for i in chairmanResponse:
                    centre=Center_det.query.filter_by(cen_id=i.cen_id,status=STATUS).first()
                    exam=Exam.query.filter_by(exam_id=i.exam_id,status=STATUS).first()
                    role=RoleDet.query.filter_by(role_id=i.role_id,role_status=STATUS).first()
                    program=ProgramDet.query.filter_by(prg_id=i.pgm_id,status=STATUS).first()
                    user=User_det.query.filter_by(user_id=i.user_id,status=STATUS).first()
                    e_date=i.exp_date
                    newchairmanlist={CHAIRMAN_ID:i.user_id,CHAIRMAN_NAME:user.name,ROLE_NAME:role.role_name,CEN_ID:i.cen_id,CEN_NAME:centre.cen_name,
                    EXAM_ID:i.exam_id,EXAM_NAME:exam.exam_name,PGM_ID:i.pgm_id,PROGRAM_NAME:program.prg_name,EXPIRE_DATE:e_date}
                    chairmanlist.append(newchairmanlist)
                chairman_fetch.update({DATA:chairmanlist}) 
                return chairman_fetch
            else:
                return session_invalid
        except Exception as e:
            return br_bad_request  


    def delete(self):
        try:
            
            requestData=request.get_json()
            user_id1=requestData[CHAIRMAN_ID]
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                chairmanlist=[]
                singlechairman=ChiefSuptd.query.filter_by(user_id=user_id1,status=STATUS).first() 
                singlechief=ChiefExaminer.query.filter_by(chief_id=user_id1,status=STATUS).first() 
                user_exist=User_det.query.filter_by(user_id=user_id1,status=STATUS).first()
                single_teach=RoleDet.query.filter_by(role_meta=TEACHER).first()
                if  singlechief!= None:
                    return chief_exist_id
                elif singlechairman!=None:
                    chairmandic={CHAIRMAN_ID:singlechairman.user_id,CEN_ID:singlechairman.cen_id,EXAM_ID:singlechairman.exam_id,CHAIRMAN_STATUS:singlechairman.status}
                    db.session.delete(singlechairman)
                    user_exist.role_id=single_teach.role_id
                    db.session.commit()
                    chairmanlist.append( chairmandic)
                    camp_success_delete.update({DATA:chairmandic})
                    return chairman_success_delete
                else:
                    return chairman_invalid_id
            else:
                return session_invalid
        except Exception as e:
            return art_bad_request


#=========================================================#
#                CHAIRMAN ADD ENDS                        #
#=========================================================#        

#=========================================================#
#                  CHAIRMAN LIST STARTS                   #                           
#=========================================================#

class ChairmanList(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if CAMP_ID in requestData and EXAM_ID in requestData:
                    camp_id=requestData[CAMP_ID]
                    exam_id=requestData[EXAM_ID]
                    campobj=Camp.query.filter_by(cen_id=camp_id,exam_id=exam_id).first()
                    if  campobj==None:
                        return camp_not_exist
                    roleobj=RoleDet.query.filter_by(role_meta="chairman").first()
                    if roleobj==None:
                        return role_not_exist
                    chairmanobj=ChiefSuptd.query.filter_by(cen_id=camp_id,exam_id= exam_id,pgm_id=campobj.prg_id,role_id=roleobj.role_id).first()
                    if  chairmanobj==None:
                        return usernotexist
                    userobj=User_det.query.filter_by(user_id=chairmanobj.user_id).first()
                    if  userobj==None:  
                        return chairman_none
                    userdict={"chairman_id":userobj.user_id,"chairman_name":userobj.name}
                    chairman_success_single_fetch.update({DATA:userdict})
                    return chairman_success_single_fetch
            else:
                return session_invalid
        except Exception as e:
            return jsonify(error)
#=========================================================#
#                  CHAIRMAN LIST ENDS                     #                           
#=========================================================#


#=========================================================#
#                CHIEF EXAMINER ADD                       #
#=========================================================#

class ChiefExaminerAdd(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                
                if CAMP_ID in requestData:
                    
                    
                    chieflist=[]
                    exam_id=requestData[EXAM_ID]
                    cen_id=requestData[CAMP_ID]
                    
                    chief_id=requestData[CHIEF_ID]
                    chair_id=requestData[CHAIRMAN_ID]
                    user_existence=User_det.query.filter_by(user_id=chief_id,status=STATUS).first()
                    if user_existence!=None:

                        if chief_id==chair_id:
                            return jsonify(chief_chairman_err)
                        chief_existence=ChiefExaminer.query.filter_by(chief_id=chief_id,status=STATUS).first()
                        
                        if chief_existence==None:
                            singleRole=RoleDet.query.filter_by(role_meta=CHAIRMAN).first()
                            single=RoleDet.query.filter_by(role_meta=CHIEFEXAMINER).first()

                            r_id=singleRole.role_id
                            chairman_existance=ChiefSuptd.query.filter_by(cen_id=cen_id,exam_id=exam_id,user_id=chair_id,role_id=r_id).first()
                            chief_exist=ChiefExaminer.query.filter_by(camp_id=cen_id,exam_id= exam_id,chief_id=chief_id,chairman_id=chair_id).first()
                            if chief_exist:
                                return exists_chiefid
                            elif chairman_existance:
                                e_date=chairman_existance.exp_date
                                en_date=datetime.strptime(e_date,"%Y-%m-%d")
                                e_date=str(en_date)
                                new_chieflist=ChiefExaminer(camp_id=cen_id,exam_id= exam_id,chief_id=chief_id,chairman_id=chair_id,end_date=en_date,status=STATUS)
                                chiefdic={EXAM_ID:exam_id,CEN_ID:cen_id,CHIEF_ID:chief_id,CHAIRMAN_ID:chair_id}
                                chieflist.append(chiefdic)
                                db.session.add(new_chieflist)
                                user_existence.role_id=single.role_id
                                db.session.commit()

                                chief_success.update({DATA:chieflist})
                                return chief_success
                            else:

                                return exists_chair
                        else:
                            return exists_chiefid
                    else:
                        return invalid
                elif CHIEFEXAM_ID in  requestData:
                    
                    chief_id=requestData[CHIEFEXAM_ID]
                    user=ChiefExaminer.query.filter_by(chiefexam_id=chief_id,status=STATUS).first()
                    if  user!=None:
                        e_date=user.end_date
                        en_date=e_date.strftime("%Y/%m/%d")
                        r={CHIEFEXAM_ID:user.chiefexam_id,EXAM_ID:user.exam_id,CEN_ID:user.camp_id,CHIEF_ID:user.chief_id,CHAIRMAN_ID:user.chairman_id,
                        END_DATE:en_date,STAT:user.status}
                        chief_single_fetch.update({DATA:r})
                        return jsonify(chief_single_fetch)
            else:
                session_invalid

        except Exception as e:
            return error     

     
    

    def get(self):
        try:
            
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                chiefResponse=ChiefExaminer.query.filter_by(status=STATUS).all()
                if chiefResponse!=[]:
                    chieflist=[]
                    for i in chiefResponse:
                        centre=Center_det.query.filter_by(cen_id=i.camp_id,status=STATUS).first()
                        exam=Exam.query.filter_by(exam_id=i.exam_id,status=STATUS).first()
                        user=User_det.query.filter_by(user_id=i.chief_id,status=STATUS).first()
                        e_date=i.end_date
                        newchieflist={CHIEFEXAM_ID:i.chiefexam_id,CHIEF_NAME:user.name,EXAM_ID:i.exam_id,EXAM_NAME:exam.exam_name,
                        CEN_ID:centre.cen_id,CEN_NAME:centre.cen_name,CHIEF_ID:i.chief_id,CHAIRMAN_ID:i.chairman_id,
                        END_DATE:str(e_date),STAT:i.status}
                        chieflist.append(newchieflist)
                        chief_fetch.update({DATA:chieflist}) 
                    return chief_fetch
                else:
                    return chief_invalid
                
            else:
                return session_invalid
        
        except Exception as e:
            return error 


    def delete(self):
        try:
            requestData=request.get_json() 
            chief_id=requestData[CHIEF_ID]
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            
            if sess_res:
                chieflist=[]
                singlechief=ChiefExaminer.query.filter_by(chief_id=chief_id,status=STATUS).first()
                singleaddl=AdditionalExaminer.query.filter_by(chief_id=chief_id,status=STATUS).first() 
                user_exist=User_det.query.filter_by(user_id=chief_id,status=STATUS).first()
                single_teach=RoleDet.query.filter_by(role_meta=TEACHER).first()

                if  singleaddl!= None:
                    return addl_exist_error
                
                elif singlechief!=None:
                    
                    # chiefdic={CHAIRMAN_ID:singlechairman.user_id,CEN_ID:singlechairman.cen_id,EXAM_ID:singlechairman.exam_id,CHAIRMAN_STATUS:singlechairman.status}
                    # db.session.delete(singlechief)
                    # db.session.delete(singlechief)
                    singlechief.status=INACTIVE
                    user_exist.role_id=single_teach.role_id

                    db.session.commit()

                    chiefdic={CHIEFEXAM_ID:singlechief.chiefexam_id,EXAM_ID:singlechief.exam_id,CEN_ID:singlechief.camp_id,
                    CHIEF_ID:singlechief.chief_id,CHAIRMAN_ID:singlechief.chairman_id,STAT:singlechief.status}
                    chieflist.append(chiefdic)
                    chief_success_delete.update({DATA:chiefdic})
                    
                    return chief_success_delete
                else:
                    return chief_invalid_id
            else:
                return session_invalid
        except Exception as e:
            return error

                   
#=========================================================#
#                CHIEF EXAMINER ADD ENDS                  #
#=========================================================#


#=========================================================#
#               CHIEF EXAMINER LIST STARTS                #
#=========================================================#

class ChiefExaminerList(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            exam_id=requestData[EXAM_ID]
            cen_id=requestData[CAMP_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                chiefResponse=ChiefExaminer.query.filter_by(exam_id=exam_id,camp_id=cen_id,status=STATUS).all()
                
                if chiefResponse!=[]:
                    chieflist=[]
                    for i in chiefResponse:
                        user=User_det.query.filter_by(user_id=i.chief_id,status=STATUS).first()
                        centre=Center_det.query.filter_by(cen_id=i.camp_id,status=STATUS).first()
                        exam=Exam.query.filter_by(exam_id=i.exam_id,status=STATUS).first()
                        newlist={CHIEF_ID:i.chief_id,CHIEF_NAME:user.name,EXAM_ID:i.exam_id,EXAM_NAME:exam.exam_name,CAMP_ID:centre.cen_id,CEN_NAME:centre.cen_name}
                        chieflist.append(newlist)
                        chief_fetch.update({DATA:chieflist}) 
                    return chief_fetch
                else:
                    return chief_invalid
                
            else:
                return session_invalid
        
        except Exception as e:           
            return error 


#=========================================================#
#               CHIEF EXAMINER LIST ENDS                  #
#=========================================================#

#===========================================================#
#                   CAMP OFFICER ADD                        #
#===========================================================#

class CampOfficerAdd(Resource):
    def post(self):
        try:
            data = request.get_json()
            session_token =data[SESSION_TOKEN]
            user_id =data[USER_ID]
            sess_res = checkSessionValidity(session_token, user_id)
            if(not sess_res):
                return session_invalid                    
            if CEN_ID in data:
                empty=[]
                emp=[]
                status1 = STATUS                
                colist = []
                cen_id1 = data[CEN_ID]
                exam_id1 = data[EXAM_ID]                
                co_id =data[CAMP_OFFI_ID]              
                co_exist = ChiefSuptd.query.filter_by(cen_id=cen_id1, exam_id=exam_id1, user_id=co_id,status=STATUS).first()
                user_exist = User_det.query.filter_by(user_id=co_id, status=status1).first()
                if(co_exist)!=None:
                    return campofficer_exist_err
                singleidchk = Camp.query.filter_by(cen_id=cen_id1,exam_id=exam_id1).first()                       
                if singleidchk==None:
                    return(campofficer_error_delete)
                # campof_exist=ChiefSuptd.query.filter_by(cen_id=cen_id1, exam_id=exam_id1).first()
                # if campof_exist!= None:
                #     return campofficer_exist
                status1 = STATUS                    
                campenddate = singleidchk.end_date
                prg_id1 =singleidchk.prg_id
                exp_date = campenddate
                exp_date = exp_date.strftime("%Y-%m-%d")               
                singleRole = RoleDet.query.filter_by(role_meta=CAMPOFFICER).first()
                role_id1 = singleRole.role_id                   
                new_campofficerlist = ChiefSuptd(exam_id=exam_id1,user_id=co_id,cen_id=cen_id1,role_id=role_id1,pgm_id=prg_id1,exp_date=exp_date,status=status1)               
                db.session.add(new_campofficerlist)
                user_exist.role_id=role_id1
                user_exist.cen_id=cen_id1
                db.session.commit()
                v1 = ChiefSuptd.query.all()
                for i in v1:
                    d = {CHIEF_SUPTD_ID : i.chief_suptd_id, EXAM_ID: i.exam_id,CAMP_OFFI_ID: i.user_id, CEN_ID: i. cen_id, ROLE_ID: i.role_id, PRG_ID: i.pgm_id, EXP_DATE: i.exp_date, CO_STATUS: i.status}
                empty.append(d)
                campofficersucss_post[DATA] = d
                return campofficersucss_post
            
        
            elif CAMP_OFFI_ID in data:
                co_id = data[CAMP_OFFI_ID]
                if sess_res:
                    user = ChiefSuptd.query.filter_by(user_id=co_id,status = STATUS).first()
                    user3 = User_det.query.filter_by(user_id=co_id).first()
                    if user != None and user3!=None:
                        d = {CAMP_OFFI_ID: user.user_id, USERNAME: user3.name, PRG_ID: user.pgm_id,EXAM_ID: user.exam_id, CEN_ID: user.cen_id, ROLE_ID: user.role_id, EXP_DATE:user.exp_date}
                        campofficer_sucss_post_co_id[DATA] = d
                        return campofficer_sucss_post_co_id
                    else:
                        campofficer_error_post_co_id[DATA] = []
                        return campofficer_error_post_co_id           
        except Exception as e:
            return err_exception

    def get(self):
        try:

            session_token = request.headers[SESSION_TOKEN]
            user_id = request.headers[USER_ID]
            sess_res = checkSessionValidity(session_token, user_id)
            if(not sess_res):
                 return session_invalid
            singleRole = RoleDet.query.filter_by(role_meta=CAMPOFFICER).first()
            coResponse = ChiefSuptd.query.filter(ChiefSuptd.role_id == singleRole.role_id, ChiefSuptd.status == STATUS).all()
            
            coList=[]          
       
            for i in coResponse :                
                centre = Center_det.query.filter_by(cen_id=i.cen_id).first()
                exam = Exam.query.filter_by(exam_id=i.exam_id).first()
                role = RoleDet.query.filter_by(role_id=i.role_id).first()
                program = ProgramDet.query.filter_by(prg_id=i.pgm_id).first()
                user = User_det.query.filter_by(user_id=i.user_id).first()
                
                e_date = i.exp_date

                NewcoList = {CHIEF_SUPTD_ID : i.cen_id, EXAM_ID: i.exam_id,CAMP_OFFI_ID: i.user_id, USERNAME: user.name, CEN_ID: i.cen_id, CEN_NAME: centre.cen_name, ROLE_ID: i.role_id, ROLE_NAME: role.role_name, PRG_ID: i.pgm_id, PRG_NAME: program.prg_name, EXP_DATE:e_date}
                coList.append(NewcoList)
            campofficer_sucss_get[DATA] = coList

            return campofficer_sucss_get

        except Exception as e:
            return err_exception
           

    
    def delete(self):
        try:

                data = request.get_json()             
                
                session_token =data[SESSION_TOKEN]
                user_id =data[USER_ID]
                sess_res = checkSessionValidity(session_token,user_id)
                if(not sess_res):
                    return session_invalid
                
                
                colist = []
                co_id = data[CAMP_OFFI_ID]
                
                exam_id1 =data[EXAM_ID]
                camp_id =data[CAMP_ID]

                singleRole = RoleDet.query.filter_by(role_meta=CAMPOFFICER).first()
               
                co_exist = ChiefSuptd.query.filter_by(role_id = singleRole.role_id, exam_id=exam_id1,user_id=co_id,status=STATUS).first()     
                        
                campchk = Camp.query.filter_by(cen_id=camp_id,exam_id=exam_id1).first()  
                
               

                if(co_exist) == None :
                    return campofficer_error_delete
                if campchk==None:
                    return jsonify(camp_not_exist)
              
                singleRole = RoleDet.query.filter_by(role_meta=PUBLIC).first()            
                colist = []
                
                co_exist.status=INACTIVE
                userData = User_det.query.filter_by(user_id=co_exist.user_id).first()
                userData.role_id=singleRole.role_id
                
                db.session.commit()
                return campofficer_sucss_delete
                
               
        except Exception as e:
            return err_exception





#===================================================#
#             CAMPOFFICER ADD ENDS                #
#===================================================#



#===================================================#
#             ADDITIONAL EXAMINER ADD STARTS        #
#===================================================#

class AdditionalExaminer_Add(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if CAMP_ID in requestData:
                    print(requestData)
                    addllist=[]
                    exam_id=requestData[EXAM_ID]
                    cen_id=requestData[CAMP_ID]
                    
                    chief_id1=requestData[CHIEF_ID]

                    addl_id1=requestData[ADDITIONAL_ID]
                    user_existence=User_det.query.filter_by(user_id=addl_id1,status=STATUS).first()
                    if user_existence!=None:
                        if addl_id1==chief_id1:
                            return jsonify(addl_chief_err)
                        addl_exist=AdditionalExaminer.query.filter_by(addl_id=addl_id1,status=STATUS).first()
                        if  addl_exist==None:
                            singleRole=RoleDet.query.filter_by(role_meta=CHIEFEXAMINER).first()
                            single=RoleDet.query.filter_by(role_meta=ADDITIONALEXAMINER).first()

                            # r_id=singleRole.role_id
                        
                            chief_existance=ChiefExaminer.query.filter_by(camp_id=cen_id,exam_id=exam_id,chief_id=chief_id1).first()
                            
                            addl_exist=AdditionalExaminer.query.filter_by(cen_id=cen_id,exam_id=exam_id,addl_id=addl_id1,chief_id=chief_id1).first()
                           
                            
                            if chief_existance:
                                
                                
                                new_addllist=AdditionalExaminer(cen_id=cen_id,exam_id= exam_id,chief_id=chief_id1,addl_id= addl_id1,status=STATUS)
                                addldic={ADDITIONAL_ID:addl_id1,EXAM_ID:exam_id,CAMP_ID:cen_id,CHIEF_ID:chief_id1}
                                addllist.append(addldic)
                                db.session.add( new_addllist)
                                user_existence.role_id=single.role_id
                                db.session.commit()
                                
                                additional_success.update({DATA:addllist})
                                return additional_success
                            else:

                                return exists_chief
                        else:
                            
                            return exists_additional       
                    else:
                        return invalid            
                        
                elif ADDITIONALEXAM_ID in  requestData:
                    
                    addlexam_id1=requestData[ADDITIONALEXAM_ID]
                
                    user=AdditionalExaminer.query.filter_by(addlexam_id= addlexam_id1,status=STATUS).first()                    
                    if  user!=None:
                    
                        r={ADDITIONALEXAM_ID:user.addlexam_id,EXAM_ID:user.exam_id,CAMP_ID:user.cen_id,
                        CHIEF_ID:user.chief_id,ADDITIONAL_ID:user.addl_id,STATUS:user.status}
                        additional_single_fetch.update({DATA:r})
                        return additional_single_fetch
                    else:
                        return invalid_addlexam_id   
            else:
                session_invalid

        except Exception as e:           
            return error     
    
    
    

    def get(self):
        try:
            
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                additionalResponse=AdditionalExaminer.query.all()
                print(additionalResponse)
                addllist=[]
                for i in additionalResponse:
                    centre=Center_det.query.filter_by(cen_id=i.cen_id,status=STATUS).first()
                    exam=Exam.query.filter_by(exam_id=i.exam_id,status=STATUS).first()
                    addlUser=User_det.query.filter_by(user_id=i.addl_id,status=STATUS).first()
                    chief=ChiefExaminer.query.filter_by(chief_id=i.chief_id,status=STATUS).first()
                    chiefUser=User_det.query.filter_by(user_id=i.chief_id,status=STATUS).first()
                    chairmanUser=User_det.query.filter_by(user_id=chief.chairman_id,status=STATUS).first()
                    # chairman=ChiefSuptd.query.filter_by(user_id=i.chairman_id).first()

                    newaddllist={ADDITIONALEXAM_ID:i.addlexam_id,ADDITIONAL_ID:i.addl_id,ADDITIONAL_NAME:addlUser.name,EXAM_ID:i.exam_id,EXAM_NAME:exam.exam_name,
                    CAMP_ID:i.cen_id,CEN_NAME:centre.cen_name,CHIEF_ID:i.chief_id,CHIEF_NAME:chiefUser.name,CHAIRMAN_ID:chief.chairman_id,CHAIRMAN_NAME:chairmanUser.name}
                    addllist.append(newaddllist)
                    print(addllist)
                    additional_fetch.update({DATA:addllist}) 
                return additional_fetch
                
            else:
                return session_invalid
        
        except Exception as e:            
            return error 


    def delete(self):
        try:
            requestData=request.get_json() 
            addl_id1=requestData[ADDITIONAL_ID]
           
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            
            if sess_res:
                addllist=[]
                singleaddl=AdditionalExaminer.query.filter_by(addl_id=addl_id1,status=STATUS).first()
                user_exist=User_det.query.filter_by(user_id=addl_id1,status=STATUS).first()
                single_teach=RoleDet.query.filter_by(role_meta=TEACHER).first()
               
                
                if singleaddl!=None:
                    addldic={ADDITIONALEXAM_ID:singleaddl.addlexam_id,ADDITIONAL_ID:singleaddl.addl_id,EXAM_ID:singleaddl.exam_id,CAMP_ID:singleaddl.cen_id,
                    CHIEF_ID:singleaddl.chief_id}
                    
                    db.session.delete(singleaddl)
                    singleaddl.status=INACTIVE
                    user_exist.role_id=single_teach.role_id
                    db.session.commit()
                    addllist.append(addldic)
                    additional_success_delete.update({DATA:addldic})
                    
                    return additional_success_delete
                else:
                    return additional_invalid_id
            else:
                return session_invalid
        except Exception as e:            
            return error
#===================================================#
#             ADDITIONAL EXAMINER ADD ENDS          #
#===================================================#

#===================================================#
#             ADDITIONAL EXAMINER LIST STARTS       #
#===================================================#
    
class AdditionalExaminerList(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            exam_id=requestData[EXAM_ID]
            cen_id=requestData[CAMP_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                role_det=RoleDet.query.filter_by(role_name=CAMP_OFFICER).first()
                csCheck=ChiefSuptd.query.filter_by(user_id=user_id,role_id=role_det.role_id).first()
                if csCheck==None:
                    return campofficerError

                addlResponse=AdditionalExaminer.query.filter_by(exam_id=exam_id,cen_id=csCheck.cen_id,status=STATUS).all()
                
                if addlResponse!=[]:
                    chieflist=[]
                    for i in addlResponse:
                        user=User_det.query.filter_by(user_id=i.addl_id,status=STATUS).first()
                        centre=Center_det.query.filter_by(cen_id=i.cen_id,status=STATUS).first()
                        exam=Exam.query.filter_by(exam_id=i.exam_id,status=STATUS).first()
                        newlist={ADDITIONAL_ID:i.addl_id,ADDITIONAL_NAME:user.name,EXAM_ID:i.exam_id,EXAM_NAME:exam.exam_name,CAMP_ID:centre.cen_id,CEN_NAME:centre.cen_name}
                        chieflist.append(newlist)
                        additional_fetch.update({DATA:chieflist}) 
                    return additional_fetch
                else:
                    return additional_no_data
                
            else:
                return session_invalid
        
        except Exception as e:
            print(e)
            return error  


#===================================================#
#             ADDITIONAL EXAMINER LIST ENDS         #
#===================================================#


#===================================================#
#             UNIVERSITY OFFICIALS LIST STARTS      #
#===================================================#
class UniversityOfficialList(Resource):
    def get(self):
        try:            
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sessionCheck=checkSessionValidity(session_token,user_id) 
            if sessionCheck:                
                resultList=[]
                singleRole=RoleDet.query.filter_by(role_meta=PUBLIC).first()
                uniOfficialsList=User_det.query.filter_by(usr_cat1=NON_TEACH,usr_cat2=UNIVER_CAT,status=STATUS,role_id=singleRole.role_id)
                if uniOfficialsList.count()>0:
                    
                    for singleOfficial in uniOfficialsList:
                        OfficialsDic={"officer_id":singleOfficial.user_id,"officer_name":singleOfficial.name}
                        resultList.append(OfficialsDic)
                    uni_fetch.update({DATA:resultList})
                return jsonify(uni_fetch)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(msg_400)
#===================================================#
#             UNIVERSITY OFFICIALS LIST ENDS        #
#===================================================#

#===================================================#
#           ANSWER SCRIPT DISTRIBUTION START        #                           
#===================================================#
class AnsScriptDistribution(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if CAMP_ID in requestData and EXAM_ID in requestData and  ADDITIONAL_EX_ID in requestData and FALSE_NO_LIST in requestData:
                    camp_id=requestData[CAMP_ID]
                    exam_id=requestData[EXAM_ID]
                    add_ex_id=requestData[ADDITIONAL_EX_ID]
                    false_no=requestData[FALSE_NO_LIST]
                    # pass this list to a function for check the false numbers are correct or not.
                    #ans=check_false_no_correct(false_no)
                    false_no_dupli_remove = list(dict.fromkeys(false_no))
                    dist_count=len(false_no_dupli_remove)
                    if len(false_no)!=len(false_no_dupli_remove):
                        return duplicate_error
                    dis_date=datetime.today()
                    chairmanobj=ChiefSuptd.query.filter_by(cen_id=camp_id,exam_id= exam_id).first()
                    if  chairmanobj==None:
                        return campnotexist_error
                    additnlobj=AdditionalExaminer.query.filter_by(addl_id=add_ex_id).first()
                    if  additnlobj==None:
                        return usernotexist
                    ans_fun=false_no_dis_funct(false_no_dupli_remove,exam_id,camp_id,add_ex_id,dis_date,dist_count,user_id)
                    return ans_fun
            else:
                return session_invalid
        except Exception as e:            
            return error

# function for distribute answerscripts
def false_no_dis_funct(false_no_dupli_remove,exam_id,camp_id,add_ex_id,dis_date,dist_count,user_id):
    if len(false_no_dupli_remove)!=0:
        false_str=false_no_convert(false_no_dupli_remove)
        usrobj=User_det.query.filter_by(user_id=user_id).first()
        exobj=Exam.query.filter_by(exam_id=exam_id).first()
        ansobj=AnswerScriptDistribution.query.filter_by(exam_id=exam_id,camp_id=camp_id,addl_id=add_ex_id).first()
        if ansobj==None:
            new_ans=AnswerScriptDistribution(exam_id=exam_id,camp_id=camp_id,addl_id=add_ex_id,ans_distribution_date=dis_date,ans_distribution_count=dist_count,ans_distribution_flase_num_list=false_str)
            db.session.add(new_ans)
            db.session.commit()
            userdict={"userid":user_id,"user_name":usrobj.name,"examid":exam_id,"exam_name":exobj.exam_name,"distribution_count":dist_count}
            ans_script_dis_success.update({DATA:userdict})
            return ans_script_dis_success 
        else:
            f_list=ansobj.ans_distribution_flase_num_list
            fal_list=Convert_to_string(f_list)
            new_fl_list=fal_list+false_no_dupli_remove
            false_list_dup= list(dict.fromkeys(new_fl_list))
            new_count=len(false_list_dup)
            new_str=false_no_convert(false_list_dup)
            ansobj.ans_distribution_count=new_count
            ansobj.ans_distribution_flase_num_list=new_str
            db.session.commit()
            userdict={"userid":user_id,"user_name":usrobj.name,"examid":exam_id,"exam_name":exobj.exam_name,"distribution_count":new_count}
            ans_script_dis_success.update({DATA:userdict})
            return ans_script_dis_success

# function for convert list to string
def false_no_convert(false_no_dupli_remove):
    false_str = '|'.join(str(e) for e in false_no_dupli_remove)
    return false_str

# function for convert string to list
def Convert_to_string(f_list): 
    falselist = list(f_list.split("|")) 
    return falselist
#===================================================#
#          ANSWER SCRIPT DISTRIBUTION   END         #                           
#===================================================#


#=========================================================#
#                 ANSWER SCRIPT DISTRIBUTION VIEW         # 
#=========================================================#

class AnsScriptDistributionView(Resource):

    def get(self):

        try: 
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            camp_id=request.headers[CAMP_ID]
            sessionCheck=checkSessionValidity(session_token,user_id) 
            if sessionCheck:
                role_det=RoleDet.query.filter_by(role_name=CHAIRMAN).first()
                csCheck=ChiefSuptd.query.filter_by(user_id=user_id,role_id=role_det.role_id).first()
                roleData=RoleDet.query.filter_by(role_name=CAMP_OFFICER).first()
                coCheck=User_det.query.filter_by(user_id=user_id,role_id=roleData.role_id).first()
                if csCheck!=None:
                    cen_id=csCheck.cen_id
                elif coCheck!=None:
                    cen_id=coCheck.cen_id
                addlResponse=AnswerScriptDistribution.query.filter_by(camp_id=cen_id).all()
                if addlResponse!=[]:
                    viewlist=[]
                    for i in addlResponse:
                        s_date=i.ans_distribution_date
                        s_date=s_date.strftime("%Y-%m-%d")

                        user=User_det.query.filter_by(user_id=i.addl_id,status=STATUS).first()
                        exam=Exam.query.filter_by(exam_id=i.exam_id,status=STATUS).first()
                        newlist={ADDITIONAL_ID:i.addl_id,ADDITIONAL_NAME:user.name,EXAM_ID:i.exam_id,EXAM_NAME:exam.exam_name,CAMP_ID:i.camp_id,
                        ANSWER_DISTRIBUTION_DATE:s_date,ANSWER_DISTRIBUTION_COUNT:i.ans_distribution_count}
                        viewlist.append(newlist)
                    answerScriptfetch.update({DATA:viewlist})
                    return answerScriptfetch
                else:
                    return answerScriptfetchErr
            else:
                return session_invalid
        except Exception as e:
                      
            return error 
#=========================================================#
#                 ANSWER SCRIPT DISTRIBUTION VIEW ENDS    # 
#=========================================================#

#=========================================================#
#       ANSWER SCRIPT RETURN START(CO MARK ENTRY)         #                           
#=========================================================#
class AnsScriptReturn(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if CAMP_ID in requestData  and  DATA_LIST in requestData:  #and EXAM_ID in requestData
                    camp_id=requestData[CAMP_ID]
                    # exam_id=requestData[EXAM_ID]
                    data=requestData[DATA_LIST]
                    flag=0
                    conf_list=[]
                    false_no_list=[]
                    conf_falseno_list=[]
                    datalist=[]
                    resultlist=[]
                    chairmanobj=ChiefSuptd.query.filter_by(cen_id=camp_id,user_id=user_id).first()                    
                    if  chairmanobj==None:
                        return campnotexist_error
                    exam_id=chairmanobj.exam_id
                    usrobj=User_det.query.filter_by(user_id=user_id).first()
                    exobj=Exam.query.filter_by(exam_id=exam_id).first()
                    for i in data:
                        falseno=i.get('false_no')
                        false_no_list.append(falseno)
                        mark=i.get('mark')
                        studmarkobj=StudentMark.query.filter_by(camp_id=camp_id,exam_id= exam_id,dfm_num=falseno,smp_status=0).first()
                        if studmarkobj==None:
                            return marknotexist_error
                        if mark==int(studmarkobj.std_mark):
                            studmarkobj.co_id=user_id
                            studmarkobj.co_mark=mark
                            studmarkobj.co_date=datetime.date(datetime.now())
                            db.session.commit()
                        else:
                            flag=1
                            conf_falseno_list.append(falseno)
                            conf_dict={"false_no":falseno,"mark":mark}
                            conf_list.append(conf_dict)
                    if flag==0:
                        ans_script_return_success.update({DATA:data})
                        return ans_script_return_success
                    else:
                        resultlist=list(set(false_no_list)-set(conf_falseno_list))
                        print(resultlist)
                        # for i in false_no_list:
                        #     c=0
                        #     for j in conf_falseno_list:
                        #         if i!=j:
                        #             c=1
                        #         else:
                        #             c=0
                        #             break
                        #     if c==1:
                        #         resultlist.append(i)
                        for i in data:
                            for j in resultlist:
                                if(j!=i.get("false_no")):
                                    continue
                                datalist.append(i)
                        ans_script_return_conflict.update({CONF_DATA:conf_list,OLD_DATA:datalist})
                        return ans_script_return_conflict
            else:
                return session_invalid
        except Exception as e:            
            return error
#=========================================================#
#                 ANSWER SCRIPT RETURN END                #                           
#=========================================================#

#=========================================================#
#            ADD MARK BY ADDITIONAL EXAMINER  START       #                           
#=========================================================#
class AddAdditionalMark(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            role_type=requestData[ROLE_TYPE]
            data=requestData[DATA_LIST]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if role_type=="A":
                    addlobj=AdditionalExaminer.query.filter_by(addl_id=user_id).first()
                    if  addlobj==None:
                        return notExists
                    cenid=addlobj.cen_id
                    exid=addlobj.exam_id
                    resultList=[]
                    for i in data:
                        falseobj=FalseNumber.query.filter_by(dfm_num=i.get('false_no')).first()
                        if  falseobj==None:
                            return falseno_not_exist
                        course_id=falseobj.cou_id
                        courobj=Course.query.filter_by(cou_id=course_id).first()
                        if  courobj==None:
                            return notExists
                        prg_id=courobj.pgm_id
                        chairmanobj=ChiefSuptd.query.filter_by(cen_id=cenid,exam_id=exid,pgm_id=prg_id).first()
                        if  chairmanobj==None:
                            return campnot_exist_error
                        reg_no=falseobj.std_reg_num
                        studmarkflsobj=StudentMark.query.filter_by(dfm_num=i.get('false_no')).first()
                        if  studmarkflsobj!=None:
                            return false_no_exist
                        studmarkobj=StudentMark.query.filter_by(dfm_num=i.get('false_no'),exam_id=exid,cou_id=course_id,prg_id=prg_id,camp_id=cenid,std_reg_num=reg_no).first()
                        if  studmarkobj!=None:
                            return stud_mark_exist
                        if i.get('smp_status')==1:
                            new_studmarkobj=StudentMark(std_reg_num=reg_no,dfm_num=i.get('false_no'),cou_id=course_id,prg_id=prg_id,exam_id=exid,camp_id=cenid,addl_id=user_id,
                            addl_mark=i.get('mark'),addl_date=datetime.today(),
                            chief_id=0,chief_mark=0,chief_date=0000-00-00,chairman_id=0,
                            chairman_mark=0,chairman_date=0000-00-00,co_id=0,co_mark=0,co_date=0000-00-00,
                            std_mark="smp",smp_status=i.get('smp_status'))
                            db.session.add(new_studmarkobj)
                            db.session.commit()
                        else:
                            new_studmarkobj=StudentMark(std_reg_num=reg_no,dfm_num=i.get('false_no'),cou_id=course_id,prg_id=prg_id,exam_id=exid,camp_id=cenid,addl_id=user_id,
                            addl_mark=i.get('mark'),addl_date=datetime.today(),
                            chief_id=0,chief_mark=0,chief_date=0000-00-00,chairman_id=0,
                            chairman_mark=0,chairman_date=0000-00-00,co_id=0,co_mark=0,co_date=0000-00-00,
                            std_mark=i.get('mark'),smp_status=i.get('smp_status'))
                            db.session.add(new_studmarkobj)
                            db.session.commit()
                    add_astnl_mark_success.update({DATA:{RESULT_DATA:resultList}})
                    return add_astnl_mark_success
                elif role_type=="C":
                    chiefobj=ChiefExaminer.query.filter_by(chief_id=user_id).first()
                    print(chiefobj)
                    if  chiefobj==None:
                        return notExists
                    cenid=chiefobj.camp_id
                    exid=chiefobj.exam_id
                    resultList=[]
                    for i in data:
                        falseobj=FalseNumber.query.filter_by(dfm_num=i.get('false_no')).first()
                        if  falseobj==None:
                            return falseno_not_exist
                        reg_no=falseobj.std_reg_num
                        course_id=falseobj.cou_id
                        courobj=Course.query.filter_by(cou_id=course_id).first()
                        if  courobj==None:
                            return notExists
                        prg_id=courobj.pgm_id
                       
                        chairmanobj=ChiefSuptd.query.filter_by(cen_id=cenid,exam_id=exid,pgm_id=prg_id).first()
                       
                        if  chairmanobj==None:
                            return campnot_exist_error
                        studmarkobj=StudentMark.query.filter_by(dfm_num=i.get('false_no'),exam_id=exid,cou_id=course_id,prg_id=prg_id,camp_id=cenid,std_reg_num=reg_no).first()
                        if  studmarkobj==None:
                            return stud_mark_not_exist
                        if i.get('smp_status')==1:
                            studmarkobj.chief_id=user_id
                            studmarkobj.chief_mark=i.get('mark')
                            studmarkobj.chief_date=datetime.today()
                            studmarkobj.std_mark="smp"
                            studmarkobj.smp_status=i.get('smp_status')
                            db.session.commit()
                        else:
                            studmarkobj.chief_id=user_id
                            studmarkobj.chief_mark=i.get('mark')
                            studmarkobj.chief_date=datetime.today()
                            studmarkobj.std_mark=i.get('mark')
                            studmarkobj.smp_status=i.get('smp_status')
                            db.session.commit()
                    add_astnl_mark_success.update({DATA:{RESULT_DATA:resultList}})
                    return add_astnl_mark_success
            else:
                return session_invalid_msg
        except Exception as e:
            return error_msg

#=========================================================#
#            ADD MARK BY ADDITIONAL EXAMINER  END         #                           
#=========================================================#
#=========================================================#
#            ADD MARK BY CHIEF EXAMINER  START            #                           
#=========================================================#
class AddChiefMark(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            print(user_id)
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if DATA_LIST in requestData:
                    data=requestData[DATA_LIST]
                    chiefobj=ChiefExaminer.query.filter_by(chief_id=user_id).first()
                    print(chiefobj)
                    if  chiefobj==None:
                        return notExists
                    cenid=chiefobj.camp_id
                    exid=chiefobj.exam_id
                    resultList=[]
                    for i in data:
                        falseobj=FalseNumber.query.filter_by(dfm_num=i.get('false_no')).first()
                        if  falseobj==None:
                            return falseno_not_exist
                        reg_no=falseobj.std_reg_num
                        course_id=falseobj.cou_id
                        courobj=Course.query.filter_by(cou_id=course_id).first()
                        if  courobj==None:
                            return notExists
                        prg_id=courobj.pgm_id
                       
                        chairmanobj=ChiefSuptd.query.filter_by(cen_id=cenid,exam_id=exid,pgm_id=prg_id).first()
                       
                        if  chairmanobj==None:
                            return campnot_exist_error
                        studmarkobj=StudentMark.query.filter_by(dfm_num=i.get('false_no'),exam_id=exid,cou_id=course_id,prg_id=prg_id,camp_id=cenid,std_reg_num=reg_no).first()
                        if  studmarkobj==None:
                            return stud_mark_not_exist
                        if i.get('smp_status')==1:
                            studmarkobj.chief_id=user_id
                            studmarkobj.chief_mark=i.get('mark')
                            studmarkobj.chief_date=datetime.today()
                            studmarkobj.std_mark="smp"
                            studmarkobj.smp_status=i.get('smp_status')
                            db.session.commit()
                        else:
                            studmarkobj.chief_id=user_id
                            studmarkobj.chief_mark=i.get('mark')
                            studmarkobj.chief_date=datetime.today()
                            studmarkobj.std_mark=i.get('mark')
                            studmarkobj.smp_status=i.get('smp_status')
                            db.session.commit()
                    add_astnl_mark_success.update({DATA:{RESULT_DATA:resultList}})
                    return add_astnl_mark_success
            else:
                return session_invalid_msg
        except Exception as e:           
            return error_msg

#=========================================================#
#            ADD MARK BY CHIEF EXAMINER  END              #                           
#=========================================================#
#=========================================================#
#                 ADD MARK BY CHAIRMAN   START            #                           
#=========================================================#
class AddChairmanMark(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id)
            if sess_res:
                false_no=requestData[FALSE_NUMBER]
                mark=requestData[MARK]
                smp_status=requestData[SMP_STATUS]
                chairmanobj=StudentMark.query.filter_by(dfm_num=false_no).first()
                if chairmanobj==None: 
                    return falseno_not_exist 
                chairmanobj1=StudentMark.query.filter_by(dfm_num=false_no,chairman_mark=0).first()
                if chairmanobj1==None:
                    return mark_exist_error
                roleobj=RoleDet.query.filter_by(role_meta=CHAIRMAN).first()
                chairmanResponse=ChiefSuptd.query.filter(ChiefSuptd.role_id==roleobj.role_id,ChiefSuptd.user_id==user_id).first()                  
                if chairmanResponse== None:
                    return chairman_error
                exam_id=chairmanResponse.exam_id                
                falseobj=FalseNumber.query.filter_by(dfm_num=false_no).first()
                reg_no=falseobj.std_reg_num
                studmarkobj=StudentMark.query.filter_by(dfm_num=false_no,exam_id= exam_id,std_reg_num=reg_no).first()                
                
                if smp_status==1:
                    studmarkobj.chairman_id=user_id
                    studmarkobj.chairman_mark=mark
                    studmarkobj.chairman_date=datetime.date(datetime.now())
                    
                    
                    studmarkobj.std_mark="smp"
                    studmarkobj.smp_status=smp_status
                    db.session.commit()
                else:
                    studmarkobj.chairman_id=user_id
                    studmarkobj.chairman_mark=mark
                    studmarkobj.chairman_date=datetime.date(datetime.now())
                    
                    studmarkobj.std_mark=mark
                    studmarkobj.smp_status=smp_status
                    db.session.commit()
                add_astnl_mark_success.update({DATA:[]})
                return add_astnl_mark_success
                

                        
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
                
                marklist=[]
                addllist=[]
                roleobj=RoleDet.query.filter_by(role_meta=CHAIRMAN).first()
                chairmanobj=ChiefSuptd.query.filter_by(user_id=user_id,role_id=roleobj.role_id).first()
                chairmanid=chairmanobj.user_id
                chiefobj=ChiefExaminer.query.filter_by(chairman_id=chairmanid).first()
                chiefid=chiefobj.chief_id
                addlobj=AdditionalExaminer.query.filter_by(chief_id=chiefid)
                if chiefobj==None:
                    return chief_exist_error
                if addlobj==None:
                    return addl_exist_error
                for i in addlobj:
                    addllist.append(i.addl_id)

                for addl in addllist:
                    singlexam=StudentMark.query.filter_by(addl_id=addl).all()
                    
                    for i in singlexam:
                        markdic={STUDENT_REGISTER_NUMBER:i.std_reg_num,ADDITIONAL_MARK:i.addl_mark,CHIEF_MARK:i.chief_mark,
                        CHAIRMAN_MARK:i.chairman_mark,CAMP_OFFICER_MARK:i.co_mark,STUDENT_MARK:i.std_mark,DFM_NUMBER:i.dfm_num}
                        
                        marklist.append(markdic)
                
                mark_fetch.update({DATA:marklist})
                return jsonify(mark_fetch)
                
            else:
                return session_invalid
        
        except Exception as e:
           
            return error 




#=========================================================#
#                 ADD MARK BY CHAIRMAN   END              #                           
#=========================================================#

#=========================================================#
#          ADDITIONAL MARK LIST      STARTS               #                           
#=========================================================#

class AdditionalMarkList(Resource):
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                chief_chk=AdditionalExaminer.query.filter_by(chief_id=user_id,status=STATUS).all()
                if chief_chk!=[]:
                    markList=[]
                    for i in chief_chk:
                        stud_dtls=StudentMark.query.filter_by(addl_id=i.addl_id).all()
                        if stud_dtls==None:
                            return jsonify(NoMarkEntry)
                        for j in stud_dtls:
                            user_chk=User_det.query.filter_by(user_id=i.addl_id).first()
                            markDic={ADDITIONAL_ID:i.addl_id,ADDITIONAL_NAME:user_chk.name,FALSENO:j.dfm_num,
                            ADDITIONAL_MARK:j.addl_mark}
                            markList.append(markDic)
                    additionalMarkFetch.update({DATA:{RESULT_DATA:markList}})
                    return jsonify(additionalMarkFetch)
                else:
                    return jsonify(NoAdditional)
            else:
                return session_invalid

        except Exception as e:
            return jsonify(err_exception)
#=========================================================#
#          ADDITIONAL MARK LIST   ENDS                    #                           
#=========================================================#





#=========================================================#
#                 MARK FINALIZE VIEW                      #                           
#=========================================================#

class MarkFinalizeView(Resource):
    def post(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                marklist=[]
                marklist1=[]
                exam_id=requestData[EXAM_ID]
                prg_id=requestData[PROGRAM_ID]
                cou_id=requestData[COURSE_ID]
                singlexam=StudentMark.query.filter_by(cou_id=cou_id,exam_id=exam_id,prg_id=prg_id).all()
                if len(singlexam)==None:
                    return mark_no_data
                if  singlexam!=[]:
                    
                    exam=Exam.query.filter_by(exam_id=exam_id).first()
                    
                    program=ProgramDet.query.filter_by(prg_id=prg_id).first()
                    course=Course.query.filter_by(cou_id=cou_id).first()
                    
                    markdic={EXAM_ID:exam_id,EXAM_NAME:exam.exam_name,PROGRAM_ID:prg_id,PROGRAM_NAME:program.prg_name,COURSE_ID:cou_id,COURSE_NAME:course.cou_name}
                    marklist.append(markdic)
                    for i in singlexam:
                        markdic1={STUDENT_REGISTER_NUMBER:i.std_reg_num,ADDITIONAL_MARK:i.addl_mark,CHIEF_MARK:i.chief_mark,
                        CHAIRMAN_MARK:i.chairman_mark,CAMP_OFFICER_MARK:i.co_mark,STUDENT_MARK:i.std_mark,DFM_NUMBER:i.dfm_num}
                        marklist1.append(markdic1)
                    dic2={RESULT:marklist1}
                    marklist.append(dic2)
                    mark_fetch.update({DATA:marklist})
                    return jsonify(mark_fetch)
                else:
                    return jsonify(invalid_id)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(err_exception)



#=========================================================#
#                 MARK FINALIZE VIEW END                   #                           
#=========================================================
#=========================================================#
#                         #                           
#=========================================================#