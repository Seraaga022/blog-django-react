from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator
from .models import Draft, DraftCategory, DraftTag
from post.models import Post, Category, Tag, PostTag, PostCategory
from user.models import User
from .serializers import DraftSerializer
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image
from print_color import print
import datetime
import base64
import json
import shutil
import os
import io
import uuid
import time

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


@api_view()
def draft_read_many_user(request):
    # Parse query parameters
    filter_param = json.loads(request.query_params.get('filter', '{}'))
    range_param = json.loads(request.query_params.get('range', '[0, 9]'))
    sort_param = json.loads(request.query_params.get('sort', '["id", "ASC"]'))

    # Apply filters, sorting, and pagination
    drafts = Draft.objects.all()

    if filter_param:
        for key, value in filter_param.items():
            drafts = drafts.filter(**{f"{key}__icontains": value})

    # Apply sorting
    if sort_param:
        field, order = sort_param
        if order.upper() == 'DESC':
            drafts = drafts.order_by(f'-{field}')
        else:
            drafts = drafts.order_by(field)

    # Apply pagination
    paginator = Paginator(drafts, 10) # Assuming a page size of 10
    page_number = range_param[0] // 10 + 1 # Calculate the page number based on the range
    drafts = paginator.get_page(page_number)

    # Prepare draft details
    draft_details = []
    for draft in drafts:
        if draft.img != 'empty':
            with open(f'draft/static/draft_img/{draft.img}', 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            draft_details.append({
                "message": 'exists',
                "id": draft.id,
                "user_id": draft.user_id,
                "title": draft.title,
                "content": draft.content,
                "img": "data:image/png;base64," + encoded_string,
            })
        else:
            draft_details.append({
                "message": 'exists',
                "id": draft.id,
                "user_id": draft.user_id,
                "title": draft.title,
                "content": draft.content,
                "img": "empty",
            })
    total = Draft.objects.all().count()

    start_index = (page_number - 1) * 10
    end_index = start_index + len(drafts) - 1

    headers = {
        'Content-Range': f'{start_index}-{end_index}/{total}',
    }

    serializer = DraftSerializer(draft_details, many=True)
    print(f"'drafts sent'", tag='success', tag_color='green', color='green', background='gray')
    return Response({"data": serializer.data}, status=200, headers=headers)

@api_view(['POST'])
def draft_create(request):
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

        unique_filename = generate_unique_filename_png('draft/static/draft_img')

        image_path = os.path.join('draft/static/draft_img', f'{unique_filename}.png')
        image.save(image_path)

        new_draft = Draft(user_id=user_id, title=title, content=content, img=f'{unique_filename}.png')
        new_draft.save()

        draft_id = new_draft.id
    else:

        new_draft = Draft(user_id=user_id, title=title, content=content)
        new_draft.save()

        draft_id = new_draft.id

    if category_name:

        category_object_id = Category.objects.get(name=category_name).id

        draft_instance = Draft.objects.get(id=draft_id).id
        category_instance = Category.objects.get(id=category_object_id).id

        new_draftCategory = DraftCategory(draft_id=draft_instance, category_id=category_instance)
        new_draftCategory.save()
    if tag_names and tag_bg_colors and tag_txt_colors:
        for name, bg, txt in zip(tag_names, tag_bg_colors, tag_txt_colors):
            tag_object_id = Tag.objects.get(name=name).id

            draft_instance = Draft.objects.get(id=draft_id).id
            tag_instance = Tag.objects.get(id=tag_object_id).id

            new_tag = DraftTag(draft_id=draft_instance, tag_id=tag_instance, backGround_color=bg, text_color=txt)
            new_tag.save()


    print('(', user_id,'), (', title, '), (', content, '), (', datetime.datetime.now(), ') created', tag='draft-created', tag_color='blue', color='white')

    return Response({'message': 'Draft defined successfully'}, status=201)
  
@api_view(['POST'])
def draft_read_one(request):
    data = json.loads(request.body)
    draft_id = data.get("id")
    
    draft_detail = {}
    draft_categories = []
    draft_tags = []
    
    if Draft.objects.filter(id=draft_id).exists():
        draft = Draft.objects.get(id=draft_id)

        if draft.img != 'empty':
            with open(f'draft/static/draft_img/{draft.img}', 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            draft_detail = {
                "id" : draft.id,
                "user_id": draft.user_id,
                "title": draft.title,
                "content": draft.content,
                "img": "data:image/png;base64," + encoded_string,
            }
        else:
            draft_detail = {
                "id" : draft.id,
                "user_id": draft.user_id,
                "title": draft.title,
                "content": draft.content,
                "img": "empty",
            }
        
        if DraftCategory.objects.filter(draft_id=draft_id).exists():
            categories = DraftCategory.objects.filter(draft_id=draft_id)
            for category in categories:
                category_name = Category.objects.get(id=category.category_id).name
                draft_categories.append({
                    "id": category.id,
                    "draft_id": category.draft_id,
                    "category_name": category_name,
                })
        if DraftTag.objects.filter(draft_id=draft_id).exists():
            tags = DraftTag.objects.filter(draft_id=draft_id)
            for tag in tags:
                tag_name = Tag.objects.get(id=tag.tag_id).name
                draft_tags.append({
                    "id": tag.id,
                    "draft_id": tag.draft_id,
                    "tag_name": tag_name,
                    "bg": tag.backGround_color,
                    "txt": tag.text_color,
                })

        print(f"'draft sent successfully'", 
        tag='success', tag_color='green', color='green', background='gray')
        return Response({"draft": draft_detail, "categories": draft_categories, "tags": draft_tags}, status=200)
    else:
        print(f"'not found'", 
        tag='Not Found', tag_color='red', color='purple', background='gray')
        return Response({'error': 'Draft Not Found'}, status=204)    

@api_view()
def draft_read_many(request):
    
    if Draft.objects.all().exists():
        drafts_details = []
        all_draft_detail = {}

        for draft in Draft.objects.all():
            if draft.img != 'empty':
                with open(f'draft/static/draft_img/{draft.img}', 'rb') as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                all_draft_detail = {
                    "id" : draft.id,
                    "user_id": draft.user_id,
                    "title": draft.title,
                    "content": draft.content,
                    "img": "data:image/png;base64," + encoded_string,
                }
            else:
                all_draft_detail = {
                    "id" : draft.id,
                    "user_id": draft.user_id,
                    "title": draft.title,
                    "content": draft.content,
                    "img": "empty",
                }
            
            drafts_categories = []
            drafts_tags = []

            if DraftCategory.objects.filter(draft_id=draft.id).exists():
                for category in DraftCategory.objects.filter(draft_id=draft.id):
                    category_name = Category.objects.get(id=category.category_id).name
                    drafts_categories.append({
                        "id": category.id,
                        "draft_id": category.draft_id,
                        "category_name": category_name,
                    })
            
            if DraftTag.objects.filter(draft_id=draft.id).exists():
                for tag in DraftTag.objects.filter(draft_id=draft.id):
                    tag_name = Tag.objects.get(id=tag.tag_id).name
                    drafts_tags.append({
                        "id": tag.id,
                        "draft_id": tag.draft_id,
                        "tag_name": tag_name,
                        "bg": tag.backGround_color,
                        "txt": tag.text_color,
                    })
            
            drafts_details.append({
                "drafts": all_draft_detail,
                "categories": drafts_categories,
                "tags": drafts_tags,
            })
        
        print(f"'drafts sent'", 
                tag='success', tag_color='green', color='green', background='gray')
        return Response({"drafts": drafts_details}, status=200)
    else:
        print(f"'not found'", 
                tag='Not Found', tag_color='red', color='purple', background='gray')
        return Response({'error': 'Drafts Not Found'}, status=204)    

@api_view(['PUT'])
def draft_update(request):
    data = json.loads(request.body)

    user_id = data.get("user")
    draft_id = data.get("draft_id")

    title = data.get("title")
    content = data.get("content")
    base64_image = data.get("img")
    category_name = data.get("category_name")
    tag_names = data.get("tag_names")
    tag_bg_colors = data.get("tag_bg_colors")
    tag_txt_colors = data.get("tag_txt_colors")

    if Draft.objects.filter(id=draft_id).exists():
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

            unique_filename = generate_unique_filename_png('draft/static/draft_img')

            image_path = os.path.join('draft/static/draft_img', f'{unique_filename}.png')
            image.save(image_path)

            obj = Draft.objects.get(id=draft_id)
            obj.title = title
            obj.content = content
            obj.date = datetime.datetime.now()
            obj.img = f'{unique_filename}.png'
            obj.save()
        else:

            obj = Draft.objects.get(id=draft_id)
            obj.title = title
            obj.content = content
            obj.date = datetime.datetime.now()
            obj.img = 'empty'
            obj.save()

        if category_name:
            obj = DraftCategory.objects.filter(draft_id=draft_id).delete()

            draft_instance = Draft.objects.get(id=draft_id).id
            category_instance = Category.objects.get(name=category_name).id

            new_draftCategory = DraftCategory(draft_id=draft_instance, category_id=category_instance)
            new_draftCategory.save()
        if tag_names and tag_bg_colors and tag_txt_colors:
            obj = DraftTag.objects.filter(draft_id=draft_id).delete()

            for name, bg, txt in zip(tag_names, tag_bg_colors, tag_txt_colors):
                tag_object_id = Tag.objects.get(name=name).id

                draft_instance = Draft.objects.get(id=draft_id).id
                tag_instance = Tag.objects.get(id=tag_object_id).id

                new_tag = DraftTag(draft_id=draft_instance, tag_id=tag_instance, backGround_color=bg, text_color=txt)
                new_tag.save()


            print('(', user_id,'), (', title, '), (', content, '), (', datetime.datetime.now(), ') update', tag='draft-updated', tag_color='blue', color='white')

            return Response({'message': 'Draft updated successfully'}, status=201)

    else:
        print('not found', tag='Not Found', tag_color='red', color='purple', background='gray')
        return Response({'message': 'Draft Not Found'}, status=204)

@api_view(['DELETE'])
def draft_delete(request, id):
    if Draft.objects.filter(id=id).exists():

        D_obj = Draft.objects.filter(id=id).delete()

        DC_obj = DraftCategory.objects.filter(draft_id=id).delete()

        DT_obj = DraftTag.objects.filter(draft_id=id).delete()

        print('draft deleted', tag='draft-deleted', tag_color='purple', color='magenta')
        return Response({'id': id}, status=204)
    else:
        print('not found', tag='Not Found', tag_color='red', color='purple', background='gray')
        return Response({'message': 'Draft Not Found'}, status=204)

@api_view(['POST'])
def draft_publish(request):
    data = json.loads(request.body)
    draft_id = data.get("id")

    if Draft.objects.filter(id=draft_id).exists():
        draft = Draft.objects.get(id=draft_id)

        if draft.img:
            source_path = f'draft/static/draft_img/{draft.img}'
            destination_path = f'post/static/post_img/{draft.img}'

            if draft.img != 'empty':
                if os.path.exists(source_path):
                    try:
                        shutil.move(source_path, destination_path)

                        if os.path.exists(destination_path):
                            print("'Successfully Draft image moved to Post image'", tag='success', tag_color='green', color='green')
                            # os.remove(source_path)
                        else:
                            print("'Post image not found'", tag='Not Found', tag_color='red', color='purple', background='gray')
                            return Response({'message': 'Draft Image Not Found'}, status=204)
                    except Exception as e:
                        print(f"'An error occurred: {e}'")
                        return Response({'message': f'Error:  {e}'}, status=500)
                else:
                    print("'draft image does not exists'", tag='Not Found', tag_color='red', color='purple', background='gray')
                    return Response({'message': 'Draft Image Not Found'}, status=204)

                new_post = Post(user_id=draft.user_id, title=draft.title, content=draft.content, date=datetime.datetime.now(), img=draft.img)
                new_post.save()
                post_id = new_post.id
            else:
                new_post = Post(user_id=draft.user_id, title=draft.title, content=draft.content, date=datetime.datetime.now())
                new_post.save()
                post_id = new_post.id
        else:

            new_post = Post(user_id=draft.user_id, title=draft.title, content=draft.content, date=datetime.datetime.now())
            new_post.save()
            post_id = new_post.id
        
        if DraftCategory.objects.filter(draft_id=draft_id).exists():
            category_id = DraftCategory.objects.get(draft_id=draft_id).category_id

            post_instance = Post.objects.get(id=post_id)
            category_instance = Category.objects.get(id=category_id)
            print(category_instance, format='bold', color='red')

            new_postCategory = PostCategory(post=post_instance, category=category_instance)
            new_postCategory.save()     
        if DraftTag.objects.filter(draft_id=draft_id).exists():
            for draftTag in DraftTag.objects.filter(draft_id=draft_id):
                draftTag_id = draftTag.tag_id
                draft_bg_color = draftTag.backGround_color
                draft_txt_color = draftTag.text_color
                name = Tag.objects.get(id=draftTag_id).name

                post_instance = Post.objects.get(id=post_id)
                tag_instance = Tag.objects.get(id=draftTag_id)

                new_tag = PostTag(post=post_instance, tag=tag_instance, backGround_color=draft_bg_color, text_color=draft_txt_color)
                new_tag.save()

        obj = Draft.objects.get(id=draft_id)
        obj.delete()

        print('(', str(draft.user_id),'), (', draft.title, '), (', draft.content, '), (', datetime.datetime.now(), ') created', tag='post-created', tag_color='blue', color='white')
        return Response({'message': 'Post defined successfully'}, status=201)
    else:
        print('not found', tag='Not Found', tag_color='red', color='purple', background='gray')
        return Response({'message': 'Draft Not Found'}, status=204)
