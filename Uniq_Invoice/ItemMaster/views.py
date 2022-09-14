from ast import Return
from mmap import PAGESIZE
from operator import inv
from tkinter import Y
from urllib import request
from django.shortcuts import render,redirect,HttpResponse
from ItemMaster.models import*
import datetime
from datetime import datetime
from django.contrib import messages
# from .models import Login_Master
from UniQInvoice.models import Company_Master
from UniQInvoice.models import Login_Master

import random
from datetime import date
from datetime import timedelta

import json
from django.http import HttpResponse
from django.http import JsonResponse


from django.db.models.functions import TruncMonth
import pandas as pd
from django.db.models import Count, Sum, Case, When
from django.db import connection


from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
# import mysql.connector
# Create your views here.

def ry(request):

    tid= Item_Master.objects.filter(IsDeleted='0')

    return render(request,"try.html",{'tid':tid})

def Login_change_psw(request):
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    if request.method== "GET":
       
        return render(request,"login-user-change-password.html",{'lid':lid,'companyname':companyname})
    elif request.method=="POST" :
        lid = Login_Master.objects.get(id = request.session['id'])
        login_user_psw=lid.Password
        old_password=request.POST['oldpassword']
        if login_user_psw == old_password :
            new_password=request.POST['Password']
            c_password=request.POST['Cpassword']
            if new_password == c_password :
                login_user_psw.password=new_password
                login_user_psw.save()
            messages.error(request,'Sucessfully update your Password ', extra_tags = 'AddItem')
            return redirect('/user_data/') 
        else:
            messages.error(request,'Invalid Old Password ', extra_tags = 'deleteItem') 
            return render(request,"login-user-change-password.html",{'lid':lid,'companyname':companyname})


def add_item(request):
    if 'id'  in request.session:
    
    
        if request.method== "POST":
            
            warehousename=request.POST.get('warehousename')
            itemname=request.POST.get('itemname')
            vehicletype=request.POST.get('vehicletype')
            itemdescription=request.POST.get('itemdescription')
            modelname=request.POST.get('modelname')
            manufecturedate=request.POST.get('manufectuerdate')
            # print(" manufecturedate : ", manufecturedate) 
            receivingdata=request.POST.get('receivingdate')
            DPprice=request.POST.get('dpprice')
            mrp=request.POST.get('mrp')
            Batterytype=request.POST.get('battery')
            Ampear=request.POST.get('ampear')
            Quantity=request.POST.get('quantity')
            CreatedDate=datetime.datetime.now()
            ModifiedDate=datetime.datetime.now()
            # print("warehousenam = ", warehousename)
            # cid = request.session['id']
            # print('cid : -[',cid)
            # companyid = Company_Master.objects.get(id=cid)
            lid = Login_Master.objects.get(id = request.session['id'])
            companyname = Company_Master.objects.get(id = lid.Company_id_id)
            
            # wid= Warehouse_Master.objects.filter(IsDeleted='0',company_id=companyname,warehouse_name=warehousename)
            # for i in wid :
                # print(i.id)
            # ware_data =  Warehouse_Master.objects.filter(id = warehousename,)
            ware_data= Warehouse_Master.objects.get(warehouse_name =warehousename )
            # print("wid :" ,ware_data )

            Item_Master.objects.create(        
                                                company_id = companyname,
                                                warehouse_id = ware_data,
                                                vehicle_type=vehicletype,
                                                item_name = itemname,
                                                item_description = itemdescription,
                                                model_name = modelname,
                                                manufecture_date = manufecturedate,
                                                receiving_data = receivingdata,
                                                DP_price = DPprice,
                                                MRP = mrp,
                                                Battery_type = Batterytype,
                                                Ampear = Ampear,
                                                Quantity = Quantity,
                                                IsDeleted = '0',
                                                IsActive ='1',
                                                CreatedBy ='uniq',
                                                CreatedDate = CreatedDate,
                                                ModifiedBy = 'warehose owner',
                                                ModifiedDate = ModifiedDate
                                            )
            messages.error(request,'Sucessfully Added Item', extra_tags = 'AddItem')
            wid= Warehouse_Master.objects.filter(IsDeleted='0') 
            tid= Item_Master.objects.filter(IsDeleted='0')
            return redirect('/display/')

        else:
            
            tid= Item_Master.objects.filter(IsDeleted='0')
            lid = Login_Master.objects.get(id = request.session['id'])
            companyname = Company_Master.objects.get(id = lid.Company_id_id)
            wid= Warehouse_Master.objects.filter(IsDeleted='0',company_id=companyname)
            # for i in wid:
            #     print("i = ",i.id)
           
            return render(request,"Item-Master.html",{ 'companyname':companyname,'wid':wid,'tid':tid})
    else:
       return redirect('/companylogin/')
        


def display(request):
     if 'id'  in request.session:
    
        
       
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        tid= Item_Master.objects.filter(IsDeleted='0',company_id=companyname)
        wid= Warehouse_Master.objects.filter(IsDeleted='0',company_id=companyname) 
        # print("tid   =  ",tid)       
        return render(request,"Item-Master_data.html",{ 'wid':wid,'tid':tid,'companyname':companyname})
     else:
       return redirect('/companylogin/')


def itemedit(request,pk):
    
        if request.method=="GET":
            
            L_id = Login_Master.objects.get(id=request.session['id'])
        
            companyname = Company_Master.objects.get(id=L_id.Company_id_id)
            warehousedata = Warehouse_Master.objects.filter(company_id_id = companyname.id)
            
            imt= Item_Master.objects.get(id = pk)
            itm_mdate= imt.manufecture_date
            itm_rdate=imt.receiving_data
            m_date = itm_mdate.strftime("%Y-%m-%d") # "%m/%d/%Y"
            r_date =itm_rdate.strftime("%Y-%m-%d")
            print("itm_mdate",itm_mdate)
            print("date and time:",m_date)	
            print("date and time:",r_date)	
            return render (request,"Item-master_edit.html",{"warehousedata":warehousedata,"imt":imt,'itm_mdate':itm_mdate,'r_date':r_date,'m_date':m_date,'itm_rdate':itm_rdate,'itm_date': itm_mdate,'companyname':companyname})
        elif request.method=="POST":
            waerhouse=request.POST['warehousename']
            vehicletype=request.POST['vehicletype']
            itemname=request.POST['itemname']
            itemdescription=request.POST['itemdescription']
            modelname=request.POST['modelname']
            manufecturedate=request.POST['manufectuerdate']
            print(" manufecturedate : ", manufecturedate)
            receivingdata=request.POST['receivingdate']
            DPprice=request.POST['dpprice']
            mrp=request.POST['mrp']
            Batterytype=request.POST['battery']
            Ampear=request.POST['ampear']
            Quantity=request.POST['quantity']
 

            imt= Item_Master.objects.get(id = pk)
            warehousedata = Warehouse_Master.objects.get(warehouse_name = waerhouse)
            imt.warehouse_id=warehousedata
            imt.item_name=itemname
            imt.vehicle_type=vehicletype
            imt.item_description=itemdescription
            imt.model_name=modelname
            imt.manufecture_date=manufecturedate
            print(" imt.manufecture_date : ", imt.manufecture_date)
            imt.receiving_data=receivingdata
            imt.DP_price=DPprice
            imt.MRP=mrp
            imt.Battery_type=Batterytype
            imt.Ampear=Ampear
            imt.Quantity=Quantity

            imt.save()
            messages.error(request,'Sucessfully Update Item', extra_tags = 'AddItem')
            tid= Item_Master.objects.filter(IsDeleted='0')
            return redirect('/display/')

def delete_data(request,pk):
    
    print(pk)
    itm= Item_Master.objects.get(id = pk)
    itm.IsDeleted=1
    itm.save()
    messages.error(request,'Sucessfully Deleted Item', extra_tags = 'deleteItem')
    tid= Item_Master.objects.filter(IsDeleted='0')
    return redirect('/display/')
    

def warehouse(request):
    if 'id'  in request.session:
        if request.method== "POST":
            warehousename=request.POST.get('warehousename')
            warehouseadd=request.POST.get('Warehouse_Add')
            CreatedDate=datetime.datetime.now()
            ModifiedDate=datetime.datetime.now()

            # C_id = Company_Master.objects.get(id=request.session['id'])
            
            L_id = Login_Master.objects.get(id=request.session['id'])
        
            cid = Company_Master.objects.get(id=L_id.Company_id_id)


            Warehouse_Master.objects.create(    
                                        company_id_id =cid.id,
                                        warehouse_name= warehousename,
                                        warehouse_address=warehouseadd,
                                        IsDeleted = '0',
                                        IsActive ='1',
                                        CreatedBy ='uniq',
                                        CreatedDate = CreatedDate,
                                        ModifiedBy = 'warehose owner',
                                        ModifiedDate = ModifiedDate
            )
            messages.error(request,'Sucessfully Added warehouse', extra_tags = 'AddItem')
            # print("sucessfully registerd ") 
            # wid= Warehouse_Master.objects.filter(IsDeleted='0')
            return redirect('/warehouseshow/')

            # return render(request,"Warehouse-Master.html",{'wid':wid})
           
        else:
            # wid= Warehouse_Master.objects.filter(IsDeleted='0')
            return redirect('/warehouseshow/')
            
    else:
        return redirect('companylogin')
def warehouseshow(request):
    if 'id'  in request.session:
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        wid= Warehouse_Master.objects.filter(IsDeleted='0',company_id=companyname) 
        return render(request,"Warehouse-Master.html",{'wid':wid,'companyname':companyname})
    else:
        return redirect('companylogin')


def warehouse_edit(request,pk):

        if request.method=="GET":
            ware_edit= Warehouse_Master.objects.get(id = pk)
            lid = Login_Master.objects.get(id = request.session['id'])
            companyname = Company_Master.objects.get(id = lid.Company_id_id)
            return render (request,"Warehouse-Master_edit.html",{"ware_edit":ware_edit,'companyname':companyname})
        elif request.method=="POST":
            
            warehousename=request.POST['warehousename']
            warehouseaddress=request.POST['Warehouse_Add']

            ware_edit= Warehouse_Master.objects.get(id = pk)
            ware_edit.warehouse_name=warehousename
            ware_edit.warehouse_address=warehouseaddress
          
            ware_edit.save()
            messages.error(request,'Sucessfully Update warehouse', extra_tags = 'AddItem') 
            return redirect('/warehouseshow/')
def delete_warehouse(request,pk):
    
    # print(pk)
   
    ware_delete= Warehouse_Master.objects.get(id = pk)
    ware_delete.IsDeleted=1
    ware_delete.save()
    messages.error(request,'Sucessfully Deleted Warehouse', extra_tags = 'deleteItem')
    return redirect('/warehouseshow/')



def user (request ) :
    if 'id'  in request.session:
        if request.POST:
  
            firstname=request.POST.get('firstname')
            lastname=request.POST.get('lastname')
            phoneno=request.POST.get('Mob_num')
           
            email=request.POST.get('email')
            password=request.POST.get('Password')
            cpassword=request.POST.get('Cpassword')
            CreatedDate=datetime.datetime.now()
            ModifiedDate=datetime.datetime.now()
            # print("warehousenam = ", warehousename)

            if password == cpassword :
            
                L_id = Login_Master.objects.get(id=request.session['id'])
        
                cid = Company_Master.objects.get(id=L_id.Company_id_id)

                User_Master.objects.create(     company_id_id= cid.id,
                                                    First_name = firstname,
                                                    Last_name = lastname,
                                                    phone_number = phoneno,
                                                    email_address = email,
                                                    password = password,
                                                    IsDeleted = '0',
                                                    IsActive ='1',
                                                    CreatedBy ='user',
                                                    CreatedDate = CreatedDate,
                                                    ModifiedBy = 'Customer',
                                                    ModifiedDate = ModifiedDate
                                                )
                messages.error(request,'Sucessfully Added', extra_tags = 'AddItem')
                # print("sucessfully registerd ") 
                return redirect('/user_data/')
                
                # uid= User_Master.objects.filter(IsDeleted='0')
                # lid = Login_Master.objects.get(id = request.session['id'])
                # companyname = Company_Master.objects.get(id = lid.Company_id_id)
                # return render(request,"User-Master-data.html",{ 'uid':uid ,'companyname':companyname})
            
            else:
                return render(request,"user-master.html",{ 'error':'password does not match' })
        else:
            return render (request ,"user-master.html")
    else:
        return redirect('/companylogin/')


def user_data(request):
    if 'id'  in request.session:
       
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        uid= User_Master.objects.filter(IsDeleted='0',company_id=companyname)
        return render(request,"User-Master-data.html",{'uid':uid,'companyname':companyname})
    else:
       return redirect('/companylogin/') 


def user_edit (request,pk ) :
    if request.method=="GET":
            u_edit= User_Master.objects.get(id = pk)
            lid = Login_Master.objects.get(id = request.session['id'])
            companyname = Company_Master.objects.get(id = lid.Company_id_id)
            return render (request,"User-Master-edit.html",{"u_edit":u_edit,'companyname':companyname})
    elif request.method=="POST":
            fname=request.POST['firstname']
            lname=request.POST['lastname']
            phone=request.POST['Mob_num']
            email=request.POST['email']
          
            # print("warehousenam = ", warehousename)
            u_edit= User_Master.objects.get(id = pk)
           
            u_edit.First_name=fname
            u_edit.Last_name=lname
            u_edit.phone_number=phone
            u_edit.email_address=email
           
            u_edit.save()
            messages.error(request,'Sucessfully Update ', extra_tags = 'AddItem')
            return redirect('/user_data/')
            
            # uid= User_Master.objects.filter(IsDeleted='0')
            # return render(request,"User-Master-data.html",{'uid':uid })



def delete_user(request,pk):
    
   
    u_delete= User_Master.objects.get(id = pk)
    u_delete.IsDeleted=1
    u_delete.save()
    messages.error(request,'Sucessfully Deleted ', extra_tags = 'deleteItem')
    return redirect('/user_data/')
    # uid= User_Master.objects.filter(IsDeleted='0')
    # return render(request,"User-Master-Data.html",{'uid':uid,'u_delete':u_delete})




def Stock_Add(request,pk):
    if request.method ==  "GET" :
        
        itm = Item_Master.objects.get(id=pk)
        tid= Item_Master.objects.filter(IsDeleted='0')
        wid= Warehouse_Master.objects.filter(IsDeleted=0)
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        return render(request,"add_stock.html",{'itm':itm,'tid':tid,'wid':wid,'companyname':companyname})
    else:
       
        warehouse_name=request.POST['warehousename']
        
        Quantity=request.POST['quantity']

        Arrving_Date=request.POST['arrvingdate'] 
        itm = Item_Master.objects.get(id=pk)
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
       
        wareid= Warehouse_Master.objects.get(id=warehouse_name)
        Stock.objects.create(   company_id =companyname,
                                Item_id = itm ,
                                Warehouse_id = wareid,
                                Quantity    =  Quantity,
                                Arrving_Date = Arrving_Date ,
        )
        itm = Item_Master.objects.get(id=pk)
        qty=itm.Quantity
        itm.Quantity=int(qty)+int(Quantity)
        itm.save()
        messages.error(request,'Sucessfully Added Stock ', extra_tags = 'AddItem')
        return redirect('/display/')
        # wid= Warehouse_Master.objects.filter(IsDeleted=0)
        # tid= Item_Master.objects.filter(IsDeleted='0')
       
        # return render(request,"Item-Master_data.html",{'tid':tid,'wid':wid})



def change_password(request,pk):
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    if request.method== "GET":
       

        uid = User_Master.objects.get(id=pk)
        return render(request,"change-password.html",{'uid':uid,'companyname':companyname})
    elif request.method=="POST" :
        uid = User_Master.objects.get(id=pk)
        user_psw=uid.password
        old_password=request.POST['oldpassword']
        if user_psw == old_password :
            new_password=request.POST['Password']
            c_password=request.POST['Cpassword']
            if new_password == c_password :
                uid.password=new_password
                uid.save()
            messages.error(request,'Sucessfully update your Password ', extra_tags = 'AddItem')
            return redirect('/user_data/') 
        else:
            messages.error(request,'Invalid Old Password ', extra_tags = 'deleteItem') 
            return render(request,"change-password.html",{'uid':uid,'companyname':companyname})
    # uid= User_Master.objects.filter(IsDeleted='0')
    # return render(request,"User-Master-Data.html",{'uid':uid})



def Add_Payment_Master(request,pk):
    Due_Payment=0
    if 'id' in request.session:
  
        if request.method ==  "GET" :
        
           
            inv_details_data=INVOICE_MASTER.objects.get(id=pk)
            # print(" inv_details_data--- ",inv_details_data)
            # print("inv_details_data------",inv_details_data.Invoiceid.DealerId)
            lid = Login_Master.objects.get(id = request.session['id'])
            companyname = Company_Master.objects.get(id = lid.Company_id_id)
            return render(request,"add-payment.html",{'inv_details_data':inv_details_data,'companyname':companyname})
        else:
        
            date=request.POST['arrvingdate']
            
            Amount=request.POST['amount']

            Payment_Type=request.POST['paymenttype'] 
            inv_details_data=INVOICE_MASTER.objects.get(id=pk)
            
            
            lid = Login_Master.objects.get(id = request.session['id'])
            companyname = Company_Master.objects.get(id = lid.Company_id_id)
           
            PAYMENT_MASTER.objects.create(  
                                    company_id=companyname,
                                    Invoice_Id =inv_details_data ,
                                    Dealer_Id =inv_details_data.DealerId,
                                    Payment_Id    =  Payment_Type,
                                    Amount = Amount ,
                                    Payment_Date=date,
                                    IsActive='1',
                                    IsDeleted='0',
            )
            PAYMENT_MASTER.objects.all()
            # inv_details=INVOICE_DETAILS.objects.get(id=pk)
            inv_data=INVOICE_MASTER.objects.get(id=pk)

            # print("------inv_details_data--------------",inv_details.Invoiceid.id)
            amt=inv_data.DueAmount
            print("amt    :",amt)
            print("Amount    :",Amount)
            inv_data.DueAmount=int(amt)-int(Amount)
            inv_data.save()
            return redirect('/Payment_Master/')
            # inv_details_data=INVOICE_DETAILS.objects.all()
            # return render(request,"Payment-Master-Data.html",{'inv_details_data':inv_details_data})
    else:
        return redirect('/companylogin/')

def Payment_Master(request):
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        inv_details_data=INVOICE_MASTER.objects.filter(company_id=companyname)
        
        return render(request,"Payment-Master-Data.html",{'inv_details_data':inv_details_data,'companyname':companyname})


def Payment_Details(request,pk):

    inv_data=INVOICE_MASTER.objects.get(id=pk)
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    payment_details=PAYMENT_MASTER.objects.filter(IsDeleted='0',Invoice_Id=inv_data)
        
    return render(request,"Payment-Details.html",{'payment_details':payment_details,'companyname':companyname})

def Edit_Payment(request,pk):
    if request.method=="GET":
            payment_edit= PAYMENT_MASTER.objects.get(id = pk)
            pdate= payment_edit.Payment_Date
            p_date = pdate.strftime("%Y-%m-%d")
            lid = Login_Master.objects.get(id = request.session['id'])
            companyname = Company_Master.objects.get(id = lid.Company_id_id)
            return render (request,"edit-payment.html",{ 'p_date':p_date,"payment_edit":payment_edit,'companyname':companyname})
    elif request.method=="POST":
            arrving_date=request.POST['arrvingdate']
            payment=request.POST['amount']
            payment_type=request.POST['paymenttype']
           
            payment_edit= PAYMENT_MASTER.objects.get(id = pk)
           
            payment_edit.Payment_Date=arrving_date
            payment_edit.Amount=payment
            payment_edit.Payment_Id=payment_type
           
            payment_edit.save()
            payment_details=PAYMENT_MASTER.objects.filter(IsDeleted='0',Invoice_Id=payment_edit.Invoice_Id.id)
            # payment_details=PAYMENT_MASTER.objects.filter(IsDeleted='0')
            return render(request,"Payment-Details.html",{'payment_details':payment_details})

def Payment_Delete(request,pk):
    Payment_delete= PAYMENT_MASTER.objects.get(id = pk)
    Payment_delete.IsDeleted=1
    Payment_delete.save()
    inv_data=PAYMENT_MASTER.objects.get(id=pk)
    print("  inv_data  ",inv_data.Invoice_Id.id)
    payment_details=PAYMENT_MASTER.objects.filter(IsDeleted='0',Invoice_Id=inv_data.Invoice_Id.id)
        
    return render(request,"Payment-Details.html",{'payment_details':payment_details})
    
def get_items_ajax(request):
    if request.method == "POST":
        item_id = request.POST['item_id']
        qty=request.POST.get('qty[]')
        print("itemid :------------------",qty)
      
        subject = Item_Master.objects.filter(id = item_id)
        print("subject------------",subject)
        for i in subject:
            name=i.DP_price
            print("name----------------------",name)
        item_data=list(subject.values())
        print
    return JsonResponse({'item_data':item_data}) 

def get_dealer_ajax(request):
    if request.method == "POST":
        dealer_id = request.POST['dealer_id']
        dealer = Dealer_Master.objects.filter(id = dealer_id)
      
        dealer_data=list(dealer.values())
        print("dealer_data-------------",dealer_data)
    return JsonResponse({'dealer_data':dealer_data}) 


  

def invoice_file(request):
    if request.method == "POST":
        in_no = request.POST.get('Invoice_Number')
        print("in_no :------------------------------------------------------------------------------",in_no)
        in_date = request.POST.get('invoice_date')
        in_duedate = request.POST.get('Invoice_Due_Date')
        dealer_Id = request.POST.get('dealer')
        Total_amt = request.POST.get('total_amount')
        po_Number = request.POST.get('invoice_po')
        Total_Tax = request.POST.get('tax')
        sub_total = request.POST.get('sub_total')
        Total_Tax_amt = request.POST.get('tax_amount')
        # qty = request.POST.get('item_Qty')
        CreatedDate=datetime.datetime.now()
        ModifiedDate=datetime.datetime.now()
        #    Qty=request.POST.getlist('qty[]')
        # Qty=request.POST.getlist('qty[]')
        # t=int(Total_amt)
        # tax=int(Total_Tax_amt)
        price=",".join(request.POST.getlist('price[]'))
        #    itm_Id=",".join(request.POST.getlist('id'))
       
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
       
        d_Id=Dealer_Master.objects.get(id=dealer_Id)
       
        INVOICE_MASTER.objects.create(
                                    company_id=companyname,
                                    InvoiceNo=in_no,
                                    InvoiceDate=in_date,
                                    InvoiceDueDate=in_duedate,
                                    DealerId=d_Id,
                                    TotalAmount=Total_amt,
                                    DueAmount=Total_amt,
                                    PoNumber=po_Number,
                                    SubTotal=sub_total,
                                    TaxAmount=Total_Tax_amt,
                                    TotalTax=Total_Tax,

                                    CreatedBy = "Bhargav",
                                    CreatedDate =CreatedDate,
                                    ModifiedBy = "Bhargav",
                                    ModifiedDate = ModifiedDate,
                                    IsDeleted='0'
                                    )

        invoice_data = INVOICE_MASTER.objects.filter(IsDeleted='0')
        for i in invoice_data:
            i_id=i.InvoiceNo
            # print(i_id)
            if i_id == in_no :
                # print(i.id)
                i_Id=INVOICE_MASTER.objects.get(id=i.id)

                PAYMENT_STATUS_MASTER.objects.create(
                                            company_id=companyname,
                                            Invoice_Id=i_Id,
                                            Total_Amount=Total_amt,
                                            Received_Amount='0',
                                            Full_Payment_Received_Date=in_duedate,
                                            IsDeleted='0',
                                            IsActive='1'
                                            )

       
        Qty= request.POST.getlist('qty[]')
        itm_Id = request.POST.getlist('id')
        itm=[]
        for i in itm_Id:
            Item_Id=Item_Master.objects.get(id=i)
            itm.append(Item_Id)
            
        

        item_dict=dict(zip(itm,Qty))
      
        for x, y  in item_dict.items():
            z=int(x.DP_price)*int(y)
            # cart=INVOICE_DETAILS.objects.filter(Item_id=x)
            # print(len(cart))
            # if len(cart)!=0:
            #     obj = INVOICE_DETAILS.objects.get(Item_id=x)
            #     print(obj)
            #     obj.Quantity=int(obj.Quantity)+1
            
            #     obj.save()
            # else:
        
            INVOICE_DETAILS.objects.create(
                                        company_id=companyname,
                                    Invoiceid=i_Id,
                                    Item_id=x,
                                    Quantity=y,
                                    Rate=z,
                                    ItemServiceNo=po_Number,
                                    IsDeleted='0'
                                    )


    
        messages.error(request,'Sucessfully created Invoice ', extra_tags = 'AddItem')
    return redirect("/Invoice_view/")

def Invoice_view(request):
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)

    all_invoice=INVOICE_MASTER.objects.filter(IsDeleted='0').order_by('-id')
    return render(request,"Invoice_view.html",{'all_invoice':all_invoice,'companyname':companyname})

import datetime
now = datetime.datetime.now().year
print(now)

def create_invoice(request):
       
        invoice_a = "INV"
        invoice_b = str(now)
        
        invoice_c = ' '.join([str(random.randint(0, 999)).zfill(6) for _ in range(1)])
        Invoice_no = invoice_a +invoice_b + invoice_c
        
        lid = Login_Master.objects.get(id = request.session['id'])
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",lid)
        c_id = Company_Master.objects.filter(id = lid.Company_id_id)
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        
        print("@@@@@@@@@@@",c_id)
        d_id = Dealer_Master.objects.filter(Company_id_id = lid.Company_id_id)
        print("```````````````````````````````````````````````",d_id)

        alldealer = Dealer_Master.objects.filter(IsDeleted='0')
        # allcustomer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='0')
        # print("allcustomer :-  ",allcustomer)
        allitem= Item_Master.objects.filter(IsDeleted = '0')
        print("tid  :-   ",allitem)
        
        for i in allitem:
            print(i)
        
        today = date.today()
        d1 = today.strftime("%b. %d, %Y")
        due_date = today + timedelta(days=15)
        Due_Date =due_date.strftime("%Y-%m-%d")
        return render(request,'invoicetest.html',{'allitem':allitem,'companyname':companyname,'c_id':c_id,'lid':lid,'d_id':d_id,'d1':d1,'Due_Date':Due_Date,'alldealer':alldealer,'Invoice_no':Invoice_no}) 

def delete_invoice(request,pk):
    print(pk)
    invoiceitem = INVOICE_DETAILS.objects.filter(Invoiceid = pk)
    delpayment = PAYMENT_MASTER.objects.filter(Invoice_Id=pk)
    delpaymentdetail = PAYMENT_MASTER.objects.filter(Invoice_Id=pk)
    
    
    invoicedelete = INVOICE_MASTER.objects.get(id = pk)
    print("invoicedelete",invoicedelete)
    for x in invoiceitem:
        if invoicedelete == x.Invoiceid :
            messages.error(request,"This Invoice can't Delete", extra_tags = 'Deleteinvoice')
            return redirect('/Invoice_view/')

    for x in delpayment:
        print("x.Invoice_Id : --------------------",x.Invoice_Id)

        if invoicedelete == x.Invoice_Id :
            messages.error(request,"This Invoice can't Delete", extra_tags = 'Deleteinvoice')
            return redirect('/Invoice_view/')

    for x in delpaymentdetail:
        print("x.Invoice_Id : --------------------",x.Invoice_Id)

        if invoicedelete == x.Invoice_Id :
            messages.error(request,"This Invoice can't Delete", extra_tags = 'Deleteinvoice')
            return redirect('/Invoice_view/')
    else:
        invoicedelete= INVOICE_MASTER.objects.get(id = pk)
        invoicedelete.IsDeleted=1            
        invoicedelete.save()
        messages.error(request,'Sucessfully Deleted Invoice ', extra_tags = 'Deleteinvoice')
    return redirect('/Invoice_view/')

def Invoice_item_del(request,pk):
    Invoice_item_delete= INVOICE_DETAILS.objects.get(id = pk)
    Invoice_item_delete.delete()
   
    return redirect(request.META['HTTP_REFERER'])




def Invoice_Edit(request,pk):
    inv_data=INVOICE_MASTER.objects.get(id=pk)
    payment = PAYMENT_MASTER.objects.filter(Invoice_Id=pk)

    for i in payment:
        if inv_data.id != i.Invoice_Id :
            messages.error(request,"This invoice can't Edit", extra_tags = 'Deleteinvoice')
            return redirect('/Invoice_view/')

    else:

    
        if request.method =="GET" :
            
            
        
            L_id = Login_Master.objects.get(id=request.session['id'])
                
            companyname = Company_Master.objects.get(id=L_id.Company_id_id)
            allitem= Item_Master.objects.filter(IsDeleted = '0')
            Items=INVOICE_DETAILS.objects.filter(IsDeleted = '0',Invoiceid=inv_data)
            itm_Id = request.POST.getlist('id')
            print("itm_Id----------------",itm_Id)
            Dealer_data = Dealer_Master.objects.filter(Company_id = companyname,IsDeleted = '0')
            i_date=inv_data.InvoiceDate
            i_due_date=inv_data.InvoiceDueDate
            invoice_date = i_date.strftime("%Y-%m-%d")
            invoice_Due_date = i_due_date.strftime("%Y-%m-%d")
           
            # print("inv_details_data-----------",inv_details_data)
            return render(request,"invoice-edit.html",{'inv_data':inv_data,'invoice_date':invoice_date,'invoice_Due_date':invoice_Due_date,'Dealer_data':Dealer_data,'companyname':companyname,'allitem':allitem,'Items':Items})
    
        elif     request.method=="POST" :
                inv_no=request.POST['Invoice_Number']
                inv_date=request.POST['invoice_date']
                inv_due_date=request.POST['Invoice_Due_Date']
                inv_po=request.POST['invoice_po']
                dealer=request.POST['dealer']
                total_amt=request.POST['total_amount']
                Due_Amount=request.POST['total_amount']
                Total_Tax=request.POST['tax']
                L_id = Login_Master.objects.get(id=request.session['id'])
                
                companyname = Company_Master.objects.get(id=L_id.Company_id_id)
                Items=INVOICE_DETAILS.objects.filter(IsDeleted = '0',Invoiceid=inv_data).delete()
                inv_data=INVOICE_MASTER.objects.get(id=pk)
                payment_s_master=PAYMENT_STATUS_MASTER.objects.get(Invoice_Id=inv_data)
                # print("payment_s_master-----------------------",payment_s_master)
               
                
                Qty= request.POST.getlist('qty[]')
              
                itm_Id = request.POST.getlist('id')
                print("itm_Id----------------",itm_Id)
                itm=[]
                for i in itm_Id:
                    Item_Id=Item_Master.objects.get(id=i)
                    itm.append(Item_Id)
                
            

              
                item_dict=dict(zip(itm,Qty))

                for x, y in item_dict.items():
                    # for i in itm:
                    #     pass
                    # if i != x :
                    z=int(x.DP_price)*int(y)
                
                    INVOICE_DETAILS.objects.create(
                                                company_id=companyname,
                                            Invoiceid=inv_data,
                                            Item_id=x,
                                            Quantity=y,
                                            Rate=z,
                                            ItemServiceNo=inv_po,
                                            IsDeleted='0'
                                            )
                   
                       
                   
                    
                    # Dealer_did = Dealer_Master.objects.get(id=Dealer_data)
                    try:
                        Dealer_data = Dealer_Master.objects.get(dealer_company_name=dealer)
                    except Dealer_Master.DoesNotExist:
                        Dealer_data = None
                        inv_data.DealerId=Dealer_data
                        inv_data.InvoiceNo=inv_no
                        inv_data.InvoiceDate=inv_date
                        inv_data.InvoiceDueDate=inv_due_date
                        inv_data.PoNumber=inv_po
                    
                        inv_data.TotalAmount=total_amt
                        inv_data.DueAmount=Due_Amount
                        inv_data.TotalTax=Total_Tax
                        payment_s_master.Total_Amount=total_amt
                        payment_s_master.save()
                    
                    
                        inv_data.save()
        
                messages.error(request,'Sucessfully Update Invoice ', extra_tags = 'AddItem')
        return redirect("/Invoice_view/")



def Create_Purchase_Order(request):
    po_a = "PO"
    po_b = str(now) 
    po_c = ' '.join([str(random.randint(0, 999)).zfill(6) for _ in range(1)])
    po_no = po_a + po_b + po_c
    
    lid = Login_Master.objects.get(id = request.session['id'])
   
    c_id = Company_Master.objects.filter(id = lid.Company_id_id)
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    
    d_id = Dealer_Master.objects.filter(Company_id_id = lid.Company_id_id)
   

    alldealer = Dealer_Master.objects.filter(IsDeleted='0')
   
    allitem= Item_Master.objects.filter(IsDeleted = '0')
    print("tid  :-   ",allitem)
    
    for i in allitem:
        print(i)
    
    today = date.today()
    d1 = today.strftime("%b. %d, %Y")
    due_date = today + timedelta(days=15)
    Due_Date =due_date.strftime("%Y-%m-%d")
    return render(request,"create-purchase-order.html",{'allitem':allitem,'companyname':companyname,'c_id':c_id,'lid':lid,'d_id':d_id,'d1':d1,'Due_Date':Due_Date,'alldealer':alldealer,'po_no':po_no}) 

    # return render (request,"purchase-order.html")

def Purchase_Items(request):
    if request.method == "POST":
        Po_No=request.POST.get('po_Number')
        Po_Date=request.POST.get('po_date')
        dealer_id=request.POST.get('dealer')
        dealer_id=request.POST.get('dealer')
        Total_Tax = request.POST.get('tax')
        sub_total = request.POST.get('sub_total')
        Total_Tax_amt = request.POST.get('tax_amount')
        Total_amt = request.POST.get('total_amount')
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
       
        d_Id=Dealer_Master.objects.get(id=dealer_id)
        POMASTER.objects.create(
                        company_id      =  companyname,
                        Dealer_Id       =  d_Id,
                        PoNumber        =  Po_No,
                        PoDate          =  Po_Date,
                        SubTotal        =  sub_total,
                        GSTTax          =  Total_Tax,
                        TaxAmount       =  Total_Tax_amt,
                        PoTotalAmount   =  Total_amt
                      
        )

       
        Qty= request.POST.getlist('qty[]')
        itm_Id = request.POST.getlist('id')
        itm=[]
        for i in itm_Id:
            Item_Id=Item_Master.objects.get(id=i)
            itm.append(Item_Id)
            
        

        item_dict=dict(zip(itm,Qty))
        po_id=POMASTER.objects.get(PoNumber=Po_No)
        poid=po_id.id
        po_Id=POMASTER.objects.get(id=poid)
        for x, y  in item_dict.items():
            z=int(x.DP_price)*int(y)

            PODETAILSMASTER.objects.create(
                            company_id  =  companyname,
                            PO_Id       = po_Id,
                            ItemId      =  x,
                            QTY         =  y,
                            Amount      =  z,
            
            )
        messages.error(request,'Sucessfully Purchase Orderd ', extra_tags = 'AddItem')
    return redirect("/Purchase_Order/")

def  Purchase_Order(request):
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    Purchase_Order_data=POMASTER.objects.filter(IsDeleted=0,company_id=companyname).order_by('-id')
    return render(request,"purchase-order-list.html",{'companyname':companyname,'Purchase_Order_data':Purchase_Order_data})

def Po_item_del(request,pk):
    po_item_delete= PODETAILSMASTER.objects.get(id = pk)
    po_item_delete.delete()
   
    return redirect(request.META['HTTP_REFERER'])

def Edit_Purchase_Order(request,pk):
    Po_Data=POMASTER.objects.get(id=pk)
    
    
    if request.method =="GET" :
        
        
    
        L_id = Login_Master.objects.get(id=request.session['id'])
        
        companyname = Company_Master.objects.get(id=L_id.Company_id_id)
        allitem= Item_Master.objects.filter(IsDeleted = '0')
        Items=PODETAILSMASTER.objects.filter(IsDeleted = '0',PO_Id=Po_Data)
        itm_Id = request.POST.getlist('id')
        print("itm_Id----------------",itm_Id)
        Dealer_data = Dealer_Master.objects.filter(Company_id = companyname,IsDeleted = '0')
        P_date=Po_Data.PoDate
        Po_date = P_date.strftime("%Y-%m-%d")
        # Dealer_did = Dealer_Master.objects.get(dealer_company_name=dealer)
        # print("Dealer_data---------",Dealer_did)

        # d_id=Dealer_Master.objects.get(id=dealer)
        # print("d_id---------",d_id)
        # print("inv_details_data-----------",inv_details_data)
        return render(request,"Edit-purchase-order.html",{'Po_Data':Po_Data,'Po_date':Po_date,'Dealer_data':Dealer_data,'companyname':companyname,'allitem':allitem,'Items':Items})

    elif     request.method=="POST" :
            po_no=request.POST['po_Number']
            po_date=request.POST['po_date']
            dealer=request.POST.get('dealer')
            print("dealer----------------",dealer)
           
            sub_total=request.POST['sub_total']
            total_amt=request.POST['total_amount']
            tax_amount=request.POST['tax_amount']
            Total_Tax=request.POST['tax']
            L_id = Login_Master.objects.get(id=request.session['id'])
            
            companyname = Company_Master.objects.get(id=L_id.Company_id_id)
            Items=PODETAILSMASTER.objects.filter(IsDeleted = '0',PO_Id=Po_Data).delete()
            Po_Data=POMASTER.objects.get(id=pk)
           
            # print("payment_s_master-----------------------",payment_s_master)
               
            Dealer_data = Dealer_Master.objects.get(dealer_company_name=dealer)
            print("Dealer_data______________",Dealer_data)
            d_id=Dealer_Master.objects.get(id=Dealer_data.id)
            print("d_id----------------",d_id)
            Qty= request.POST.getlist('qty[]')
            print("Qty-----------------",Qty)
            itm_Id = request.POST.getlist('Itemname')
            print("itm_Id----------------",itm_Id)
            itm=[]
            for i in itm_Id:
                Item_Id=Item_Master.objects.get(item_name=i)
                Itm_Id=Item_Master.objects.get(id=Item_Id.id)
                itm.append(Itm_Id)
            
        

            
            item_dict=dict(zip(itm,Qty))

            for x, y in item_dict.items():
                # for i in itm:
                #     pass
                # if i != x :
                z=int(x.DP_price)*int(y)
            
                PODETAILSMASTER.objects.create(
                            company_id  =  companyname,
                            PO_Id       = Po_Data,
                            ItemId      =  x,
                            QTY         =  y,
                            Amount      =  z,
                )
                    

            
            Po_Data.Dealer_Id=d_id,
            Po_Data.PoNumber=po_no
            Po_Data.PoDate=po_date
            Po_Data.PoTotalAmount=total_amt
            Po_Data.GSTTax=Total_Tax
            Po_Data.TaxAmount=tax_amount
            Po_Data.SubTotal=sub_total
            Po_Data.Dealer_Id.save()
            Po_Data.save()
    
            messages.error(request,'Sucessfully Update Invoice ', extra_tags = 'AddItem')
    return redirect("/Invoice_view/")

def Purchase_Order_cancle(request,pk):

    Purchse_order=POMASTER.objects.get(id=pk)

    Purchse_order.IsDeleted=1
    Purchse_order.save()
    return redirect("/Purchase_Order/")

# reports

def invoice_summery_by_month(request):
    month_wise_count = INVOICE_MASTER.objects.annotate(month=TruncMonth('InvoiceDate')).values('month').annotate(c=Sum('TotalAmount')).values('month', 'c').order_by('month')                     # (might be redundant, haven't tested) select month and count 
    print("x :-------------",month_wise_count)
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    return render(request,"R_invoice_sum.html",{'month_wise_count':month_wise_count,'companyname':companyname})

def dealer_summery_by_month(request):
    
    dealer_wise_data = INVOICE_MASTER.objects.values('DealerId').annotate(Sum('TotalAmount'))
    print("y :--------------",dealer_wise_data)
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    return render(request,"R_dealer_sum.html",{'dealer_wise_data':dealer_wise_data,'companyname':companyname})

def Payment_Satus_per_invoice(request):
    inv_details_data=INVOICE_DETAILS.objects.all()
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)    
    return render(request,"R_Payment_Satus.html",{'inv_details_data':inv_details_data,'companyname':companyname})
    
def stock_model_wise(request):
    stock = Item_Master.objects.all()
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    return render(request,"R_stock_model.html",{'stock':stock,'companyname':companyname})

def vehicle(request):
    if request.method == "POST":
        selectedvel = request.POST['velinfo']
        print("itemid :------------------",selectedvel)
        vell = Item_Master.objects.filter(vehicle_type = selectedvel)
        print("subject------------",vell)
        # for i in vell:
        #     name=i.
        vehical_data=list(vell.values())
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        return JsonResponse({'vehical_data':vehical_data}) 
        
        # return render(request,"R_ledger.html")
    
def ledger(request):
    all_invoice = INVOICE_MASTER.objects.all()
    print("all invoice : ----------------------",all_invoice)
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    for i in all_invoice:
        print("shghdf :-----",i.id)
        payment_details=PAYMENT_MASTER.objects.filter(Invoice_Id_id=i.id)
        print("pament :- ",payment_details)
        
    return render(request,"R_ledger.html",{'all_invoice':all_invoice,'payment_details':payment_details,'companyname':companyname})

def purchace_order_pdf_view(request,pk):
    po_data=POMASTER.objects.get(id=pk)
    if request.method == "GET" :

        L_id = Login_Master.objects.get(id=request.session['id'])
        
        companyname = Company_Master.objects.get(id=L_id.Company_id_id)
        allitem= Item_Master.objects.filter(IsDeleted = '0')
        Items=PODETAILSMASTER.objects.filter(IsDeleted = '0',PO_Id=po_data)
        itm_Id = request.POST.getlist('id')
        print("itm_Id----------------",itm_Id)
        Dealer_data = Dealer_Master.objects.filter(Company_id = companyname,IsDeleted = '0')
        P_date=po_data.PoDate
        Po_date = P_date.strftime("%Y-%m-%d")
        # Dealer_did = Dealer_Master.objects.get(dealer_company_name=dealer)
        # print("Dealer_data---------",Dealer_did)

        # d_id=Dealer_Master.objects.get(id=dealer)
        # print("d_id---------",d_id)
        # print("inv_details_data-----------",inv_details_data)
        return render(request,"purchase-orderpdf.html",{'po_data':po_data,'Po_date':Po_date,'Dealer_data':Dealer_data,'companyname':companyname,'allitem':allitem,'Items':Items})


def Invoice_Pdf(request,pk):
    inv_data=INVOICE_MASTER.objects.get(id=pk)
   
    if request.method =="GET" :
     
        L_id = Login_Master.objects.get(id=request.session['id'])
            
        companyname = Company_Master.objects.get(id=L_id.Company_id_id)
        # allitem= Item_Master.objects.filter(IsDeleted = '0')
        Items=INVOICE_DETAILS.objects.filter(IsDeleted = '0',Invoiceid=inv_data)
        # itm_Id = request.POST.getlist('id')
        # print("itm_Id----------------",itm_Id)
        # Dealer_data = Dealer_Master.objects.filter(Company_id = companyname,IsDeleted = '0')
        i_date=inv_data.InvoiceDate
        i_due_date=inv_data.InvoiceDueDate
        invoice_date = i_date.strftime("%Y-%m-%d")
        invoice_Due_date = i_due_date.strftime("%Y-%m-%d")
        
        # print("inv_details_data-----------",inv_details_data)
        return render(request,"invoice-Pdf.html",{'inv_data':inv_data,'invoice_date':invoice_date,'invoice_Due_date':invoice_Due_date,'companyname':companyname,'Items':Items})
    


# creditnote
def creditnote_view(request):
    if 'id'  in request.session:
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        allcredit = CREDITNOTE_MASTER.objects.filter(IsDeleted = 0)      
        return render(request,"creditnote.html",{'companyname':companyname,'allcredit':allcredit})
    else:
        return redirect('/companylogin/')

def creditnote_add(request):
    if 'id' in request.session:
        allcredit = CREDITNOTE_MASTER.objects.filter(IsDeleted = 1) 
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        allcredit = CREDITNOTE_MASTER.objects.filter(IsDeleted = 1)
        alldealer = Dealer_Master.objects.filter(IsDeleted = 0)      
        print("alldealer -----------------",alldealer)
        return render(request,"creditnote_add.html",{'companyname':companyname,'allcredit':allcredit,'alldealer':alldealer})
    else:
        return redirect('/companylogin/')

def dealersinvoice(request):
    if request.method == "POST":
        selecteddealinfo = request.POST['dealinfo']
        print("selecteddealinfo :------------------",selecteddealinfo)
        vell = INVOICE_MASTER.objects.filter(DealerId = selecteddealinfo)
        print("vell : ---------------",vell)
        invoicedata = []
        for i in vell:
            a=i.InvoiceNo
            invoicedata.append({"invoice_number":a})
            print("subject------------",a)
        print("vehical_data---------------------------------------------------------------",invoicedata)
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        return JsonResponse({'invoicedata':invoicedata}) 
    
def get_invoice_data(request):
    if request.method == "POST":
        getinvoice = request.POST['selectedinvoice']
        print('selectedinvoice :-------------------',getinvoice)
        
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        
        inv = INVOICE_MASTER.objects.filter(InvoiceNo = getinvoice,company_id = companyname.id)
        print("in : ---------------",inv)
        allitems = []
        itemdetialdata = {}
        for x in inv:
            # print("x : --------",x.id)
            invdetail =INVOICE_DETAILS.objects.filter(Invoiceid =x.id)
            # print('invdetail : ------------',invdetail)
            for c in invdetail:
                # print("c : ============================",c.Item_id.id)
                detailitems= Item_Master.objects.filter(id =c.Item_id.id)
                # print("detailitems:_------------------------------------0--",detailitems)
                for k in detailitems:
                    print("k : --------------------------------",k.DP_price)
                    itemdetialdata={'id':k.id,'itemname':k.item_name,'itemdesc':k.item_description,'modelname':k.model_name,'ampear':k.Ampear,'price':k.DP_price}
                # itemdetial = itemdetialdata.append(detailitems)
                    print("itemdetialdata : ---------------------------------",itemdetialdata)
                    allitems.append(itemdetialdata)
                    print("allitems  : -------------------",allitems)
  
            
            invoicedetaildata=list(invdetail.values())
            print('invoicedetaildata : -----------------',invoicedetaildata)
            
            return JsonResponse({'invoicedetaildata':invoicedetaildata,'allitems':allitems}) 

def add_credit_items(request):
    if request.method == "POST":
        invoicenumber=request.POST.get('invoicenumber')
        x = INVOICE_MASTER.objects.get(InvoiceNo=invoicenumber)
        Itemid=request.POST.get('Itemid')
        z = Item_Master.objects.get(id=Itemid)
        itemname=request.POST.get('Itemname')
        itemdesc=request.POST.get('itemdesc')
        modelname=request.POST.get('modelname')
        ampear = request.POST.get('ampear')
        Quantity=request.POST.get('Quantity')
        price=request.POST.get('price')
        Rate=request.POST.get('Rate')
        dealer = request.POST.get('dealer')
        y = Dealer_Master.objects.get(id=dealer)
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        d1 = date.today()
        
        today = datetime.date.today()
        now = today.year
        
        print(now)
        cn_a = "CN"
        cn_b = str(now)
        
        cn_c = ' '.join([str(random.randint(0, 999)).zfill(6) for _ in range(1)])
        cn_no = cn_a +cn_b + cn_c
        
        print("cn_no : ------------",cn_no)
        
        CREDITNOTE_MASTER.objects.create(
            creditnumber=cn_no,
            company_id=companyname,
            Invoice_id=x,
            CreditNoteDate=d1,
            DealerId=y,
            CreditNoteAmount=Rate,
            IsDeleted=0,
            CreatedBy='Dhruvisha',
            CreatedDate=d1,
            ModifiedBy='Dhruvisha',
            ModifiedDate=d1,
            IsCancel=0
            
            
        )
        
        last_obj = CREDITNOTE_MASTER.objects.last()
        crditid = CREDITNOTE_MASTER.objects.get(id =last_obj.id)
        
        CREDITNOTE_DETAILS.objects.create(
            creditid=crditid,
            company_id=companyname,
            Invoiceid=x,
            Item_id=z,
            Quantity=Quantity,
            Rate=Rate,
            ItemServiceNo='12345',
            IsDeleted='0'

        )
    return redirect("/creditnote_view/")
    
    

   

def delete_credit_items(request):
   
    return redirect('/display/')

def select_credit_note(request,id):
    print("id: ------------------------",id)
    creditdata = CREDITNOTE_MASTER.objects.filter(id=id)
    print("creditdata  : ---------------------",creditdata)
    creditdetail = CREDITNOTE_DETAILS.objects.filter(creditid=id,IsDeleted=0)
    print("creditdetail : ---------------",creditdetail)

    return render(request,"creditnote_edit.html",{'creditdata':creditdata,'creditdetail':creditdetail})

def edit_credit_note(request,id):
    if request.method =="POST":
        dealer = request.POST.get('dealer')
        print("dealer : ---------------------",dealer)
        inno = request.POST.get('inno')
        print("inno : ---------------------",inno)
        creditdata = CREDITNOTE_MASTER.objects.filter(id=id)
        print("creditdata  : ---------------------",creditdata)
        creditdetail = CREDITNOTE_DETAILS.objects.filter(creditid=id,IsDeleted=0)
        print("creditdetail : ---------------",creditdetail)

    return render(request,"creditnote_edit.html",{'creditdata':creditdata,'creditdetail':creditdetail})
    # return redirect("/creditnote_view/")

def delete_credit_selecteditem(request,id):
    print(id)
    credititem = CREDITNOTE_DETAILS.objects.get(id = id)
    print("credititem",credititem)
    credititem.IsDeleted=1            
    credititem.save()
    messages.error(request,'Credit Note Deleted Successfully', extra_tags = 'successadded')

    return redirect('/select_credit_note/{credititem.Invoiceid}')
def cancel_credit_listitem(request,id):
    print(id)
    credititem = CREDITNOTE_MASTER.objects.get(id = id)
    print("credititem",credititem)
    credititem.IsCancel=1            
    credititem.save()
    messages.error(request,'Credit Note Canceled Successfully', extra_tags = 'successadded')
    return redirect("/creditnote_view/")
  
# reports

def invoice_summery_by_month(request):
    if 'id'  in request.session:
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        month_wise_count = INVOICE_MASTER.objects.annotate(month=TruncMonth('InvoiceDate')).values('month').annotate(c=Sum('TotalAmount')).values('month', 'c').order_by('month')                     # (might be redundant, haven't tested) select month and count 
        print("x :-------------",month_wise_count)

        return render(request,"R_invoice_sum.html",{'month_wise_count':month_wise_count,'companyname':companyname})
 

        wid= Warehouse_Master.objects.filter(IsDeleted='0',company_id=companyname) 
        return render(request,"Warehouse-Master.html",{'wid':wid,'companyname':companyname})
    else:
        return redirect('companylogin')

def dealer_summery_by_month(request):
    dealername = []
    deal = Dealer_Master.objects.filter(IsDealer = 1)
    # print("deal :---------------",deal.id)
    dealer_wise_data = INVOICE_MASTER.objects.values('DealerId').annotate(Sum('TotalAmount'))
    print("y :--------------",dealer_wise_data)
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    for i in dealer_wise_data:
        print("i : ==========",i)
        print(i.get('DealerId'))
        deal = Dealer_Master.objects.get(id=i.get('DealerId'))
        print("x :---------------",deal)
        dealername.append(deal)
        

    context={
        'dealer_wise_data':dealer_wise_data,
        'companyname':companyname,
        'dealername':dealername
    }
        
    print("dealername",dealername)
    return render(request,"R_dealer_sum.html",context)

def Payment_Satus_per_invoice(request):
    inv_details_data=INVOICE_DETAILS.objects.all()
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)    
    return render(request,"R_Payment_Satus.html",{'inv_details_data':inv_details_data,'companyname':companyname})
    
def stock_model_wise(request):
    
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    print('companyname: ------------ ',companyname.id)
    stock = Item_Master.objects.filter(IsDeleted = 0, company_id = companyname.id)
    print('stock : ---------------',stock)
    return render(request,"R_stock_model.html",{'stock':stock,'companyname':companyname})

def vehicle(request):
    if request.method == "POST":
        selectedvel = request.POST['velinfo']
        print("itemid :------------------",selectedvel)
        
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)

        vell = Item_Master.objects.filter(vehicle_type = selectedvel,IsDeleted = 0, company_id = companyname.id)
        vehical_data = []
        for i in vell:
        
            a=i.warehouse_id.warehouse_name
            b= i.model_name
            c=i.Quantity
            vehical_data.append({"modelname" :b,"stock":c,"warehousename":a})
        print("subject------------",a,b,c)
        print("vehical_data---------------------------------------------------------------",vehical_data)
        return JsonResponse({'vehical_data':vehical_data}) 
    
def ledger(request):
    all_invoice = INVOICE_MASTER.objects.all()
    print("all invoice : ----------------------",all_invoice)
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    for i in all_invoice:
        print("shghdf :-----",i.id)
        payment_details=PAYMENT_MASTER.objects.filter(Invoice_Id_id=i.id)
        print("pament :- ",payment_details)
        
    return render(request,"R_ledger.html",{'all_invoice':all_invoice,'payment_details':payment_details,'companyname':companyname})

def transactions(request):
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    itemslist = INVOICE_DETAILS.objects.filter(IsDeleted=0)
    print("itemslist  : -----------------------------",itemslist)
    paymentslist=[]
    for i in itemslist:
        payments  = PAYMENT_MASTER.objects.filter(Invoice_Id=i.Invoiceid,IsDeleted=0)
        paymentslist.append(payments)
    print("paymentslist : -------------------------------",paymentslist)

    return render(request,"R_transaction.html",{'itemslist':itemslist,'paymentslist':paymentslist,'companyname':companyname})
    
def item_report(request):
    itemsreport = {}
    poitems=[]
    initems=[]
    itemhtml=[]
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    itm = Item_Master.objects.filter(company_id=companyname,IsDeleted=0)

    for i in itm:
        poitm = PODETAILSMASTER.objects.filter(ItemId=i.id)
        for x in poitm:
            itemhtml.append(x)
    print("itemhtml : -----------------------------",itemhtml)

    for i in itm:
        total = INVOICE_DETAILS.objects.values('Item_id').annotate(Sum('Rate')).annotate(Sum('Quantity'))
    print("total : -------------------------",total)

    for q in itemhtml:
        print("a : ---------------------------------------------",q) 
        itemreport = {'ItemId':q.ItemId.id,'Itemname':q.ItemId.item_name,'QTY':q.QTY,'Amount':q.Amount}
        poitems.append(itemreport)
    print("poitems : ---------------------",poitems)
    

    return render(request,"R_month_item.html",{'companyname':companyname,'poitems':poitems,'total':total})

def profit_loss(request):
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    return render(request,"R_profit_loss.html",{'companyname':companyname})

def warehouseWise_stock(request):
    all_warehouse = Warehouse_Master.objects.filter(IsDeleted=0)
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    return render(request,"R_warehouse_stock.html",{'all_warehouse':all_warehouse,'companyname':companyname})

def item_report_ajex(request):
     if request.method == "POST":
        iteminfor = request.POST['iteminfo']
        print("iteminfor :------------------",iteminfor)
        item_data = []
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        if iteminfor == '0':
            print("in if   : ----------------------------")
            items = Item_Master.objects.filter(IsDeleted = 0, company_id = companyname.id)
            print("items : ---------------------------",items)
            for i in items:
                
                a=i.item_name
                b= i.Quantity
                c=i.warehouse_id.warehouse_name
                print("c  : --------------------------",c)
                item_data.append({"itemname" :a,"quantity":b,"price":c})
                                    # {"User_Name":"John Doe","score":"10","team":"1"}
                print("subject------------",a,b,c)

            # vehical_data=list([[a],[b],[c]])
            print("item_data---------------------------------------------------------------",item_data)
            return JsonResponse({'item_data':item_data}) 
    
        else:
            print("in else   : ----------------------------")
            items = Item_Master.objects.filter(warehouse_id = iteminfor,IsDeleted = 0, company_id = companyname.id)
            print("items : ---------------------------",items)
            
            for i in items:
            
                a=i.item_name
                b= i.Quantity
                c=i.warehouse_id.warehouse_name
                item_data.append({"itemname" :a,"quantity":b,"price":c})
                                    # {"User_Name":"John Doe","score":"10","team":"1"}
                print("subject------------",a,b,c)

            # vehical_data=list([[a],[b],[c]])
            print("item_data---------------------------------------------------------------",item_data)
        
            return JsonResponse({'item_data':item_data}) 
    
def low_stock(request):
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    items = Item_Master.objects.filter(Quantity__lte=10,IsDeleted = 0, company_id = companyname.id)
    print("items : ---------------------------",items)
    return render(request,"R_low_stock.html",{'items':items,'companyname':companyname})

def day_wise_saleitem(request):
    lid = Login_Master.objects.get(id = request.session['id'])
    companyname = Company_Master.objects.get(id = lid.Company_id_id)
    todaydate=date.today()
    print("todaydate  : ===============---------",todaydate)
    inmasdata=INVOICE_MASTER.objects.filter(InvoiceDate=todaydate,IsDeleted=0)
    print("inmasdata:------------",inmasdata)
    # for x in inmasdata:
    #     inmasdetail=INVOICE_DETAILS.objects.filter(Invoiceid=x.id)
    # print("inmasdetail : =--------------------",inmasdetail)
    return render(request,"R_daywisesale.html",{'companyname':companyname})