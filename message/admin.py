from django.contrib import admin
from message import models


class MessageInline(admin.TabularInline):
    """Inline for messages in topics admin
    """

    extra = 0
    fields = ('content',)
    model = models.Message
    readonly_fields = ('creator', 'created', 'updated')


@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):

    fields = ('name', 'creator', 'created', 'updated')
    inlines = (MessageInline,)
    list_display = ('name', 'creator', 'created', 'updated')
    list_filter = ('creator__username', 'created', 'updated')
    readonly_fields = ('creator', 'created', 'updated')
    search_fields = (
        'name', 'creator__first_name', 'creator__last_name', 'creator__email', 'creator__username'
    )

    def save_model(self, request, obj, form, change):
        """Save request user as creator
        """

        obj.creator = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        """Automatically add request user as creator for related messages
        """

        if formset.model == models.Message:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.creator = request.user
                instance.save()
        else:
            formset.save()


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    fields = ('content', 'topic', 'creator', 'created', 'updated')
    readonly_fields = ('creator', 'created', 'updated')
    list_display = ('content', 'creator', 'created', 'updated')
    list_filter = ('topic__name', 'creator__username', 'created', 'updated')
    search_fields = (
        'content', 'topic__name', 'creator__first_name', 'creator__last_name', 'creator__email', 'creator__username'
    )

    def save_model(self, request, obj, form, change):
        """Save request user as creator
        """

        obj.creator = request.user
        obj.save()
