from django.template.loader import render_to_string
from django.utils.text import slugify
from django.utils.safestring import SafeString

from crispy_forms import bootstrap as bs
from crispy_forms.layout import LayoutObject
from crispy_forms.utils import flatatt, TEMPLATE_PACK

class Div(LayoutObject):
    template = "%s/layout/div.html"
    css_class = None

    def __init__(self, *fields, css_id=None, css_class=None, template=None, **kwargs):
        self.fields = list(fields)

        if self.css_class and css_class:
            self.css_class += f" {css_class}"
        elif css_class:
            self.css_class = css_class

        self.css_id = css_id
        self.template = template or self.template
        self.flat_attrs = flatatt(kwargs)
        self.kwargs = kwargs

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        fields = self.get_rendered_fields(form, context, template_pack, **kwargs)
        
        template = self.get_template_name(template_pack)
        return render_to_string(template, {"div": self, "fields": fields})

class Container(Div):
    def __init__(self, name, *fields, css_id=None, css_class=None, template=None, active=None, **kwargs):
        super().__init__(*fields, css_id=css_id, css_class=css_class, template=template, **kwargs)
        self.name = name
        self._active_originally_included = active is not None
        self.active = active or False
        if not self.css_id:
            self.css_id = slugify(self.name, allow_unicode=True)

    def __contains__(self, field_name):
        """
        check if field_name is contained within tab.
        """
        return field_name in (pointer.name for pointer in self.get_field_names())

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        if self.active:
            if "active" not in self.css_class:
                self.css_class += " active"
        else:
            self.css_class = self.css_class.replace("active", "")
        return super().render(form, context, template_pack)

class Tab(Container):
    css_class = 'tab-pane'
    link_template = '%s/layout/tab-link.html'

    def __init__(self, name, *fields, css_id=None, css_class=None, template=None, active=None, **kwargs):
        super().__init__(*fields, css_id=css_id, css_class=css_class, template=template, **kwargs)
        self.name = name
        self._active_originally_included = active is not None
        self.active = active or False
        # self.kwargs = kwargs
        if not self.css_id:
            self.css_id = slugify(self.name, allow_unicode=True)

    def render_link(self, template_pack=TEMPLATE_PACK, **kwargs):
        link_template = self.link_template % template_pack
        abc = {}
        abc['link'] = self
        
        return render_to_string(link_template, abc)
    
class TabHolder(Div):
    template = "bootstrap4/layout/tab.html"

    def first_container_with_errors(self, errors):
        """
        Returns the first container with errors, otherwise returns None.
        """
        for tab in self.fields:
            errors_here = any(error in tab for error in errors)
            if errors_here:
                return tab
        return None

    def open_target_group_for_form(self, form):
        """
        Makes sure that the first group that should be open is open.
        This is either the first group with errors or the first group
        in the container, unless that first group was originally set to
        active=False.
        """
        target = self.first_container_with_errors(form.errors.keys())
        if target is None:
            target = self.fields[0]
            if not getattr(target, "_active_originally_included", None):
                target.active = True
            return target

        target.active = True
        return target

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        for tab in self.fields:
            tab.active = False
        
        # Open the group that should be open.
        self.open_target_group_for_form(form)
        content = self.get_rendered_fields(form, context, template_pack)
        print("TAB HOLDER", [t.kwargs for t in self.fields], type(content), type(context))
        links = SafeString("".join(tab.render_link(template_pack) for tab in self.fields))

        context.update({"tabs": self, "links": links, "content": content})
        template = self.get_template_name(template_pack)
        return render_to_string(template, context.flatten())