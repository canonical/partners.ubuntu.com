from django.contrib import admin
from cms.models import (
    Partner, Category, IndustrySector, Programme, ServiceOffered, Region,
    Quote, Link, InsightsTag, Text
)


class PartnerAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class IndustrySectorAdmin(admin.ModelAdmin):
    pass


class ProgrammeAdmin(admin.ModelAdmin):
    pass


class ServiceOfferedAdmin(admin.ModelAdmin):
    pass


class RegionAdmin(admin.ModelAdmin):
    pass


class QuoteAdmin(admin.ModelAdmin):
    pass


class LinkAdmin(admin.ModelAdmin):
    pass


class InsightsTagAdmin(admin.ModelAdmin):
    pass


class TextAdmin(admin.ModelAdmin):
    pass


admin.site.register(Partner, PartnerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(IndustrySector, IndustrySectorAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(ServiceOffered, ServiceOfferedAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(InsightsTag, InsightsTagAdmin)
admin.site.register(Text, TextAdmin)
