# Django Deletion Records

This simple Django app contains a mechanism to track deleted model records.
Unlike the soft-deletion mechanism, the deleted content is saved to a separate
table.

The deleted records are inserted via database triggers, so you don't have to
write any additional code or change your base model classes. In fact, you only
need to perform related migration operations, and you are good to go; the
deleted records will start to appear in Django admin site.

## Comparison with soft delete

### Pros

* No overly-complicated application code. To make soft-deletion work, you
  need to override model managers so that deleted records are kept out. Even
  then, the abstraction is very leaky when managers are not available such
  as doing aggregations or joins.

* Database constraints are easier since you don't need to consider deleted
  records.

* Managing relationships are easier, for example you don't need to worry
  about `ForeignKey` cascades.

* Deleted records do not affect undeleted records at all. More often than
  not, soft-delete create problems with new or existing rows because
  someone forgets that soft-deleted records are actually there.

### Cons

* Reversing deletions are pretty difficult. In soft-delete, you can just flip
  a column (most of the time). For deletion records, you'll have to manually
  re-insert the data (and its dependencies).

* Data lookup is relatively difficult especially if you're maintaining
  complex relationships spanning multiple tables. In soft-delete, you can
  just do regular SQL lookups. However, deletion records require custom
  resolution for `ForeignKey`'s and such.

* Deletion operations are *relatively* slower since soft-delete updates
  are faster and there is no trigger penalty.

Soft-deleting is convenient when you need to restore data but creates
complexity in application code. Deletion records are much easier manage,
however it is difficult to restore data.

You may also use soft-deletes alongside deletion records if you want to keep
some tables soft-deleted and others recorded (for example, as audit logs).

## Installation

> `django-deletion-records` only works for PostgreSQL, other database backends
> are not supported.

1. Install from PyPI:

    ```shell
    pip install django-deletion-records
    ```

2. Add `deletion_records` to your `INSTALLED_APPS`, such as:

    ```python
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # ...
        'deletion_records',
    ]
    ```

3. Run migrate for `deletion_records`:

    ```shell
    python manage.py migrate deletion_records

    Operations to perform:
      Apply all migrations: deletion_records
    Running migrations:
      Applying deletion_records.0001_initial... OK
    ```

### Marking a model for deletion

To start recording deletions for a given model, you'll need to perform a
`RunSQL` operation (that will create the related trigger) via Django
migrations.

To start, create an empty migration file in your related app:

```shell
python manage.py makemigrations --empty your-app
```

This will create an empty migration with no operations. To get the related
operations we'll use the `deletion_migration_operations` management command:

```shell
python manage.py deletion_migration_operations yourapp.User

# yourapp.User
operations = [
    migrations.RunSQL(
        """
        CREATE TRIGGER deleted_record_insert
            AFTER DELETE
            ON yourapp_user
            FOR EACH ROW
        EXECUTE FUNCTION deletion_record_insert();
        """,
        reverse_sql="DROP TRIGGER IF EXISTS deleted_record_insert ON yourapp_user CASCADE;",
    )
]
```

Copy the given operations to your empty migration file, and apply the
migrations. Deletion records will start to appear, that's it!

## Tips

* You can supply multiple models for `deletion_migration_operations` to get
  multiple operations at once.

* You can have multiple operations in one migration file if you want to. It
  just depends on how you want to handle the migrations.

* If you want to enable deletion records for a third party model, you can
  still employ the steps above. You just need to figure out a proper
  application (that'll hold the migrations), people generally use "core" apps
  to do that kind of stuff.

* Reversing the migration created above will drop the related trigger, thus
  stopping the deletion recording. The formerly deleted records will be still
  available.

If you want to hard-delete some records (or manage deleted records for any
other reason), you can use the provided model as such:

```python
from deletion_records.models import DeletedRecord

# Deletes User objects with provided ids.
DeletedRecord.objects.filter(
    table_name="yourapp_user", object_id__in=[2, 3, 4]
).delete()
```

```python
from deletion_records.models import DeletedRecord

# Fetch a deleted record and view the data.
user = DeletedRecord.objects.get(table_name="account_user", object_id=276833)

assert user.data == {
    "id": 276833,
    "email": "lauren62@example.com",
    "is_staff": False,
    "password": "pbkdf2_sha256$600000$4X48PbRIeemb2ECW1pIlO4$jFuePmugUuTE4D6nIbP9TxGKcYxLBut81bR4JbshU8I=",
    "username": "qwSyeamDqT",
    "is_active": True,
    "last_name": "Jackson",
    "first_name": "Cynthia",
    "last_login": None,
    "date_joined": "2024-01-16T19:35:32.331011+00:00",
    "is_superuser": False,
}
```

You can also browse deleted records via Django admin.

## Credits

I primarily read the following posts to implement this in Django:

https://brandur.org/fragments/deleted-record-insert

https://brandur.org/soft-deletion
