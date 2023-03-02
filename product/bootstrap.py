import logging
import sys
from django.conf import settings
from django.template.loader import get_template, render_to_string
from django.utils.text import slugify
from django.utils.safestring import mark_safe, SafeString

from crispy_forms import bootstrap as bs
# from crispy_forms.base import KeepContext
from crispy_forms.layout import LayoutObject
from crispy_forms.utils import (
    flatatt, TEMPLATE_PACK, default_field_template
)

# def render_field(
#     field,
#     form,
#     context,
#     template=None,
#     labelclass=None,
#     layout_object=None,
#     attrs=None,
#     template_pack=TEMPLATE_PACK,
#     extra_context=None,
#     **kwargs,
# ):
#     """
#     Renders a django-crispy-forms field

#     :param field: Can be a string or a Layout object like `Row`. If it's a layout
#         object, we call its render method, otherwise we instantiate a BoundField
#         and render it using default template 'CRISPY_TEMPLATE_PACK/field.html'
#         The field is added to a list that the form holds called `rendered_fields`
#         to avoid double rendering fields.
#     :param form: The form/formset to which that field belongs to.
#     :template: Template used for rendering the field.
#     :layout_object: If passed, it points to the Layout object that is being rendered.
#         We use it to store its bound fields in a list called `layout_object.bound_fields`
#     :attrs: Attributes for the field's widget
#     :template_pack: Name of the template pack to be used for rendering `field`
#     :extra_context: Dictionary to be added to context, added variables by the layout object
#     """
#     added_keys = [] if extra_context is None else extra_context.keys()
#     with KeepContext(context, added_keys):
#         if field is None:
#             return SafeString("")

#         FAIL_SILENTLY = getattr(settings, "CRISPY_FAIL_SILENTLY", True)

#         inline = field.inline
#         if inline:
#             if isinstance(inline, type):
#                 print("INLINE", inline)
#             elif isinstance(inline, list):
#                 for i in inline:
#                     print("LIST INLINE", i)

#         # if hasattr(field, 'inline'):
#         #     if field.inline: #context.update({"formset": field.inline})
#         #         inline = field.inline
#         #         for fs in inline: #context.update({"formset": fs()})
#         #             # print("FSS", fs)
#         #             # context.update({"formset": f['image'] for f in fs()})
#         #             cus = field.render(fs(), context, template_pack=template_pack)

#         #             print("ATTR RENDER", cus)
#         if hasattr(field, "render"):
#             return field.render(form, context, template_pack=template_pack)

#         try:
#             # Injecting HTML attributes into field's widget, Django handles rendering these
#             bound_field = form[field.fields]
#             field_instance = bound_field.field
#             if attrs is not None:
#                 widgets = getattr(field_instance.widget, "widgets", [field_instance.widget])

#                 # We use attrs as a dictionary later, so here we make a copy
#                 list_attrs = attrs
#                 if isinstance(attrs, dict):
#                     list_attrs = [attrs] * len(widgets)

#                 for index, (widget, attr) in enumerate(zip(widgets, list_attrs)):
#                     if hasattr(field_instance.widget, "widgets"):
#                         if "type" in attr and attr["type"] == "hidden":
#                             field_instance.widget.widgets[index] = field_instance.hidden_widget(attr)

#                         else:
#                             field_instance.widget.widgets[index].attrs.update(attr)
#                     else:
#                         if "type" in attr and attr["type"] == "hidden":
#                             field_instance.widget = field_instance.hidden_widget(attr)

#                         else:
#                             field_instance.widget.attrs.update(attr)

#         except KeyError:
#             if not FAIL_SILENTLY:
#                 raise Exception("Could not resolve form field '%s'." % field)
#             else:
#                 field_instance = None
#                 logging.warning("Could not resolve form field '%s'." % field, exc_info=sys.exc_info())

#         if hasattr(form, "rendered_fields"):
#             if field not in form.rendered_fields:
#                 form.rendered_fields.add(field)
#             else:
#                 if not FAIL_SILENTLY:
#                     raise Exception("A field should only be rendered once: %s" % field)
#                 else:
#                     logging.warning("A field should only be rendered once: %s" % field, exc_info=sys.exc_info())

#         if field_instance is None:
#             html = SafeString("")
#         else:
#             if template is None:
#                 if form.crispy_field_template is None:
#                     template = default_field_template(template_pack)
#                 else:  # FormHelper.field_template set
#                     template = get_template(form.crispy_field_template)
#             else:
#                 template = get_template(template)

#             # We save the Layout object's bound fields in the layout object's `bound_fields` list
#             if layout_object is not None:
#                 if hasattr(layout_object, "bound_fields") and isinstance(layout_object.bound_fields, list):
#                     layout_object.bound_fields.append(bound_field)
#                 else:
#                     layout_object.bound_fields = [bound_field]

#             context.update(
#                 {
#                     "field": bound_field,
#                     "labelclass": labelclass,
#                     "flat_attrs": flatatt(attrs if isinstance(attrs, dict) else {}),
#                 }
#             )
#             if extra_context is not None:
#                 context.update(extra_context)
#             html = template.render(context.flatten())

#         return html
    
# class KeepContext:
#     """
#     Context manager that receives a `django.template.Context` instance and a list of keys

#     Once the context manager is exited, it removes `keys` from the context, to avoid
#     side effects in later layout objects that may use the same context variables.

#     Layout objects should use `extra_context` to introduce context variables, never
#     touch context object themselves, that could introduce side effects.
#     """

#     def __init__(self, context, keys):
#         self.context = context
#         self.keys = keys

#     def __enter__(self):
#         pass

#     def __exit__(self, type, value, traceback):
#         for key in list(self.keys):
#             if key in self.context:
#                 del self.context[key]

class Div(LayoutObject):
    template = "bootstrap/layout/div.html"
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
        
        template = self.get_template_name(self.template)
        return render_to_string(template, {"div": self, "fields": fields})

# class Container(Div):
#     def __init__(self, name, *fields, css_id=None, css_class=None, template=None, active=None, inline=None, **kwargs):
#         super().__init__(*fields, css_id=css_id, css_class=css_class, template=template, **kwargs)
#         self.name = name
#         self._active_originally_included = active is not None
#         self.active = active or False
#         self.inline = inline
#         if not self.css_id:
#             self.css_id = slugify(self.name, allow_unicode=True)

#     def __contains__(self, field_name):
#         """
#         check if field_name is contained within tab.
#         """
#         return field_name in (pointer.name for pointer in self.get_field_names())

#     def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
#         if self.active:
#             if "active" not in self.css_class:
#                 self.css_class += " active"
#         else:
#             self.css_class = self.css_class.replace("active", "")
#         return super().render(form, context, template_pack)

# class Tab(Container):
#     css_class = 'tab-pane'
#     link_template = '%s/layout/tab-link.html'

#     def __init__(self, name, *fields, css_id=None, css_class=None, template=None, active=None, inline=None, **kwargs):
#         super().__init__(*fields, css_id=css_id, css_class=css_class, template=template, inline=inline, **kwargs)
#         self.name = name
#         self._active_originally_included = active is not None
#         self.active = active or False
#         self.inline = inline
#         if not self.css_id:
#             self.css_id = slugify(self.name, allow_unicode=True)

#     def render_link(self, template_pack=TEMPLATE_PACK, **kwargs):
#         link_template = self.link_template % template_pack
#         abc = {}
#         abc['link'] = self
        
#         return render_to_string(link_template, abc)
    
# class TabHolder(Div):
#     template = "bootstrap/layout/tab.html"

#     def get_rendered_fields(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
#         sf = self.fields.copy()
#         for f in self.fields:
#             print("HOLDER DIV", type(sf), f)
#             if isinstance(f.inline, type):
#                 print(f.inline())
#             if isinstance(f.inline, list):
#                 for ls in f.inline:
#                     print("TYPE",ls)
#                     # print("LIST", [l.fields for l in ls()])
#         return SafeString(
#             "".join(render_field(field, form, context, template_pack=template_pack, **kwargs) for field in sf)
#         )

#     def first_container_with_errors(self, errors):
#         """
#         Returns the first container with errors, otherwise returns None.
#         """
#         for tab in self.fields:
#             errors_here = any(error in tab for error in errors)
#             if errors_here:
#                 return tab
#         return None

#     def open_target_group_for_form(self, form):
#         """
#         Makes sure that the first group that should be open is open.
#         This is either the first group with errors or the first group
#         in the container, unless that first group was originally set to
#         active=False.
#         """
#         target = self.first_container_with_errors(form.errors.keys())
#         if target is None:
#             target = self.fields[0]
#             if not getattr(target, "_active_originally_included", None):
#                 target.active = True
#             return target

#         target.active = True
#         return target

#     def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
#         for tab in self.fields:
#             tab.active = False
        
#         # Open the group that should be open.
#         self.open_target_group_for_form(form)
#         content = self.get_rendered_fields(form, context, template_pack)
#         links = SafeString("".join(tab.render_link(template_pack) for tab in self.fields))
        
#         context.update({"tabs": self, "links": links, "content": content, "inline": [f.inline for f in self.fields]})
#         template = self.get_template_name(template_pack)
#         return render_to_string(template, context.flatten())
    
class TabForm:
    def __init__(self, name, *fields, inline=None, **kwargs):
        self.name = name
        self.fields = fields
        self.inline = inline
        self.kwargs = kwargs
        self.id_link = slugify(self.name, allow_unicode=True)
    
    # def get_rendered_fields(self, form, context, template_pack=None, labelclass=None, **kwargs):
    #     return SafeString(
    #         "".join(render_field(
    #             field,
    #             form,
    #             context,
    #             labelClass=labelclass,
    #             template=template_pack,
    #             **kwargs
    #         ) for field in self.fields)
    #     )

    def nav_links(self):
        template = 'bootstrap/layout/tab-links.html'
        context = {
            "links": self
        }
        return render_to_string(template, context)
        # return {"id_link": self.id_link, "name": self.name}
    
    def tabs_nav(self):
        template = 'bootstrap/layout/tab.html'
        context = {
            "tabs": self.id_link
        }
        return render_to_string(template, context)

def render_field(
        field,
        form,
        context,
        template=None,
        inline=None,
        attrs=None,
        labelClass=None,
        extra_context=None,
        **kwargs
):
    # for i, fd in enumerate(field):
    bound_field = form[field]
    field_instance = bound_field.field
    print("INLINE", inline)
    if attrs is not None:
        widgets = getattr(field_instance.widget, "widgets", [field_instance.widget])
        list_attrs = attrs

        if isinstance(attrs, dict):
            list_attrs = [attrs] * len(widgets)

        for index, (widget, attr) in enumerate(zip(widgets, list_attrs)):
            if hasattr(field_instance.widget, "widgets"):
                if "type" in attr and attr["type"] == "hidden":
                    field_instance.widget.widgets[index] = field_instance.hidden_widget(attr)
                else:
                    field_instance.widget.widgets[index].attrs.update(attr)
            else:
                if "type" in attr and attr["type"] == "hidden":
                    field_instance.widget = field_instance.hidden_widget(attr)
                else:
                    field_instance.widget.attrs.update(attr)

    if hasattr(form, "rendered_fields"):
        if field not in form.rendered_fields:
            form.rendered_fields.add(field)
        else:
            logging.warning("A field should only be rendered once: %s" % field, exc_info=sys.exc_info())
    
    if field_instance is None:
        html = SafeString("")
    else:
        if template is None:
            template = get_template(form.template)
        else:
            template = get_template(template)
        
        context.update({
            "field": bound_field,
            "labelclass": labelClass,
            "inline": inline
        })

        if extra_context is not None:
            context.update(extra_context)
        
        html = template.render(context.flatten())
    return html

    
class NavTabs:
    def __init__(self, form=None, *field) -> None:
        self.fields = field
        self.form = form
    
    def get_rendered_fields(self, context, field, template_pack=None, labelclass=None, **kwargs):
        # for f in field:
        #     print("RENDERED FIELD", f)
        rf = [render_field(f, self.form, context, template=template_pack, inline=field.inline, **kwargs) for f in field.fields]
        print("PRE RF", rf)
        return SafeString("".join([r for r in rf]))

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
    
    def nav_tabs(self, context):
        # tabs = self.get_rendered_fields(context, 'bootstrap/layout/div.html')
        # fields = self.get_rendered_fields(context, template_pack='bootstrap/field.html')
        tabs = SafeString("".join(tab.tabs_nav() for tab in self.fields))
        return tabs
    
    def render(self, context, **kwargs):
        content = []
        for tab in self.fields:
            tab.active = False
            t = {}
            t["id_link"] = tab.id_link
            t["content"] = self.get_rendered_fields(context, tab, template_pack='bootstrap/field.html')
            content.append(t)
        
        self.open_target_group_for_form(self.form)
        # content = self.get_rendered_fields(context, template_pack='bootstrap/field.html')
        links = SafeString("".join(tab.nav_links() for tab in self.fields))
        # links = "".join(tab.nav_links() for tab in self.fields)
        context.update(
            {
                "tabs": content,
                "links": links,
                "form": self.form
            }
        )
        # print("RENDERED", context['tabs'])
        template = "bootstrap/form.html"
        return render_to_string(template, context.flatten())