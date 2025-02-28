from sqladmin import ModelView
from glovo_app.db.models import UserProfile, Category


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username, UserProfile.role]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]

