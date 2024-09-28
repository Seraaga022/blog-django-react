from .models import User
from post.models import Post
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from .serializers import *
from PIL import Image
import base64
import json
import os
import io
import uuid
import hashlib
import time
import datetime
from print_color import print
# import bcrypt

# password = b'super secret password'


[{3, 'username', 'password', 'mail@gmail.com'}, 
{11, 'user', 'pass', 'email0@gmail.com'}, 
{12, 'customerOne', 'passOne', 'emailC1@gmail.com'}]


def generate_unique_filename_png(directory):
    while True:
            # Generate a random UUID and convert it to a string
        random_name = str(uuid.uuid4())
            # Append the current timestamp to the UUID
        file_name = f'{random_name}_{int(time.time())}'
        #     # Create the full file path
        file_path = os.path.join(directory, f'{file_name}.png')
            # Check if the file already exists
        if not os.path.exists(file_path):
            return file_name
def hash_text(text):
    if text:
        # Encode the text to bytes, as the hashing functions require byte input
        hashed_text = hashlib.sha256(text.encode('utf-8')).hexdigest()
        return hashed_text


@api_view(['POST'])
def handle_login(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        customer = ''
        encoded_string = ''
        username_hash = ''
        password_hash = hash_text(password)

        if username:
            username_hash = hash_text(username)
            try:
                if User.objects.filter(username=username_hash, password=password_hash).exists():
                    customer = User.objects.get(username=username_hash, password=password_hash)
                elif User.objects.filter(email=username, password=password_hash).exists():
                    customer = User.objects.get(email=username, password=password_hash)

            except ObjectDoesNotExist:
                print("'User does not exists'", tag='Not Found', tag_color='red', color= 'purple')
                return Response({'message': 'User does not exist'}, status=204)
        else:
            return Response({'message': 'plz enter username'}, status=400)

        if customer and customer.role != 'user':
            try:
                with open(f'user/static/customer_img/{customer.img}', 'rb') as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                print('(username:', customer.username, '), (email:', customer.email, '), (password:', customer.password, ')', tag='CUSTOMER-INFO', color='white', tag_color='white', format='bold', background='gray')
                
            except FileNotFoundError:
                with open(f'user/static/customer_img/blank-img.png', 'rb') as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                print('(username:', customer.username, '), (email:', customer.email, '), (password:', customer.password, ')', tag='CUSTOMER-INFO', color='white', tag_color='white', format='bold', background='gray')
                
            print("'", customer.role, "'", tag='CUSTOMER-ROLE',tag_color='blue', background='gray', color='blue', format='bold')

            return Response({
                'message': 'User exists',
                'role': customer.role,
                'id': customer.id,
                'username': customer.username,
                'email': customer.email,
                'password': customer.password,
                'date': customer.date,
                'image': "data:image/png;base64," + encoded_string,
            }, status=200)

        else:
            print("'User does not exist OR its user'", tag='Not Found', tag_color='red', color= 'purple')
            return Response({'message': 'An Error Accoured'}, status=400)
            
    except json.JSONDecodeError:
        print('Json decode error', tag='LOGIN-Error', color='red', tag_colour='red')
        return Response({'error': 'Invalid JSON'}, status=400)

@api_view(['POST'])
def handle_login_user(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        customer = ''
        encoded_string = ''
        username_hash = ''
        password_hash = hash_text(password)

        if username:
            username_hash = hash_text(username)
            try:
                if User.objects.filter(username=username_hash, password=password_hash).exists():
                    customer = User.objects.get(username=username_hash, password=password_hash)
                elif User.objects.filter(email=username, password=password_hash).exists():
                    customer = User.objects.get(email=username, password=password_hash)
            except ObjectDoesNotExist:
                print("'User does not exists'", tag='Not Found', tag_color='red', color= 'purple')
                return Response({'message': 'User does not exist'}, status=204)
        else:
            return Response({'message': 'plz enter username'}, status=400)

        if customer and customer.role != 'customer':
            try:
                with open(f'user/static/customer_img/{customer.img}', 'rb') as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                print('(username:', customer.username, '), (email:', customer.email, '), (password:', customer.password, ')', tag='CUSTOMER-INFO', color='white', tag_color='white', format='bold', background='gray')
                
            except FileNotFoundError:
                with open(f'user/static/customer_img/blank-img.png', 'rb') as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                print('(username:', customer.username, '), (email:', customer.email, '), (password:', customer.password, ')', tag='CUSTOMER-INFO', color='white', tag_color='white', format='bold', background='gray')
                
            print("'", customer.role, "'", tag='CUSTOMER-ROLE',tag_color='blue', background='gray', color='blue', format='bold')

            return Response({
                'message': 'User exists',
                'role': customer.role,
                'id': customer.id,
                'username': customer.username,
                'email': customer.email,
                'password': customer.password,
                'date': customer.date,
                'image': "data:image/png;base64," + encoded_string,
            }, status=200)

        else:
            print("'User does not exists OR its customer'", tag='Not Found', tag_color='red', color= 'purple')
            return Response({'message': 'An Error Accoured'}, status=400)
            
    except json.JSONDecodeError:
        print('Json decode error', tag='LOGIN-Error', color='red', tag_colour='red')
        return Response({'error': 'Invalid JSON'}, status=400)

@api_view(['POST'])
def handle_signup(request):

    data = json.loads(request.body)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    base64_image = data.get("img")
    password_hash = hash_text(password)
    username_hash = hash_text(username)


    if User.objects.filter(username=username_hash, password=password_hash):
        print("'User already exists'")
        return Response({'message': 'User already exists'}, status=400)

    if base64_image:
        # this is 0nd inddex-> "data:image/png;base64,"
        # "viasdfjlkjlaskdjwiq .." <-this part is 1st index 
        image_data = base64.b64decode(base64_image.split(',')[1])
        image = Image.open(io.BytesIO(image_data))

        if image.format != 'PNG':
            image = image.convert('RGBA')

        unique_filename = generate_unique_filename_png('user/static/customer_img')

        image_path = os.path.join('user/static/customer_img', f'{unique_filename}.png')
        image.save(image_path)

        
        if User.objects.filter(username=username_hash).exists():
            print("'User already exists'", tag='warning', tag_color='yellow', color='yellow')
            return Response({'message': 'User already exists'}, status=400)

        if User.objects.filter(email=email).exists():
            print("'User already exists'", tag='warning', tag_color='yellow', color='yellow')
            return Response({'message': 'User already exists'}, status=400)

        new_user = User(username=username_hash, email=email, password=password_hash, date=datetime.datetime.now(), img=f'{unique_filename}.png')
        new_user.save()

    else:

        if User.objects.filter(username=username_hash).exists():
            print("'User already exists'", tag='warning', tag_color='yellow', color='yellow')
            return Response({'message': 'User already exists'}, status=400)
        if User.objects.filter(email=email).exists():
            print("'User already exists'", tag='warning', tag_color='yellow', color='yellow')
            return Response({'message': 'User already exists'}, status=400)


        new_user = User(username=username_hash, email=email, password=password_hash, date=datetime.datetime.now())
        new_user.save()        

    print('(', email, '), (', username_hash, '), (', password_hash, ')')
    return Response({'message': 'User registered successfully'}, status=201)

@api_view(['PUT'])
def update_user(request):
    data = json.loads(request.body)

    user_id = data.get("user_id")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    base64_image = data.get("img")

    password_hash = hash_text(password)
    username_hash = hash_text(username)

    if User.objects.filter(id=user_id).exists():
        if base64_image:

            image_data = base64.b64decode(base64_image.split(',')[1])
            image = Image.open(io.BytesIO(image_data))

            if image.format != 'PNG':
                image = image.convert('RGBA')

            unique_filename = generate_unique_filename_png('user/static/customer_img')

            image_path = os.path.join('user/static/customer_img', f'{unique_filename}.png')
            image.save(image_path)

            user_obj = User.objects.get(id=user_id)
            for_username = User.objects.get(id=user_id)
            if username_hash != for_username.username and username:
                user_obj.username = username_hash
            for_email = User.objects.get(id=user_id)
            if email != for_email.email and email:
                user_obj.email = email
            for_password = User.objects.get(id=user_id)
            if password_hash != for_password.password and password:
                user_obj.password = password_hash
            user_obj.date = datetime.datetime.now()
            user_obj.img = f'{unique_filename}.png'
            user_obj.save()
    
        else:
            
            obj = User.objects.get(id=user_id)
            for_username = User.objects.get(id=user_id)
            if hash_text(username) != for_username.username and username:
                obj.username = username_hash
            for_email = User.objects.get(id=user_id)
            if email != for_email.email and email:
                obj.email = email
            for_password = User.objects.get(id=user_id)
            if password_hash != for_password.password and password:
                obj.password = password_hash
            obj.date = datetime.datetime.now()
            obj.img = 'blank-img.png'
            obj.save()

        print('(', email, '), (', username_hash, '), (', password_hash, ') successfully updated', tag='user-updated', tag_color='blue', color='white')
        return Response({'message': 'User updated successfully'}, status=201)
    else:
        print("'User does not exists'", tag='Not Found', tag_color='red', color= 'purple')
        return Response({'message': 'User Not Found'}, status=204)

@api_view(['PUT'])
def user_update_user(request, user_id):

    role = request.data.get("role")
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    image_file = request.FILES.get("image")

    if User.objects.filter(id=user_id).exists():
        if User.objects.get(id=user_id).email != email and User.objects.filter(email=email).exists():
            return Response({'message': 'User already exists'}, status=400)

        if User.objects.filter(id=user_id, password=password).exists() and User.objects.get(id=user_id, password=password).password == password:
            password_hash = password
        else:
            password_hash = hash_text(password)
        if User.objects.filter(id=user_id, username=username).exists() and User.objects.get(id=user_id, username=username).username == username:
        # if User.objects.filter(id=user_id, username=hash_text(username)).exists() and User.objects.get(id=user_id, username=hash_text(username)).username == hash_text(username):
            username_hash = username
        else:
            username_hash = hash_text(username)

        
        if image_file:
            image = Image.open(image_file)

            if image.format != 'PNG':
                image = image.convert('RGBA')

            unique_filename = generate_unique_filename_png('user/static/customer_img')
            image_path = os.path.join('user/static/customer_img', f'{unique_filename}.png')
            image.save(image_path)

            obj = User.objects.get(id=user_id)

            if username_hash != User.objects.get(id=user_id).username and username:
                obj.username = username_hash
            for_email = User.objects.get(id=user_id)
            if email != for_email.email and email:
                obj.email = email
            for_password = User.objects.get(id=user_id)
            if password_hash != for_password.password and password:
                obj.password = password_hash
            obj.date = datetime.datetime.now()
            obj.role = role
            obj.img = f'{unique_filename}.png'
            obj.save()
        else:
            
            obj = User.objects.get(id=user_id)
            if username and hash_text(username) != User.objects.get(id=user_id).username:
                obj.username = username_hash
            if email and email != User.objects.get(id=user_id).email:
                obj.email = email
            if password and hash_text(password) != User.objects.get(id=user_id).password:
                obj.password = password_hash
            obj.date = datetime.datetime.now()
            obj.role = role
            obj.save()

        total = User.objects.all().count()

        serializer = UserSerializer(obj)
        print(serializer.data, tag='user-updated', tag_color='blue', color='blue')
        return Response({"data": serializer.data}, status=201)
    else:
        print("'User does not exists'", tag='Not Found', tag_color='red', color= 'purple')
        return Response({'message': 'User Not Found'}, status=204)

@api_view(['GET'])
def get_one_user(request, id):
        try:
            if User.objects.filter(id=id).exists():
                customer = User.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({'message': 'User does not exist'}, status=404)


        if customer:
            try:
                with open(f'user/static/customer_img/{customer.img}', 'rb') as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                print('(', customer.username, '), (', customer.email, '), (', customer.password, ')')
            except FileNotFoundError:
                with open(f'user/static/customer_img/blank-img.png', 'rb') as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                print('(', customer.username, '), (', customer.email, '), (', customer.password, ')')
            print(customer.role)
            return Response({
                'role': customer.role,
                'id': customer.id,
                'username': customer.username,
                'email': customer.email,
                'password': customer.password,
                'date': customer.date,
                'image': "data:image/png;base64," + encoded_string,
            }, status=200)
        else:
            return Response({'message': 'User does not exist'}, status=400)

@api_view()
def get_all_user(request):
    
    filter_param = json.loads(request.query_params.get('filter', '{}'))
    range_param = json.loads(request.query_params.get('range', '[0, 9]'))
    sort_param = json.loads(request.query_params.get('sort', '["id", "ASC"]'))

    users = User.objects.all()

    if filter_param:
        for key, value in filter_param.items():
            users = users.filter(**{f"{key}__icontains": value})

    if sort_param:
        field, order = sort_param
        if order.upper() == 'DESC':
            users = users.order_by(f'-{field}')
        else:
            users = users.order_by(field)

    paginator = Paginator(users, 10) # Assuming a page size of 10
    page_number = range_param[0] // 10 + 1 # Calculate the page number based on the range
    users = paginator.get_page(page_number)

    
    all_users = []
    # if users:
    for customer in users:
        try:
            with open(f'user/static/customer_img/{customer.img}', 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            with open(f'user/static/customer_img/blank-img.png', 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        all_users.append({
            "role": customer.role,
            "id": customer.id,
            "username": customer.username,
            "email": customer.email,
            "password": customer.password,
            "date": customer.date,
            "image": "data:image/png;base64," + encoded_string,
        })

    total = User.objects.all().count()
    start_index = (page_number - 1) * 10
    end_index = start_index + len(users) - 1

    headers = {
    'Content-Range': f'{start_index}-{end_index}/{total}',
    }

    return Response({"data": all_users}, status=200, headers=headers)
    # else:
    #     return Response({'message': 'There is no any user'}, status=400)

@api_view(['DELETE'])
def user_delete(request, id):
    if User.objects.filter(id=id).exists():
        U_obj = User.objects.filter(id=id).delete()

        print(f'deleted user id: {id}', tag='user-deleted', tag_color='purple', color='magenta')
        return Response({ "id": id }, status=204)
    else:
        print('not found', tag='Not Found', tag_color='red', color='purple', background='gray')
        return Response({'message': 'Post Not Found'}, status=204)
