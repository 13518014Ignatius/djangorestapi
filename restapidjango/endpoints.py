from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# login_request function 
# a POST endpoint to log in using username and password
# returns token and 200 OK if successful, but error message and 400 BAD REQUEST if not successful
@api_view(['POST'])
def login_request(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
# register_request function 
# a POST endpoint to register a user using username, password, and email
# returns success message and 201 CREATED if successful, but error message and 400 BAD REQUEST if not successful
@api_view(['POST'])
def register_request(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    if not username or not password or not email:
        return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
        return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password, email=email)
    user.save()
    return Response({"success": "User created"}, status=status.HTTP_201_CREATED)

# list_users_request function 
# a GET endpoint to get a list of username and email of all users stored in the database
# returns user_list and 200 OK
@api_view(['GET'])
def list_users_request(request):
    users = User.objects.all()
    user_list = []
    for user in users:
        user_list.append({"username": user.username, "email": user.email})
    return Response(user_list, status=status.HTTP_200_OK)

# add_user_request function 
# a POST endpoint to add a new user
# similar to register_request, but requiring to be logged on
# returns success message and 201 CREATED if successful, but error message and 400 BAD REQUEST/403 FORBIDDEN if not successful
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user_request(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    if not username or not password or not email:
        return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
        return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password, email=email)
    user.save()
    return Response({"success": "User created"}, status=status.HTTP_201_CREATED)

# remove_user_request function 
# a DELETE endpoint to delete a user from the database
# returns success message and 204 NO CONTENT if successful, but error message and 400 BAD REQUEST/404 NOT FOUND if not successful
@api_view(['DELETE'])
def remove_user_request(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            user.delete()
            return Response({"success": "User deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
# login_request function 
# a POST endpoint to log in using username and password
# returns token and 200 OK if successful, but error message and 400 BAD REQUEST if not successful    
def authenticate_with_token(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return None