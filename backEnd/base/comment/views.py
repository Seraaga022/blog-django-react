from .models import Comment
from user.models import User 
from post.models import Post
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.paginator import Paginator
from .serializers import *
import datetime
import json
from django.utils import timezone
from print_color import print


@api_view()
def test(request):
    result = Comment.objects.all()
    serializer = CommentSerializer(result, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def comment_create(request):
    data = json.loads(request.body)

    user_id = data.get("user")
    content = data.get("content")
    post_id = data.get("post_id")

    user_instance = User.objects.get(id=user_id)
    post_instance = Post.objects.get(id=post_id)

    new_comment = Comment(user=user_instance, post=post_instance, content=content, date=datetime.datetime.now())
    new_comment.save()

    print('(', user_id,'), (', post_id, '), (', content, '), (', datetime.datetime.now(), ') created', tag='comment-created', tag_color='blue', color='white')
    return Response({'message': 'Comment defined successfully'}, status=201)

@api_view(['POST'])
def comment_read_one(request):
    data = json.loads(request.body)

    comment_id = data.get("id")
    
    if Comment.objects.filter(id=comment_id).exists():
        comment = Comment.objects.get(id=comment_id)
        serializer = CommentSerializer(comment)
        
        print(f"'comment sent successfully'", 
        tag='success', tag_color='green', color='green', background='gray')
        return Response({"comment": serializer.data}, status=200)
    else:
        print(f"'not found'", 
        tag='Not Found', tag_color='red', color='purple', background='gray')
        return Response({'error': 'Comment Not Found'}, status=204)    
    # else:
    #     print(f"'your request: {request.method}'", 
    #     tag='warning', tag_color='yellow', color='yellow', background='gray')
    #     return Response({'error': 'Invalid request method'}, status=405)

@api_view()
def comment_read_many_post(request, id):
        # id is sending for using as post_id
        if Comment.objects.filter(post=id).exists():

            comments = Comment.objects.filter(post=id)

            serializer = CommentSerializer(comments, many=True)
                            
            print(f"'comments sent'", 
                    tag='success', tag_color='green', color='green', background='gray')
            return Response({"comments": serializer.data}, status=200)
        else:
            print(f"'not found'", 
                    tag='Not Found', tag_color='red', color='purple', background='gray')
            return Response({'error': 'Comments Not Found'}, status=204)    

@api_view()
def comment_read_all(request):
    # Parse query parameters
    filter_param = json.loads(request.query_params.get('filter', '{}'))
    range_param = json.loads(request.query_params.get('range', '[0, 9]'))
    sort_param = json.loads(request.query_params.get('sort', '["id", "ASC"]'))

    # Apply filters, sorting, and pagination
    comments = Comment.objects.all()

    if filter_param:
        for key, value in filter_param.items():
            comments = comments.filter(**{f"{key}__icontains": value})

    # Apply sorting
    if sort_param:
        field, order = sort_param
        if order.upper() == 'DESC':
            comments = comments.order_by(f'-{field}')
        else:
            comments = comments.order_by(field)

    # Apply pagination
    paginator = Paginator(comments, 10) # Assuming a page size of 10
    page_number = range_param[0] // 10 + 1 # Calculate the page number based on the range
    comments = paginator.get_page(page_number)

    # if comments:
    total = Comment.objects.all().count()

    start_index = (page_number - 1) * 10
    end_index = start_index + len(comments) - 1

    headers = {
    'Content-Range': f'{start_index}-{end_index}/{total}',
    }
    
    serializer = CommentSerializer(comments, many=True)

    print({"data": serializer.data}, format='bold')

    print(f"'comments sent'", 
            tag='success', tag_color='green', color='green', background='gray')
    return Response({"data": serializer.data}, status=200, headers=headers)
    # else:
    #     print(f"'not found'", 
    #             tag='Not Found', tag_color='red', color='purple', background='gray')
    #     return Response({'message': 'There is no any comment'}, status=404)

@api_view(['PUT'])
def comment_update(request):

    data = json.loads(request.body)
    comment_id = data.get("id")
    user_id = data.get("user")
    content = data.get("content")

    if Comment.objects.filter(id=comment_id).exists():
        user_instance = User.objects.get(id=user_id)

        obj = Comment.objects.get(id=comment_id, user=user_instance)
        obj.content = content
        obj.date = datetime.datetime.now()
        obj.save()

        print('(', comment_id, '), (', user_id, '), (', content, ') updated', tag='comment-updated', tag_color='blue', color='white')
        return Response({'message': 'Comment updated successfully'}, status=201)
    else:
        print('not found', tag='Not Found', tag_color='red', color='purple', background='gray')
        return Response({'message': 'Comment Not Found'}, status=204)

@api_view(['DELETE'])
def comment_delete(request, id):
    if Comment.objects.filter(id=id).exists():

        obj = Comment.objects.get(id=id).delete()

        print('comment deleted', tag='comment-deleted', tag_color='purple', color='magenta')
        return Response({ 'id': id }, status=204)
    else:
        print('not found', tag='Not Found', tag_color='red', color='purple', background='gray')
        return Response({'message': 'Comment Not Found'}, status=204)
