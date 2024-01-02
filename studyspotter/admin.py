from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import StudySpot

class StatusCategoryListsFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'status_category'

    def lookups(self, request, model_admin):
        return (
            ('approved', 'Approved'),
            ('pending', 'Pending'),
            ('rejected', 'Rejected'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'approved':
            return queryset.filter(status=StudySpot.APPROVED)
        if self.value() == 'pending':
            return queryset.filter(status=StudySpot.PENDING)
        if self.value() == 'rejected':
            return queryset.filter(status=StudySpot.REJECTED)

class StudySpotAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ['name']
    search_fields = ['name']

    class Meta:
        model = StudySpot

admin.site.register(StudySpot, StudySpotAdmin)

# class StatusCategoryListsFilter(admin.SimpleListFilter):
#     title = 'Status'
#     parameter_name = 'status_category'

#     def lookups(self, request, model_admin):
#         return (
#             ('approved', 'Approved'),
#             ('pending', 'Pending'),
#             ('rejected', 'Rejected'),
#         )
    
#     def queryset(self, request, model_admin):
#         if self.value() == 'approved':
#             return queryset.filter(
#                 StudySpot(status=StudySpot.APPROVED))
#         if self.value() == 'pending':
#             return queryset.filter(
#                 StudySpot(status=StudySpot.PENDING))
#         if self.value() == 'rejected':
#             return queryset.filter(
#                 StudySpot(status=StudySpot.REJECTED))

# admin.site.register(StudySpot)
# list_filter = ('status',)
# list_filter = (StatusCategoryListsFilter)