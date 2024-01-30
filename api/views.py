# from django
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator,EmptyPage
from django.db import transaction

#from drf
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

#from local app 'api'
from api.models import user_details
from api.utils import user_details_save
from api.serializers import User_detailsSerializer

# python modules
import traceback
import json                                             #JavaScript Object Notation

    
class UserAPI(APIView):
    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        if isinstance(data,list):
            conflicts = []
            try:
                with transaction.atomic():
                    for i in range(len(data)):
                        
                        print('1>',data[i], type(data[i]))
                        serializer = User_detailsSerializer(data=data[i])
                        
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            conflicts.append([i+1,serializer.errors])
                        print('2>',conflicts)
                    
                        # user_details.objects.bulk_create(entries)
                    return Response('New Users Created!',conflicts, status=201)
            except:
                print(traceback.format_exc())
                return Response(conflicts,status=400)
        else:
            check = user_details_save(data)
            if check:
                return Response(check, status=400)
            else:
                return Response('New User Created!', status=201)


    # to return requested users.
    @csrf_exempt
    def get(self,request,pk=None):
        if pk: 
            try:
                user = user_details.objects.get(id=pk)
                print(user)
                if user:
                    serializer = User_detailsSerializer(user)
                    return Response(serializer.data,status=200)            
            
                else:                 #if the user does not exists this resposne will be sent.
                    return Response('User Does Not Exsits.', status=500)
            except:
                print(traceback.format_exc())
                return Response('Server Error', status=500)
        else:
            try:
                    page_get = int(request.GET.get('page',1))   #retrieves the value of the 'page' parameter from the request's GET parameters, converting it to an integer with a default value of 1. This parameter tells the code which page of entries are to be shown.
                    limit = int(request.GET.get('limit',5))     #retrieves the value of the 'limit' parameter from the request's GET parameters, with this we can set the limit on entries shown per page.
                    name = request.GET.get('name','')           #variable used in searching of user by name as a substring in First Name or Last Name in database. Default value set to '', if nothing in sent 
                    sort = request.GET.get('sort','id')           #variable used for sort the list of users according to user desired attribute (age,id,etc.). By default it is in ascending order but if '-' is at the front(eg:'-age') then the order is descending.
                    print(page_get,limit,name,sort)
                    users = user_details.objects.all()          #retrieves all entries from the table
                    print('1>', users)
                    if name:
                        users = users.filter(first_name__icontains=name) | users.filter(last_name__icontains=name)   #the pipe operator '|' is used to combine results of filters. '__icontains' returns all names containing substring(name) and it is case insensitive.  

                    if len(sort)>0:                  
                        print('2>', sort)
                        users = users.order_by(sort)                #list of users according to user desired attribute (age,id,etc.).
                        # print('3>', users)
                    
                    print('4>', users)
                    serializer = User_detailsSerializer(users, many=True)
                    p = Paginator(serializer.data,limit)           #paginating the list of user dictionaries (user_lst) with a specified limit of items per page (limit). 
                    res_page = p.page(page_get)             #res_page holds the items at the specified page.
                    print('5>',res_page,)
                    return Response(res_page.object_list,status=200)  # safe=False argument is used when the data to be serialized is not a dictionary but a list.

            except(EmptyPage):                              # this exception is used if the user requests a page that does not hold any items.
                return Response('Empty Page.', status=500)    

            except:
                print(traceback.format_exc())
                return Response('Server Error', status=500)


    @csrf_exempt
    def put(self,request,pk):
        data = json.loads(request.body)
        try:
            # Retrieve the existing instance from the database
            user_instance = user_details.objects.filter(pk=pk).first()
            if user_instance:
                serializer = User_detailsSerializer(user_instance, data=data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response('Entry Updated!', status=200)
                else:
                    return Response(serializer.errors, status=400)
            else:
                return Response('User Does Not Exsits.', status=500)
        except:
                print(traceback.format_exc())
                return Response('Server Error', status=500)

   
    @csrf_exempt
    def delete(self,request,pk=None):                           #this method deletes a single entry from the table based on user id given by the user.
        if pk:                        
            try:
                user = user_details.objects.get(pk=pk)     #to retrieve user based on primary key attributegiven by the user. 
                user.delete()                               #this deletes the entry.
                return Response('Entry Deleted!', status=200)
            
            except(user_details.DoesNotExist):
                return Response('User Does Not Exsits.', status=500)

            except:
                print(traceback.format_exc())
                return Response('Server Error', status=500)

        #this segment deletes all user.
        else:
            try:
                first_name = request.GET.get('first_name','')
                last_name = request.GET.get('last_name','')
                age_start = int(request.GET.get('age_start', 0))  # Default value of 0 if not provided
                age_end = int(request.GET.get('age_end', 0))
                start_id = int(request.GET.get('start_id', 0))  
                end_id = int(request.GET.get('end_id', 0))  

                users = user_details.objects.all()

                # Filter based on provided parameters
                if first_name:
                    users = users.filter(first_name__iexact=first_name)     # case-insensitive matching for first_name.
                if last_name:
                    users = users.filter(last_name__iexact=last_name)       # case-insensitive matching for last_name.
                if age_start < age_end:
                    users = users.filter(age__gte=age_start, age__lte=age_end)      #__gte filters all ages greater than or eaqual to age_start.
                if start_id < end_id:
                    users = users.filter(id__gte=start_id, id__lte=end_id)          #__lte filterd all ids less than or eaqual to end_id.

                # Delete filtered entries
                
                user_list = []
                for user in users:
                    user_dic = {
                        'id' : user.id,
                        'first_name' : user.first_name,
                        'last_name' : user.last_name,
                        'email' : user.email,
                    }
                    user_list.append(user_dic)
                print(user_list)
                users.delete()
                if user_list:
                    return Response(f'Entries Deleted:{user_list}', status=200)
                else:
                    return Response('Users does not exists!', status=400)
                
            
            except:
                print(traceback.format_exc())
                return Response('Server Error', status=500)