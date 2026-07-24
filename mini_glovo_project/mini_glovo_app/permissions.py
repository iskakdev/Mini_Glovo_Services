from rest_framework.permissions import BasePermission
from .models import Store


class IsStoreOwner(BasePermission):
    message = 'Создавать и изменять магазины может только владелец магазина'

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'status', None) == 'store_owner'
        )


class IsStoreOwnerObject(BasePermission):
    message = 'Изменять и удалять может только владелец данного магазина'

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        store = obj if isinstance(obj, Store) else obj.store
        return store.store_owner == request.user.id


class IsOwnerOfStore(BasePermission):
    message = 'Добавлять товар может только владелец соответствующего магазина'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        store_id = request.data.get('store')
        if not store_id:
            return False
        return Store.objects.filter(id=store_id, store_owner=request.user.id).exists()


class IsSimpleUser(BasePermission):
    message = 'Оставлять отзывы может только пользователь с ролью simple_user'

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'status', None) == 'simple_user'
        )


class IsReviewOwner(BasePermission):
    message = 'Изменять и удалять отзыв может только его автор'

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'status', None) == 'simple_user'
            and obj.user == request.user.id
        )