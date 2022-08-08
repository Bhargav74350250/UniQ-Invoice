from mmap import PAGESIZE
from tkinter import Y
from django.shortcuts import render,redirect,HttpResponse
from ItemMaster.models import*
import datetime
from datetime import datetime
# from .models import Login_Master
from UniQInvoice.models import Company_Master
from UniQInvoice.models import Login_Master




# Create your views here.

def add_item(request):
    if 'id'  in request.session:
    
    
        if request.method== "POST":
            
            warehousename=request.POST.get('warehousename')
            itemname=request.POST.get('itemname')
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
            CreatedDate=datetime.now()
            ModifiedDate=datetime.now()
            # print("warehousenam = ", warehousename)
            cid = Company_Master.objects.get(id=request.session['id'])
            print("Dates = ", manufecturedate, receivingdata)
            wid= Warehouse_Master.objects.get(id = warehousename)


            Item_Master.objects.create(        
                                                company_id = cid,
                                                warehouse_id = wid,
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
            print("sucessfully registerd ")
            wid= Warehouse_Master.objects.filter(IsDeleted='0') 
            tid= Item_Master.objects.filter(IsDeleted='0')
            return render(request,"Item-Master_data.html",{'wid':wid,'tid':tid})
        else:
            wid= Warehouse_Master.objects.filter(IsDeleted='0')
            tid= Item_Master.objects.filter(IsDeleted='0')
            # for i in wid:
            #     print("i = ",i.id)
            return render(request,"Item-Master.html",{'wid':wid,'tid':tid})
    else:
       return redirect('/companylogin/')
        


def display(request):
     if 'id'  in request.session:
    
        tid= Item_Master.objects.filter(IsDeleted='0') 
        print("tid   =  ",tid)       
        wid= Warehouse_Master.objects.filter(IsDeleted='0')
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        return render(request,"Item-Master_data.html",{ 'wid':wid,'tid':tid,'companyname':companyname})
     else:
       return redirect('/companylogin/')


def itemedit(request,pk):
    
        if request.method=="GET":
            
            L_id = Login_Master.objects.get(id=request.session['id'])
        
            cid = Company_Master.objects.get(id=L_id.Company_id_id)
            warehousedata = Warehouse_Master.objects.filter(company_id_id = cid.id)
            
            imt= Item_Master.objects.get(id = pk)
            itm_mdate= imt.manufecture_date
            itm_rdate=imt.receiving_data
            m_date = itm_mdate.strftime("%Y-%m-%d") # "%m/%d/%Y"
            r_date =itm_rdate.strftime("%Y-%m-%d")
            print("itm_mdate",itm_mdate)
            print("date and time:",m_date)	
            print("date and time:",r_date)	
            return render (request,"Item-master_edit.html",{"warehousedata":warehousedata,"imt":imt,'itm_mdate':itm_mdate,'r_date':r_date,'m_date':m_date,'itm_rdate':itm_rdate,'itm_date': itm_mdate})
        elif request.method=="POST":
            
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
            imt.item_name=itemname
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
            
            tid= Item_Master.objects.filter(IsDeleted='0')
            return render(request,"Item-Master_data.html",{'tid':tid})

def delete_data(request,pk):
    
    print(pk)
    itm= Item_Master.objects.get(id = pk)
    itm.IsDeleted=1
    itm.save()
    tid= Item_Master.objects.filter(IsDeleted='0')
    return render(request,"Item-Master_data.html",{'tid':tid})
    return redirect(display)

def warehouse(request):
    if 'id'  in request.session:
        if request.method== "POST":
            warehousename=request.POST.get('warehousename')
            warehouseadd=request.POST.get('Warehouse_Add')
            CreatedDate=datetime.now()
            ModifiedDate=datetime.now()

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
            print("sucessfully registerd ") 
            wid= Warehouse_Master.objects.filter(IsDeleted='0')
            return render(request,"Warehouse-Master.html",{'wid':wid})
           
        else:
            wid= Warehouse_Master.objects.filter(IsDeleted='0')
            return render(request,"Warehouse-Master.html",{'wid':wid})
            
    else:
        return redirect('companylogin')
def warehouseshow(request):
    if 'id'  in request.session:
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        wid= Warehouse_Master.objects.filter(IsDeleted='0')

        for i in wid:
            print("i = ", i)
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
            wid= Warehouse_Master.objects.filter(IsDeleted='0')
            lid = Login_Master.objects.get(id = request.session['id'])
            companyname = Company_Master.objects.get(id = lid.Company_id_id)
            return render(request,"Warehouse-Master.html",{'wid':wid ,'companyname':companyname})
def delete_warehouse(request,pk):
    
    print(pk)
    
    ware_delete= Warehouse_Master.objects.get(id = pk)
    ware_delete.IsDeleted=1
    ware_delete.save()
    wid= Warehouse_Master.objects.filter(IsDeleted='0')
    return render(request,"Warehouse-Master.html",{'wid':wid})



def user (request ) :
    if 'id'  in request.session:
        if request.POST:
  
            firstname=request.POST.get('firstname')
            lastname=request.POST.get('lastname')
            phoneno=request.POST.get('Mob_num')
           
            email=request.POST.get('email')
            password=request.POST.get('Password')
            cpassword=request.POST.get('Cpassword')
            CreatedDate=datetime.now()
            ModifiedDate=datetime.now()
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
                print("sucessfully registerd ") 
                
                uid= User_Master.objects.filter(IsDeleted='0')
                lid = Login_Master.objects.get(id = request.session['id'])
                companyname = Company_Master.objects.get(id = lid.Company_id_id)
                return render(request,"User-Master-data.html",{ 'uid':uid ,'companyname':companyname})
            
            else:
                return render(request,"user-master.html",{ 'error':'password does not match' })
        else:
            return render (request ,"user-master.html")
    else:
        return redirect('/companylogin/')


def user_data(request):
    if 'id'  in request.session:
        uid= User_Master.objects.filter(IsDeleted='0')
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
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
            psw=request.POST['Password']
            # print("warehousenam = ", warehousename)
            u_edit= User_Master.objects.get(id = pk)
           
            u_edit.First_name=fname
            u_edit.Last_name=lname
            u_edit.phone_number=phone
            u_edit.email_address=email
            u_edit.password=psw
            u_edit.save()
            
            uid= User_Master.objects.filter(IsDeleted='0')
            return render(request,"User-Master-data.html",{'uid':uid })



def delete_user(request,pk):
    
   
    u_delete= User_Master.objects.get(id = pk)
    u_delete.IsDeleted=1
    u_delete.save()
    uid= User_Master.objects.filter(IsDeleted='0')
    return render(request,"User-Master-Data.html",{'uid':uid,'u_delete':u_delete})




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
       
       
        wareid= Warehouse_Master.objects.get(id=warehouse_name)
        Stock.objects.create(   Item_id = itm ,
                                Warehouse_id = wareid,
                                Quantity    =  Quantity,
                                Arrving_Date = Arrving_Date ,
        )
        itm = Item_Master.objects.get(id=pk)
        qty=itm.Quantity
        itm.Quantity=int(qty)+int(Quantity)
        itm.save()
        wid= Warehouse_Master.objects.filter(IsDeleted=0)
        tid= Item_Master.objects.filter(IsDeleted='0')
       
        return render(request,"Item-Master_data.html",{'tid':tid,'wid':wid})

def ry(request):
    return render(request,"try.html")


def change_password(request,pk):
    if request.method== "GET":
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)

        uid = User_Master.objects.get(id=pk)
        return render(request,"change-password.html",{'uid':uid,'companyname':companyname})
    elif request.method=="POST" :
        uid = User_Master.objects.get(id=pk)
        new_password=request.POST['Password']
        c_password=request.POST['Cpassword']
        if new_password == c_password :
            uid.password=new_password
            uid.save()
        
    uid= User_Master.objects.filter(IsDeleted='0')
    return render(request,"User-Master-Data.html",{'uid':uid})


# for generating pdf invoice
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

from django.views.generic import TemplateView, FormView, CreateView, ListView, UpdateView, DeleteView, DetailView, View

def fetch_resources(uri, rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class GenerateInvoice(View):
    def get(self, request, pk, *args, **kwargs):
        # try:
        #     order_db = Order.objects.get(id = pk, user = request.user, payment_status = 1)     #you can filter using order_id as well
        # except:
        #     return HttpResponse("505 Not Found")
        # data = {
        #     'order_id': order_db.order_id,
        #     'transaction_id': order_db.razorpay_payment_id,
        #     'user_email': order_db.user.email,
        #     'date': str(order_db.datetime_of_payment),
        #     'name': order_db.user.name,
        #     'order': order_db,
        #     'amount': order_db.total_amount,
        # }
        name='Bhargav'
        data={'name':name}
        pdf = render_to_pdf('Invoice-Pdf.html')
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(data['order_id'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")




