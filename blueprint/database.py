import pyrebase
import requests
import urllib.request
import hashlib
import json
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
import random
import string
import cryptocode
import os
from algo.testingalgo import *

config = {
	'apiKey': "",
	'authDomain': "",
	'projectId': "",
	'storageBucket': "",
	'messagingSenderId': "",
	'appId': "",
	'measurementId': "",
	'databaseURL':""

}

databaseconfig = {
"apiKey": "",
"authDomain": "",
"databaseURL": "",
"projectId": "",
"storageBucket": "",
"serviceAccount": ""
}

#for key in config.keys():
    #if key == "databaseURL":
    #    continue
    #val = os.environ.get(key)
    #config[key] = val

#for key in databaseconfig.keys():
    #val = os.environ.get(key)
    #databaseconfig[key] = val

config = {
	'apiKey': "AIzaSyB3EuVdoM4dHQCUwEYScbvbnxiXGXObdnc",
	'authDomain': "fyp-22-s3-07.firebaseapp.com",
	'projectId': "fyp-22-s3-07",
	'storageBucket': "fyp-22-s3-07.appspot.com",
	'messagingSenderId': "787854218747",
	'appId': "1:787854218747:web:85731507643d24aa3e275e",
	'measurementId': "G-R5DHSG3RTK",
	'databaseURL':''

}

databaseconfig = {
"apiKey": "AIzaSyB3EuVdoM4dHQCUwEYScbvbnxiXGXObdnc",
"authDomain": "fyp-22-s3-07.firebaseapp.com",
"databaseURL": "https://fyp-22-s3-07-default-rtdb.asia-southeast1.firebasedatabase.app",
"projectId": "fyp-22-s3-07",
"storageBucket": "fyp-22-s3-07.appspot.com",
"serviceAccount": "serviceAccountKey.json"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

firebase = pyrebase.initialize_app(databaseconfig)
database = firebase.database()
storage =firebase.storage()

def register_user(username,password):
    user = auth.create_user_with_email_and_password(username,password)
    #auth.send_email_verification(user['idToken'])

def get_encrypted_id(message,password):
    return cryptocode.encrypt(message,hashlib.sha256(password.encode()).hexdigest())

def get_decrypted_id(message,password):
    return cryptocode.decrypt(message,hashlib.sha256(password.encode()).hexdigest())

def reset_password(username):
    auth.send_password_reset_email(username)

def set_sign_up_user_information(username,user_information):
    database.child("sign_up_users").child(hashlib.sha256(username.encode()).hexdigest()).set(user_information)

def create_store_owner(username,user_information):
    database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).set(user_information)
    set_subscription(username,599,"store_owner") #when create store owner, we will give it a basic 1 year plan with auto renew = true
    database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("projects").update({"limit":2})
    database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("plan").update({"expiry":set_expiry_date("Yearly")})

def create_moderator(username,user_information):
    database.child("moderators").child(hashlib.sha256(username.encode()).hexdigest()).set(user_information)

def freeze_unfreeze_store_owner(username):
    user = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).get()
    if user.val()["status"]:
        database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).update({"status":False})
    else:
        database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).update({"status":True})
    
def delete_store_owner(username):#does not delete from firebase authentication currently
    user = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).get()
    delete_id = user.val()["deleteid"]
    decrypted_key = get_decrypted_id(delete_id,username)
    deleted_user = auth.sign_in_with_email_and_password(username,decrypted_key)
    auth.delete_user_account(deleted_user["idToken"])
    database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).remove()
    
def delete_moderator(username):#does not delete from firebase authentication currently
    user = database.child("moderators").child(hashlib.sha256(username.encode()).hexdigest()).get()
    delete_id = user.val()["deleteid"]
    decrypted_key = get_decrypted_id(delete_id,username)
    deleted_user = auth.sign_in_with_email_and_password(username,decrypted_key)
    auth.delete_user_account(deleted_user["idToken"])
    database.child("moderators").child(hashlib.sha256(username.encode()).hexdigest()).remove()

def approve_reject_user(username,action):#maybe send email to user that it has been approved
    database.child("sign_up_users").child(hashlib.sha256(username.encode()).hexdigest()).update({"approval":action})
    if action:
        database.child("sign_up_users").child(hashlib.sha256(username.encode()).hexdigest()).update({"status":"approved"})
    else:
        database.child("sign_up_users").child(hashlib.sha256(username.encode()).hexdigest()).update({"status":"rejected"})
    shift_approved_user(username)

def shift_approved_user(username): #maybe can do a automatic trigger?
    sign_up_users = database.child("sign_up_users").child(hashlib.sha256(username.encode()).hexdigest()).get()
    sign_up_users_plan = database.child("sign_up_users").child(hashlib.sha256(username.encode()).hexdigest()).child("plan").get()
    if sign_up_users.val()["approval"] and sign_up_users.val()["status"] == "approved" and sign_up_users_plan.val() != None:
        plan = {"cost":sign_up_users_plan.val()["cost"],"desc":sign_up_users_plan.val()["desc"],"expiry":set_expiry_date(sign_up_users_plan.val()["cost"]) ,"renew":sign_up_users_plan.val()["renew"],"type":sign_up_users_plan.val()["type"]}
        user_information= {"username":sign_up_users.val()["username"],"deleteid":sign_up_users.val()["deleteid"], "firstname":sign_up_users.val()["firstname"],"lastname":sign_up_users.val()["lastname"],"company":sign_up_users.val()["company"],"industry":sign_up_users.val()["industry"],"contact":sign_up_users.val()["contact"],"url":sign_up_users.val()["url"],"status":sign_up_users.val()["approval"],"emailverification":sign_up_users.val()["emailverification"],"role":"store_owner"}
        database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).set(user_information)
        database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("plan").update(plan) 
        database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("projects").update({"limit":get_limit_by_plan(plan["desc"])}) 
        database.child("sign_up_users").child(hashlib.sha256(username.encode()).hexdigest()).remove()
        
def update_user_information(username,user_information,role):
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).update(user_information)

def login_user(username,password):
    user = auth.sign_in_with_email_and_password(username,password)
    user_information = get_general_user_information(username)
    return user,user_information

def get_general_user_information(username): #have a function that returns name, role dictionary object
    user = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).get()
    demo_user = database.child("demo_users").child(hashlib.sha256(username.encode()).hexdigest()).get()
    signed_user = database.child("sign_up_users").child(hashlib.sha256(username.encode()).hexdigest()).get()
    moderator = database.child("moderators").child(hashlib.sha256(username.encode()).hexdigest()).get()
    administrator = database.child("administrators").child(hashlib.sha256(username.encode()).hexdigest()).get()
    
    if user.val() != None:
        name = user.val()["firstname"]+" " + user.val()["lastname"]
        role = user.val()["role"]
        try:
            #print(renew_subscription(username))
            if renew_subscription(username) == None:
                return {"fullname":name,"role":role}
            elif renew_subscription(username):
                return {"fullname":name,"role":role}
        finally:
            return {"fullname":name,"role":role}#{"fullname":name,"role":"sign_up_user"}
    elif demo_user.val() != None:
        name = demo_user.val()["firstname"]+" " + demo_user.val()["lastname"]
        role = demo_user.val()["role"]
        return {"fullname":name,"role":role}
    elif signed_user.val() != None:
        name = signed_user.val()["firstname"]+" " + signed_user.val()["lastname"]
        role = signed_user.val()["role"]
        return {"fullname":name,"role":role}
    elif moderator.val() != None:
        name = moderator.val()["firstname"]+" " + moderator.val()["lastname"]
        role = moderator.val()["role"]
        return {"fullname":name,"role":role}
    elif administrator.val() != None:
        name = administrator.val()["firstname"]+" " + administrator.val()["lastname"]
        role = administrator.val()["role"]
        return {"fullname":name,"role":role}
    return None

def get_status(username):
    user = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).get()
    if user.val() != None:
        return user.val()["status"]
    else:
        return None

def firebase_user_information(user):
    return auth.get_account_info(user['idToken'])

def get_random_password(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def createDemoAccount():
    demo_username = get_random_password(8)+"@gmail.com"
    demo_password = get_random_password(8)
    user = auth.create_user_with_email_and_password(demo_username,demo_password)
    return demo_username,demo_password
    
def set_demo_user(username,user_information):
    database.child("demo_users").child(hashlib.sha256(username.encode()).hexdigest()).set(user_information)
    database.child("demo_users").child(hashlib.sha256(username.encode()).hexdigest()).child("projects").update({"counter":1,"limit":1})
    database.child("demo_users").child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").update({1:{"category":"Shoes","id":1,"pname":"Demo Project","url":"https://www.lazada.sg/men-sports-clothing-t-shirts","counter":1,"crawler":"single_page","projectcsv":""}}) # set the projectcsv to be from the same for all demo
    database.child("demo_users").child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child("1").child("item").child("1").update({"tcategory":"highheels","category":"Shoes","id":1,"imageurl":"https://quirkytravelguy.com/wp-content/uploads/2021/01/giant-adidas-shoes.jpg","name":"Branded Shoes"})

def demo_user_exist(username):
    try:
        all_demo_users = database.child("demo_users").get()
        for user in all_demo_users.each():
            if username == user.val()['email']:
                return True
        return False
    except:
        return False
    
def get_demo_information(email):
    user = database.child("demo_users").child(hashlib.sha256(email.encode()).hexdigest()).get()
    name = user.val()["firstname"]+" " + user.val()["lastname"]
    demo_username = user.val()["demo_username"]
    demo_password = user.val()["demo_password"]
    return name,demo_username,demo_password

def get_faqs(user):    
    if user == "default_user":
        all_faqs = database.child("faqs").child("default_user").get()
        faq_lists = []
        for user in all_faqs.each():
            faq_lists.append({"question":user.key(),"answer":user.val()})
        return faq_lists
    if user == "store_owner":
        all_faqs = database.child("faqs").child("store_owner").get()
        faq_lists = []
        for user in all_faqs.each():
            faq_lists.append({"question":user.key(),"answer":user.val()})
        return faq_lists
   
def get_pricing(subscriptiontype):
    if subscriptiontype == "monthly":
        all_pricing = database.child("pricing").child("monthly").get()
        all_monthly_pricing_list = {}
        for user in all_pricing.each():
            all_monthly_pricing_list[user.key()] = user.val()
        return all_monthly_pricing_list
    if subscriptiontype == "yearly":
        all_pricing = database.child("pricing").child("yearly").get()
        all_yearly_pricing_list = {}
        for user in all_pricing.each():
            all_yearly_pricing_list[user.key()] = user.val()
        return all_yearly_pricing_list

def get_plan_pricing(amt):
    amount = int(amt)
    if amount <= 109:
        all_pricing = database.child("pricing").child("monthly").get()
        for plan in all_pricing.each():
            if plan.val() == amount:
                return {"plan": {"type" : "Monthly", "desc":plan.key(),"cost":amount,"expiry":"","renew":True}}
    else:
        all_pricing = database.child("pricing").child("yearly").get()
        for plan in all_pricing.each():
            if plan.val() == amount:
                return {"plan": {"type" : "Yearly", "desc":plan.key(),"cost":amount,"expiry":"","renew":True}}

def get_limit_by_plan(desc):
    if desc == "Basic":
        return 2
    elif desc == "Pro":
        return 5
    else:
        return 9999

def check_if_project_limit(username,role):
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    user = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).get()
    all_projects = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").get()
    try:
        if all_projects.val()[0] != None:
            return len(all_projects.val()) == user.val()["projects"]["limit"]
        else:
            return (len(all_projects.val()) -1) == user.val()["projects"]["limit"]
    except TypeError as e:
        print(e)
        return False
    except KeyError as e:
        print(e)
        if role == "demo_user":
            database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").update({"limit":1})
            return len(all_projects.val()) == user.val()["projects"]["limit"]
        else:
            database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").update({"limit":get_limit_by_plan(user.val()["plan"]["desc"])})
            return len(all_projects.val()) == user.val()["projects"]["limit"]
    

def set_expiry_date(plantype):
    if plantype == "Monthly":
        expiry = date.today() + relativedelta(months=+1)
        return expiry.strftime("%d/%m/%Y")
    else:
        expiry = date.today() + relativedelta(months=+12)
        return expiry.strftime("%d/%m/%Y")

def get_start_date(expiry_date,plantype):
    if plantype == "Monthly":
        start_date = datetime.strptime(expiry_date,"%d/%m/%Y") - relativedelta(months=+1)
        return start_date.strftime("%d/%m/%Y")
    else:
        start_date = datetime.strptime(expiry_date,"%d/%m/%Y") - relativedelta(months=+12)
        return start_date.strftime("%d/%m/%Y")

def check_user_subscription(username,amt,role):
    amount = int(amt)
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    try:
            user = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("plan").get()           
            return amount != user.val()["cost"]
    except Exception as e:
        print(e)
        return True
    
def set_subscription(username,amount,role):#need to define for expiry, once approve the expiry will start?
    current_plan = get_plan_pricing(amount)
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    elif role == "sign_up_user":
        user_role = "sign_up_users"
    database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).update(current_plan)
    
    if user_role == "users":
        user = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).get()
        if user.val()["status"] == True:
            database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("plan").update({"expiry":set_expiry_date(user.val()["plan"]["type"])})
            database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").update({"limit":current_plan["plan"]["desc"]})
        
def retrieve_all_project(username,role):
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    try:
        project = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").get()
        all_project = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").get()
        all_project_list = []
        if len(all_project.val()) == 1:#if there is only 1 item in the list
            for proj in all_project.val():
                all_project_list.append({"id":all_project.val()[proj]["id"],"pname":all_project.val()[proj]["pname"],"category":all_project.val()[proj]["category"],"url":all_project.val()[proj]["url"]})
            return all_project_list
        for proj in all_project.val():
            if proj != None:
                all_project_list.append({"id":proj["id"],"pname":proj["pname"],"category":proj["category"],"url":proj["url"]})
        return all_project_list
    except TypeError as e:
        return []

def get_userproject_limit(username,role):
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    try:
        return database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").get().val()["limit"]
    except Exception as e:
        print(e)
        return 0

def set_project(username, project_information,role):
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    if project_information["id"] == 1:
        crawl_id = (hashlib.sha256(username.encode()).hexdigest()+";"+str(1))
        database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").update({"counter":1})
        crawl_information = {crawl_id:{"url":project_information["url"],"crawler":project_information["crawler"],"projectcsv":crawl_id}}
        set_url_to_crawl_list(crawl_information)
        project_information["projectcsv"] = crawl_id
    else:
        crawl_id = (hashlib.sha256(username.encode()).hexdigest()+";"+str(project_information["id"]))
        database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").update({"counter":project_information["id"]})
        crawl_information = {crawl_id:{"url":project_information["url"],"crawler":project_information["crawler"],"projectcsv":crawl_id}}
        set_url_to_crawl_list(crawl_information)
        project_information["projectcsv"] = crawl_id
    database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child(project_information["id"]).update(project_information)

def retrieve_all_project_recommendations(username,project_id,role):
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    try:
        all_project_items = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child(project_id).get()
        if all_project_items.val()["recommendations"] != None:
            items = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child(project_id).child("recommendations").get()
            list_of_recommendations_for_output = []
            for item in items.each():
                if item != None:
                    list_of_recommendations_for_output.append({"name":item.key().replace("_"," "),"category":item.val()["category"],"list":'<br><br>'.join(item.val()["list"]),"statistics":"data:image/png;base64, "+ item.val()["statistics"] })      
        return list_of_recommendations_for_output
    except KeyError as e:
        project_csv_url = all_project_items.val()["projectcsv"]+".csv"
        try:
            print(urllib.request.urlopen(get_dataset_from_storage(project_csv_url)))
            list_of_recommendations,list_of_graphs = get_algorithm_output(get_dataset_from_storage(),get_dataset_from_storage(project_csv_url))
            database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child(project_id).child("recommendations").update(list_of_recommendations)
            
            list_of_recommendations_for_output = []
            for key,graph in list_of_graphs.items():
                database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child(project_id).child("recommendations").child(key).update({"statistics":graph})
                #list_of_recommendations[key]["statistics"] = "data:image/png;base64, "+ graph 
                list_of_recommendations_for_output.append({"name":key.replace("_"," "),"category":list_of_recommendations[key]["category"],"list":list_of_recommendations[key]["list"],"statistics":"data:image/png;base64, "+ graph })
            return list_of_recommendations_for_output
        except Exception as e:
            print(e)
            return {}
        return 
    except TypeError as e:
        return {} 

def set_url_to_crawl_list(crawl_information):
    database.child("crawl_lists").update(crawl_information)
    
def delete_project_by_id(username, project_id,role):
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child(project_id).remove()

def get_project_by_id_exists(username,project_id,role):
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    try:
        all_project = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child(project_id).get()
        return all_project.val() != None
    except TypeError as e:
        return False

def get_all_store_owner_information_for_manage_store_owner():
    all_users = database.child("users").get()
    all_users_list = []
    try:
        for user in all_users.each():
            fullname = user.val()["firstname"] + " " + user.val()["lastname"]
            if user.val()["status"]:
                image = "images/active.png"
                freezetext = "Freeze"
            else:
                image = "images/inactive.png"
                freezetext = "Unfreeze"
            userhash = hashlib.sha1(user.val()["username"].encode()).hexdigest()
            all_users_list.append({"industry":user.val()["industry"],"freezebutton":user.val()["username"],"deletebutton":user.val()["username"],"name":fullname,"company":user.val()["company"],"status":image,"freezetext":freezetext,"freezemodaltarget":"#fmodal"+userhash,"deletemodaltarget":"#dmodal"+userhash,"deletemodalbox":"dmodal"+userhash,"freezemodalbox":"fmodal"+userhash})
        return all_users_list
    except TypeError as e:
        return all_users_list

def get_all_store_owner_information_for_approve_reject():
    all_users = database.child("sign_up_users").get()
    all_users_list = []
    try:
        for user in all_users.each():
            if user.val()["status"] == "pending":
                fullname = user.val()["firstname"] + " " + user.val()["lastname"]
                userhash = hashlib.sha1(user.val()["username"].encode()).hexdigest()
                all_users_list.append({"industry":user.val()["industry"],"approvebutton":user.val()["username"],"rejectbutton":user.val()["username"],"name":fullname,"company":user.val()["company"],"approvemodaltarget":"#fmodal"+userhash,"rejectmodaltarget":"#dmodal"+userhash,"rejectmodalbox":"dmodal"+userhash,"approvemodalbox":"fmodal"+userhash})
        return all_users_list
    except TypeError as e:
        return []  
        

def get_all_store_owner_information_for_admin_overview():
    all_users = database.child("users").get()
    all_sign_users = database.child("sign_up_users").get()
    moderators = database.child("moderators").get()
    all_users_list = {"active":0,"inactive":0,"frozen":0,"pending":0,"moderator":0}
    try:
        for user in all_users.each():
            if user != None:                
                if user.val()["status"]:
                    all_users_list["active"] +=1
                else:
                    all_users_list["frozen"] +=1
    except TypeError as e:
        print(e)

    try:
        for user in all_sign_users.each():
            if user != None:      
                if user.val()["status"] == "approved":
                    all_users_list["inactive"] +=1
                elif user.val()["status"] == "pending":
                    all_users_list["pending"] +=1
    except TypeError as e:
        print(e)
        
    try:
        for user in moderators.each():
            if user != None:                
                all_users_list["moderator"] +=1
    except TypeError as e:
        print(e)
        
    return all_users_list

def get_all_moderator_information_for_manage_moderator():
    all_moderators = database.child("moderators").get()
    all_moderators_list = []
    try:
        for user in all_moderators.each():
            fullname = user.val()["firstname"] + " " + user.val()["lastname"]
            userhash = hashlib.sha1(user.val()["username"].encode()).hexdigest()
            all_moderators_list.append({"deletebutton":user.val()["username"],"name":fullname,"deletemodaltarget":"#dmodal"+userhash,"deletemodalbox":"dmodal"+userhash})
        return all_moderators_list
    except TypeError as e:
        return []

def get_store_owner_information(username,role):
    if role == "store_owner":
        user = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).get()
        name = user.val()["firstname"]+" " + user.val()["lastname"]
        fname = user.val()["firstname"]
        lname = user.val()["lastname"]
        cname = user.val()["company"]
        url = user.val()["url"]
        email = user.val()["username"]
        contact = user.val()["contact"]
        industry = user.val()["industry"]
        
        return {"fname":fname,"lname":lname, "name":name,"email":email,"url": url,"company": cname,"industry":industry,"contact":contact}
    elif role == "demo_user":
        user = database.child("demo_users").child(hashlib.sha256(username.encode()).hexdigest()).get()
        name = user.val()["firstname"]+" " + user.val()["lastname"]
        fname = user.val()["firstname"]
        lname = user.val()["lastname"]
        cname = ""
        url = user.val()["url"]
        email = user.val()["demo_username"]
        contact = user.val()["contact"]
        industry = ""
        
        return {"fname":fname,"lname":lname, "name":name,"email":email,"url": url,"company": cname,"industry":industry,"contact":contact}
    elif role == "sign_up_user":
        user = database.child("sign_up_users").child(hashlib.sha256(username.encode()).hexdigest()).get()
        name = user.val()["firstname"]+" " + user.val()["lastname"]
        fname = user.val()["firstname"]
        lname = user.val()["lastname"]
        cname = user.val()["company"]
        url = user.val()["url"]
        email = user.val()["username"]
        contact = user.val()["contact"]
        industry = user.val()["industry"]
        
        return {"fname":fname,"lname":lname, "name":name,"email":email,"url": url,"company": cname,"industry":industry,"contact":contact}
    

def get_owner_subscription_information(username):
    user = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).get()
    name = user.val()["firstname"]+" " + user.val()["lastname"]
    cname = user.val()["company"]
    url = user.val()["url"]
    email = user.val()["username"]
    
    subscription = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("plan").get()
    accounttype = subscription.val()["desc"]
    subscriptiontype = subscription.val()["type"]
    expirydate = subscription.val()["expiry"]
    renew = subscription.val()["renew"]
    return {"name":name,"email":email,"url": url,"company": cname,"accounttype":accounttype,"subscriptiontype":subscriptiontype,"expirydate":expirydate,"renew":renew,"startdate":get_start_date(expirydate,subscriptiontype)}
    
def update_auto_renew_subscription(username,value):
    database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("plan").update({"renew":value})

def renew_subscription(username):
    user_plan = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("plan").get()
    today_date = datetime.strptime((date.today().strftime("%d/%m/%Y")),'%d/%m/%Y')
    expiry_date = datetime.strptime(user_plan.val()["expiry"],'%d/%m/%Y')
    if user_plan.val()["renew"] and today_date >= expiry_date: #auto renew is on, expiry date reached
        current_expiry = user_plan.val()["expiry"]
        current_plantype = user_plan.val()["type"]
        database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("plan").update({"expiry":set_expiry_date(current_plantype)})
        return True
    elif not user_plan.val()["renew"] and today_date > expiry_date:   
        user = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).get()
        user_information= {"username":user.val()["username"],"deleteid":user.val()["deleteid"], "firstname":user.val()["firstname"],"lastname":user.val()["lastname"],"company":user.val()["company"],"industry":user.val()["industry"],"contact":user.val()["contact"],"url":user.val()["url"],"approval":True,"status":"approved","emailverification":user.val()["emailverification"],"role":"sign_up_user"}
        database.child("sign_up_users").child(hashlib.sha256(username.encode()).hexdigest()).set(user_information)   
        database.child("users").remove(hashlib.sha256(username.encode()).hexdigest())# this will delete user from users
        return False
    return None
        
def get_project_by_id(username,project_id,role):
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    try:
        all_project = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child(project_id).get()
        if all_project.val() != None:
            return {"id":all_project.val()["id"],"pname":all_project.val()["pname"],"category":all_project.val()["category"],"url":all_project.val()["url"]}
        return None
    except TypeError as e:
        return None

def get_project_item_by_id(username,project_id,item_id,role):
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    try:
        all_project_item = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child(project_id).child("items").child(item_id).get()
        if all_project_item.val() != None:
            return {"id":all_project_item.val()["id"],"category":all_project_item.val()["category"],"tcategory":all_project_item.val()["tcategory"],"imageurl":all_project_item.val()["imageurl"],"name":all_project_item.val()["name"],"recommendations":all_project_item.val()["recommendations"],"statistics":all_project_item.val()["statistics"]}
        return None
    except TypeError as e:
        return None
        
def retrieve_project_id(username,role):
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    try:
        all_project = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").get()
        return all_project.val()["counter"]+1 #if got counter, return counter+1
    except TypeError as e:#if no counter, set counter as 1
        return 1
    except KeyError as e:
        return 1
        
def retrieve_item_id(username,project_id,role):
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    project_id = str(project_id)
    try:
        all_project_item = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child(project_id).get()
        return all_project_item.val()["counter"]+1
    except KeyError as e:#if no counter, set counter as 1
        return 1 
    except TypeError as e:
        return 1 
        
def set_project_item(username,project_id,item_id,item_information,role):
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    project_id = str(project_id)
    item_id = str(item_id)
    user = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child(project_id).get()
    category = user.val()["category"]
    item_information["imageurl"] = generate_image_for_item(category)
    if item_information["id"] == 1:
        database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child(project_id).update({"counter":1})
    else:
        database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child(project_id).update({"counter":item_information["id"]})
    database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child(project_id).child("items").child(item_id).update(item_information)

def generate_image_for_item(query):
    # get the API KEY here: https://developers.google.com/custom-search/v1/overview
    API_KEY = "AIzaSyB3EuVdoM4dHQCUwEYScbvbnxiXGXObdnc"
    # get your Search Engine ID on your CSE control panel
    SEARCH_ENGINE_ID = "92c7cbcd5818645e5"

    startIndex = "1"
    print(f"query = {query}")
    searchUrl = "https://www.googleapis.com/customsearch/v1?q=" + \
        query + "&start=" + startIndex + "&key=" + API_KEY + "&cx=" + SEARCH_ENGINE_ID + \
        "&searchType=image"
    r = requests.get(searchUrl)
    response = r.content.decode('utf-8')
    result = json.loads(response)
    random_number = random.randint(0, (len(result['items'])-1))
    return result['items'][random_number]['link']

def retrieve_all_project_items(username,project_id,role):
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    try:
        all_project_items = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child(project_id).child("items").get()
        all_project_items_list = []
        if len(all_project_items.val()) == 1 or len(all_project_items.val()) == 2:#if there is only 1 item in the list
            for item in all_project_items.val():            
                #all_project_items_list.append({"id":all_project_items.val()[item]["id"],"name":all_project_items.val()[item]["name"],"brand":all_project_items.val()[item]["brand"],"price":all_project_items.val()[item]["price"],"gender":all_project_items.val()[item]["gender"],"age_group":all_project_items.val()[item]["age_group"],"imageurl":all_project_items.val()[item]["imageurl"]})
                if item != None:
                    all_project_items_list.append({"id":item["id"],"name":item["name"],"category":item["category"],"imageurl":item["imageurl"]})
                    #print(all_project_items_list)
            return all_project_items_list
        for item in all_project_items.val():
            if item != None:
                all_project_items_list.append({"id":item["id"],"name":item["name"],"category":item["category"],"imageurl":item["imageurl"]})#all_project_items_list.append({"id":all_project_items.val()[item]["id"],"name":all_project_items.val()[item]["name"],"brand":all_project_items.val()[item]["brand"],"price":all_project_items.val()[item]["price"],"gender":all_project_items.val()[item]["gender"],"age_group":all_project_items.val()[item]["age_group"],"imageurl":all_project_items.val()[item]["imageurl"]})
                #print(all_project_items_list)
        return all_project_items_list
    except TypeError as e:
        return []     


def retrieve_issue_id(username,role):
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    try:
        all_issues = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("issues").get()
        return all_issues.val()["counter"]+1
    except TypeError as e:
        return 1 

def retrieve_issue_id(username):
    try:
        all_issues = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("issues").get()
        return all_issues.val()["counter"]+1
    except TypeError as e:
        return 1 

def retrieve_all_user_issues(username,role):
    user_role = "users"
    if role == "demo_user":
        user_role = "demo_users"
    try:
        all_issues = database.child(user_role).child(hashlib.sha256(username.encode()).hexdigest()).child("issues").child("userissues").get()
        all_issues_list = []
        if len(all_issues.val()) == 1:#if there is only 1 item in the list
            for proj in all_issues.val():
                all_issues_list.append({"id":all_issues.val()[proj]["id"],"status":all_issues.val()[proj]["status"],"description":all_issues.val()[proj]["description"],"images":all_issues.val()[proj]["images"]})
            return all_issues_list
        for issue in all_issues.val():
            if issue != None:
                all_issues_list.append({"id":issue["id"],"status":issue["status"],"description":issue["description"],"images":issue["images"]})
        return all_issues_list
    except TypeError as e:
        return []        


       
def upload_issue(username,uploaded_files,issue_information):
    if issue_information["id"] == 1:
        database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("issues").set({"counter":1})
    else:
        database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("issues").update({"counter":issue_information["id"]})
    uploaded_files_url = []
    for file in uploaded_files:
        if file.filename == "":
            temp_file = storage.child("temp.png").get_url(None)
            local_filename, headers = urllib.request.urlretrieve(temp_file)
            storage.child("issues").child(hashlib.sha256(username.encode()).hexdigest()).child(str(retrieve_issue_id(username))).child("temp.png").put(local_filename)
            file_url = storage.child("issues").child(hashlib.sha256(username.encode()).hexdigest()).child(str(retrieve_issue_id(username))).child("temp.png").get_url(None)
            uploaded_files_url.append(file_url)
        else:    
            #for file in uploaded_files:
            storage.child("issues").child(hashlib.sha256(username.encode()).hexdigest()).child(str(retrieve_issue_id(username))).child(file.filename).put(file)
            file_url = storage.child("issues").child(hashlib.sha256(username.encode()).hexdigest()).child(str(retrieve_issue_id(username))).child(file.filename).get_url(None)
            uploaded_files_url.append(file_url)
    issue_information["images"] = uploaded_files_url
    database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("issues").child("userissues").child(issue_information["id"]).set(issue_information)
    
    database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("issues").child("userissues").child(issue_information["id"]).update({"reportdate":datetime.now().strftime("%d/%m/%Y %H:%M")})

def last_created_date(report_date):
    expiry_date = datetime.strptime(report_date,"%d/%m/%Y %H:%M")
    today_date = datetime.strptime(datetime.now().strftime("%d/%m/%Y %H:%M"),"%d/%m/%Y %H:%M")
    remainder_day = today_date - expiry_date
    if remainder_day.days == 0:
        if (remainder_day.seconds / 60) < 60:
            return (str(int(remainder_day.seconds /60)) + " minutes ago")
        else:
            return (str(int(remainder_day.seconds /3600)) + " hours ago")
    elif remainder_day.days > 30 and remainder_day.days < 365:
        return (str(int(remainder_day.days /30)) + " months ago")
    elif remainder_day.days > 365:
        return (str(int(remainder_day.days /365)) + "." + str(int(remainder_day.days % 365)) + " years ago")
    elif (remainder_day.days) < 30:
        return (str(remainder_day.days) + " days ago")

def report_date_in_timestamp(report_date):
    dt_obj = datetime.strptime(report_date,'%d/%m/%Y %H:%M')
    return dt_obj.timestamp()

def retrieve_all_issues_for_problem_reported():
    all_user = database.child("users").child().get()
    issue_list = []
    current_issues = {}
    for user in all_user.each():
        try:
            #print(user.val()["issues"]["userissues"])
            for issue in user.val()["issues"]["userissues"]:
                if issue != None:
                    #all_issues.update(user.val()["username"]:{all_issues})
                    if issue["status"] == "Processing":
                        status = "images/active.png"
                        actiontext = "Close"
                    else:
                        status = "images/closed.png"
                        actiontext = "Delete"
                    userhash = hashlib.sha1(user.val()["username"].encode()).hexdigest()
                    print(issue["reportdate"])
                    print(report_date_in_timestamp(issue["reportdate"]))
                    issue_list.append({"fullname":user.val()["firstname"]+" "+user.val()["lastname"],"status":status,"id":issue["id"],"datereported":last_created_date(issue["reportdate"]),"timestamp":report_date_in_timestamp(issue["reportdate"]),"description":issue["description"][:28],"description2":issue["description"],"images":issue["images"],"actiontext":actiontext,"actiontext2":actiontext + " Issue","actiontext3":actiontext + " this issue?","actionmodaltarget":"#amodal"+userhash,"actionmodalbox":"amodal"+userhash,"actionbutton":user.key()+";"+str(issue["id"]),"bs_id":"accord"+userhash + str(issue["id"]),"bs_target":"#accord"+userhash + str(issue["id"]),"aria_control":"accord"+userhash + str(issue["id"]) })
        except KeyError as e:
            continue
    return issue_list
 
def retrieve_all_issues_count():
    all_user = database.child("users").child().get()
    current_issues = {"active":0,"closed":0}
    for user in all_user.each():
        try:
            #print(user.val()["issues"]["userissues"])
            for issue in user.val()["issues"]["userissues"]:
                if issue != None:
                    #all_issues.update(user.val()["username"]:{all_issues})
                    if issue["status"] == "Processing":
                        current_issues["active"] += 1
                    else:
                        current_issues["closed"] += 1
        except KeyError as e:
            continue
    return current_issues
    

def update_issue_status(action):
    username = action.split(";")[0]
    issue_id = action.split(";")[1]
    user_issue = database.child("users").child(username).child("issues").child("userissues").child(issue_id).get()
    if user_issue.val()["status"] == "Processing":
        database.child("users").child(username).child("issues").child("userissues").child(issue_id).update({"status":"Resolved"})
        return "closed"
    else:
        user = database.child("users").child(username).get()
        delete_id = user.val()["deleteid"]
        decrypted_key = get_decrypted_id(delete_id,user.val()["username"])
        deleted_user = auth.sign_in_with_email_and_password(user.val()["username"],decrypted_key)     
        issue = database.child("users").child(username).child("issues").child("userissues").child(issue_id).get()
        for image in issue.val()["images"]:  
            delete_file = image.replace("%2F","/")[71:]
            delete_file = delete_file.split("?")[0]
            storage.delete(delete_file,deleted_user["idToken"])        
        database.child("users").child(username).child("issues").child("userissues").child(issue_id).remove()
        return "deleted"

def upload(filename,file):
    storage.child(filename).put(file)          
    
def get_category_for_dropdown():
    categories = database.child("category").get()
    return categories.val()
    
def get_category_for_algorithm(username,project_id,item_id):
    project_id = str(project_id)
    item_id = str(item_id)
    item = database.child("users").child(hashlib.sha256(username.encode()).hexdigest()).child("projects").child("userprojects").child(project_id).child("items").child(item_id).get()
    category1 = item.val()["category"]
    category2 = item.val()["tcategory"]
    return category1,category2    
    
def get_dataset_from_storage(project_name=""):
    if project_name != "":
        try:
            url = storage.child(project_name).get_url(None)
            return url
        except Exception as e:
            print(e)
            return None
    url = storage.child("main_dataset.csv").get_url(None)  # getting the url from storage
    return url
    
def check_if_company_name_unique(company):
    all_users = database.child("users").get()
    all_sign_users = database.child("sign_up_users").get()
    lists_of_all_company_used = []
    try:
        for user in all_users.each():
            lists_of_all_company_used.append(user.val()["company"].lower())
    except Exception as e:
        print(e)
        
    try:
        for user in all_sign_users.each():
            lists_of_all_company_used.append(user.val()["company"].lower())
    except Exception as e:
        print(e)
    print(lists_of_all_company_used)
    return company.lower() not in lists_of_all_company_used
