from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post, Category, Tag, PostCategory, PostTag
from comment.models import Comment
from user.models import User
from .serializers import PostSerializer
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image
from print_color import print
import datetime
import base64
import json
import os
import uuid
import io



def generate_unique_filename_png(directory):
    while True:
            # Generate a random UUID and convert it to a string
        random_name = str(uuid.uuid4())
            # Append the current timestamp to the UUID
        file_name = f'{random_name}_{str(uuid.uuid4())}'
        #     # Create the full file path
        file_path = os.path.join(directory, f'{file_name}.png')
            # Check if the file already exists
        if not os.path.exists(file_path):
            return file_name


@api_view(['POST'])
def post_create(request):

    data = json.loads(request.body)

    user_id = data.get("user")
    title = data.get("title")
    content = data.get("content")
    base64_image = data.get("img")
    category_name = data.get("category_name")
    tag_names = data.get("tag_names")
    tag_bg_colors = data.get("tag_bg_colors")
    tag_txt_colors = data.get("tag_txt_colors")

    user_role = ''
    post_id = 0
    

    try:
        user_role = User.objects.get(id=user_id).role
        print("'User exists'", tag='Found', tag_color='green', color= 'green')
    except ObjectDoesNotExist:
        print("'User does not exists'", tag='Not Found', tag_color='red', color= 'purple')
        return Response({'message': 'User does not exist'}, status=204)

    if user_role != 'customer':
        print("'Its not customer'", tag='wrong-role', tag_color='red', color= 'purple')
        return Response({'message': 'Unknown auther'}, status=204)
                
    if category_name:
        if Category.objects.filter(name=category_name).exists():
            print("'Category already exists'", 
            tag='warning', tag_color='yellow', color='yellow', background='gray')

        else:
            new_category = Category(name=category_name, created_at=datetime.datetime.now())
            new_category.save()
            category_id = new_category.id

            print(f"' Category created: `{category_id}` '", 
            tag='success', tag_color='blue', color='blue', background='gray')

    if tag_names:
        for name in tag_names:
            if Tag.objects.filter(name=name).exists():
                print("'Tag already exists'", 
                tag='warning', tag_color='yellow', color='yellow', background='gray')

            else:
                new_tag = Tag(name=name)              
                new_tag.save()
                tag_id = new_tag.id
            
                print(f"' Tag created: `{tag_id}` '", 
                tag='success', tag_color='blue', color='blue', background='gray')

    if base64_image:
        image_data = base64.b64decode(base64_image.split(',')[1])
        image = Image.open(io.BytesIO(image_data))

        if image.format != 'PNG':
            image = image.convert('RGBA')

        unique_filename = generate_unique_filename_png('post/static/post_img')

        image_path = os.path.join('post/static/post_img', f'{unique_filename}.png')
        image.save(image_path)

        new_post = Post(user_id=user_id, title=title, content=content, date=datetime.datetime.now(), img=f'{unique_filename}.png')
        new_post.save()

        post_id = new_post.id
        
    else:
        new_post = Post(user_id=user_id, title=title, content=content, date=datetime.datetime.now())
        new_post.save()

        post_id = new_post.id

    if category_name:
        category_object_id = Category.objects.get(name=category_name).id

        post_instance = Post.objects.get(id=post_id).id
        category_instance = Category.objects.get(id=category_object_id).id

        new_postCategory = PostCategory(post_id=post_instance, category_id=category_instance)
        new_postCategory.save()

    if tag_names and tag_bg_colors and tag_txt_colors:
        for name, bg, txt in zip(tag_names, tag_bg_colors, tag_txt_colors):
            tag_object_id = Tag.objects.get(name=name).id

            post_instance = Post.objects.get(id=post_id).id
            tag_instance = Tag.objects.get(id=tag_object_id).id

            new_tag = PostTag(post_id=post_instance, tag_id=tag_instance, backGround_color=bg, text_color=txt)
            new_tag.save()

    print('(', user_id,'), (', title, '), (', content, '), (', datetime.datetime.now(), ') created', tag='post-created', tag_color='blue', color='white')

    return Response({'message': 'Post defined successfully'}, status=201)
        
@api_view(['POST'])
def post_read_one(request):
    
    data = json.loads(request.body)
    post_id = data.get("id")
    
    post_detail = {}
    post_categories = []
    post_tags = []
    post_comments = []

    
    if Post.objects.filter(id=post_id).exists():
        post = Post.objects.get(id=post_id)
        
        if post.img != 'empty':
            with open(f'post/static/post_img/{post.img}', 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            post_detail = {
                "id" : post.id,
                "user_id": post.user_id,
                "title": post.title,
                "content": post.content,
                "date": post.date,
                "img": "data:image/png;base64," + encoded_string,
            }
        else:
            post_detail = {
                "id" : post.id,
                "user_id": post.user_id,
                "title": post.title,
                "content": post.content,
                "date": post.date,
                "img": "empty",
            }

        if PostCategory.objects.filter(post_id=post_id).exists():
            categories = PostCategory.objects.filter(post_id=post_id)
            for category in categories:
                category_name = Category.objects.get(id=category.category_id).name
                post_categories.append({
                    "id": category.id,
                    "post_id": category.post_id,
                    "category_name": category_name,
                })
        if PostTag.objects.filter(post_id=post_id).exists():
            tags = PostTag.objects.filter(post_id=post_id)
            for tag in tags:
                tag_name = Tag.objects.get(id=tag.tag_id).name
                post_tags.append({
                    "id": tag.id,
                    "post_id": tag.post_id,
                    "tag_name": tag_name,
                    "bg": tag.backGround_color,
                    "txt": tag.text_color,
                })
        if Comment.objects.filter(post_id=post_id).exists():
            comments = Comment.objects.filter(post_id=post_id)
            for comment in comments:
                post_comments.append({
                    "id": comment.id,
                    "user_id": comment.user_id,
                    "content": comment.content,
                    "post_id": comment.post_id,
                    "date": comment.date,
                })

        print(f"'post sent successfully'", 
        tag='success', tag_color='green', color='green', background='gray')
        return Response({"post": post_detail, "categories": post_categories, "tags": post_tags, "comments": post_comments}, status=200)
    else:
        print(f"'not found'", 
        tag='Not Found', tag_color='red', color='purple', background='gray')
        return Response({'error': 'Post Not Found'}, status=204)    

@api_view()
def post_read_many_user(request):
    # Parse query parameters
    filter_param = json.loads(request.query_params.get('filter', '{}'))
    range_param = json.loads(request.query_params.get('range', '[0, 9]'))
    sort_param = json.loads(request.query_params.get('sort', '["id", "ASC"]'))

    # Apply filters, sorting, and pagination
    posts = Post.objects.all()

    if filter_param:
        for key, value in filter_param.items():
            posts = posts.filter(**{f"{key}__icontains": value})

    # Apply sorting
    if sort_param:
        field, order = sort_param
        if order.upper() == 'DESC':
            posts = posts.order_by(f'-{field}')
        else:
            posts = posts.order_by(field)

    # Apply pagination
    paginator = Paginator(posts, 10) # Assuming a page size of 10
    page_number = range_param[0] // 10 + 1 # Calculate the page number based on the range
    posts = paginator.get_page(page_number)

    # Prepare post details
    post_details = []
    for post in posts:

        # if PostCategory.objects.filter(post_id=post.id).exists():
        #     categories = PostCategory.objects.filter(post_id=post.id)
        #     for category in categories:
        #         category_name = Category.objects.get(id=category.category_id).name
        #         post_categories.append({
        #             "id": category.id,
        #             "post_id": category.post_id,
        #             "category_name": category_name,
        #     })
        # if PostTag.objects.filter(post_id=post.id).exists():
        #     tags = PostTag.objects.filter(post_id=post.id)
        #     for tag in tags:
        #         tag_name = Tag.objects.get(id=tag.tag_id).name
        #         post_tags.append({
        #             "id": tag.id,
        #             "post_id": tag.post_id,
        #             "tag_name": tag_name,
        #             "bg": tag.backGround_color,
        #             "txt": tag.text_color,
        #         })

        if post.img != 'empty':
            with open(f'post/static/post_img/{post.img}', 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            post_details.append({
                "message": 'exists',
                "id": post.id,
                "user_id": post.user_id,
                "title": post.title,
                "content": post.content,
                "date": post.date,
                "img": "data:image/png;base64," + encoded_string,
            })
        else:
            post_details.append({
                "message": 'exists',
                "id": post.id,
                "user_id": post.user_id,
                "title": post.title,
                "content": post.content,
                "date": post.date,
                "img": "empty",
            })
    total = Post.objects.all().count()

    start_index = (page_number - 1) * 10
    end_index = start_index + len(posts) - 1

    headers = {
        'Content-Range': f'{start_index}-{end_index}/{total}',
    }

    serializer = PostSerializer(post_details, many=True)
    print(f"'posts sent'", tag='success', tag_color='green', color='green', background='gray')
    # print({"data": serializer.data,  "headers": headers})
    return Response({"data": serializer.data}, status=200, headers=headers)

@api_view()
def post_read_many_customer(request):
    if Post.objects.all().exists():
        post_details = []
        post_detail = {}
        
        for post in Post.objects.all():
            if post.img != 'empty':
                with open(f'post/static/post_img/{post.img}', 'rb') as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                post_detail = {
                    "id" : post.id,
                    "user_id": post.user_id,
                    "title": post.title,
                    "content": post.content,
                    "date": post.date,
                    "img": "data:image/png;base64," + encoded_string,
                }
            else:
                post_detail = {
                    "id" : post.id,
                    "user_id": post.user_id,
                    "title": post.title,
                    "content": post.content,
                    "date": post.date,
                    "img": "empty",
                }
            
            # Fetch categories, tags, and comments for each post.
            post_categories = []
            post_tags = []
            post_comments = []
            
            if PostCategory.objects.filter(post_id=post.id).exists():
                categories = PostCategory.objects.filter(post_id=post.id)
                for category in categories:
                    category_name = Category.objects.get(id=category.category_id).name
                    post_categories.append({
                        "id": category.id,
                        "post_id": category.post_id,
                        "category_name": category_name,
                    })
            if PostTag.objects.filter(post_id=post.id).exists():
                tags = PostTag.objects.filter(post_id=post.id)
                for tag in tags:
                    tag_name = Tag.objects.get(id=tag.tag_id).name
                    post_tags.append({
                        "id": tag.id,
                        "post_id": tag.post_id,
                        "tag_name": tag_name,
                        "bg": tag.backGround_color,
                        "txt": tag.text_color,
                    })
            if Comment.objects.filter(post_id=post.id).exists():
                for comment in Comment.objects.filter(post_id=post.id):
                    post_comments.append({
                        "id": comment.id,
                        "user_id": comment.user_id,
                        "content": comment.content,
                        "post_id": comment.post_id,
                        "date": comment.date,
                    })
            
            post_details.append({
                "posts": post_detail,
                "categories": post_categories,
                "tags": post_tags,
                "comments": post_comments
            })
        
        print(f"'posts sent'", 
                tag='success', tag_color='green', color='green', background='gray')
        return Response({"posts": post_details}, status=200)
    else:
        print(f"'not found'", 
                tag='Not Found', tag_color='red', color='purple', background='gray')
        return Response({'error': 'Posts Not Found'}, status=204)    

@api_view(['PUT'])
def post_update(request):
    data = json.loads(request.body)

    post_id_put = data.get("id")
    title = data.get("title")
    content = data.get("content")
    base64_image = data.get("img")
    category_name = data.get("category_name")
    tag_names = data.get("tag_names")
    tag_bg_colors = data.get("tag_bg_colors")
    tag_txt_colors = data.get("tag_txt_colors")

    if Post.objects.filter(id=post_id_put).exists():
        if category_name:
            if Category.objects.filter(name=category_name).exists():

                print("'Category already exists'", 
                tag='warning', tag_color='yellow', color='yellow', background='gray')

            else:
                
                new_category = Category(name=category_name, created_at=datetime.datetime.now())
                new_category.save()

                print(f"' Category created: `{new_category.name}` '", 
                tag='success', tag_color='blue', color='blue', background='gray')
        if tag_names:
            for name in tag_names:
                if Tag.objects.filter(name=name).exists():
                    print("'Tag already exists'", 
                    tag='warning', tag_color='yellow', color='yellow', background='gray')

                else:
                    new_tag = Tag(name=name)              
                    new_tag.save()
                    tag_id = new_tag.id
                
                    print(f"' Tag created: `{tag_id}` '", 
                    tag='success', tag_color='blue', color='blue', background='gray')

        if base64_image:
            image_data = base64.b64decode(base64_image.split(',')[1])
            image = Image.open(io.BytesIO(image_data))

            if image.format != 'PNG':
                image = image.convert('RGBA')

            unique_filename = generate_unique_filename_png('post/static/post_img')

            image_path = os.path.join('post/static/post_img', f'{unique_filename}.png')
            image.save(image_path)


            obj = Post.objects.get(id=post_id_put)
            obj.title = title
            obj.content = content
            obj.date = datetime.datetime.now()
            obj.img = f'{unique_filename}.png'
            obj.save()
        else:

            obj = Post.objects.get(id=post_id_put)
            obj.title = title
            obj.content = content
            obj.date = datetime.datetime.now()
            obj.img = 'empty'
            obj.save()

        # if category_name:
        #     obj = PostCategory.objects.get(post_id=post_id_put).delete()

        #     id = Category.objects.get(name=category_name).id
            
        #     new_postCategory = PostCategory(post_id=post_id_put, category_id=id)
        #     new_postCategory.save()      
        # if tag_names:
        #     obj = PostTag.objects.filter(post_id=post_id_put).delete()

        #     for name in tag_names:
        #         id = Tag.objects.get(name=name).id

        #         new_postTag = PostTag(post_id=post_id_put, tag_id=id)
        #         new_postTag.save()
        if category_name:
            obj = PostCategory.objects.filter(post_id=post_id_put).delete()

            post_instance = Post.objects.get(id=post_id_put).id
            category_instance = Category.objects.get(name=category_name).id

            new_postCategory = PostCategory(post_id=post_instance, category_id=category_instance)
            new_postCategory.save()
        if tag_names and tag_bg_colors and tag_txt_colors:
            obj = PostTag.objects.filter(post_id=post_id_put).delete()

            for name, bg, txt in zip(tag_names, tag_bg_colors, tag_txt_colors):
                tag_object_id = Tag.objects.get(name=name).id

                post_instance = Post.objects.get(id=post_id_put).id
                tag_instance = Tag.objects.get(id=tag_object_id).id

                new_post_tag = PostTag(post_id=post_instance, tag_id=tag_instance, backGround_color=bg, text_color=txt)
                new_post_tag.save()


            print('(', title, '), (', content, '), (', datetime.datetime.now(), ') update', tag='post-updated', tag_color='blue', color='white')

            return Response({'message': 'Post updated successfully'}, status=201)


        print('(', title, '), (', content, '), (', datetime.datetime.now(), ') updated', tag='post-updated', tag_color='blue', color='white')

        return Response({'message': 'Post updated successfully'}, status=201)
    else:
        print('not found', tag='Not Found', tag_color='red', color='purple', background='gray')
        return Response({'message': 'Post Not Found'}, status=204)

@api_view(['DELETE'])
def post_delete(request, id):
    if Post.objects.filter(id=id).exists():

        P_obj = Post.objects.filter(id=id).delete()

        PC_obj = PostCategory.objects.filter(post_id=id).delete()

        PT_obj = PostTag.objects.filter(post_id=id).delete()

        print('post deleted', tag='post-deleted', tag_color='purple', color='magenta')
        return Response({'message': 'Post deleted successfully'}, status=204)
        # return Response({'message': 'Post deleted successfully'}, status=204)
    else:
        print('not found', tag='Not Found', tag_color='red', color='purple', background='gray')
        return Response({'message': 'Post Not Found'}, status=204)

@api_view(['DELETE'])
def post_delete_user(request, id):
    if Post.objects.filter(id=id).exists():
        P_obj = Post.objects.filter(id=id).delete()

        PC_obj = PostCategory.objects.filter(post_id=id).delete()

        PT_obj = PostTag.objects.filter(post_id=id).delete()

        print(f'deleted post id: {id}', tag='post-deleted', tag_color='purple', color='magenta')
        return Response({'id': id}, status=204)
    else:
        print('not found', tag='Not Found', tag_color='red', color='purple', background='gray')
        return Response({'message': 'Post Not Found'}, status=204)
