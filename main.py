from tkinter import *
from functools import partial
from pymongo import MongoClient
from pprint import pprint
import tkinter.messagebox
import random
import datetime
import smtplib

client = MongoClient()

db=client["demo"]
accounts=db["account"]
branch=db["branch"]
customer=db["customer"]
loan=db["loan"]
transactions=db["transactions"]

chk=0
password=custid=0
otp_c=False

def check_otp(custid):
    global otp_c
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    #Next, log in to the server
    server.login('SVAN.online.banking.system@gmail.com', 'SVAN1234')

    #Send the mail'''
    otp=random.randint(100000,999999)
    msg = 'Hey '+customer.find_one({'c_id':custid})['name']+',\n\nThe One-Time Password for your transaction is '+str(otp)+'. Please do not share this pin with anyone.\n\nSVAN Online Banking System'
    sub='Transaction-OTP'
    message='Subject: {}\n\n{}'.format(sub,msg)

    receive_mail=customer.find_one({'c_id':custid})['email']
    # The /n separates the message from the headers
    server.sendmail('nachistatslearning1@gmail.com', receive_mail, message)
    server.close()
    temp=Tk()
    temp.geometry('100x50+1000+100320')
    tkinter.messagebox.showinfo('OTP_Sent','Your OTP has been sent to '+receive_mail)
    temp.destroy()

    print(otp)
    otp_entry=Tk()
    l1=Label(otp_entry,text="Enter the OTP: ")
    l1.pack(side=LEFT)
    e1=Entry(otp_entry)
    e1.pack(side=LEFT)
    b1=Button(otp_entry,text="VERIFY",command=partial(compare,otp,e1,otp_entry))
    b1.pack(side=BOTTOM)
    otp_entry.mainloop()
    return otp_c

def compare(otp,e1,otp_entry):
    global otp_c
    if(otp==int(e1.get())):
        otp_c=True
    else:
        otp_c=False
    otp_entry.destroy()
    return


class view_passbook():
    def __init__(self,acc_no):
        self.passbook=Tk()
        self.passbook.geometry("300x300+700+250")
        heading=Label(self.passbook,text="Account Passbook")
        heading.place(x=100,y=0)
        account_detail=accounts.find_one({'a_id':acc_no})
        branch_detail=branch.find_one({'b_id':account_detail['b_id']})

        l1=Label(self.passbook,text="Account No:",anchor="e",width=12)
        l2=Label(self.passbook,text="Account Type:", anchor="e",width=12)
        l3=Label(self.passbook,text="Balance:",anchor="e",width=12)
        l4=Label(self.passbook,text="Branch:",anchor="e",width=12)
        l5=Label(self.passbook,text="IFSC Code:",anchor="e",width=12)
        l6=Label(self.passbook,text="Branch Manager:",anchor="e",width=12)

        l7=Label(self.passbook,text=account_detail["a_id"],anchor="w",width=20)
        l8=Label(self.passbook,text=account_detail["type"],anchor="w",width=20)
        l9=Label(self.passbook,text=account_detail["balance"],anchor="w",width=20)
        l10=Label(self.passbook,text=account_detail["b_id"],anchor="w",width=20)
        l11=Label(self.passbook,text=branch_detail["ifsc"],anchor="w",width=20)
        l12=Label(self.passbook,text=branch_detail["manager_name"],anchor="w",width=20)
        b_show=Button(self.passbook,text="Show All Transactions",command=partial(self.show_transaction,acc_no))
        b_back=Button(self.passbook,text="Back",command=partial(self.back,acc_no))

        l1.place(x=20,y=40)
        l7.place(x=125,y=40)
        l2.place(x=20,y=60)
        l8.place(x=125,y=60)
        l3.place(x=20,y=80)
        l9.place(x=125,y=80)
        l4.place(x=20,y=100)
        l10.place(x=125,y=100)
        l5.place(x=20,y=120)
        l11.place(x=125,y=120)
        l6.place(x=20,y=140)
        l12.place(x=125,y=140)
        b_show.place(x=90,y=170)
        b_back.place(x=130,y=200)

    def show_transaction(self,acc_no):
        self.trans=Tk()
        k=0
        self.trans.geometry("1000x1000+200+250")
        for j in transactions.find({'from':acc_no}):
            k+=1
        for j in transactions.find({'to':acc_no}):
            k+=1
        l1=[]
        l2=[]
        l3=[]
        l4=[]
        l5=[]
        l6=[]
        l7=[]
        l8=[]
        k+=10
        for i in range(k+1):
            l1.append(0)
            l2.append(0)
            l3.append(0)
            l4.append(0)
            l5.append(0)
            l6.append(0)
            l7.append(0)
            l8.append(0)


        l1[0]=Label(self.trans,text="T_ID:",justify=CENTER,width=12)
        l2[0]=Label(self.trans,text="Type:", justify=CENTER,width=12)
        l3[0]=Label(self.trans,text="From:",justify=CENTER,width=12)
        l4[0]=Label(self.trans,text="To:",justify=CENTER,width=12)
        l5[0]=Label(self.trans,text="Amount:",justify=CENTER,width=12)
        l6[0]=Label(self.trans,text="Date:",justify=CENTER,width=12)
        l7[0]=Label(self.trans,text="Description",justify=CENTER,width=20)
        l8[0]=Label(self.trans,text="Receiving IFSC",justify=CENTER,width=20)

        l1[0].grid(row=0,column=0)
        l2[0].grid(row=0,column=1)
        l3[0].grid(row=0,column=2)
        l4[0].grid(row=0,column=3)
        l5[0].grid(row=0,column=4)
        l6[0].grid(row=0,column=5)
        l7[0].grid(row=0,column=6)
        l8[0].grid(row=0,column=7)
        k=1
        for i in transactions.find({'from':acc_no}):
            l1[k]=Label(self.trans,text=i['t_id'],width=12)
            l2[k]=Label(self.trans,text=i['type'],width=12)
            l3[k]=Label(self.trans,text=i['from'],width=12)
            l4[k]=Label(self.trans,text=i['to'],width=12)
            l5[k]=Label(self.trans,text=i['amount'],width=12)
            l6[k]=Label(self.trans,text=i['date'],width=21)
            l7[k]=Label(self.trans,text=i['description'],width=20)
            l8[k]=Label(self.trans,text=i['r_ifsc'],width=20)

            l1[k].grid(row=k,column=0)
            l2[k].grid(row=k,column=1)
            l3[k].grid(row=k,column=2)
            l4[k].grid(row=k,column=3)
            l5[k].grid(row=k,column=4)
            l6[k].grid(row=k,column=5)
            l7[k].grid(row=k,column=6)
            l8[k].grid(row=k,column=7)
            k+=1

        for i in transactions.find({'to':"Acc No:"+acc_no}):
            l1[k]=Label(self.trans,text=i['t_id'],width=12)
            l2[k]=Label(self.trans,text=i['type'],width=12)
            l3[k]=Label(self.trans,text=i['from'],width=12)
            l4[k]=Label(self.trans,text=i['to'],width=12)
            l5[k]=Label(self.trans,text=i['amount'],width=12)
            l6[k]=Label(self.trans,text=i['date'],width=21)
            l7[k]=Label(self.trans,text=i['description'],width=20)
            l8[k]=Label(self.trans,text=i['r_ifsc'],width=20)

            l1[k].grid(row=k,column=0)
            l2[k].grid(row=k,column=1)
            l3[k].grid(row=k,column=2)
            l4[k].grid(row=k,column=3)
            l5[k].grid(row=k,column=4)
            l6[k].grid(row=k,column=5)
            l7[k].grid(row=k,column=6)
            l8[k].grid(row=k,column=7)
            k+=1





    def back(self,acc_no):
        custid=accounts.find_one({'a_id':acc_no})['owner']
        self.passbook.destroy()
        home(custid)

class fund_transfer:
        def __init__(self,acc_no):
            self.funds_transfer=Tk()
            self.funds_transfer.geometry("430x300+700+250")
            heading=Label(self.funds_transfer,text="Funds Transfer")
            heading.place(x=140,y=0)

            l1=Label(self.funds_transfer,text="To account", anchor="e",width=12)
            l2=Label(self.funds_transfer,text="IFSC Code",anchor="e",width=12)
            l3=Label(self.funds_transfer,text="Amount:",anchor="e",width=12)
            l4=Label(self.funds_transfer,text="Description:",anchor="e",width=12)
            b_pay=Button(self.funds_transfer,text="Transfer",command=partial(self.check_transfer,acc_no))
            b_back=Button(self.funds_transfer,text="Back",command=partial(self.back,acc_no))

            self.e1=Entry(self.funds_transfer)
            self.e2=Entry(self.funds_transfer)
            self.e3=Entry(self.funds_transfer,width=20,)
            self.e4=Text(self.funds_transfer,height=4,width=15)

            l1.place(x=20,y=60)
            l2.place(x=20,y=90)
            l3.place(x=20,y=120)
            l4.place(x=20,y=150)

            self.e1.place(x=125,y=60)
            self.e2.place(x=125,y=90)
            self.e3.place(x=125,y=120)
            self.e4.place(x=125,y=155)

            b_pay.place(x=130,y=250)
            b_back.place(x=200,y=250)

        def check_transfer(self,acc_no):
            to_acc=self.e1.get()
            des=self.e4.get("1.0",'end-1c')
            transfer_amount=float(self.e3.get())
            ifsc=self.e2.get()
            b_no=accounts.find_one({'a_id':to_acc})
            self.funds_transfer.destroy()
            if(b_no==None):
                temp=Tk()
                temp.geometry('100x50+1000+100320')
                tkinter.messagebox.showinfo('Error!','Wrong Account Number!!!')
                temp.destroy()
                home(accounts.find_one({'a_id':acc_no})['owner'])
            else:

                b_no=accounts.find_one({'a_id':to_acc})['b_id']
                IFSC=branch.find_one({'b_id':b_no})['ifsc']
                if(IFSC!=ifsc):
                    temp=Tk()
                    temp.geometry('100x50+1000+100320')
                    tkinter.messagebox.showinfo('Error!','Wrong IFSC Code!!!')
                    temp.destroy()
                    home(accounts.find_one({'a_id':acc_no})['owner'])

                else:
                    if(check_otp(accounts.find_one({'a_id':acc_no})['owner'])==False):
                        temp=Tk()
                        temp.geometry('100x50+1000+100320')
                        tkinter.messagebox.showinfo('Error!','Wrong OTP!!!')
                        temp.destroy()
                        #home(accounts.find_one({'a_id':acc_no})['owner'])

                    else:
                        balance=float(str(accounts.find_one({'a_id':acc_no})['balance']))
                        min_balance=accounts.find_one({'a_id':acc_no})['min_balance']
                        to_bal=float(accounts.find_one({'a_id':to_acc})['balance'])

                        if(balance-float(min_balance)>=transfer_amount):
                            balance-=transfer_amount
                            to_bal+=transfer_amount
                            accounts.update_one({'a_id':acc_no},{'$set':{'balance':str(balance)}})
                            accounts.update_one({'a_id':to_acc},{'$set':{'balance':str(to_bal)}})
                            print("from bal:"+str(balance))
                            print("to bal:"+str(to_bal))
                            t_id=random.randint(10000,99999)
                            transaction={'t_id':'T'+str(t_id),"type":"Fund Transfer","from":acc_no,"to":"Acc No:"+to_acc,"amount":str(transfer_amount),"date":str(datetime.datetime.now()),"r_ifsc":IFSC,"description":des}
                            transactions.insert_one(transaction)
                            #pprint(transaction)
                            temp=Tk()
                            temp.geometry('100x50+1000+100320')
                            tkinter.messagebox.showinfo('Success!','Bill payment success\n Your Available Balance:'+str(balance))
                            temp.destroy()

                        else:
                            temp=Tk()
                            temp.geometry('100x50+1000+100320')
                            tkinter.messagebox.showinfo('Error!','Bill payment Unsuccess\nInsufficient Funds')
                            temp.destroy()

                    home(accounts.find_one({'a_id':acc_no})['owner'])

        def back(self,acc_no):
            custid=accounts.find_one({'a_id':acc_no})['owner']
            self.funds_transfer.destroy()
            home(custid)

class loan_page:
    def __init__(self,acc_no):
        loan_detail=loan.find_one({"a_id":acc_no})
        self.ln_detail=loan_detail
        if(loan_detail==None):
            temp=Tk()
            temp.geometry('100x50+1000+100320')
            tkinter.messagebox.showinfo('Error!',"No loans under this account")
            temp.destroy()
            home(accounts.find_one({"a_id":acc_no})['owner'])
        else:
            self.loan_details=Tk()
            self.loan_details.geometry("300x300+700+250")
            pprint(loan_detail)
            heading=Label(self.loan_details,text="Your Loan Details")
            heading.place(x=70,y=0)

            l1=Label(self.loan_details,text="Loan ID:",anchor="e",width=12)
            l2=Label(self.loan_details,text="Account No:", anchor="e",width=12)
            l3=Label(self.loan_details,text="Loan Amt:",anchor="e",width=12)
            l4=Label(self.loan_details,text="Pending Amt:",anchor="e",width=12)
            l5=Label(self.loan_details,text="Issue Date:",anchor="e",width=12)
            l6=Label(self.loan_details,text="Pending Months:",anchor="e",width=12)
            l7=Label(self.loan_details,text='Duration:',anchor="e",width=12)

            l8=Label(self.loan_details,text=loan_detail["l_id"],anchor="w",width=20)
            l9=Label(self.loan_details,text=loan_detail["a_id"],anchor="w",width=20)
            l10=Label(self.loan_details,text=loan_detail["amount"],anchor="w",width=20)
            l11=Label(self.loan_details,text=loan_detail["due"],anchor="w",width=20)
            l12=Label(self.loan_details,text=loan_detail["issue_date"],anchor="w",width=20)
            l13=Label(self.loan_details,text=loan_detail["loan_period"],anchor="w",width=20)
            l14=Label(self.loan_details,text=loan_detail["remaining_months"],anchor="w",width=20)
            b_pay_loan=Button(self.loan_details,text="Pay this months due",command=partial(self.check_loan,acc_no))
            b_back=Button(self.loan_details,text="Back",command=partial(self.back,acc_no))

            l15=Label(self.loan_details,text='Monthly Due:',anchor="e",width=12)
            monthly_due=float(loan_detail["amount"])/float(loan_detail["loan_period"])
            monthly_due=round(monthly_due,2)
            l16=Label(self.loan_details,text=monthly_due,anchor="w",width=20)

            l1.place(x=30,y=40)
            l8.place(x=135,y=40)
            l2.place(x=30,y=60)
            l9.place(x=135,y=60)
            l3.place(x=30,y=80)
            l10.place(x=135,y=80)
            l4.place(x=30,y=100)
            l11.place(x=135,y=100)
            l5.place(x=30,y=120)
            l12.place(x=135,y=120)
            l6.place(x=30,y=140)
            l13.place(x=135,y=140)
            l7.place(x=30,y=160)
            l14.place(x=135,y=160)
            l15.place(x=30,y=180)
            l16.place(x=135,y=180)

            b_pay_loan.place(x=100,y=220)
            b_back.place(x=130,y=260)

    def check_loan(self,acc_no):
        self.loan_details.destroy()
        if(check_otp(accounts.find_one({'a_id':acc_no})['owner'])==False):
            temp=Tk()
            temp.geometry('100x50+1000+100320')
            tkinter.messagebox.showinfo('Error!','Wrong OTP!!!')
            temp.destroy()
            home(accounts.find_one({'a_id':acc_no})['owner'])
        else:

            balance=float(accounts.find_one({'a_id':acc_no})['balance'])
            min_balance=accounts.find_one({'a_id':acc_no})['min_balance']
            loan_amount=round(float(self.ln_detail["amount"])/float(self.ln_detail["loan_period"]),2)

            if(balance-float(min_balance)>=(loan_amount)):
                balance-=loan_amount
                accounts.update_one({'a_id':acc_no},{'$set':{'balance':str(round(balance,2))}})
                t_id=random.randint(10000,99999)
                transaction={'t_id':'T'+str(t_id),"type":"Loan Payment","from":acc_no,"to":"Loan No:"+self.ln_detail['l_id'],"amount":str(loan_amount),"date":str(datetime.datetime.now()),"r_ifsc":"","description":"Loan Payment"}
                transactions.insert_one(transaction)
                temp=Tk()
                temp.geometry('100x50+1000+100320')
                tkinter.messagebox.showinfo('Success!','Bill payment success\n Your Available Balance:'+str(round(balance,2)))
                temp.destroy()
                due=float(loan.find_one({'a_id':acc_no})['due'])-loan_amount
                loan.update_one({'a_id':acc_no},{'$set':{'due':due}})
                loan.update_one({'a_id':acc_no},{'$set':{'remaining_months':str(float(loan.find_one({'a_id':acc_no})['remaining_months']-1))}})


            else:
                tkinter.messagebox.showinfo('Error!','Bill payment Unsuccess\nInsufficient Funds')

            home(accounts.find_one({'a_id':acc_no})['owner'])

    def back(self,acc_no):
        custid=accounts.find_one({'a_id':acc_no})['owner']
        self.loan_details.destroy()
        home(custid)

class pay_bill:

    def __init__(self,acc_no):
        self.pay_bills=Tk()

        self.pay_bills.geometry("380x260+700+250")
        heading=Label(self.pay_bills,text="Pay Bills")
        heading.place(x=140,y=0)
        account_details=accounts.find_one({"a_id":acc_no})

        l1=Label(self.pay_bills,text="Bill No:", anchor="e",width=12)
        l2=Label(self.pay_bills,text="Bill Description:",anchor="e",width=12)
        l3=Label(self.pay_bills,text="Amount:",anchor="e",width=12)

        self.e1=Entry(self.pay_bills)
        self.e2=Text(self.pay_bills,height=4,width=16)
        self.e3=Entry(self.pay_bills,width=20,)

        l1.place(x=20,y=60)
        l2.place(x=20,y=90)
        l3.place(x=20,y=170)


        self.e1.place(x=125,y=60)
        self.e2.place(x=125,y=90)
        self.e3.place(x=125,y=170)

        b_pay=Button(self.pay_bills,text="PAY",command=partial(self.check_balance,acc_no))
        b_back=Button(self.pay_bills,text="Back",command=partial(self.back,acc_no))
        b_pay.place(x=140,y=210)
        b_back.place(x=180,y=210)
        self.pay_bills.mainloop()


    def back(self,acc_no):
        custid=accounts.find_one({'a_id':acc_no})['owner']
        self.pay_bills.destroy()
        home(custid)

    def check_balance(self,acc_no):
        bill_amount=float(self.e3.get())
        bill_no=self.e1.get()
        des=self.e2.get("1.0",'end-1c')
        #self.pay_bills.destroy()
        self.pay_bills.destroy()
        if(check_otp(accounts.find_one({'a_id':acc_no})['owner'])==False):
            temp=Tk()
            temp.geometry('100x50+1000+100320')
            tkinter.messagebox.showinfo('Error!','Wrong OTP!!!')
            temp.destroy()
            home(accounts.find_one({'a_id':acc_no})['owner'])

        else:
            temp=Tk()
            temp.geometry('100x50+1000+1020')
            balance=float(accounts.find_one({'a_id':acc_no})['balance'])
            min_balance=accounts.find_one({'a_id':acc_no})['min_balance']


            if(balance-int(min_balance)>=(bill_amount)):
                balance-=bill_amount
                accounts.update_one({'a_id':acc_no},{'$set':{'balance':str(balance)}})
                t_id=random.randint(10000,99999)
                transaction={'t_id':'T'+str(t_id),"type":"Bill Payment","from":acc_no,"to":"Bill No:"+bill_no,"amount":str(bill_amount),"date":str(datetime.datetime.now()),"r_ifsc":"","description":des}
                transactions.insert_one(transaction)

                pprint(transaction)

                tkinter.messagebox.showinfo('Success!','Bill payment success\n Your Available Balance:'+str(balance))

            else:
                tkinter.messagebox.showinfo('Error!','Bill payment Unsuccess\nInsufficient Funds')
            temp.destroy()
            home(accounts.find_one({'a_id':acc_no})['owner'])

class modify_detail:

    customer_id=0
    def __init__(self,custid):
        self.customer_id=custid
        self.modify_details=Tk()
        self.modify_details.geometry("400x300+700+250")
        heading=Label(self.modify_details,text="Customer Details")
        heading.place(x=140,y=0)
        customer_detail=customer.find_one({"c_id":custid})
        address='\n'
        address=address.join(customer_detail['address'])

        l1=Label(self.modify_details,text="Name:", anchor="e",width=12)
        l2=Label(self.modify_details,text="Address:",anchor="e",width=12)
        l3=Label(self.modify_details,text="Phone Number:",anchor="e",width=12)
        l4=Label(self.modify_details,text="Email Id:",anchor="e",width=12)

        l11=Label(self.modify_details,text=customer_detail["name"],justify=CENTER,width=20)
        l22=Label(self.modify_details,text=address,justify=CENTER,width=20)
        l33=Label(self.modify_details,text=customer_detail["p_no"],justify=CENTER,width=20)
        l44=Label(self.modify_details,text=customer_detail["email"],justify=CENTER)


        e1=Entry(self.modify_details,)
        e2=Entry(self.modify_details,width=20,)
        e3=Entry(self.modify_details,width=20,)
        e4=Entry(self.modify_details,)

        b1=Button(self.modify_details,text="change",width=10,height=1,command=partial(self.change,1))
        b2=Button(self.modify_details,text="change",width=10,height=1,command=partial(self.change,2))
        b3=Button(self.modify_details,text="change",width=10,height=1,command=partial(self.change,3))
        b4=Button(self.modify_details,text="change",width=10,height=1,command=partial(self.change,4))
        self.b_save=Button(self.modify_details,text="Save")
        b_back=Button(self.modify_details,text="Back",command=partial(self.back,custid))

        l1.place(x=20,y=60)
        l11.place(x=125,y=60)
        b1.place(x=300,y=60)
        l2.place(x=20,y=80)
        l22.place(x=125,y=80)
        b2.place(x=300,y=85)
        l3.place(x=20,y=145)
        l33.place(x=125,y=145)
        b3.place(x=300,y=145)
        l4.place(x=20,y=165)
        l44.place(x=125,y=165)
        b4.place(x=300,y=170)
        b_back.place(x=200,y=200)

        self.modify_details.mainloop()

    def back(self,custid):
        self.modify_details.destroy()
        home(custid)


    def change(self,ch):

        self.e_new_data=Entry(self.modify_details,width=27)
        is_addr=False

        if(ch==1):
            self.e_new_data.place(x=125,y=60)
            field="name"

        elif(ch==2):
            self.e_new_data=Text(self.modify_details,height=4,width=20)
            self.e_new_data.place(x=125,y=80)
            field="address"
            is_addr=True


        elif(ch==3):
            self.e_new_data.place(x=125,y=145)
            field="p_no"

        elif(ch==4):
            self.e_new_data.place(x=125,y=165)
            field="email"

        self.b_save=Button(self.modify_details,text="Save",command=partial(self.update,field,is_addr))
        self.b_save.place(x=160,y=200)

    def update(self,field,is_addr):

        if(is_addr==True):
            new_data=self.e_new_data.get("1.0",'end-1c').split("\n")
            new_data=','.join(new_data)
            new_data=new_data.split(",",4)

        else:
            new_data=self.e_new_data.get()
        customer.update_one({"c_id":self.customer_id},{"$set":{field:new_data}})
        self.modify_details.destroy()
        temp=Tk()
        temp.geometry('100x50+1000+100320')
        tkinter.messagebox.showinfo('Success!',"Data updated")
        temp.destroy()
        home(self.customer_id)
        #pprint(customer.find_one({"c_id":self.customer_id}))
        print(new_data)

class details:

    def __init__(self,custid):
        self.view_details=Tk()
        self.view_details.geometry("300x300+700+250")
        heading=Label(self.view_details,text="Customer Details")
        heading.place(x=70,y=0)
        customer_detail=customer.find_one({"c_id":custid})
        address='\n'
        address=address.join(customer_detail['address'])

        l1=Label(self.view_details,text="Customer ID:",anchor="e",width=12)
        l2=Label(self.view_details,text="Name:", anchor="e",width=12)
        l3=Label(self.view_details,text="Address:",anchor="e",width=12)
        l4=Label(self.view_details,text="Phone Number:",anchor="e",width=12)
        l5=Label(self.view_details,text="Email Id:",anchor="e",width=12)

        l6=Label(self.view_details,text=customer_detail["c_id"],anchor="w",width=20)
        l7=Label(self.view_details,text=customer_detail["name"],anchor="w",width=20)
        l8=Label(self.view_details,text=address,anchor="w",width=20)
        l9=Label(self.view_details,text=customer_detail["p_no"],anchor="w",width=20)
        l10=Label(self.view_details,text=customer_detail["email"],anchor="w")
        b_exit=Button(self.view_details,text="BACK",command=partial(self.back,custid))

        l1.place(x=20,y=40)
        l6.place(x=125,y=40)
        l2.place(x=20,y=60)
        l7.place(x=125,y=60)
        l3.place(x=20,y=80)
        l8.place(x=125,y=80)
        l4.place(x=20,y=145)
        l9.place(x=125,y=145)
        l5.place(x=20,y=165)
        l10.place(x=125,y=165)
        b_exit.place(x=120,y=200)

    def back(self,custid):
        self.view_details.destroy()
        home(custid)

class home:

    def options(self,*accno):
        self.home_page.geometry("230x350+700+250")
        accno=accno[1]
        acc=accounts.find_one({"a_id":accno})

        b_view_details=Button(self.home_page,text="View Details",width=13,height=4,command=partial(self.open,acc['owner'],1))
        b_modify_details=Button(self.home_page,text="Modify Details",width=13,height=4,command=partial(self.open,acc['owner'],2))
        b_view_passbook=Button(self.home_page,text="View Passbook",width=13,height=4,command=partial(self.open,acc['a_id'],3))
        b_fund_transfer=Button(self.home_page,text="Fund Transfer",width=13,height=4,command=partial(self.open,acc['a_id'],4))
        b_pay_bills=Button(self.home_page,text="Pay Bills",width=13,height=4,command=partial(self.open,acc['a_id'],5))
        b_loan=Button(self.home_page,text="Loan",width=13,height=4,command=partial(self.open,acc['a_id'],6))
        b_logout=Button(self.home_page,text="LOGOUT",command=partial(self.open,0,7))


        b_view_details.place(x=8,y=60)
        b_modify_details.place(x=120,y=60)
        b_view_passbook.place(x=8,y=135)
        b_fund_transfer.place(x=120,y=135)
        b_pay_bills.place(x=8,y=210)
        b_loan.place(x=120,y=210)
        b_logout.place(x=85,y=295)


    def open(self,c_id=0,ch=0):
        self.home_page.destroy()
        if(ch==1):
            details(c_id)


        elif(ch==2):
            modify_detail(c_id)

        elif(ch==3):
            view_passbook(c_id)

        elif(ch==4):
            fund_transfer(c_id)

        elif(ch==5):
            pay_bill(c_id)

        elif(ch==6):
            loan_page(c_id)

        elif(ch==7):
            login()




    def __init__(self,custid):
        self.home_page=Tk()
        customer_detail=customer.find_one({"c_id":custid})
        self.home_page.geometry("250x90+700+280")
        self.heading=Label(self.home_page, text="Welcome: "+customer_detail["name"], justify=CENTER)
        self.heading.place(x=70,y=0)

        c_accounts=[]
        for i in accounts.find({"owner":custid}):
            c_accounts.append(i["a_id"])
        a_id=StringVar(self.home_page)
        a_id.set("Select")
        acc=OptionMenu(self.home_page,a_id,*c_accounts,command=partial(self.options,a_id.get()))
        acc.place(x=85,y=20)

        self.home_page.mainloop()

class login:
    def check(self):
        custid=self.e_custid.get()
        password=self.e_password.get()

        customer_detail=customer.find_one({"c_id":custid})
        if(password == customer_detail["password"] and custid==customer_detail["c_id"]):
            self.login_page.destroy()
            home(custid)
        else:
            tkinter.messagebox.showinfo('Error!','The customer ID and the password do not match')


    def __init__(self):
        self.login_page=Tk()
        self.login_page.geometry("250x90+700+280")

        self.heading=Label(self.login_page, text="Welcome to SVAN Online Banking System")
        self.heading.grid(row=0,columnspan=2)
        self.l_custid=Label(self.login_page, text="Customer Id")
        self.l_password=Label(self.login_page, text="Password")

        self.e_custid=Entry(self.login_page)
        self.e_password=Entry(self.login_page,show="*")
        self.l_custid.grid(row=1)
        self.l_password.grid(row=2)
        self.e_custid.grid(row=1,column=1)
        self.e_password.grid(row=2,column=1)
        self.b_login=Button(self.login_page,text="login",command=self.check)
        self.b_login.grid(row=3,columnspan=2)
        self.b_bypass=Button(self.login_page,text="BYPASS",command=partial(home,"C0003"))
        #self.b_bypass.grid(row=3,column=2)
        self.login_page.mainloop()

SVAN_Banking_System=login()
