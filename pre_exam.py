

from model import *
from constants import *
from flask_restful import Resource, Api
import json
from flask import Flask,jsonify,request
from datetime import datetime,time,timedelta,date
from datetime import *
from secrets import token_urlsafe
from user_mngmnt import *
import logging



#=========================================================#
#                  EXAM CENTER ADD STARTS                 #                           
#=========================================================#
class ExamCenter_Add(Resource):
    def post(self):
        try:
            data=request.get_json()
            session_token=data[SESSION_TOKEN]
            user_id=data[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if 'cen_id' in data:
                    cen_id1=data['cen_id'] 
                
                    user=Center_det.query.filter_by(cen_id=cen_id1,status=STATUS).first()
                    if user!= None:  
                        cdic={"center_id":user.cen_id,"center_name":user.cen_name,"center_code":user.cen_code,"center_address":user.cen_addr,"center_city":user.cen_city,
                        "center_location":user.cen_loc,"center_district":user.cen_dist,"center_pin":user.cen_pin,"center_phone_num":user.cen_phone_num,"center_email":user.cen_email,
                        "center_mobile":user.cen_mobile,"center_type":user.cen_type,"status":user.status}
                        centerFetch.update({DATA:cdic})
                        return  jsonify(centerFetch)
                    else:
                        return jsonify(invalid)
                elif 'center_name' in data:
                    centerlist=[]
                    name_of_center=data['center_name']
                    c_code=data['center_code']
                    address=data['address']
                    location=data['cen_loc']
                    city=data['city']
                    district=data['district']
                    pincode=data['pincode']
                    ph_no=data['ph_no']
                    email_id=data['email_id']
                    mob=data['mob']
                    cen_type=data['cen_type']
                    cen_codechk=Center_det.query.filter_by(cen_code=c_code,status=STATUS).first()
                    user=Center_det.query.filter_by(cen_name=name_of_center,status=STATUS).first()
                    user1=Center_det.query.filter_by(cen_email=email_id,status=STATUS).first()
                    if cen_codechk!=None:
                        return codeExist_exam 
                    if user1!=None:
                        return emailExist
                    elif (user == None)and(user1==None): 
                        addexam=Center_det(cen_name=name_of_center,cen_code=c_code,cen_addr=address,cen_city=city,cen_dist=district,cen_loc=location,
                        cen_pin=pincode,cen_phone_num=ph_no,cen_email=email_id,cen_mobile=mob,cen_type=cen_type,status="active")
                        db.session.add(addexam)
                        db.session.commit()
                        dic={"center_name":name_of_center,"center_code":c_code,"Address":address,"Location":location,"city":city,"district":district,
                        "pincode":pincode,"ph_no":ph_no,"email_id":email_id}
                        centerlist.append(dic)
                        centerAdd.update({DATA:centerlist})
                        return jsonify(centerAdd)
                    else:
                        return examcenterExist
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
                user=Center_det.query.filter_by(status=STATUS).all()
                list1=[]
                for i in user:
                    cdic={"center_id":i.cen_id,"center_name":i.cen_name,"center_code":i.cen_code,"center_address":i.cen_addr,"center_location":i.cen_loc,"center_city":i.cen_city,
                    "center_district":i.cen_dist,"center_pin":i.cen_pin,"center_phone_num":i.cen_phone_num,"center_email":i.cen_email,
                    "center_mobile":i.cen_mobile,"center_type":i.cen_type,"status":i.status}
                    list1.append(cdic)
                    centerAllFetch.update({DATA:list1})
                return  centerAllFetch
            else:
                return session_invalid
        except Exception as e:
            return error

    def delete(self):
        try:
            data=request.get_json()
            cen_id1=data['cen_id']
            session_token=data[SESSION_TOKEN]
            user_id=data[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                emp=[]
                art_chk=ArticleDistribution.query.filter_by(cen_id=cen_id1,art_status=STATUS).first()
                cs_chk=ChiefSuptd.query.filter_by(cen_id=cen_id1,status=STATUS).first()
                examroom_chk=ExamHall.query.filter_by(cen_id=cen_id1,hall_status=STATUS).first()
                hallalt_chk=HallAllotment.query.filter_by(cen_id=cen_id1,hall_allot_status=STATUS).first()
                invg_chk=ExamInvigilator.query.filter_by(cen_id=cen_id1,invig_status=STATUS).first()
                stud_chk=Student.query.filter_by(cen_id=cen_id1,status=STATUS).first()
                examRole_chk=ExamRole.query.filter_by(cen_id=cen_id1,exam_role_status=STATUS).first()
                camp_chk=Camp.query.filter_by(cen_id=cen_id1,camp_status=STATUS).first()
                accesskey_chk=AccessKeyGen.query.filter_by(cen_id=cen_id1,key_status=STATUS).first()
                chief_chk=ChiefExaminer.query.filter_by(camp_id=cen_id1,status=STATUS).first()
                asd_chk=AnswerScriptDistribution.query.filter_by(camp_id=cen_id1).first()
                if examroom_chk!=None or examRole_chk!=None or camp_chk!=None or accesskey_chk!=None:
                    return deleteError
                elif art_chk!=None or chief_chk!=None or asd_chk!=None:
                    return deleteError
                elif cs_chk!=None or hallalt_chk!=None or invg_chk!=None or stud_chk!=None:
                    return deleteError
                else:
                    user=Center_det.query.filter_by(cen_id=cen_id1).first()
                    if user!= None:
                        db.session.delete(user)
                        db.session.commit()
                        dic={"center_id":cen_id1,"center_name":user.cen_name}
                        emp.append(dic)
                        centerDelete.update({"DATA":emp})
                        return jsonify(centerDelete)
                    else:
                        return jsonify(invalid)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(error)


    def put(self):
        try:
            data=request.get_json()
            session_token=data[SESSION_TOKEN]
            user_id=data[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                cen_id1=data['cen_id']
                name_of_center=data['n_center']
                c_code=data['center_code']
                address=data['address']
                location=data['location']
                city=data['city']
                district=data['district']
                pincode=data['pincode']
                ph_no=data['ph_no']
                email_id=data['email_id']
                mob=data['mob']
                cen_type=data['cen_type']    
                emp1=[]
                emailchk=Center_det.query.filter(Center_det.cen_id !=cen_id1,Center_det.cen_email ==email_id)
                centerchk=Center_det.query.filter(Center_det.cen_id !=cen_id1,Center_det.cen_name ==name_of_center)
                centercode_chk=Center_det.query.filter(Center_det.cen_id !=cen_id1,Center_det.cen_code ==c_code)
                e=(emailchk.count())
                c=(centerchk.count())
                cen_codeExist=(centercode_chk.count())
                dic={"center:name":name_of_center}
                emp1.append(dic)
                if e>0:
                    return emailExist
                elif c>0:
                    return examcenterExist
                elif cen_codeExist>0:
                    return codeExist
                else:
                    user=Center_det.query.filter_by(cen_id=cen_id1,status=STATUS).first()
                    if user!=None:
                        
                        user.cen_name=name_of_center
                        user.cen_code=c_code
                        user.cen_addr=address
                        user.cen_city=city
                        user.cen_loc=location
                        user.cen_dist=district
                        user.cen_pin=pincode
                        user.cen_phone_num=ph_no
                        user.cen_email=email_id
                        user.cen_mobile=mob
                        user.cen_type=cen_type
                        db.session.commit()                       
                        centerUpdate.update({DATA:emp1})
                        return centerUpdate
                    else:
                        return invalid
            else:
                return session_invalid
        except Exception as e:
            return error
#=========================================================#
#               EXAM CENTER ADD ENDS                      #                           
#=========================================================#


#=========================================================#
#               DESIGNATION ADD ENDS                      #                           
#=========================================================#
class Designation_Add(Resource):
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                user=designation_det.query.all()
                l1=[]
                for i in user:
                    n=i.des_id
                    n1=i.des_name
                    n2=i.des_code                
                    n4=i.status
                    emp=[]
                    d={"des_id":n,"des_name":n1,"des_code":n2,"status":n4}
                    l1.append(d)
                    success.update({DATA:l1})
                return success
            else:
                return session_invalid
        except Exception as e:
            return error     

    def post(self):
        try:
            data=request.get_json()
            session_token=data[SESSION_TOKEN]
            user_id=data[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if 'des_id' in data:
                    desid=data["des_id"]
                    emp=[]
                    user=designation_det.query.filter_by(des_id=desid).first()                
                    if user!=None:
                        r={"designationid":user.des_id,"desgname":user.des_name,"desgcode":user.des_code,"desgstatus":user.status}
                    
                        success.update({DATA:r})
                        return success
                    else:
                        return invalid
                elif 'des_name' in data:
                    name=data["des_name"]
                    code=data["des_code"]
                    status="active"
                    emp1=[]
                    emp=[]
                    user1=designation_det.query.filter_by(des_name=name).first()
                    user=designation_det.query.filter_by(des_code=code).first()
                    dic={"designationname":name,"designationcode":code,"designationstatus":status}
                    emp1.append(dic)
                    if user1!=None:
                        return desExist
                    elif user!=None:
                        return codeExist_des
                    else:                    
                        r=designation_det(des_name=name,des_code=code,status=status)
                        db.session.add(r)
                        db.session.commit()
                        successDes.update({DATA:emp1})
                        return successDes
            else:
                return session_invalid
        except Exception as e:
            return error





          
        
    def put(self):
        try:
           
            content=request.get_json()
            session_token=content[SESSION_TOKEN]
            user_id=content[USER_ID]
           
            desid=content["des_id"]
            name=content["des_name"]
            code=content["des_code"]
            status="active"
            emp1=[]
            emp=[]
            sess_res=checkSessionValidity(session_token,user_id)
            if sess_res:
                des_chk=designation_det.query.filter(designation_det.des_id !=desid,designation_det.des_name==name)
                des_chk1=designation_det.query.filter(designation_det.des_id !=desid,designation_det.des_code==code)
                dnamecount=(des_chk.count())
                dcodecount=(des_chk1.count())
                if dnamecount>0:
                    return nameExist_des
                elif dcodecount>0:
                    return codeExist_des
                else:
                    chk_user=designation_det.query.filter_by(des_id=desid).first()
                    if chk_user!=None:

                        chk_user.des_name=name
                        chk_user.des_code=code
                        # chk_user.des_cat=cat
                        chk_user.status=status
                        dic={"designationid":chk_user.des_id,"designationname":chk_user.des_name,"designationcode":chk_user.des_code,"designationstatus":chk_user.status}
                        emp1.append(dic)
                        db.session.commit()
                        des_update_success.update({DATA:emp1})
                        return des_update_success
                    else:
                        return invalid
            else:
                return session_invalid
        except Exception as e:
            return error
    
    def delete(self):
        try:
            data=request.get_json()
            session_token=data[SESSION_TOKEN]
            user_id=data[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            desid=data["des_id"]
            emp=[]
            if sess_res:
                user1=User_det.query.filter_by(des_id=desid).first()
                if user1!=None:
                    return desdeleteError
                else:
                    user=designation_det.query.filter_by(des_id=desid).first()
                    if user!=None:
                        name=user.des_name
                        emp1=[]
                        db.session.delete(user)
                        db.session.commit()
                        dic={"des_id":desid,"des_name":name}
                        emp1.append(dic)
                        successDet.update({DATA:emp1})
                        return successDet                   
                    else:
                        return invalid
            else:
                return session_invalid
        except Exception as e:
            return error
#=========================================================#
#                      DESIGNATION ADD ENDS               #                           
#=========================================================#


#=========================================================#
#                      ACTION ADD STARTS                  #                           
#=========================================================#
class Action_Add(Resource):
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                actionResponse=ActionDet.query.all()
                actionList=[]
                for action in actionResponse:
                    actionDic={ACTION_CODE:action.act_code,ACTION_NAME:action.act_name}
                    actionList.append(actionDic)
                action_fetch.update({DATA:actionList})
                return jsonify(action_fetch)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(role_bad_request)
#=========================================================#
#                      ACTION ADD ENDS                    #                           
#=========================================================#


#=========================================================#
#                      ROLE ADD STARTS                    #                           
#=========================================================#
class Role_Add(Resource):    
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                roleResponse=RoleDet.query.all()
                roleList=[]
                for role in roleResponse:
                    roleDic={ROLE_ID:role.role_id,ROLE_NAME:role.role_name,ROLE_PERMISSION:role.role_permission}
                    roleList.append(roleDic)
                role_fetch.update({DATA:roleList})
                return jsonify(role_fetch)
            else:
                return session_invalid
        except Exception as e:
            return jsonify(role_bad_request)
    def post(self):
        try:
            # Check session
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                roleList=[]
                if ROLE_ID in requestData:
                    r_id=requestData[ROLE_ID]
                    singleRole=RoleDet.query.filter_by(role_id=r_id).first()
                    if singleRole !=None:
                        roleList.append({ROLE_ID:singleRole.role_id,ROLE_NAME:singleRole.role_name,ROLE_PERMISSION:singleRole.role_permission.split("|")})                  
                        role_fetch.update({DATA:roleList})
                        return jsonify(role_fetch)
                    else:
                        role_invalid_id.update({DATA:roleList})
                        return jsonify(role_invalid_id)
                elif ROLE_NAME in requestData:
                    r_name=requestData[ROLE_NAME]
                    new_role_permission=requestData[ROLE_PERMISSION]
                    new_role_name=r_name.replace(" ","")
                    new_role_name=new_role_name.lower()
                    role_exist=RoleDet.query.filter_by(role_meta=new_role_name)
                    if role_exist.count()==1:
                        return jsonify(role_exist_err)
                    new_role=RoleDet(role_name=r_name,role_permission=new_role_permission,role_meta=new_role_name,role_status=STATUS)                    
                    db.session.add(new_role)
                    db.session.commit()
                    roleList.append({ROLE_NAME:r_name,ROLE_PERMISSION:new_role_permission})
                    role_add.update({DATA:roleList})
                    return jsonify(role_add)    
            else:
                return session_invalid     
        except Exception as e:
            return jsonify(role_bad_request)
    def put(self):
        try:
            # Check session
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                roleList=[]
                r_id=requestData[ROLE_ID]
                up_r_name=requestData[ROLE_NAME]
                up_r_permission=requestData[ROLE_PERMISSION]
                new_role_name=up_r_name.replace(" ","")
                new_role_name=new_role_name.lower()
                role_exist=RoleDet.query.filter(RoleDet.role_id!=r_id , RoleDet.role_meta==new_role_name)            
                if role_exist.count()>0:
                    return jsonify(role_exist_err)
                singleRole=RoleDet.query.filter_by(role_id=r_id).first()
                if singleRole !=None:
                    singleRole.role_name=up_r_name
                    singleRole.role_permission=up_r_permission
                    singleRole.role_meta=new_role_name
                    db.session.commit()
                    roleDic={ROLE_ID:singleRole.role_id,ROLE_NAME:singleRole.role_name,ROLE_PERMISSION:singleRole.role_permission}                                
                    roleList.append(roleDic)
                    role_update.update({DATA:roleList})
                    return jsonify(role_update)
                else:
                    role_invalid_id.update({DATA:roleList})
                    return jsonify(role_invalid_id) 
            else:
                return session_invalid                                          
        except Exception as e:
            return jsonify(role_bad_request)
    def delete(self):
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                roleList=[]
                r_id=requestData[ROLE_ID]
                userRole=User_det.query.filter_by(role_id=r_id).first()
                if userRole !=None:
                    return jsonify(role_delete_fail)
                chiefRole=ChiefSuptd.query.filter_by(role_id=r_id).first()
                if chiefRole !=None:
                    return jsonify(role_delete_fail)
                singleRole=RoleDet.query.filter_by(role_id=r_id).first()
                if singleRole !=None:
                    roleDic={ROLE_ID:singleRole.role_id,ROLE_NAME:singleRole.role_name,ROLE_PERMISSION:singleRole.role_permission}                                
                    db.session.delete(singleRole)
                    db.session.commit()
                    roleList.append(roleDic)
                    role_delete.update({DATA:roleList})
                    return jsonify(role_delete)
                else:
                    role_invalid_id.update({DATA:roleList})
                    return jsonify(role_invalid_id)
            else:
                return session_invalid
            
        except Exception as e:
            return jsonify(role_bad_request)

#=========================================================#
#                      ROLE ADD ENDS                      #                           
#=========================================================#


#=========================================================#
#                      DEGREE ADD STARTS                  #                           
#=========================================================#
class Addegree(Resource):
    def post(self):
        try:
            data=request.get_json()
            session_token=data[SESSION_TOKEN]
            user_id=data[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if 'deg_id' in data:
                    degid=data["deg_id"]
                    emp=[]
                    user=degree_det.query.filter_by(deg_id=degid).first()
                    if user!=None:
                        r={"degid":user.deg_id,"name":user.deg_name,"degcode":user.deg_code,"stat":user.status}
                        success.update({DATA:r})
                        return success
                        
                    else:
                        return invalid
                elif 'deg_name' in data:
                    name=data["deg_name"]
                    status=data["deg_code"]
                    stat="active"
                    emp1=[]
                    emp=[]
                    user=degree_det.query.filter_by(deg_name=name).first()
                    user1=degree_det.query.filter_by(deg_code=status).first()
                    dict1={"degname":name,"degcode":status,"degstat":stat}
                    emp1.append(dict1)
                    if user!=None:
                        return degExist
                    elif user1!=None:
                        return codeExist
                    else:
                        r=degree_det(deg_name=name,deg_code=status,status=stat)
                        db.session.add(r)
                        db.session.commit()
                        successDeg.update({DATA:emp1})
                        return successDeg
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
                user=degree_det.query.all()
                l1=[]
                emp=[]
                for i in user:
                    n=i.deg_id
                    n1=i.deg_name
                    n2=i.deg_code
                    n3=i.status
                    d={"deg_id":n,"deg_name":n1,"deg_code":n2,"status":n3}
                    l1.append(d)
                    fetch.update({DATA:l1})
                return fetch
            else:
                return session_invalid
        except Exception as e:
            return error
    def put(self):
        try:
            content=request.get_json()
            session_token=content[SESSION_TOKEN]
            user_id=content[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            degid=content["deg_id"]
            name=content["deg_name"]
            status=content["deg_code"]
            stat="active"
            emp1=[]
            emp=[]
            if sess_res:
                deg_chk=degree_det.query.filter(degree_det.deg_id !=degid,degree_det.deg_name==name)
                deg_chk1=degree_det.query.filter(degree_det.deg_id !=degid,degree_det.deg_code==status)
                dnamecount=(deg_chk.count())
                dcodecount=(deg_chk1.count())
                if dnamecount>0:
                    return nameExist
                elif dcodecount>0:
                    return codeExist
                else:
                    chk_user=degree_det.query.filter_by(deg_id=degid).first()
                    dict1={"degid":degid,"degname":name,"degcode":status,"degstatus":stat}
                    emp1.append(dict1)
                    if chk_user!=None:
                        chk_user.deg_name=name
                        chk_user.deg_code=status
                        chk_user.status=stat
                        db.session.commit()
                        successUpd.update({DATA:emp1})
                        return successUpd               
                    else:
                        return invalid
            else:
                return session_invalid
        except Exception as e:
            return error
    def delete(self):
        try:
            data=request.get_json()
            session_token=data[SESSION_TOKEN]
            user_id=data[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id)
            degid=data["deg_id"]
            emp=[]
            emp1=[]
            if sess_res:
                degid_chk=branch_det.query.filter_by(deg_id=degid).first()
                degid_chk1=ProgramDet.query.filter_by(deg_id=degid).first()
                if degid_chk!=None:
                    return degdeleteError
                elif degid_chk1!=None:
                    return degdeleteError
                else:
                    user=degree_det.query.filter_by(deg_id=degid).first()
                    print(user)
                    if user!=None:
                        name=user.deg_name
                        db.session.delete(user)
                        db.session.commit()
                        dic={"deg_id":degid,"deg_name":name}
                        emp1.append(dic)
                        # print("ghgjuhgu")
                        delete_success.update({DATA:emp1})
                        return delete_success
                    else:
                        return invalid
            else:
                return session_invalid
        except Exception as e: 
            print(e)           
            return error
#=========================================================#
#                      DEGREE ADD ENDS                    #                           
#=========================================================#


#=========================================================#
#                      BRANCH ADD STARTS                  #                           
#=========================================================#
class Addbranch(Resource):
    def post(self):
        
        try:
            requestData=request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if BRANCH_ID in requestData:
                    brid1=requestData[BRANCH_ID]
                    user=branch_det.query.filter_by(br_id=brid1).first()
                    print(user)
                    if user!=None:
                        d={BRANCH_ID:user.br_id,BRANCH_NAME:user.br_name,BRANCH_CODE:user.br_code,DEGREE_ID:user.deg_id,BRANCH_STATUS:user.br_status}
                        br_success_single_fetch.update({DATA:d})
                        return br_success_single_fetch
                    else:
                        return br_invalid_id

                elif BRANCH_NAME in requestData:
                    empty=[]
                    brname1=requestData[BRANCH_NAME]
                    brcode1=requestData[BRANCH_CODE]
                    degid1=requestData[DEGREE_ID]
                    status1=BRANCH_STATUS
                    user=branch_det.query.filter_by(br_name=brname1,).first()
                    user1=branch_det.query.filter_by(br_code=brcode1,).first()
                    v=degree_det.query.filter_by(deg_id=degid1).first()
                    dic={BRANCH_NAME:brname1,BRANCH_CODE:brcode1,DEGREE_ID: degid1,DEGREE_NAME:v.deg_name}
                    empty.append(dic)
                    if user!=None:
                        return br_exist_name
                    elif user1!=None:
                        return br_exist_code
                    else:
                        r=branch_det(br_name=brname1,br_code=brcode1,deg_id=degid1,br_status=STATUS)
                        db.session.add(r)
                        db.session.commit()
                        br_success_add.update({DATA:empty})
                        return br_success_add
            else:
                return session_invalid
        except Exception as e:
            return br_bad_request    
            
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                user=branch_det.query.all()
                l1=[]
                for i in user:
                    v=degree_det.query.filter_by(deg_id=i.deg_id).first()
                    d={BRANCH_ID:i.br_id,BRANCH_NAME:i.br_name,BRANCH_CODE:i.br_code,DEGREE_ID:i.deg_id,DEGREE_NAME:v.deg_name,BRANCH_STATUS:i.br_status}
                    l1.append(d)
                    br_fetch.update({DATA:l1})   
                return br_fetch
            else:
                return session_invalid
        except Exception as e:
            return br_bad_request  
    



    def put(self):
        try:
            requestData=request.get_json()
            brid1=requestData[BRANCH_ID]
            brname1=requestData[BRANCH_NAME]
            brcode1=requestData[BRANCH_CODE]
            degid1=requestData[DEGREE_ID]
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                empty=[]
                brnamechk=branch_det.query.filter(branch_det.br_id !=brid1,branch_det.br_name==brname1)
                brcodechk=branch_det.query.filter(branch_det.br_id !=brid1,branch_det.br_code==brcode1)
                bnamecount=(brnamechk.count())
                bcodecount=(brcodechk.count())
                if bnamecount>0:
                    return br_exist_name
                elif bcodecount>0:
                    return br_exist_code
                else:
                    chk_user=branch_det.query.filter_by(br_id=brid1).first()
                    if chk_user!=None:
                        print(chk_user)
                        chk_user.br_name=brname1
                        chk_user.br_code=brcode1
                        print(chk_user.deg_id)
                        chk_user.deg_id=degid1
                        print(chk_user.deg_id)
                        db.session.commit()
                        dic1={BRANCH_ID:brid1,BRANCH_NAME:chk_user.br_name,BRANCH_CODE:chk_user.br_code,DEGREE_ID:chk_user.deg_id}
                        empty.append(dic1)
                        br_success_edit.update({DATA:empty})
                        return br_success_edit
                    else:
                        return br_invalid_id
            else:
                 return session_invalid           
        except Exception as e:
            return br_bad_request



    def delete(self):
        try:
            data=request.get_json()
            brid1=data[BRANCH_ID]
            session_token=data[SESSION_TOKEN]
            user_id=data[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                empty=[]
                brid_chk=Section_det.query.filter_by(br_id=brid1).first()
                if brid_chk!=None:
                    return brdeleteError
                else:
                    user=branch_det.query.filter_by(br_id=brid1).first() 
                    dic={BRANCH_ID:user.br_id,BRANCH_NAME:user.br_name,BRANCH_CODE:user.br_code,BRANCH_STATUS:user.br_status}
                    if user!=None:
                        db.session.delete(user)
                        db.session.commit()
                        empty.append(dic)
                        br_success_delete.update({DATA:empty})
                        return br_success_delete
                    else:
                        return br_invalid_id
            else:
                session_invalid  
        except Exception as e:
            return br_bad_request    
#=========================================================#
#                      BRANCH ADD ENDS                    #                           
#=========================================================#


#=========================================================#
#                      SECTION ADD STARTS                 #                           
#=========================================================#
class Addsection(Resource):
    def post(self):
        try:
            data=request.get_json()
            session_token=data[SESSION_TOKEN]
            user_id=data[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if SECTION_ID in data:
                    secid1=data[SECTION_ID]
                    user=Section_det.query.filter_by(sec_id=secid1).first()                
                    if user!=None:
                        d={SECTION_ID:user.sec_id,SECTION_NAME:user.sec_name,BRANCH_ID:user.br_id,SECTION_CODE:user.sec_code,STATUS:user.sec_status}
                        sec_success_single_fetch.update({DATA:d})
                        return sec_success_single_fetch
                    else:
                        return sec_invalid_id
            
                elif SECTION_NAME in data:                    
                    empty=[]
                    secname1=data[SECTION_NAME]
                    brid1=data[BRANCH_ID]
                    seccode1=data[SECTION_CODE]
                    status=STATUS
                    user=Section_det.query.filter_by(sec_name=secname1).first()
                    user1=Section_det.query.filter_by(sec_code=seccode1,).first()
                    v=branch_det.query.filter_by(br_id=brid1).first()              
                    dic1={SECTION_NAME:secname1,SECTION_CODE:seccode1,BRANCH_ID:brid1,BRANCH_NAME:v.br_name}
                    empty.append(dic1)
                    if user!=None:
                        return sec_exist_name
                    elif user1!=None:
                        return sec_exist_code
                    else:
                        r=Section_det(sec_name=secname1,br_id= brid1,sec_code=seccode1,sec_status=STATUS)
                        db.session.add(r)
                        db.session.commit()
                        sec_success_add.update({DATA:empty})
                        return sec_success_add
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
                user=Section_det.query.all()
                l1=[]
           
                for i in user:
                    v=branch_det.query.filter_by(br_id=i.br_id).first()

                    d={SECTION_ID:i.sec_id,SECTION_NAME:i.sec_name,SECTION_CODE:i.sec_code,BRANCH_ID:i.br_id,BRANCH_NAME:v.br_name,"section_status":i.sec_status}
                    l1.append(d)
                    sec_fetch.update({DATA:l1})
                return sec_fetch  
            else:
                session_invalid        
        except Exception as e:
            print(e)            
            return sec_bad_request    
    def put(self):
        try:     
           
            content=request.get_json()
            secid1=content[SECTION_ID]
            empty=[]
           
            secname1=content[SECTION_NAME]
            seccode1=content[SECTION_CODE]
           
            brid=content[BRANCH_ID]
            session_token=content[SESSION_TOKEN]
            user_id=content[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:          
            

                secnamechk=Section_det.query.filter(Section_det.sec_id !=secid1,Section_det.sec_name==secname1)
                seccodechk=Section_det.query.filter(Section_det.sec_id !=secid1,Section_det.sec_code==seccode1)
                snamecount=(secnamechk.count())
                scodecount=(seccodechk.count())
           
                if snamecount>0:
                    return sec_exist_name
                elif scodecount>0:
                    return sec_exist_code
                else:
                    chk_user=Section_det.query.filter_by(sec_id=secid1).first()
                    print(chk_user)
            

                    if chk_user!=None:
                   
                        chk_user.sec_name=secname1
                        chk_user.sec_code=seccode1
                   
                        chk_user.br_id=brid
                        db.session.commit()
                    
                        dic1={SECTION_ID:chk_user.sec_id,SECTION_NAME:chk_user.sec_name,SECTION_CODE:chk_user.sec_code,STATUS:chk_user.sec_status}
                        empty.append(dic1)
                   
                
                        sec_success_edit.update({DATA:empty})
                        return sec_success_edit
                    else:
                        return sec_invalid_id
            else:
                session_invalid
            
        
        except Exception as e:
            return sec_bad_request 

    def delete(self):
        try:
            data=request.get_json()
            secid1=data[SECTION_ID]
            empty=[]
          
            session_token=data[SESSION_TOKEN]
            user_id=data[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
            
                user=Section_det.query.filter_by(sec_id=secid1).first() 
                dic={SECTION_ID:user.sec_id,SECTION_NAME:user.sec_name,SECTION_CODE:user.sec_code,STATUS:user.sec_status}
                if user!=None:

                
                    db.session.delete(user)
                    db.session.commit()
                    empty.append(dic)
                    sec_success_delete.update({DATA:empty})
                    return sec_success_delete
                else:
                    return sec_invalid_id
            else:
                session_invalid
        
        
        except Exception as e:
            return sec_bad_request   
#=========================================================#
#                      SECTION ADD ENDS                   #                           
#=========================================================#

#=========================================================#
#                      PROGRAM ADD STARTS                 #                           
#=========================================================#



class ProgramDetails(Resource):
    def post(self):
        try:
            data = request.get_json()
            session_token = data[SESSION_TOKEN]
            user_id = data[USER_ID]
            sess_res = checkSessionValidity(session_token,  user_id)
            if(not sess_res):
                return session_invalid
           
            if PRG_ID in data:
                prg_id = data[PRG_ID]
                if sess_res:
                    user = ProgramDet.query.filter_by(prg_id=prg_id).first()
                    if user != None:
                        d = {PRG_ID: user.prg_id, PRG_NAME: user.prg_name,
                            PRG_CODE: user.prg_code, DEG_ID: user.deg_id,
                            PRG_STATUS: user.status}
                        prg_sucss_post_id[DATA] = d

                        return prg_sucss_post_id

                    else:
                        prg_err_post_id[DATA] =[]
                        return prg_err_post_id

            elif PRG_NAME in data:
                if sess_res:
                    empty = []
                    emp = []
                    prg_name1 = data[PRG_NAME]
                    prg_code1 = data[PRG_CODE]
                    deg_id = data[DEG_ID]
                    prg_nm=prg_name1.replace(" ","")
                    prg_nm=prg_nm.lower()
                    program_exist=ProgramDet.query.filter_by(prg_meta=prg_nm)
                    if program_exist.count()==1:
                        return jsonify(Prg_exist_err)                    
                    
                    program_code_exist=ProgramDet.query.filter_by(prg_code=prg_code1 )
                    if program_code_exist.count()>0:
                        return jsonify(prg_code_exist_err)

                    sm1 = ProgramDet(prg_name=prg_name1,prg_code=prg_code1, deg_id=deg_id,status=STATUS,prg_meta=prg_nm)                        
                    db.session.add(sm1)
                    db.session.commit()
                    return jsonify(prg_sucss_post)               
        except Exception as e:      
            return err_exception
            

    def get(self):
        try:
            session_token = request.headers[SESSION_TOKEN]
            user_id = request.headers[USER_ID]
            sess_res = checkSessionValidity(session_token,  user_id)
            if sess_res:
                prgData=db.session.query(ProgramDet,degree_det).with_entities(ProgramDet.prg_id.label(PRG_ID),ProgramDet.prg_name.label(PRG_NAME),ProgramDet.prg_code.label(PRG_CODE),degree_det.deg_name.label(DEG_NAME)).filter(ProgramDet.deg_id==degree_det.deg_id).order_by(ProgramDet.prg_name).all()
                prgRes=list(map(lambda n:n._asdict(),prgData))
                prg_sucss_get[DATA] = prgRes
                return prg_sucss_get 
            else:
                return jsonify(session_invalid)           
        except Exception as e:           
            return err_exception
           

    def put(self):
        try:
            content = request.get_json()
            session_token = content[SESSION_TOKEN]
            user_id = content[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id)
            if sess_res:
                empty = []
                emp = []
                
                prg_id = content[PRG_ID]
                prg_name = content[PRG_NAME]
                
                prg_code = content[PRG_CODE]
                deg_id = content[DEG_ID]
                prg_nm=prg_name.replace(" ","")
                prg_nm=prg_nm.lower()
                program_exist=ProgramDet.query.filter(ProgramDet.prg_meta==prg_nm,ProgramDet.prg_id!=prg_id)
                program_code_exist=ProgramDet.query.filter(ProgramDet.prg_code==prg_code,ProgramDet.prg_id!=prg_id)
                if program_exist.count()==1:
                    return jsonify(Prg_exist_err)
                
                elif program_code_exist.count()>0:
                    return jsonify(prg_code_exist_err)

                chk_user1 = degree_det.query.filter_by(deg_id=deg_id).first()
                chk_user =ProgramDet.query.filter_by(prg_id=prg_id).first()
                if chk_user1 != None and chk_user != None:
                    chk_user.prg_name = prg_name
                    chk_user.prg_code = prg_code
                    chk_user.deg_id = deg_id
                
                    db.session.commit()
                    d = {PRG_ID: chk_user.prg_id, PRG_NAME: chk_user.prg_name,PRG_CODE: chk_user.prg_code, DEG_ID: chk_user.deg_id}
                    empty.append(d)
                    return prg_sucss_put
                else:
                    return prg_err_put
            else:
                 return jsonify(session_invalid)   

        except Exception as e:        
            return err_exception
           

    def delete(self):
        try:
            empty = []
            emp = []
            data = request.get_json()            
            session_token = data[SESSION_TOKEN]
            user_id = data[USER_ID]
            prg_id = data[PRG_ID]
            user = ProgramDet.query.filter_by(prg_id=prg_id).first()
            dic = {PRG_ID: user.prg_id, PRG_NAME: user.prg_name,PRG_CODE: user.prg_code, DEG_ID: user.deg_id, PRG_STATUS: user.status}
            if user != None:
                db.session.delete(user)
                db.session.commit()
                empty.append(dic)
                prg_sucss_delete[DATA] = dic
                return prg_sucss_delete
            else:
                return prg_err_delete
        except Exception as e:            
            return err_exception

#=========================================================#
#                      PROGRAM ADD ENDS                   #                           
#=========================================================#



#=========================================================#
#                      USER ADD STARTS                    #                           
#=========================================================#
class AddUser(Resource):
    def post(self):
        try:
            data=request.get_json()
            session_token=data[SESSION_TOKEN]
            user_id=data[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                if 'u_id' in data:
                    u_id=data["u_id"]
                    user=User_det.query.filter_by(user_id=u_id,status=STATUS).first()
                    if user!=None:
                        if user.cen_id == -1:
                            userdic={}
                            des=designation_det.query.filter_by(des_id=user.des_id,status=STATUS).first()
                            role=RoleDet.query.filter_by(role_id=user.role_id,role_status=STATUS).first()
                            brmap=BranchMapping.query.filter_by(emp_id=user.emp_id,status=STATUS).first()
                            userdic={"user_id":user.user_id,"emp_id":user.emp_id,"user_name":user.name,"user_address":user.usr_add,"user_location":user.usr_loc,"user_city":user.usr_city,
                            "user_pin":user.usr_pin,"user_mobile":user.usr_mobile,"user_phone":user.usr_phone,"user_email":user.usr_email,"user_cat1":user.usr_cat1,
                            "user_cat2":user.usr_cat2,"user_cat3":user.usr_cat3,"role_id":user.role_id,"des_id":user.des_id,"branch_id":brmap.br_id,
                            "section_id":brmap.sec_id,"role_name":role.role_name,"designation_name":des.des_name}
                            
                            userSingleFetch.update({DATA:userdic})
                        
                            return  userSingleFetch
                        else:
                            center_chk=Center_det.query.filter_by(cen_id=user.cen_id,status=STATUS).first()
                            des=designation_det.query.filter_by(des_id=user.des_id,status=STATUS).first()
                            role=RoleDet.query.filter_by(role_id=user.role_id,role_status=STATUS).first()
                            brmap=BranchMapping.query.filter_by(emp_id=user.emp_id,status=STATUS).first()

                            userdic={"user_id":user.user_id,"emp_id":user.emp_id,"cen_district":center_chk.cen_dist,"cen_id":user.cen_id,"user_name":user.name,"user_address":user.usr_add,"user_location":user.usr_loc,"user_city":user.usr_city,
                            "user_pin":user.usr_pin,"user_mobile":user.usr_mobile,"user_phone":user.usr_phone,"user_email":user.usr_email,"user_cat1":user.usr_cat1,
                            "user_cat2":user.usr_cat2,"user_cat3":user.usr_cat3,"role_id":user.role_id,"des_id":user.des_id,"branch_id":brmap.br_id,
                            "section_id":brmap.sec_id,"role_name":role.role_name,"designation_name":des.des_name}
                            userSingleFetch.update({DATA:userdic})
                            
                            return  userSingleFetch
                    else:
                        return invalid
                elif 'emp_id' in data:

                    emp_id=data["emp_id"]
                    u_name=data["user_name"]
                    cen_id=data["cen_id"]
                    u_add=data["user_address"]
                    u_loc=data["user_location"]
                    u_pin=data["user_pin"]
                    u_city=data["user_city"]
                    u_mobile=data["user_mobile"]
                    u_phone=data["user_phone"]
                    u_email=data["user_email"]
                    u_uname=data["user_username"]
                    u_pswd=data["user_password"]
                    role_id=data["role_id"]
                    des_id=data["des_id"]
                    u_cat1=data["user_cat1"]
                    u_cat2=data["user_cat2"]
                    u_cat3=data["user_cat3"]
                    b_id=data["branch_id"]
                    s_id=data["section_id"]
                    status="active"
                
                    timestamp1 = datetime.now()
                    useremp=User_det.query.filter_by(emp_id=emp_id,status=STATUS).first()
                    if useremp!=None:
                        return empidExist
                    else:
                        user=User_det.query.filter_by(usr_email=u_email,status=STATUS).first()
                        userlist=[]
                        if user ==None:
                            adduser=User_det(emp_id=emp_id,name=u_name,usr_add=u_add,usr_loc=u_loc,usr_pin=u_pin,usr_city=u_city,usr_mobile=u_mobile,
                            usr_phone=u_phone,usr_email=u_email,usr_uname=u_uname,usr_pswd=u_pswd,role_id=role_id,des_id=des_id,cen_id=cen_id,
                            usr_cat1=u_cat1,usr_cat2=u_cat2,usr_cat3=u_cat3,status=status)
                            db.session.add(adduser)
                            db.session.commit()
                            userdic={"name":u_name}
                            userlist.append(userdic)
                            branchmap=BranchMapping(emp_id=emp_id,br_id=b_id,sec_id=s_id,joining_date=timestamp1,rel_date="",status="active")
                            db.session.add(branchmap)
                            db.session.commit()
                            adduserSuccess.update({DATA:userlist})
                            return adduserSuccess

                        else:
                            return emailExist
            else:
                return session_invalid
        except Exception as e:
            return error


    def put(self):
        try:
            data=request.get_json()
            session_token=data[SESSION_TOKEN]
            user_id=data[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                u_id=data['u_id']
                emp_id=data['emp_id']
                sec_id=data['section_id']
                br_id=data['branch_id']
                u_name=data["user_name"]
                u_pin=data["user_pin"]
                cen_id=data["cen_id"]
                u_add=data["user_address"]
                u_loc=data["user_location"]
                u_city=data["user_city"]
                u_mobile=data["user_mobile"]
                u_phone=data["user_phone"]
                email_id=data["user_email"]
                role_id=data["role_id"]
                des_id=data["des_id"]
                u_cat1=data["user_cat1"]
                u_cat2=data["user_cat2"]
                u_cat3=data["user_cat3"]                
                timestamp1 = datetime.now()
                user=User_det.query.filter_by(user_id=u_id,status=STATUS).first()
                email_chk=User_det.query.filter(User_det.user_id !=u_id,User_det.usr_email ==email_id,User_det.status==STATUS)
                email_count=email_chk.count()
                emp_chk=User_det.query.filter(User_det.user_id !=u_id,User_det.emp_id ==emp_id,User_det.status==STATUS)
                emp_count=emp_chk.count()
                if user != None:
                    dic={"user_id":u_id,"name":u_name}
                    userUpdate.update({DATA:dic})
                    brmap=BranchMapping.query.filter_by(emp_id=user.emp_id,status=STATUS).first()
                    if email_count!=0:
                        return emailExist
                    if emp_count!=0:
                        return empidExist

                    if ((brmap.br_id)==br_id):
                        user.name=u_name
                        user.emp_id=emp_id
                        user.usr_add=u_add
                        user.cen_id=cen_id
                        user.usr_loc=u_loc
                        user.usr_pin=u_pin
                        user.usr_city=u_city
                        user.usr_mobile=u_mobile
                        user.usr_phone=u_phone
                        user.usr_email=email_id
                        user.usr_uname=email_id
                        user.des_id=des_id
                        user.role_id=role_id
                        user.usr_cat1=u_cat1
                        user.usr_cat2=u_cat2
                        user.usr_cat3=u_cat3
                        brmap.emp_id=emp_id
                        db.session.commit()
                        return userUpdate
                    else:
                        user.name=u_name
                        user.emp_id=emp_id
                        user.usr_add=u_add
                        user.cen_id=cen_id
                        user.usr_loc=u_loc
                        user.usr_pin=u_pin
                        user.usr_city=u_city
                        user.usr_mobile=u_mobile
                        user.usr_phone=u_phone
                        user.usr_email=email_id
                        user.usr_uname=email_id
                        user.des_id=des_id
                        user.role_id=role_id
                        user.usr_cat1=u_cat1
                        user.usr_cat2=u_cat2
                        user.usr_cat3=u_cat3
                        edirbr=BranchMapping(emp_id=brmap.emp_id,sec_id=sec_id,br_id=br_id,joining_date=brmap.joining_date,rel_date=timestamp1,status="active")
                        db.session.add(edirbr)
                        db.session.commit()
                        userAdd.update({DATA:dic})
                        return userAdd
                else:
                    return invalid
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
                #user=User_det.query.filter_by(status=STATUS).all()
                #user=db.session.query(User_det,designation_det,RoleDet).with_entities(User_det.user_id,User_det.name,User_det.usr_add,User_det.usr_mobile,RoleDet.role_name,designation_det.des_name).filter(designation_det.des_id==User_det.des_id,RoleDet.role_id==User_det.role_id,User_det.status==STATUS,designation_det.status==STATUS,RoleDet.role_status==STATUS).all()
                user=db.session.query(User_det,designation_det,RoleDet,ChiefSuptd).with_entities(User_det.user_id.label("user_id"),User_det.name.label("user_name"),User_det.usr_add.label("user_address"),User_det.usr_mobile.label("user_mobile"),RoleDet.role_name.label("role_name"),designation_det.des_name.label("designation_name")).filter(designation_det.des_id==User_det.des_id,RoleDet.role_id==User_det.role_id,User_det.status==STATUS,designation_det.status==STATUS,RoleDet.role_status==STATUS).order_by(User_det.name).all()
                #userFetch=[u._asdict() for u in user]
                userData=list(map(lambda n:n._asdict(),user))                
               # udict=user[0]._asdict()
                #return userfetch
                #list1=[]
                #for i in user:
                  

                   # des=designation_det.query.filter_by(des_id=i.des_id,status=STATUS).first()
                    #role=RoleDet.query.filter_by(role_id=i.role_id,role_status=STATUS).first()
                
                    # brmap=BranchMapping.query.filter_by(emp_id=i.emp_id,status=STATUS).first()
                    # branch_chk=branch_det.query.filter_by(br_id=brmap.br_id,br_status=STATUS).first()
                    # sec_chk=Section_det.query.filter_by(sec_id=brmap.sec_id,sec_status=STATUS).first()
                    
                    # dic={"user_name":i.name,"user_address":i.usr_add,
                    # "user_mobile":i.usr_mobile,"role_name":role.role_name,"designation_name":des.des_name,
                    # }

                #      dic={"user_id":i.user_id,"user_name":i.name,"user_address":i.usr_add,
                #      "user_mobile":i.usr_mobile,"role_name":i.role_name,"designation_name":i.des_name,
                #      }


                #      list1.append(dic)
                userFetch.update({DATA:userData})                
                return  userFetch
            else:
                return session_invalid
        except Exception as e:
            return error

    
    def delete(self):
        try:
            data=request.get_json()
            session_token=data[SESSION_TOKEN]
            user_id=data[USER_ID]
            u_id=data['u_id']
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:                      
                dellist=[]
                user=User_det.query.filter_by(user_id=u_id,status=STATUS).first()
                chief_chk=ChiefSuptd.query.filter_by(user_id=u_id,status=STATUS).first()
                exam_chk=ExamRole.query.filter_by(user_id=u_id,exam_role_status=STATUS).first()
                invig_chk=ExamInvigilator.query.filter_by(user_id=u_id,invig_status=STATUS).first()
                session_chk=Session.query.filter_by(user_id=u_id,status=STATUS).first()
                chiefexaminer_chk=ChiefExaminer.query.filter_by(chief_id=u_id,status=STATUS).first()
                addexaminer_chk=AdditionalExaminer.query.filter_by(addl_id=u_id,status=STATUS).first()
                addexaminerchief_chk=AdditionalExaminer.query.filter_by(chief_id=u_id,status=STATUS).first()
                if user!= None:
                    if chief_chk==None and exam_chk==None and invig_chk==None and session_chk==None and chiefexaminer_chk==None and addexaminer_chk==None and addexaminerchief_chk==None:

                        user.status=INACTIVE
                        db.session.commit()
                        dic={"user_id":u_id,"name":user.name}
                        userdeleteSuccess.update({DATA:dic})
                        dellist.append(dic)
                        userdeleteSuccess.update({DATA:dellist})
                        return userdeleteSuccess
                    else:
                        return userdeleteError
                    
                else:
                    return invalid
            else:
                return session_invalid
        except Exception as e:      
            return error
#=========================================================#
#                      USER ADD ENDS                      #                           
#=========================================================#


#=========================================================#
#              CHIEF SUPERINTENDENT ADD STARTS            #                           
#=========================================================#
class ChiefSuperintendent(Resource):
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]            
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:                
                user = ChiefSuptd.query.filter_by(pgm_id='-1',status=STATUS).all()
                list1 = []
                for i in user:
                    singleUser=User_det.query.filter_by(user_id=i.user_id).first()
                    singleExam=Exam.query.filter_by(exam_id=i.exam_id).first() 
                    singleCenter=Center_det.query.filter_by(cen_id=i.cen_id).first()              
                    cdic={"exam_id":i.exam_id,"exam_name":singleExam.exam_name,"cs_id":i.user_id,"cs_name":singleUser.name,"cen_id":i.cen_id,"cen_name":singleCenter.cen_name,"status":i.status,"role_id":i.role_id,"exp_date":i.exp_date}
                    list1.append(cdic)
                success.update({'data':list1})
                return jsonify(success)
            else:
                return session_invalid
        except Exception as e:
            return jsonify(msg_400)

    def post(self):
        try:
            data=request.get_json()
            session_token=data[SESSION_TOKEN]
            user_id=data[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                empdata=[]
                if 'exam_id' in data and 'cen_id' in data and 'cs_id' in data:
                    cen_id1=data['cen_id']
                    exam_id1=data['exam_id']
                    cs_id1=data['cs_id']
                    # centerCheck = Center_det.query.filter_by(cen_id=cen_id1).all()
                    examCheck = Exam.query.filter_by(exam_id=exam_id1).all()
                    userCheck = User_det.query.filter_by(user_id=cs_id1,cen_id=cen_id1).all()
                    # print(examCheck,userCheck)
                    if  examCheck != [] and userCheck != []:
        
                        user = ChiefSuptd.query.filter_by(user_id=cs_id1).all()
                        # print(user)
                        if user == []:
                            # print(user)
                            cen_id1=data['cen_id'] 
                            # print(cen_id1)
                            exam_id1=data['exam_id']
                            # print(exam_id1)
                            cs_id1=data['cs_id']
                            # print(cs_id1)
                            userCheck = User_det.query.filter_by(user_id=cs_id1,cen_id=cen_id1).first()
                            examCheck = Exam.query.filter_by(exam_id=exam_id1).first()
                            role_post = RoleDet.query.filter_by(role_meta="chiefsuperintendent").first()
                            # print(role_post)
                            exam_exp_date = examCheck.end_date
                            # print(type(exam_exp_date))
                        
                            str_exp_date = str(exam_exp_date)
                            strip_date =datetime.strptime(str_exp_date, "%Y-%m-%d").date()
                            # print(strip_date)
                            exp_date = strip_date+ timedelta(days=7)
                            date_exp = exp_date.strftime("%Y-%m-%d")                            
                            addData=ChiefSuptd(exam_id=examCheck.exam_id,user_id=userCheck.user_id,cen_id=userCheck.cen_id,status="active",role_id=role_post.role_id,exp_date=date_exp,pgm_id="-1")
                            userCheck.role_id = role_post.role_id
                            # print(addData)
                            db.session.add(addData)
                            # print("saved")
                            db.session.commit()
                            # print("database")

                            return jsonify(success1)
                        else:
                            return jsonify(already_exists)
                    else:
                        return jsonify(invalid_id)
                elif 'exam_id' in data:
                    e_id=data['exam_id']
                    user = ChiefSuptd.query.filter_by(pgm_id='-1',exam_id=e_id).all()
                    list1 = []
                    if user==[]:
                        return jsonify(cs_not_exist)
                    for i in user:
                        singleUser=User_det.query.filter_by(user_id=i.user_id).first()
                        singleExam=Exam.query.filter_by(exam_id=i.exam_id).first() 
                        singleCenter=Center_det.query.filter_by(cen_id=i.cen_id).first()              
                        cdic={"exam_id":i.exam_id,"exam_name":singleExam.exam_name,"cs_id":i.user_id,"cs_name":singleUser.name,"cen_id":i.cen_id,"cen_name":singleCenter.cen_name}
                        list1.append(cdic)
                    success.update({'data':list1})
                    return jsonify(success)

            else:
                return session_invalid
        

        except Exception as e:
            return jsonify(msg_400)

    def delete(self):
        try:
            data=request.get_json()
            session_token=data[SESSION_TOKEN]
            user_id=data[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                empdata=[]
                if 'cs_id' in data:
                    cs_id1=data['cs_id']
                    user_exist=User_det.query.filter_by(user_id=cs_id1,status=STATUS).first()
                    single_teach=RoleDet.query.filter_by(role_meta=TEACHER).first()
                    checkId = ChiefSuptd.query.filter_by(user_id=cs_id1,pgm_id="-1").first()
                    if checkId == None:
                        return jsonify(no_exist)
                    else:
                        cdic={"exam_id":checkId.exam_id,"user_id":checkId.user_id,"cen_id":checkId.cen_id,"status":checkId.status,"role_id":checkId.role_id,"exp_date":checkId.exp_date}
                        empdata.append(cdic)
                        # db.session.delete(checkId)
                        checkId.status=INACTIVE
                        # checkId
                        user_exist.role_id=single_teach.role_id
                        db.session.commit()
                        deleted.update({'data':empdata})
                        return jsonify(deleted)
            else:
                return session_invalid


        except Exception as e:
            return jsonify(msg_400)
#=========================================================#
#              CHIEF SUPERINTENDENT ADD ENDS              #                           
#=========================================================#


#=========================================================#
#      CHIEF SUPERINTENDENT ORDER GENERATION STARTS       #                           
#=========================================================#
def emp_list_convert(emp_list):

    emp_str = '|'.join(str(e)
    for e in emp_list)
    return emp_str

 


class CSOrderGeneration(Resource):
    def post(self):
        try:
            data=request.get_json()
            session_token=data[SESSION_TOKEN]
            user_id=data[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            
            if sess_res:
                list1 = []
                if ORDER_NUMBER in data and ORDER_DATE in data and EXAM_ID in data and EMP_ID_LIST in data:
                    order_num1 = data[ORDER_NUMBER]
                    order_date1 = data[ORDER_DATE]
                    exam_id1 = data[EXAM_ID]
                    emp_list = data[EMP_ID_LIST]
                    empdata=[]
                    order=OrderGeneration.query.filter_by(exam_id=exam_id1).first()                    
                    if order!=None:
                        return jsonify(exam_exist)
                    exam=ChiefSuptd.query.filter_by(exam_id=exam_id1,pgm_id=-1).first()
                    center=exam.cen_id
                    center_table = Center_det.query.filter_by(cen_id=center).first()
                    for i in emp_list:
                        user_table = User_det.query.filter_by(user_id=i).first()
                        empname=user_table.name
                        exam_table = Exam.query.filter_by(exam_id=exam_id1).first()
                        examstartdate=exam_table.start_date
                        examstartdate1=examstartdate.strftime("%Y-%m-%d")
                        examenddate=exam_table.end_date
                        examenddate1=examenddate.strftime("%Y-%m-%d")
                        emplist1=emp_list_convert(emp_list)
                        user_dic = {USER_NAME:user_table.name,EMPLOYEE_ID:user_table.emp_id,EMPLOYEE_NAME:empname,EMAIL_ID:user_table.usr_email,CENTRE_ID:user_table.cen_id,CENTER_NAME:center_table.cen_name,
                        EXAM_ID:exam_id1,EXAM_NAME:exam_table.exam_name,EXAM_START_DATE:examstartdate1,EXAM_END_DATE:examenddate1,EMP_ID_LIST:emplist1,ORDER_NUMBER:order_num1,ORDER_DATE:order_date1}
                        empdata.append(user_dic)
                    data1 = OrderGeneration(order_number=order_num1,order_date=order_date1,emp_id_list=emplist1,status=STATUS,exam_id=exam_id1)
                    db.session.add(data1)
                    db.session.commit()
                    success1.update({DATA:empdata})
                    return jsonify (success1)
                    
                elif EXAM_ID in data:
                    exam_id1= data[EXAM_ID]
                    cs_data = ChiefSuptd.query.filter_by(exam_id=exam_id1,pgm_id=PRGID).all()
                    if cs_data != None:
                        for i in cs_data:
                            user_name_id = i.user_id
                            user_name = User_det.query.filter_by(user_id=user_name_id).first()
                            dict1 = {CS_NAME:user_name.name,CS_ID:user_name_id,EXAM_id:i.exam_id}
                            list1.append(dict1)
                            success.update({DATA:list1})
                        return jsonify(success)
                    else:
                        return jsonify(no_exist)
            else:    
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(msg_400)


    
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id)
            
            if sess_res:
                csResponse=OrderGeneration.query.all()               
                resList=[]
                for i in csResponse:
                    emplist=i.emp_id_list.split ('|')
                    list1=[]
                    for empId in emplist:
                        user_table = User_det.query.filter_by(user_id=empId).first()
                        if user_table.cen_id!=-1:
                            empname=user_table.name
                            center_table =Center_det.query.filter_by(cen_id=user_table.cen_id).first()
                            newCslist={USER_ID:user_table.user_id,EMPLOYEE_NAME:empname,EMPLOYEE_ID:user_table.emp_id,
                            CENTER_ID:user_table.cen_id,CENTER_NAME:center_table.cen_name,ORDER_ID:i.order_id,
                            ORDER_NUMBER:i.order_number,ORDER_DATE:i.order_date}
                        list1.append(newCslist)                
                    csFetch.update({DATA:list1}) 
                return jsonify(csFetch)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            
            return jsonify(br_bad_request)




#=========================================================#
#      CHIEF SUPERINTENDENT ORDER GENERATION ENDS         #                           
#=========================================================#


#=========================================================#
#                INVIGILATOR ADD STARTS                   #                           
#=========================================================#
class TeacherList(Resource):
    def get(self):
        try: 
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            prg_id=request.headers[PRG_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                teacherlist=[]
                singleRole=RoleDet.query.filter_by(role_meta=TEACHER).first()
                roleid=singleRole.role_id
                singleprogram=ProgramDet.query.filter_by(prg_id=prg_id).first()
                degreeid=singleprogram.deg_id
                singlebranch=branch_det.query.filter_by(deg_id=degreeid).first()                
                branchid=singlebranch.br_id
                br_mapping=BranchMapping.query.filter_by(br_id=branchid).all()
                teacherList=User_det.query.filter_by(role_id=roleid,usr_cat1=TEACH_CAT,status=STATUS).all()
                for singleTeacher in teacherList:
                    for singleUser in br_mapping:
                        if singleTeacher.emp_id==singleUser.emp_id:                    
                            teacherdic={TEACHER_ID:singleTeacher.user_id,TEACHER_NAME:singleTeacher.name}
                            teacherlist.append(teacherdic)
                br_fetch.update({DATA:teacherlist})   
                return br_fetch
            else:
                return session_invalid
        except Exception as e:           
            return jsonify(br_bad_request) 

    def post(self):
        try:            
            requestData=request.get_json()                        
            session_token=requestData[SESSION_TOKEN]
            u_id=requestData[USER_ID]
            sessionCheck=checkSessionValidity(session_token,u_id)
            if sessionCheck:
                if CENTER_ID in requestData:
                    c_id=requestData[CENTER_ID]
                    resultList=[]
                    # teacherList=User_det.query.filter(User_det.cen_id==c_id,User_det.usr_cat1==TEACH_CAT,User_det.status==STATUS,User_det.role_id!=2,User_det.role_id!=22)
                    teacherList=User_det.query.filter(User_det.cen_id==c_id,User_det.usr_cat1==TEACH_CAT,User_det.status==STATUS,User_det.role_id==6)
                    if teacherList.count()>0:
                        for teacher in teacherList:
                            teachDic={TEACHER_ID:teacher.user_id,TEACHER_NAME:teacher.name}
                            resultList.append(teachDic)
                        teacher_fetch.update({DATA:resultList})
                        return jsonify(teacher_fetch)
                    else:
                        return jsonify(teacher_fetch_empty)
                else:
                    resultList=[]
                    teacherList=User_det.query.filter_by(usr_cat1=TEACH_CAT,status=STATUS)
                    if teacherList.count()>0:
                        for teacher in teacherList:
                            teachDic={"teacher_id":teacher.user_id,"teacher_name":teacher.name}
                            resultList.append(teachDic)
                        teacher_fetch.update({DATA:resultList})
                    return jsonify(teacher_fetch)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(msg_400)

    


class AddInvigilator(Resource):
    # def get(self):
    #     try:
    #         user=ExamInvigilator.query.all()
    #         list1=[]            
    #         for i in user:
    #             cdic={"exam_id":i.exam_id,"inveglator_id":i.inveglator_id,"cen_id":i.cen_id,"status":i.status}
    #             list1.append(cdic)
    #         success.update({'data':list1})
    #         return jsonify(success)

    #     except Exception as e:
    #         return jsonify(msg_400)

    def post(self):
        try:
            data=request.get_json()
            session_token=data[SESSION_TOKEN]
            u_id=data[USER_ID]
            empdata=[]
            chkSession=checkSessionValidity(session_token,u_id)
            if chkSession:

                if 'cen_id' in data and 'exam_id' in data and 'inv_list' in data:
                    invg_list=data['inv_list']
                    cen_id1=data['cen_id'] 
                    exam_id1=data['exam_id']
                    for i in invg_list:
                        chk_existance=ExamInvigilator.query.filter_by(exam_id=exam_id1,cen_id=cen_id1,user_id=i,invig_status=STATUS).first()
                        if chk_existance !=None:
                            invig_already_exists.update({DATA:empdata})
                            return invig_already_exists
                        assignInveg = ExamInvigilator(exam_id=exam_id1,cen_id=cen_id1,user_id=i,invig_status="active")
                        db.session.add(assignInveg)
                        db.session.commit()
                    empdata.append({EXAM_ID:exam_id1,'inv_list':invg_list,CENTER_ID:cen_id1})
                    success1.update({DATA:empdata})
                    return jsonify(success1)
                if 'cen_id' in data:
                    cen_id1=data['cen_id']
                    
                    invigilatorResponse=ExamInvigilator.query.filter_by(cen_id=cen_id1,invig_status=STATUS).all()
                    invigList=[]
                    userIdList=[]
                    examIdDicList=[]
                    examIdList=[]
                    for invigilator in invigilatorResponse:
                        invigList.append(invigilator.user_id)
                        examIdList.append(invigilator.exam_id)
                        examDic={USER_ID:invigilator.user_id,EXAM_ID:invigilator.exam_id}
                        examIdDicList.append(examDic)
                    
                    if len(invigList)==0:
                        return jsonify(invig_not_exist)
                    userResultList=[]
                    for u_id in invigList:
                        singleUser=User_det.query.filter_by(user_id=u_id).first()
                        userDic={INV_NAME:singleUser.name,EMPLOYEE_ID:singleUser.emp_id,USER_ID:singleUser.user_id}
                        userResultList.append(userDic)
                    examResultList=[]
                    for e_id in examIdList:
                        singleExam=Exam.query.filter_by(exam_id=e_id).first()
                        examDic={EXAM_ID:singleExam.exam_id,EXAM_NAME:singleExam.exam_name}
                        examResultList.append(examDic)
                    Res=[]
                    for i in examIdDicList:
                        for j in examResultList:
                            if i.get(EXAM_ID)==j.get(EXAM_ID):
                                i.update(j)
                        for k in userResultList:
                            if i.get(USER_ID)==k.get(USER_ID):
                                i.update(k)                            
                        Res.append(i)
                    
                    teacher_fetch.update({DATA:Res})
                    return jsonify(teacher_fetch)
                    # print(userResultList)
                    # print(examResultList)

                    

                    # userResponse=Exa
                    # print(invigilatorResponse)
                    if user!=None:
                        for i in user:
                            cdic={"inveg_id":i.inveg_id,"exam_id":i.exam_id,"user_id":i.inveglator_id,"cen_id":i.cen_id,"status":i.status}
                            empdata.append(cdic)
                            success.update({'data':empdata})
                        return jsonify(success)
                    else:
                        return jsonify(no_invegilator)
                    
            else:
                return jsonify(session_invalid)
                
            

        except Exception as e:
            
            return jsonify(msg_400)

    def delete(self):
        try:
            data=request.get_json()
            session_token=data[SESSION_TOKEN]
            u_id=data[USER_ID]
            empdata=[]
            chkSession=checkSessionValidity(session_token,u_id)
            if chkSession:        
                cen_id1=data['cen_id'] 
                exam_id1=data['exam_id']
                inv_id=data['inv_id']
                false_exist=FalseNumber.query.filter_by(inv_id=inv_id).first()
                if false_exist!=None:
                    return jsonify(invg_delete_error)                    
                user_exist=User_det.query.filter_by(user_id=inv_id,status=STATUS).first()
                single_teach=RoleDet.query.filter_by(role_meta=TEACHER).first()
                user=ExamInvigilator.query.filter_by(cen_id=cen_id1,exam_id=exam_id1,user_id=inv_id,invig_status=STATUS).first()
                if user!= None:
                    user.invig_status=INACTIVE
                    user_exist.role_id=single_teach.role_id
                    db.session.commit()
                    deleted.update({DATA:empdata})

                    return jsonify(deleted)
                else:
                    return jsonify(invg_delete_error)
            else:
                return jsonify(session_invalid)
            
        except Exception as e:
            return jsonify(msg_400)
#=========================================================#
#                 INVIGILATOR ADD ENDS                    #                           
#=========================================================#


#=========================================================#
#                      EXAM HALL ADD STARTS               #                           
#=========================================================#
class ExamRoomDetails(Resource):
    def post(self):
        try:

            data = request.get_json()
            if ROOM_ID in data:
                h_id = data[ROOM_ID]
                user = ExamHall.query.filter_by(hall_id=h_id).first()
                if user != None:
                    d = {ROOM_ID: user.hall_id, CEN_ID: user.cen_id,
                         ROOM_NO: user.hall_no, ROOM_CAPACITY: user.hall_capacity, BUILDING_NAME: user.hall_name}
                    room_sucss_post_id["data"]=d

                    return room_sucss_post_id

                else:

                    return room_err_post_id

            elif ROOM_NO in data:
                empty = []
                emp = []
                cen_id = data[CEN_ID]
                room_no = data[ROOM_NO]
                room_capacity = data[ROOM_CAPACITY]
                building_name = data[BUILDING_NAME]
                #status= data["status"]
                chk_user = ExamHall.query.filter_by(hall_no=room_no).first()

                if chk_user == None:
                    sm1 = ExamHall(cen_id=cen_id, hall_no=room_no, hall_capacity=room_capacity,hall_free=0,hall_alloted=0,
                                   hall_name=building_name,hall_status=STATUS)
                    db.session.add(sm1)
                    db.session.commit()
                    v1 = ExamHall.query.all()
                    # for i in v1:
                    d  = { CEN_ID: cen_id,ROOM_NO: room_no, ROOM_CAPACITY: room_capacity, BUILDING_NAME: building_name}
                    empty.append(d)
                    room_sucss_post["data"]=d
                    return room_sucss_post
                else:
                    return room_err_post_add

        except Exception as e:  
            print(e)         
            return err_exception

    def get(self):
        try:
            c_id=request.headers[CENTER_ID]
            user =ExamHall.query.filter_by(cen_id=c_id,hall_status="active").all()
            l1 = []
            for i in user:
                n1 = i.hall_id
                n2 = i.cen_id
                n3 = i.hall_no
                n4 = i.hall_capacity
                n5 = i.hall_name                
                n6 = i.hall_status

                d = {ROOM_ID: n1,  CEN_ID: n2,  ROOM_NO: n3,
                     ROOM_CAPACITY: n4, BUILDING_NAME: n5,ROOM_STATUS :n6}
                l1.append(d)
            room_sucss_get.update({"data":l1})

            return room_sucss_get
        except Exception as e:
            return err_exception

    def put(self):
        try:
            empty = []
            emp = []
            content = request.get_json()
            room_id = content[ROOM_ID]
            cen_id = content[CEN_ID]
            room_no = content[ROOM_NO]
            room_capacity = content[ROOM_CAPACITY]
            building_name = content[BUILDING_NAME]

            chk_user1 = Center_det.query.filter_by(
                cen_id=cen_id).first()
            chk_user = ExamHall.query.filter_by(
                hall_id=room_id).first()

            if chk_user != None and chk_user1 != None:
                chk_user.cen_id = cen_id
                chk_user.hall_no = room_no
                chk_user.hall_capacity = room_capacity
                chk_user.hall_name = building_name
                db.session.commit()
                dic = {ROOM_ID: chk_user.hall_id, CEN_ID: chk_user.cen_id, ROOM_NO: chk_user.hall_no,
                       ROOM_CAPACITY: chk_user.hall_capacity, BUILDING_NAME: chk_user.hall_name}
                empty.append(dic)
                room_sucss_put["data"]=dic
                return room_sucss_put
            else:

                return room_err_put

        except Exception as e:
            return err_exception

    def delete(self):

        try:
            empty = []
            emp = []
            data = request.get_json()
            session_token =data["session_token"]
            user_id =data["user_id"]
            room_id = data[ROOM_ID]
            cen_id = data[CEN_ID]
            chk_user1 = Center_det.query.filter_by(cen_id=cen_id).first()
            roomAllotement = HallAllotment.query.filter_by(hall_id=room_id,cen_id=cen_id).first()        
            if roomAllotement != None:
                return jsonify(room_err_delete)
            user = ExamHall.query.filter_by(hall_id=room_id, cen_id=cen_id).first()
            dic = {ROOM_ID: user.hall_id, CEN_ID: user.cen_id,ROOM_NO: user.hall_no, ROOM_CAPACITY: user.hall_capacity, BUILDING_NAME: user.hall_name, ROOM_STATUS: user.hall_status}

            if user != None and chk_user1 != None:
                    db.session.delete(user)
                    db.session.commit()
                    empty.append(dic)
                    room_sucss_delete["data"] = dic
                    return room_sucss_delete
            else:
                return room_err_delete

        except Exception as e:
            return err_exception

#=========================================================#
#                      EXAM HALL ADD ENDS                 #                           
#=========================================================#


#=========================================================#
#                COURSE STARTS                            #                           
#=========================================================#
class CourseAdd(Resource):
    def post(self):
        try:
            requestData = request.get_json()
            s_id=requestData[SESSION_TOKEN]
            u_id=requestData[USER_ID]
            chkSession=checkSessionValidity(s_id,u_id)
            if chkSession:
                p_id=requestData[PROGRAM_ID]
                courseResultList=[]
                courseResponse=Course.query.filter_by(pgm_id=p_id).all()
                for course in courseResponse:
                    courseDic={COURSE_ID:course.cou_id,COURSE_NAME:course.cou_name,PROGRAM_ID:course.pgm_id}
                    courseResultList.append(courseDic)
                course_fetch_success.update({DATA:courseResultList})
                return jsonify(course_fetch_success)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(bad_request)
        



#=========================================================#
#                COURSE ENDS                              #                           
#=========================================================#


#=========================================================#
#                EXAM HALL ALLOTEMENT STARTS              #                           
#=========================================================#
# class ExamHallAllotment(Resource):
#     def get(self):
#         try:
#             s_id=request.headers[SESSION_TOKEN]
#             u_id=request.headers[USER_ID]
#             c_id=request.headers[CENTER_ID]
#             chkSession=checkSessionValidity(s_id,u_id)
#             if chkSession:
#                 hallResponse=ExamHall.query.filter_by(cen_id=c_id).all()  
#                 hallResultList=[]
                           
#                 for hall in hallResponse:
#                     hallExamResult=HallExamMapping.query.filter_by(hall_id=hall.hall_id)
#                     hallDetailsList=[]   
#                     for singleHall in hallExamResult:
#                         hallDetails={EXAM_HALL_CAPACITY:singleHall.hall_capacity,EXAM_HALL_ALLOTTED:singleHall.hall_alloted,EXAM_HALL_FREE:singleHall.hall_free}                        
                        
#                         examInfo=Exam.query.filter_by(exam_id=singleHall.exam_id).first()
#                         hallDic={EXAM_NAME:examInfo.exam_name,EXAM_HALL_NUMBER:hall.hall_no,EXAM_HALL_NAME:hall.hall_name,EXAM_HALL_CAPACITY:hallDetails.get(EXAM_HALL_CAPACITY),EXAM_HALL_ALLOTTED:hallDetails.get(EXAM_HALL_ALLOTTED),EXAM_HALL_FREE:hallDetails.get(EXAM_HALL_FREE)}
#                         hallResultList.append(hallDic)
#                 hall_allotment_fetch.update({DATA:hallResultList})    
#                 return hall_allotment_fetch
#             else:
#                 return jsonify(session_invalid)       
       
#         except Exception as e:
#             return jsonify(err_exception)
#     def post(self):
#         try:
#             requestData = request.get_json()
#             if EXAM_HALL_ID and STUDENT_COUNT in requestData:
#                 h_id=requestData[EXAM_HALL_ID]
#                 c_id=requestData[CEN_ID]
#                 e_id=requestData[EXAM_ID]
#                 p_id=requestData[PROGRAM_ID]
#                 cr_id=requestData[COURSE_ID]                
#                 s_count=requestData[STUDENT_COUNT]
#                 s_id=requestData[SESSION_TOKEN]
#                 u_id=requestData[USER_ID]
#                 e_date=datetime.today()              
#                 chkSession=checkSessionValidity(s_id,u_id)
#                 if chkSession:                    
#                     singleHall=ExamHall.query.filter_by(hall_id=h_id,cen_id=c_id).first()
#                     singleExam=Exam.query.filter_by(exam_id=e_id).first()
#                     if singleExam==None:
#                         return jsonify(hall_allotment_invalid_data)                
#                     if singleHall==None:
#                         return jsonify(hall_allotment_invalid_data)
#                     studentList=Student.query.filter_by(cen_id=c_id,exam_id=e_id,prg_id=p_id).all()
#                     allotedList=HallAllotment.query.filter_by(cen_id=c_id,exam_id=e_id,prg_id=p_id,cou_id=cr_id).all()
#                     studentRegNum=[]
#                     studentAllotedRegNum=[]
#                     finalStudentList=[]
#                     for singleStudent in studentList:
#                         studentRegNum.append(singleStudent.std_id)  
#                     for allotedStudent in allotedList:
#                         studentAllotedRegNum.append(allotedStudent.std_id)
#                     finalStudentList=[i for i in studentRegNum if i not in studentAllotedRegNum ]
#                     finalStudentList=finalStudentList[:s_count]
#                     if len(finalStudentList)!=0:
#                         if singleHall.hall_capacity <s_count:   
#                             return jsonify(hall_allotment_count_invalid)
#                        # Updating Hall allotment table
#                         for i in range(len(finalStudentList)):
#                             allotment=HallAllotment(exam_id=e_id,std_id=finalStudentList[i],cen_id=c_id,hall_id=h_id,hall_allot_date=e_date,hall_allot_status=STATUS,prg_id=p_id,cou_id=cr_id)
#                             db.session.add(allotment)
#                             db.session.commit()
#                        # Updating Exam Hall Mapping table
#                         exam_hall=HallExamMapping.query.filter_by(hall_id=h_id,exam_id=e_id).first()
#                         if exam_hall ==None:   
                                          
#                             h_alloted=len(finalStudentList)
#                             h_free=singleHall.hall_capacity-h_alloted                            
#                             hallMapp=HallExamMapping(hall_id=h_id,exam_id=e_id,hall_capacity=singleHall.hall_capacity,hall_alloted=h_alloted,hall_free=h_free)
#                             db.session.add(hallMapp)
#                             db.session.commit()
#                         else:
#                             if int(exam_hall.hall_free)==0 or exam_hall.hall_free<s_count:
#                                 return jsonify(hall_allotment_count_invalid)
#                             h_alloted=exam_hall.hall_alloted+s_count
#                             h_free=exam_hall.hall_capacity-h_alloted
#                             exam_hall.hall_alloted=h_alloted
#                             exam_hall.hall_free=h_free
#                             db.session.commit()
#                         # Need to implement email send 
#                         resultList=[]
#                         resultDic={EXAM_NAME:singleExam.exam_name,EXAM_HALL_NAME:singleHall.hall_name,EXAM_HALL_NUMBER:singleHall.hall_no,EXAM_HALL_CAPACITY:singleHall.hall_capacity,EXAM_HALL_ALLOTTED:h_alloted,EXAM_HALL_FREE:h_free}
#                         resultList.append(resultDic)
#                         hall_allotment_success.update({DATA:resultList})
#                         return jsonify(hall_allotment_success)
#                     else:
#                         return jsonify(hall_allotment_exist) 
#                 else:
#                     return jsonify(session_invalid)
#         except Exception as e:
#             return jsonify(hall_allotment_bad_request)


class ExamHallAllotment(Resource):
    def post(self):
        try:
            requestData = request.get_json()
            s_id=requestData[SESSION_TOKEN]
            u_id=requestData[USER_ID]
            chkSession=checkSessionValidity(s_id,u_id)
            if chkSession:
                resultList=[]
                h_id=requestData[EXAM_HALL_ID]
                c_id=requestData[CEN_ID]
                e_id=requestData[EXAM_ID]
                p_id=requestData[PROGRAM_ID]
                cr_id=requestData[COURSE_ID]
               
                studentchk=Student.query.filter_by(prg_id=p_id,exam_id=e_id,cen_id=c_id).all()
                if studentchk== None:
                    return no_student_err
                std_count=len(studentchk)                
                allotcount=HallAllotment.query.filter_by(exam_id=e_id,prg_id=p_id,cen_id=c_id,cou_id=cr_id).all()
                allottedstd_count=len(allotcount)
                # start_date=datetime.now().strftime("%Y-%m-%d 00:00:00")
                # end_date=datetime.now().strftime("%Y-%m-%d 23:59:59")
                examDate=ExamTimetable.query.filter_by(exam_id=e_id,prg_id=p_id,cou_id=cr_id).first()

                hallDetails=HallCapacity.query.filter_by(hall_id=h_id,exam_date=examDate.date).first()
                print(hallDetails)
                examHallCheck=ExamHall.query.filter_by(hall_id=h_id).first()
                print(examHallCheck)
                if hallDetails==None:
                    
                    studdic={EXAM_HALL_CAPACITY:examHallCheck.hall_capacity,EXAM_HALL_ALLOTTED:0,EXAM_HALL_FREE:examHallCheck.hall_capacity,
                    EXAM_HALL_NAME:examHallCheck.hall_name,EXAM_HALL_NUMBER:examHallCheck.hall_no,EXAM_HALL_ID:examHallCheck.hall_id}
                    br_fetch.update({DATA:studdic})
                    return jsonify(br_fetch)
                else:
                    studdic={EXAM_HALL_CAPACITY:hallDetails.hall_capacity,EXAM_HALL_ALLOTTED:hallDetails.hall_alloted,EXAM_HALL_FREE:hallDetails.hall_free,
                    EXAM_HALL_NAME:examHallCheck.hall_name,EXAM_HALL_NUMBER:examHallCheck.hall_no,EXAM_HALL_ID:examHallCheck.hall_id}
                    br_fetch.update({DATA:studdic})
                    return jsonify(br_fetch)

                

                    





                # studentchk=db.session.query(HallCapacity,ExamTimetable).with_entities(HallCapacity.hall_alloted,HallCapacity.hall_capacity,HallCapacity.hall_free).filter(ExamTimetable.exam_id==e_id,ExamTimetable.cou_id==cr_id,ExamTimetable.prg_id==p_id,HallCapacity.hall_id==h_id,HallCapacity.exam_date==ExamTimetable.date).all()
                # print()
                # print(studentchk)
                # if studentchk ==[]:
                #     return no_student_allot_err
                
                
                # hall_capacity=studentchk[0][1]
                # # print(hall_capacity)
                # hall_alloted=studentchk[0][0]
                # # print(hall_alloted)
                # hall_free=studentchk[0][2]
                # # print(hall_free)
                
                # studdic={EXAM_HALL_CAPACITY:hall_capacity,EXAM_HALL_ALLOTTED:hall_alloted,EXAM_HALL_FREE:hall_free,STUDENT_COUNT:std_count,ALLOTED_STUDENT:allottedstd_count}
                # resultList.append(studdic)
                # br_fetch.update({DATA:resultList})
                # return jsonify(br_fetch)

            else:
                return jsonify(session_invalid)
        except Exception as e:
            
            return jsonify(err_exception)



class HallAllot(Resource):
    def post(self):
        try:
            requestData = request.get_json()
            s_id=requestData[SESSION_TOKEN]
            u_id=requestData[USER_ID]
            chkSession=checkSessionValidity(s_id,u_id)
            if chkSession:
                resultList=[]
                h_id=requestData[EXAM_HALL_ID]
                c_id=requestData[CEN_ID]
                e_id=requestData[EXAM_ID]
                p_id=requestData[PROGRAM_ID]
                cr_id=requestData[COURSE_ID]
                alloted_std_count=requestData[ALLOTED_STUDENT]
                e_date=date.today()
                singleHall=ExamHall.query.filter_by(hall_id=h_id,cen_id=c_id).first()
                singleExam=Exam.query.filter_by(exam_id=e_id).first()
                start_date=datetime.now().strftime("%Y-%m-%d 00:00:00")
                end_date=datetime.now().strftime("%Y-%m-%d 23:59:59")
                exam=ExamTimetable.query.filter(ExamTimetable.exam_id==e_id,ExamTimetable.prg_id==p_id,ExamTimetable.cou_id==cr_id,
                ExamTimetable.date>start_date,ExamTimetable.date<end_date).first()
                # exam=ExamTimetable.query.filter_by(exam_id=e_id,prg_id=p_id,cou_id=cr_id).first()
                
                if exam ==None:
                    return jsonify(noExam)
                examdate=exam.date
                if singleExam==None:
                    return jsonify(hall_allotment_invalid_data)                
                if singleHall==None:
                    return jsonify(hall_allotment_invalid_data)
                # studentchk=db.session.query(HallExamMapping,ExamTimetable).with_entities(HallExamMapping.hall_alloted,HallExamMapping.hall_capacity,HallExamMapping.hall_free).filter(ExamTimetable.exam_id==e_id,ExamTimetable.cou_id==cr_id,ExamTimetable.prg_id==p_id,HallExamMapping.hall_id==h_id).all()
                # print(studentchk)
                # if len(studentchk) == 0:
                #     return "no student"
                studentList=Student.query.filter_by(cen_id=c_id,exam_id=e_id,prg_id=p_id).all()
                if studentList ==[]:
                    return jsonify(no_student_err)
                allotedList=HallAllotment.query.filter_by(cen_id=c_id,exam_id=e_id,prg_id=p_id,cou_id=cr_id).all()
                studentRegNum=[]
                studentAllotedRegNum=[]
                finalStudentList=[]
                for singleStudent in studentList:
                    studentRegNum.append(singleStudent.std_id)  
                for allotedStudent in allotedList:
                    studentAllotedRegNum.append(allotedStudent.std_id)
                finalStudentList=[i for i in studentRegNum if i not in studentAllotedRegNum ]
                if(alloted_std_count>len(finalStudentList)):
                    return hall_allotment_count_invalid
                finalStudentList=finalStudentList[:alloted_std_count]

                if len(finalStudentList)!=0:
                       # Updating Hall allotment table
                    for i in range(len(finalStudentList)):
                        allotment=HallAllotment(exam_id=e_id,std_id=finalStudentList[i],cen_id=c_id,hall_id=h_id,hall_allot_date=e_date,hall_allot_status=STATUS,prg_id=p_id,cou_id=cr_id,exam_date=examdate)
                        db.session.add(allotment)
                        # db.session.commit()
                       # Updating Exam Hall Mapping table
                    exam_hall=HallCapacity.query.filter_by(hall_id=h_id).first()
                    
                    if exam_hall ==None:   
                        if singleHall.hall_capacity <alloted_std_count:   
                            return jsonify(hall_allotment_count_invalid)              
                        h_alloted=alloted_std_count
                        h_free=singleHall.hall_capacity-h_alloted
                        hallMapp=HallCapacity(hall_id=h_id,hall_capacity=singleHall.hall_capacity,hall_alloted=h_alloted,hall_free=h_free,exam_date=examdate)
                        db.session.add(hallMapp)
                        # db.session.commit()
                    else:
                        if int(exam_hall.hall_free)==0 or exam_hall.hall_free<alloted_std_count:
                            return jsonify(hall_allotment_count_invalid)
                        h_alloted=exam_hall.hall_alloted+alloted_std_count
                        h_free=exam_hall.hall_capacity-h_alloted
                        exam_hall.hall_alloted=h_alloted
                        exam_hall.hall_free=h_free
                        # db.session.commit()
                    # Need to implement email send 
                    resultList=[]
                    db.session.commit()
                    resultDic={EXAM_NAME:singleExam.exam_name,EXAM_HALL_NAME:singleHall.hall_name,EXAM_HALL_NUMBER:singleHall.hall_no,EXAM_HALL_CAPACITY:singleHall.hall_capacity,EXAM_HALL_ALLOTTED:h_alloted,EXAM_HALL_FREE:h_free}
                    resultList.append(resultDic)
                    hall_allotment_success.update({DATA:resultList})
                    return jsonify(hall_allotment_success)
                else:
                    return jsonify(hall_allotment_exist) 
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(err_exception)
            



#=========================================================#
#              EXAM HALL ALLOTEMENT ENDS                  #                           
#=========================================================#        

#=========================================================#
#              EXAM HALL ALLOTEMENT VIEW STARTS           #                           
#=========================================================#        
   


class ExamHallAllotmentView(Resource):
    
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            center_id=request.headers[CENTER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                    emptylist=[]
                    examallotlist=[]
                    singleallot=HallAllotment.query.filter_by(cen_id=center_id).all()
                    if  singleallot!=None:
                        center=Center_det.query.filter_by(cen_id=center_id).first()
                        cendic={CENTER_ID:center_id,CENTER_NAME:center.cen_name}
                        emptylist.append(cendic)
                        for i in singleallot:
                            exam=Exam.query.filter_by(exam_id=i.exam_id).first()
                            hall=ExamHall.query.filter_by(hall_id=i.hall_id).first()
                            studentname=Student.query.filter_by(std_id=i.std_id).first()
                            program=ProgramDet.query.filter_by(prg_id=i.prg_id).first()
                            hallallotdic={EXAM_ID:i.exam_id,EXAM_NAME:exam.exam_name,PROGRAM_ID:i.prg_id,PROGRAM_NAME:program.prg_name,EXAM_HALL_ID:i.hall_id,EXAM_HALL_NAME:hall.hall_name,STUDENT_ID:i.std_id,STUDNAME:studentname.std_name}
                            examallotlist.append(hallallotdic)
                        dic2={STUDENT_LIST:examallotlist}
                        emptylist.append(dic2)
                        hall_allotment_fetch.update({DATA:emptylist})
                        return jsonify(hall_allotment_fetch)
                    else:
                        return jsonify(invalid_id)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(err_exception)

#=========================================================#
#        STUDENT  HALL ALLOTMENT LIST      STARTS         #                           
#=========================================================# 

class StudentHallAllotmentList(Resource):
    
    def post(self):
        try:
            requestData = request.get_json()
            session_token=requestData[SESSION_TOKEN]
            user_id=requestData[USER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                examList=[]
                studList=[]
                cur_time=datetime.now()
                c_time=cur_time.strftime("%H%M")
                
                if int(c_time)<1230:
                    section=FN
                    examDate=datetime.now().strftime("%Y-%m-%d 09:30:00")
                    invCheck=InvigilatorExamHall.query.filter(InvigilatorExamHall.inv_id==user_id,
                    InvigilatorExamHall.exam_date==examDate).first()
                elif int(c_time)>1230:
                    section=AN
                    examDate=datetime.now().strftime("%Y-%m-%d 13:30:00")
                    invCheck=InvigilatorExamHall.query.filter(InvigilatorExamHall.inv_id==user_id,
                    InvigilatorExamHall.exam_date>=examDate).first() 
                    
                start_date=datetime.now().strftime("%Y-%m-%d 00:00:00")
                end_date=datetime.now().strftime("%Y-%m-%d 23:59:59")
                
                
                if invCheck!=None:
                    hallCheck=HallAllotment.query.filter(HallAllotment.hall_id==invCheck.hall_id,HallAllotment.cen_id==invCheck.cen_id,
                    HallAllotment.exam_date>start_date,HallAllotment.exam_date<end_date).all()
                   
                    for i in hallCheck:

                        examDate=ExamTimetable.query.filter(ExamTimetable.exam_id==i.exam_id,ExamTimetable.date>start_date,ExamTimetable.date<end_date,ExamTimetable.section==section).first()
                        if examDate!=None:
                            examList.append(i.std_id)
                        
                    for i in examList:
                        
                        studCheck=Student.query.filter_by(std_id=i).first()
                        

                        studDic={STUDENT_ID:studCheck.std_id,STUDNAME:studCheck.std_name,STUDREG:studCheck.std_reg}
                        studList.append(studDic)
                        
                    # for i in examList:
                    #     hallCheck=HallAllotment.query.filter(HallAllotment.hall_id==i.get("hall_id"),HallAllotment.exam_id==i.get("exam_id"),
                    #     HallAllotment.exam_date>start_date,HallAllotment.exam_date<end_date).all()
                    #     for j in hallCheck:
                    # #         studCheck=Student.query.filter_by(std_id=j.std_id).first()
                        
                    hall_allotment_fetch.update({DATA:studList})
                    return hall_allotment_fetch
                else:
                    return no_inv_allot_err
            else:
                return jsonify(session_invalid)
       
        except Exception as e:
            return jsonify(err_exception)
#=========================================================#
#        STUDENT  HALL ALLOTMENT LIST      ENDS           #                           
#=========================================================# 

#=========================================================#
#        HALL WISE STUDENT LISTING         STARTS         #                           
#=========================================================# 

class HallwiseStudentList(Resource):
    def post(self):
        try:
            requestData = request.get_json()
            s_id=requestData[SESSION_TOKEN]
            u_id=requestData[USER_ID]
            chkSession=checkSessionValidity(s_id,u_id)
            if chkSession:
                resultList=[]
                h_id=requestData[EXAM_HALL_ID]
                c_id=requestData[CEN_ID]
                hallCheck=HallAllotment.query.filter_by(hall_id=h_id,cen_id=c_id).all()
                if hallCheck!=[]:
                    for i in hallCheck:
                        studCheck=Student.query.filter_by(std_id=i.std_id).first()
                        examHall=ExamHall.query.filter_by(hall_id=i.hall_id).first()
                        examCheck=Exam.query.filter_by(exam_id=i.exam_id).first()
                        studDic={STUDENT_ID:i.std_id,STUDNAME:studCheck.std_name,STUDREG:studCheck.std_reg,EXAM_NAME:examCheck.exam_name,
                        EXAM_HALL_NAME:examHall.hall_name,EXAM_HALL_NUMBER:examHall.hall_no}
                        resultList.append(studDic)
                    resultList=sorted(resultList, key = lambda k:k[STUDREG])
                    hall_allotment_fetch.update({DATA:resultList})
                    return jsonify(hall_allotment_fetch)
                else:
                    return jsonify(no_student_allot_err)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(err_exception)

# class HallwiseStudentList(Resource):
#     def post(self):
#         try:
#             requestData = request.get_json()
#             s_id=requestData[SESSION_TOKEN]
#             u_id=requestData[USER_ID]
#             chkSession=checkSessionValidity(s_id,u_id)
#             if chkSession:
#                 resultList=[]
#                 h_id=requestData[EXAM_HALL_ID]
#                 c_id=requestData[CEN_ID]
#                 hallCheck=db.session.query(HallAllotment,Student,ExamHall,Exam).with_entities(HallAllotment.std_id.label(STUDENT_ID),Student.std_name.label(STUDNAME),
#                 Student.std_reg.label(STUDREG),Exam.exam_name.label(EXAM_NAME),ExamHall.hall_name.label(EXAM_HALL_NAME),ExamHall.hall_no.label(EXAM_HALL_NUMBER)).filter(Student.std_id==HallAllotment.std_id,ExamHall.hall_id==HallAllotment.hall_id,Exam.exam_id==HallAllotment.exam_id).order_by(Student.std_reg).all()
#                 if hallCheck!=[]:
#                     userData=list(map(lambda n:n._asdict(),hallCheck))
#                     hall_allotment_fetch.update({DATA:userData})
#                     return jsonify(hall_allotment_fetch)
#                 else:
#                     return jsonify(no_student_allot_err)
#             else:
#                 return jsonify(session_invalid)
#         except Exception as e:
#             return jsonify(err_exception)

#=========================================================#
#        HALL WISE STUDENT LISTING         ENDS          #                           
#=========================================================#


#=========================================================#
#         CENTER SPECIFIC EXAM LIST STARTS                #                           
#=========================================================#
class CenterExam(Resource):    
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            cen_id=request.headers[CENTER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                
                cenlist=[]
                
                singleidchk=Student.query.filter_by(cen_id=cen_id).all()
                if  singleidchk!=None:
                    for i in singleidchk:
                        exam=Exam.query.filter_by(exam_id=i.exam_id).first()
                        date=exam.start_date.strftime("%Y-%m-%d")
                        date2=exam.end_date.strftime("%Y-%m-%d")
                       
                        centerdic={CENTER_ID:i.cen_id,EXAM_ID:i.exam_id,EXAM_NAME:exam.exam_name,EXAM_CODE:exam.exam_code,START_DATE:date,END_DATE:date2}
                        cenlist.append(centerdic)
                    result = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in cenlist)] 
                    prgfetch.update({DATA:result})
                    return jsonify(prgfetch)
                else:
                    return jsonify(invalid_id)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(err_exception)

#=========================================================#
#         CENTER SPECIFIC EXAM LIST ENDS                  #                           
#=========================================================#

#=========================================================#
#         CENTER SPECIFIC CAMP LIST STARTS                #                           
#=========================================================#

class CenterCamp(Resource):    
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            cen_id=request.headers[CENTER_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                cenlist=[]
                
                singleidchk=Student.query.filter_by(cen_id=cen_id).all()
                if  singleidchk!=None:
                    for i in singleidchk:
                        exam=Exam.query.filter_by(exam_id=i.exam_id).first()
                        camp=Camp.query.filter_by(exam_id=i.exam_id).first()
                        st_date=camp.start_date
                        s_date=st_date.strftime('%d-%m-%Y')
                        end_date=camp.end_date
                        e_date=end_date.strftime('%d-%m-%Y')
                        center=Center_det.query.filter_by(cen_id=camp.cen_id).first()
                        prg=ProgramDet.query.filter_by(prg_id=camp.prg_id).first()

                        centerdic={CENTER_ID:i.cen_id,EXAM_ID:i.exam_id,EXAM_NAME:exam.exam_name,START_DATE:s_date,
                        END_DATE:e_date,CAMP_NAME:center.cen_name,PRG_NAME:prg.prg_name}
                        cenlist.append(centerdic)
                        result = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in cenlist)]
                    cenfetch.update({DATA:result})
                    return jsonify(cenfetch)
                else:
                    return jsonify(invalid_id)
            else:
                return jsonify(session_invalid)
        except Exception as e:
            return jsonify(err_exception)


#=========================================================#
#         CENTER SPECIFIC CAMP LIST ENDS                  #                           
#=========================================================#


#=========================================================#
#                EXAM SPECIFIC COURSE START               #                           
#=========================================================#
class GetExamCourse(Resource):
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            exam_id=request.headers[EXAM_ID]
            prg_id=request.headers[PRG_ID]
            sess_res=checkSessionValidity(session_token,user_id) 
            if sess_res:
                    start_date=datetime.now().strftime("%Y-%m-%d 00:00:00")
                    end_date=datetime.now().strftime("%Y-%m-%d 23:59:59")
                    courselist=[]
                    courseslist=[]
                    timetableobj=ExamTimetable.query.filter(ExamTimetable.prg_id==prg_id,ExamTimetable.exam_id==exam_id,ExamTimetable.date>=start_date).all()
                    if timetableobj==[]:
                        exam_course_success.update({DATA:courseslist})
                        return exam_course_success
                    for i in timetableobj:
                        courselist.append(i.cou_id)
                    for j in courselist:
                        courseobj=Course.query.filter_by(cou_id=j).first()
                        coursedict={COURSE_ID:j,COURSE_NAME:courseobj.cou_name}
                        courseslist.append(coursedict)
                    exam_course_success.update({DATA:courseslist})
                    return exam_course_success
            else:
                return session_invalid
        except Exception as e:
            return error
#=========================================================#
#                EXAM SPECIFIC COURSE END                 #                           
#=========================================================#

#=========================================================#
#                BRANCH SPECIFIC SECTION STARTS           #                           
#=========================================================#
class BranchSection(Resource):
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            b_id=request.headers[BRANCH_ID] 
            sess_res=checkSessionValidity(session_token,user_id)             
            if sess_res:
                    sectionData=db.session.query(branch_det,Section_det).with_entities(Section_det.sec_id.label(SECTION_ID),Section_det.sec_name.label(SECTION_NAME)).filter(Section_det.br_id==b_id).all()
                    sectionRes=list(map(lambda n:n._asdict(),sectionData))
                    sec_fetch.update({DATA:sectionRes})
                    return jsonify(sec_fetch)
            else:
                return session_invalid
        except Exception as e:
            
            return error
#=========================================================#
#              BRANCH SPECIFIC SECTION ENDS               #                           
#=========================================================#

#=========================================================#
#                 USER ROLES STARTS                       #                           
#=========================================================#
class UserRole(Resource):
    def get(self):
        try:
            session_token=request.headers[SESSION_TOKEN]
            user_id=request.headers[USER_ID]
            # ipaddress=get_my_ip()            
            # application.logger.error("User with id "+user_id+" access the api/v1/user_role from "+ ipaddress) 
            sess_res=checkSessionValidity(session_token,user_id)             
            if sess_res:
                    roleData=db.session.query(RoleDet).with_entities(RoleDet.role_id.label(ROLE_ID),RoleDet.role_name.label(ROLE_NAME)).filter(RoleDet.role_status==STATUS,RoleDet.role_meta!=CAMPOFFICER,RoleDet.role_meta!=CHIEFSUPERINTENDENT,RoleDet.role_meta!=CHIEFEXAMINER,RoleDet.role_meta!=ADDITIONALEXAMINER,RoleDet.role_meta!=CHAIRMAN).all()
                    roleRes=list(map(lambda n:n._asdict(),roleData))
                    sec_fetch.update({DATA:roleRes})                    
                    return jsonify(sec_fetch)
            else:
                return session_invalid
        except Exception as e:
            return error
#=========================================================#
#                    USER ROLES ENDS                      #                           
#=========================================================#