class AdminsDBRouter:
    """
    A router to control all database operations on models in the admins app.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'admins':
            return 'admins'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'admins':
            return 'admins'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations only within the same DB
        if obj1._meta.app_label == 'admins' and obj2._meta.app_label == 'admins':
            return True
        elif 'admins' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'admins':
            return db == 'admins'
        return db == 'default'
