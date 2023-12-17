from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
import json
from django.views import View
from api.cred import *
from django.core.paginator import Paginator,EmptyPage
from api.models import user_details
from django.views.decorators.csrf import csrf_exempt
import traceback



@csrf_exempt
# to create a new user.
def post_user(request):
    # this method extracts data from request assigning it to variables. 
    def data_retival(data):
                uid = data.get('id')
                first_name = data.get('first_name')
                last_name = data.get('last_name')
                company_name = data.get('company_name')
                age = data.get('age')
                city = data.get('city')
                state = data.get('state')
                zip = data.get('zip')
                email = data.get('email')
                web = data.get('web')

                db = user_details.objects.filter(id=uid)
                db_id = db.first().id
                print('db id>>>>',db_id)

                # if db_id == None:
                #     return HttpResponse(f'ID:{uid} already exsits.', status=500) #????????????????


                user = user_details(
                            id = uid,
                            first_name = first_name,
                            last_name = last_name,
                            company_name = company_name,
                            age = age,
                            city = city,
                            state = state,
                            zip = zip,
                            email = email,
                            web = web
                        )
                user.save()

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            if isinstance(data, list):
                print('list')
                for entry in data:
                    data_retival(entry)
                return HttpResponse('New Users Created!',status=201)
            else:
                data_retival(data)
                return HttpResponse('New User Created!',status=201)

        except:
            print(traceback.format_exc())
            return HttpResponse('Server ERROR...', status=500)



def get_users_all(request):
        try:
            if request.method == 'GET':
                page_get = int(request.GET.get('page',1))
                limit = int(request.GET.get('limit',5))
                name = request.GET.get('name','')
                sort = request.GET.get('sort','')
                descend = False
                print(page_get,limit,name,sort)
                users = user_details.objects.all()
                user_lst = []
                print('1>', users)
                if name:
                    users = users.filter(first_name__icontains=name) | users.filter(last_name__icontains=name)

                print('2>', users)
                if sort:
                    if '-' in sort:
                        sort = sort[1:]  
                        descend = True                    
                    users.order_by(sort)
                    print('3>', users)
                
                print('4>',descend, users)

                if descend == False:
                    users = users[::-1]
                    print('5>', users)

                for user in users:
                    user_dic = {
                    'id' : user.id,
                    'first_name' : user.first_name,
                    'last_name' : user.last_name,
                    'company_name' : user.company_name,
                    'city' : user.city,
                    'state' : user.state,
                    'zip' : user.zip,
                    'email' : user.email,
                    'web' : user.web,
                    'age' : user.age,
                    }
                    user_lst.append(user_dic)
                
                p = Paginator(user_lst,limit)
                res_page = p.page(page_get)
                return JsonResponse(res_page.object_list, safe=False, status=200)

        except(EmptyPage):
            return HttpResponse('Empty Page.', status=500)

        except:
            print(traceback.format_exc())
            return HttpResponse('Server Error', status=500)
        

def get_user(request,uid):
    if request.method == 'GET':
        try:
            user = user_details.objects.get(id=uid)
            user_dic = {
                    'id' : uid,
                    'first_name' : user.first_name,
                    'last_name' : user.last_name,
                    'company_name' : user.company_name,
                    'city' : user.city,
                    'state' : user.state,
                    'zip' : user.zip,
                    'email' : user.email,
                    'web' : user.web,
                    'age' : user.age,
                }
            print(user_dic)
            return JsonResponse(user_dic,status=200)
        
        except(user_details.DoesNotExist):
            return HttpResponse('User Does Not Exsits.', status=500)
        except:
            print(traceback.format_exc())
            return HttpResponse('Server Error', status=500)  
            

@csrf_exempt
def update_user(request,uid):

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            users = user_details.objects.filter(id=uid)
            print('1>',users)
            if users.exists():
                user = users.first()
                user.first_name = data.get('first_name', user.first_name)
                user.last_name = data.get('last_name', user.last_name)
                user.company_name = data.get('company_name', user.company_name)
                user.age = data.get('age', user.age)
                user.city = data.get('city', user.city)
                user.state = data.get('state', user.state)
                user.zip = data.get('zip', user.zip)
                user.email = data.get('email', user.email)
                user.web = data.get('web', user.web)

                user.save()

                return HttpResponse('Entry Updated!', status=200)

        except(user_details.DoesNotExist):
            return HttpResponse('User Does Not Exsits.', status=500)

        except:
            print(traceback.format_exc())
            return HttpResponse('Server Error', status=500)
        
@csrf_exempt
def delete_user(request,uid):
     if request.method == 'DELETE':
        try:
            user = user_details.objects.get(id=uid)
            user.delete()
            return HttpResponse('Entry Deleted!', status=200)
        
        except(user_details.DoesNotExist):
            return HttpResponse('User Does Not Exsits.', status=500)

        except:
            print(traceback.format_exc())
            return HttpResponse('Server Error', status=500)


@csrf_exempt     
def delete_all(request):
    if request.method == 'DELETE':
        try:
            users = user_details.objects.all()
            users.delete()
            return HttpResponse('All Entries Deleted!', status=200)
        
        except:
            print(traceback.format_exc())
            return HttpResponse('Server Error', status=500)