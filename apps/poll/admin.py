from django.contrib import admin

from apps.poll.models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = (
        'question_text',
        'pub_date',
        'is_published_recently',
    )
    list_filter = ['pub_date']
    search_fields = ['question_text']
    readonly_fields = ('pub_date',)


admin.site.register(Question, QuestionAdmin)
