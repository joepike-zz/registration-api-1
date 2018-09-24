def user_detail_schema(obj):
    return {
        'email': obj.email,
        'username': obj.username,
        'first_name': obj.first_name,
        'last_name': obj.last_name
        # 'date_created': obj.date_created
    }
