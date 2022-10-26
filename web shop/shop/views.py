from django.shortcuts import redirect, render
import base64, uuid
from django.contrib import messages
from shop.models import NewWallet
from bankservice.models import user_model, transaction
from bankservice import myUtils
# Create your views here.

def shop_main(request):
    try:
        req = NewWallet.objects.waiting(ref_id=request.session['user_ref_id'], is_verify=True)
        request.session['wallet_available'] = req.ref_id
    except:
        request.session['wallet_available'] = "empty"
        
    return render(request, 'shop.html')

def paymentmethod(request):
    return render(request, 'payment.html')

def AddWallet(request):
    walletid = request.POST.get('walletid')
    plaintext = base64.b64decode(walletid)
    
    for _ in range(0, 2):
        plaintext = base64.b64decode(plaintext.decode())
    plaintext = plaintext.decode()[4::]
        
    new_request = NewWallet(
        ref_id = plaintext
    )
    new_request.save()
    
    messages.info(request,"please comfirm wallet at the Bank Service.")
    return render(request, 'payment.html')
    

def buy_now(request):
    ciphertext = request.POST.get('ciphertext')
    rsa = myUtils.myRSA()
    dec_data = rsa.decrypt(ciphertext).decode().split("||")
    if dec_data[0] != "salt":
        messages.info(request,"* authorization failed")
        return redirect('shop')
    _, price, walletid, input_pin = dec_data
    
    get_user = user_model.objects.get_user_by_id(user_ref_id=walletid)
    if get_user is None:
        messages.info(request, "fail: User error.")
        return redirect('shop')
    
    myaes = myUtils.myAES(myUtils.mySECRET)
    user_pin = myaes.decrypt(get_user.pin)
    
    if user_pin != input_pin:
        messages.info(request,"* fail: pin-invalid")
        return redirect('shop')
    
    get_user.account_balance = get_user.account_balance - float(price)
    get_user.save()
    request.session['balance'] = get_user.account_balance
    
    new_transaction = transaction(
        ref_id = str(uuid.uuid1())[:13],
        from_user = walletid,
        to_user = "THE CONTACTSWAP",
        transaction_type = "buying",
        amount = price,
        is_verify = True,
    )
    new_transaction.save()
    
    messages.info(request,"Thank you for shopping at CONTACTSWAP")
    return redirect('shop')


def jordan_red(request):
    return render(request, 'jordan_red.html')
def bag(request):
    return render(request, 'bag.html')
def bag2(request):
    return render(request, 'bag2.html')
def shoes(request):
    return render(request, 'shoes.html')