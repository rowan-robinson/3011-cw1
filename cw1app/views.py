from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from cw1app.models import Professor, Module, ModuleInstance, Rating
from cw1app.serializers import UserSerializer, ProfessorSerializer, ModuleSerializer, ModuleInstanceSerializer, RatingSerializer
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from django.db.models import Avg

# - API ENDPOINT - root
# core functionality
@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "users": reverse("user-list", request=request, format=format),
        "professors": reverse("professor-list", request=request, format=format),
        "modules": reverse("module-list", request=request, format=format),
        "moduleinstances": reverse("moduleinstance-list", request=request, format=format),
        "ratings": reverse("rating-list", request=request, format=format),
    })

# - API ENDPOINT - user login
# allows users to log in
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def user_login(request):
    # get the username and password from the request
    # and use these to authenticate the user
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key
            }, status=200
        )
    else:
        return Response({
            "error": "Credentials are invalid!"
            }, status=400
        )

# - API ENDPOINT - user logout
# allows users to log out
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def user_logout(request):
    # check if the user is even authenticated
    if request.auth is None:
        logout(request)
        return Response(status=200)

    # attempt to delete the auth token
    try:
        request.user.auth_token.delete()
        return Response(status=200)
    except Token.DoesNotExist:
        return Response({
            "error": "Token is invalid!"
            }, status=400
        )

# - API ENDPOINT - user view/edit
# allows users to be viewed and edited
@permission_classes([permissions.AllowAny])
class UserViewSet(viewsets.ModelViewSet):
    """
    List or edit users.
    """
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer

# - API ENDPOINT - professor list
# lists all professors
class ProfessorViewSet(viewsets.ModelViewSet):
    """
    List all professors.
    """
    queryset = Professor.objects.all().order_by("code")
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.IsAuthenticated]

# - API ENDPOINT - professor avg rating
# gives the average rating of a professor for a specific module
class ProfessorAvgViewSet(viewsets.ModelViewSet):
    """
    Gives average rating of a professor for a specific module.
    """
    # 'request' necessary despite never explicitly being referred to
    def retrieve(self, request, professorCode, moduleCode):
        try:
            professor = Professor.objects.get(code=professorCode)
            module = Module.objects.get(code=moduleCode)
            avgRating = Rating.objects.filter(professor_id=professorCode, module_id=moduleCode).aggregate(Avg("score"))["score__avg"]
            if avgRating:
                avgRating = round(avgRating)
            else:
                avgRating = -1
            return Response({
                'professor-code': professor.code,
                'professor-name': professor.name,
                'module-code': module.code,
                'module-name': module.name,
                'avg-rating': int(avgRating),
            }, status=200)
        except:
            return Response({
                "error": "Could not find chosen professor/module combination!"
            }, status=400)
        
# - API ENDPOINT - module list
# lists all modules
class ModuleViewSet(viewsets.ModelViewSet):
    """
    List all modules.
    """
    queryset = Module.objects.all().order_by("code")
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]

# - API ENDPOINT - module instance list
# lists all module instances
class ModuleInstanceViewSet(viewsets.ModelViewSet):
    """
    List all module instances.
    """
    queryset = ModuleInstance.objects.all().order_by("id")
    serializer_class = ModuleInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]

# - API ENDPOINT - rating list
# lists all ratings
class RatingViewSet(viewsets.ModelViewSet):
    """
    List all ratings made of module instances by users.
    """
    queryset = Rating.objects.all().order_by("score")
    serializer_class = RatingSerializer

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)