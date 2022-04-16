from django.shortcuts import render

# Create your views here.
def index(request):
    from .models import User
    users=User.objects.all()
    p=users[len(users)-1].pic
    print(p.url)
    
    return render(request,'index.html',{"pic":p.url})



def uploadImage(request):
    p=request.FILES['image']
    from .models import User
    user=User(pic=p)
    user.save()
    return render(request,'index.html')

def output(request):
    # if request.method=="POST":
    #     image= request.POST.get('image')
    #     project1=detect(image=image)
    #     project1.save()
    from .models import User
    users=User.objects.all()
    p=users[len(users)-1].pic
    print(p.url[1:])
    # c1={
    #   "initial":p.url
    # }
    import cv2
    import pytesseract

    # Read the image file
    image = cv2.imread(p.url[1:])
    # Convert to Grayscale 9Image
    # width ,height=400,400
    # image=cv2.resize(image,(width,height))
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Canny Edge Detection
    canny_edge = cv2.Canny(gray_image, 170, 200)

    # Find contours based on Edges
    contours, new  = cv2.findContours(canny_edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours, key = cv2.contourArea, reverse = True)[:30]

    # Initialize license Plate contour and x,y coordinates
    contour_with_license_plate = None
    license_plate = None
    x = None
    y = None
    w = None
    h = None

    # Find the contour with 4 potential corners and creat ROI around it
    for contour in contours:
        # Find Perimeter of contour and it should be a closed contour
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
        if len(approx) == 4: #see whether it is a Rect
            contour_with_license_plate = approx
            x, y, w, h = cv2.boundingRect(contour)
            license_plate = gray_image[y:y + h, x:x + w]
            break

    # Removing Noise from the detected image, before sending to Tesseract
    license_plate = cv2.bilateralFilter(license_plate, 11, 17, 17)
    (thresh, license_plate) = cv2.threshold(license_plate, 150, 180, cv2.THRESH_BINARY)

    #Text Recognition
    text = pytesseract.image_to_string(license_plate)
    # #Draw License Plate and write the Text
    image = cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 3) 
    image = cv2.putText(image, text, (x-100,y-50), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,255,0), 6, cv2.LINE_AA)


    print("License Plate :", text)
    # cv2.imshow("License Plate Detection",image)
    # cv2.imwrite(p.url[1:],image)
    cv2.imwrite('media/profiles/car0.jpg',image)
    # cv2.waitKey(0)
    context={
        "text":text, 
        "pic":p.url,
      
    }
   
    return render(request,"wait.html", context)

def index1111(request):
    # context={
    #     "variable1" :"ashok the great",
    #     "variable2" :"ashok the great part(2)"
    # }
    return render(request,'index1111.html')
   # return HttpResponse("this is home page")


def about(request):
   
    return render(request,'about.html')
   # return HttpResponse("this is about page")

def services(request):
   

    return render(request,'services.html')
    
    #return HttpResponse("this is services page")
def project1(request):

    return render(request,'project1.html')

def contact(request):
    if request.method=="POST":
        name= request.POST.get('name')
        email= request.POST.get('email')
        phone= request.POST.get('phone')
        desc= request.POST.get('desc')
        contact=Contact(name=name,email=email,phone=phone,desc=desc,date=datetime.today())
        contact.save()

    return render(request,'contact.html')