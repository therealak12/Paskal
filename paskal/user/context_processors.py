def add_user_info(request):
    return {
        'user': request.user
    }
