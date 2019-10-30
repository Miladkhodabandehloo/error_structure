from django.db import models
from django.core.cache import cache
from hashlib import md5


class CacheQuerySet(models.QuerySet):
    def get(self, *args, **kwargs):
        if "pk" in kwargs and len(kwargs) == 1:
            key = "{cache_key}_PK_{pk}".format(cache_key=self.model.cache_key(), pk=kwargs["pk"])
            cached_obj = cache.get(key)
            if cached_obj is None:
                db_obj = super(CacheQuerySet, self).get(*args, **kwargs)
                cache.set(key, db_obj, self.model.CACHE_TIMEOUT)
                return db_obj
            return cached_obj
        return super(CacheQuerySet, self).get(*args, **kwargs)

    def update(self, **kwargs):
        super(CacheQuerySet, self).update(**kwargs)
        keys = cache.keys("%s_*" % self.model.cache_key())
        cache.delete_many(keys)

    def get_or_create_cache(self, *args, **kwargs):
        query_hash = md5(str(self.query).encode()).hexdigest()
        key = "%s_FILTER_%s" % (self.model.cache_key(), query_hash)
        cached_objects = cache.get(key)
        if cached_objects is None:
            db_objects = list()
            for obj in self.all():
                db_objects.append(obj)
            cache.set(key, db_objects, self.model.CACHE_TIMEOUT)
            return db_objects
        return cached_objects


class CachedModel(models.Model):
    CACHE_TIMEOUT = 10 * 60

    @classmethod
    def cache_key(cls):
        return cls.__name__.upper()

    @property
    def my_key(self):
        return "{cache_key}_PK_{pk}".format(cache_key=self.cache_key(), pk=self.pk)

    objects = CacheQuerySet().as_manager()

    def save(self, *args, **kwargs):
        super(CachedModel, self).save(*args, **kwargs)
        filter_keys = cache.keys("%s_FILTER_*" % self.cache_key())
        cache.delete_many(filter_keys)
        cache.set(self.my_key, self, self.CACHE_TIMEOUT)

    def delete(self):
        cache.delete(self.my_key)
        filter_keys = cache.keys("%s_FILTER_*" % self.cache_key())
        cache.delete_many(filter_keys)
        super(CachedModel, self).delete()

    class Meta:
        abstract = True
