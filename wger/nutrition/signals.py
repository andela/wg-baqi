from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from wger.nutrition.models import NutritionPlan, Meal, MealItem

signals = [post_save, post_delete]


@receiver(signals, sender=NutritionPlan)
@receiver(signals, sender=Meal)
@receiver(signals, sender=MealItem)
def cache_deletion_on_change(sender, instance, **kwargs):
    '''
    Delete cache key when there is a change
    in the nutrition plan, meals or mealitem
    '''
    plan = instance.get_owner_object()
    cache.delete(plan.id)
