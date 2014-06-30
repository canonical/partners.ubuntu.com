from django.contrib import admin
from cms.models import (
    Partner, Technology, IndustrySector, Programme, ServiceOffered, Region,
    Quote, Link, InsightsTag, Text
)


class TextInline(admin.TabularInline):
    model = Text
    extra = 0


class QuoteInline(admin.TabularInline):
    model = Quote
    extra = 0


class LinkInline(admin.TabularInline):
    model = Link
    extra = 0


class InsightsTagInline(admin.TabularInline):
    model = InsightsTag
    extra = 0


class PartnerAdmin(admin.ModelAdmin):

    def technology(obj):
        return ",".join([str(o) for o in obj.technology.all()])

    def industry_sector(obj):
        return ",".join([str(o) for o in obj.industry_sector.all()])

    def programme(obj):
        return ",".join([str(o) for o in obj.programme.all()])

    def service_offered(obj):
        return ",".join([str(o) for o in obj.service_offered.all()])

    def region(obj):
        return ",".join([str(o) for o in obj.region.all()])

    list_display = ('upper_case_name',)

    def shorter_description(self, obj):
        if len(obj.short_description) < 70:
            return obj.short_description
        else:
            return obj.short_description[0:64-1] + "[...]"

    shorter_description.short_description = 'Short Description'

    technology.short_description = 'Technology'
    industry_sector.short_description = 'Industry Sector'
    programme.short_description = 'Programme'
    service_offered.short_description = 'Service Offered'
    region.short_description = 'Region'

    prepopulated_fields = {"slug": ("name",)}

    list_display = (
        'name',
        'logo',
        'published',
        'shorter_description',
        'featured',
        'generate_page',
        technology,
        industry_sector,
        programme,
        service_offered,
        region,
    )
    list_filter = (
        'published',
        'featured',
        'generate_page',
        'technology',
        'industry_sector',
        'programme',
        'service_offered',
        'region'
    )
    list_editable = (
        'published',
        'logo'
    )
    search_fields = ['name']
    readonly_fields = (
        'created_by',
        'updated_by'
    )
    fieldsets = (
        ('Partner Information', {
            'fields': (
                'name',
                'slug',
                'featured',
                'short_description',
                'published',
                'logo',
                'external_page',
                'external_fallback',
            )
        }),
        ('Categories', {
            'fields': (
                'technology',
                'industry_sector',
                'programme',
                'service_offered',
                'region'
            )
        }),
        ('Detailed partner Information', {
            'classes': ('collapse',),
            'fields': (
                'generate_page',
                'long_description',
            )
        }),
        ("Other", {
            'fields': ('notes', 'created_by', 'updated_by')
        }),
    )
    inlines = [
        TextInline,
        QuoteInline,
        LinkInline,
        InsightsTagInline
    ]
    change_form_template = 'admin/asterix_change_form.html'


class TechnologyAdmin(admin.ModelAdmin):
    pass


class IndustrySectorAdmin(admin.ModelAdmin):
    pass


class ProgrammeAdmin(admin.ModelAdmin):
    pass


class ServiceOfferedAdmin(admin.ModelAdmin):
    pass


class RegionAdmin(admin.ModelAdmin):
    pass


class MetadataAdmin(admin.ModelAdmin):
    readonly_fields = (
        'created_by',
        'updated_by'
    )


class QuoteAdmin(admin.ModelAdmin):
    pass


class LinkAdmin(admin.ModelAdmin):
    pass


class InsightsTagAdmin(admin.ModelAdmin):
    pass


class TextAdmin(admin.ModelAdmin):
    pass


admin.site.register(Partner, PartnerAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(IndustrySector, IndustrySectorAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(ServiceOffered, ServiceOfferedAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(InsightsTag, InsightsTagAdmin)
admin.site.register(Text, TextAdmin)
