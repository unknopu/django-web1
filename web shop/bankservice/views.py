from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate

from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers

from bankservice import myUtils
import uuid, re, hashlib
from bankservice.models import user_model, personalKey, transaction
from shop.models import NewWallet
import base64

# Create your views here.
def homepage(request):
    try:
        if request.session['is_login'] == True:
            return redirect('myaccount')
    except:
        return render(request, 'index.html')
    
def signuppage(request):
    try:
        if request.session['is_login'] == True:
            return redirect('myaccount')
    except:
        return render(request, 'signup.html')
    
def transferpage(request):
    try:
        if request.session['is_login'] == True:
            return render(request, 'transfer.html')
    except:
        return render(request, 'signup.html')

def account(request):
    try:
        if request.session['is_login'] == True:
            get_user = user_model.objects.get_user_by_id(user_ref_id=request.session['user_ref_id'])
            if get_user is None:
                messages.info(request, "fail: User error.")
                return redirect('/')
            request.session['balance'] = get_user.account_balance
            return render(request, 'account.html')
    except:
        return render(request, 'index.html')
    
def history(request):
    data = transaction.objects.get(from_user=request.session['user_ref_id'])
    trans = {
        'id':data.ref_id,
        'type':data.transaction_type,
        'amount':data.amount,
        'time':data.time_stamp,
    }
    return render(request, 'view_transaction.html', data)

def confirmWallet(request):
    req = NewWallet.objects.waiting(ref_id=request.session['user_ref_id'], is_verify=False)
    if req is None:
        request.session['wallet_request'] = False
        context = {
        'date':""
        }
        return render(request, 'confirmwallet.html', context)
    request.session['wallet_request'] = True
    context = {
        'date':req.time_stamp,
        'ref_id':req.ref_id,
    }
    return render(request, 'confirmwallet.html', context)

def comfirmAdd(request):
    walletid = request.POST.get('walletid')
    plaintext = base64.b64decode(walletid)
    for _ in range(0, 2):
        plaintext = base64.b64decode(plaintext.decode())
    plaintext = plaintext.decode()[4::]   
     
    req = NewWallet.objects.waiting(ref_id=plaintext, is_verify=False)
    req.is_verify = True
    req.save()
    request.session['wallet_available'] = plaintext
    messages.info(request, "the wallet approved.")
    return redirect('confirmwallet')


def signup(request):
    enc_data=request.POST.get('ciphertext')
    plaintext = base64.b64decode(base64.b64decode(enc_data)).decode()
    data = plaintext.split('||')
    
    iusername=data[1]
    fullname=data[6]
    iemail=data[4]
    password=data[2]
    repassword=data[3]
    idnumber=data[5]

    expr = r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$'
    if not re.match(expr, iemail):
        messages.info(request, 'Email is elligal!')
        return redirect('/')
    
    if password==repassword and password != '':
        if user_model.objects.filter(username=iusername).exists():
            messages.info(request,'Username exists')
            return redirect('/')
        elif user_model.objects.filter(email=iemail).exists():
            messages.info(request,'Email exists')
            return redirect('/')
        else :
            UserRefID = uuid.uuid1()
            password = password + myUtils.mySECRET
            hash_password = hashlib.sha512(password.encode()).hexdigest()
            
            aes = myUtils.myAES(myUtils.mySECRET)
            pin_aes = aes.encrypt(iusername+"123")
            
            try:
                user_model.objects.add_user(user_ref_id=UserRefID, 
                                                  username=iusername, 
                                                  password=hash_password, 
                                                  email=iemail, 
                                                  fullname=fullname, 
                                                  identity_number=idnumber, 
                                                  pin=pin_aes,)
                
                e, n, d = myUtils.myNewPersonalKey()
                userKey = personalKey(
                    user_ref_id=UserRefID,
                    e=e,
                    n=n,
                    d=d
                )
                userKey.save()
                
            except Exception as e:
                messages.info(request,e)
                return redirect('/')
                
            messages.info(request,"Your registration have been save.")
            return redirect('/')
    else :
        messages.info(request, 'Invalid password input!')
        return redirect('/')
    
def login(request):
    ciphertext = request.POST.get('ciphertext')
    plaintext = base64.b64decode(ciphertext).decode().split("||")
    
    username, password = plaintext[1], plaintext[2]
    
    if (username == '' or password == ''):
        messages.info(request,"username and password can't be empty.")
        return redirect('/')
    
    password = password + myUtils.mySECRET
    hash_password = hashlib.sha512(password.encode()).hexdigest()
    
    get_user = user_model.objects.get_user(username=username, password=hash_password)
    if get_user is None:
        messages.info(request, "fail: User error.")
        return redirect('/')
    
    user_publicKey = personalKey.objects.publicKey(get_user.user_ref_id)
    if user_publicKey is None:
        messages.info(request, "fail: User key error.")
        return redirect('/')
    
    
    sever_key = myUtils.myRSA()
    server_privatekey = sever_key.get_privteKey()
    server_privateKey = str(server_privatekey[0]) +' ||' + str(server_privatekey[1])
    enc_key2 = sever_key.get_publicKey()
    
    request.session['is_login'] = True
    request.session['user_ref_id'] = get_user.user_ref_id
    request.session['balance'] = get_user.account_balance
    request.session['username'] = get_user.fullname.split(' ')[0]
    request.session['publickey'] = enc_key2.decode()
    request.session['wallet_available'] = "empty"
    
    return redirect('myaccount')
    
def logout(request):
    request.session.flush()
    return redirect('/')
    
def deposit(request):
    ciphertext = request.POST.get('ciphertext')
    rsa = myUtils.myRSA()
    dec_data = rsa.decrypt(ciphertext).decode().split("||")
    if dec_data[0] != "salt":
        messages.info(request, "authorization failed")
        return redirect('myaccount')
    _, amount, input_pin, user_ref_id = dec_data
    
    get_user = user_model.objects.get_user_by_id(user_ref_id=user_ref_id)
    if get_user is None:
        messages.info(request, "fail: User error.")
        return redirect('/')
    
    myaes = myUtils.myAES(myUtils.mySECRET)
    user_pin = myaes.decrypt(get_user.pin)
    
    if user_pin == input_pin:
        get_user.account_balance += float(amount)
        get_user.save()
        request.session['balance'] = get_user.account_balance
        
        new_transaction = transaction(
            ref_id = str(uuid.uuid1())[:13],
            from_user = user_ref_id,
            to_user = user_ref_id,
            transaction_type = "deposit",
            amount = amount,
            is_verify = True,
        )
        new_transaction.save()
        
        messages.info(request, "deposit successfully.")
        return redirect('myaccount')
    else:
        messages.info(request, "fail: pin-invalid")
        return redirect('myaccount')

def transfer(request):
    ciphertext = request.POST.get('ciphertext')
    rsa = myUtils.myRSA()
    dec_data = rsa.decrypt(ciphertext).decode().split("||")
    _, amount, input_pin, user_ref_id, toacc = dec_data
    
    new_transaction = transaction(
        ref_id = str(uuid.uuid1())[:13],
        from_user = user_ref_id,
        to_user = toacc,
        transaction_type = "transfer",
        amount = amount,
        is_verify = False,
    )
    
    # fetch transferor and do pin validation; return if pin failed.
    transferor = user_model.objects.get_user_by_id(user_ref_id=user_ref_id)
    if transferor is None:
        messages.info(request, "Transferor account not found")
        return redirect('mytransfer')
    myaes = myUtils.myAES(myUtils.mySECRET)
    user_pin = myaes.decrypt(transferor.pin)
    if user_pin != input_pin:
        messages.info(request, "authorization failed")
        return redirect('mytransfer')
    
    reciever = user_model.objects.get_user_by_id(user_ref_id=toacc)
    if reciever is None:
        messages.info(request, "Recipient account doesn't exist")
        return redirect('mytransfer')
    
    transferor.account_balance -= float(amount)
    request.session['balance'] = transferor.account_balance
    transferor.save()
    reciever.account_balance += float(amount)
    reciever.save()
    new_transaction.is_verify = True
    new_transaction.save()
    # print("=============================")
    # print(amount, input_pin, user_ref_id, toacc)
    # print("=============================")
    
    messages.info(request, "Transfer successfully.")
    return redirect('mytransfer')
    