import re

from django import template
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.template.loader import get_template
from django.utils.encoding import force_str
from django.utils.functional import keep_lazy
from django.utils.safestring import mark_safe


register = template.Library()

def my_model(model_name:str):
    model = ContentType.objects.get(
        model=model_name
    ).model_class()
    return model

class RenderTable:
    def script(self, tag):
        default = """
            <script>
                document.addEventListener("DOMContentLoaded", ()=>{
                    const myData = JSON.parse('"""f'{tag}'"""');

                    const to_date_str = (to_dt) => {
                        const date_format = new Date(to_dt);
                        const date_option = {
                            weekday: 'long',
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                        }
                        const new_date = date_format.toLocaleDateString('id', date_option) +
                        " " + date_format.toLocaleTimeString('id');
                        return new_date
                    };

                    const imgTag = (img)=>{
                        const tag = img ? "<img src='/media/"+img+"' width='100'>" : ''
                        return tag
                    };

                    let edit = "{% url 'product:product_edit' 0 %}"

                    const thead = [
                        "SKU", "Name", "Featured Image", "Category", "Brand", "BOM File",
                        "Cost Price", "Created At", "Updated At", "Status", "Actions"
                    ]
                    const tbody = []
                    myData.map((items) => {
                        let item = items.fields;
                        let row = []
                        row.push(
                            item.sku,
                            item.name,
                            imgTag(item.featured_image),
                            item.category,
                            item.brand,
                            item.bom_file,
                            item.cost_price,
                            to_date_str(item.created_at),
                            to_date_str(item.updated_at),
                            item.status,
                            '<a href="'+edit.replace(0, items.pk)+'" class="btn btn-info btn-sm">Edit</a>'
                        )
                        tbody.push(row)
                    })

                    const myTable = new window.simpleDatatables.DataTable("#tableProduct", {
                        perPage: 10,
                        perPageSelect: [10, 25, 50, 100],
                        data: {
                            headings: thead,
                            data: tbody
                        }
                    });
                }, false)
            </script>
        """
        return default
        
    def render_script(self, cls):
        src = mark_safe(self.script(cls))
        return src

@register.simple_tag
def img_url(cls, img_id):
    model = my_model(cls)
    data = model.objects.get(
        pk = img_id
    )
    if data.featured_image:
        return data.featured_image.url


@register.simple_tag
def data_tables(value):
    script = RenderTable()
    return script.render_script(value)

class FormTabNode(template.Node):
    def __init__(self, form, template_pkg=None) -> None:
        self.form = form
        # self.helper = helper
        self.template = template_pkg

    # def get_render(self, context):
    #     from product.bootstrap import NavTabs
    #     if self not in context.render_context:
    #         context.render_context[self] = (
    #             template.Variable(self.form())
    #         )
    #     form = context.render_context[self]
        
    #     actual_form = form.resolve(context)

    #     if self.helper is not None:
    #         helper = self.helper#.resolve(context)
    #     else:
    #         helper = NavTabs() if not hasattr(actual_form, "helper") else actual_form.helper

    #     # try:
    #     #     if helper.template:
    #     #         self.template = helper.template
    #     # except AttributeError:
    #     #     pass

    #     self.actual_helper = helper

    #     response_dict = self.get_response_dict(context)
    #     node_context = context.__copy__()
    #     node_context.update({"is_bound": actual_form.is_bound})
    #     node_context.update(response_dict)
    #     final_context = node_context.__copy__()
    #     return final_context
    
    # def get_response_dict(self, context):
    #     form_type = "form"
    #     response_dict = {}

    #     if "csrf_token" in context:
    #         response_dict["csrf_token"] = context["csrf_token"]
    #     return response_dict

    def render(self, context):
        print("HELPERS", self.helper.render(self.form, context))
        # my_template = 'bootstrap/form.html'
        # c = self.get_render(context).flatten()
        # templ = get_template(my_template)
        # return templ.render(c)

@register.simple_tag(takes_context=True)
def tabbular_form(context, value):
    helper = value.helper
    return helper.render(context)

# @register.tag(name="tabbed_form")
# def do_tabbed_form(parser, token):
#     # form = value
    
#     # tab = FormTabNode(form, form.helper, 'bootstrap/form.html')
#     # print(tab.render(context))
#     # tokens = token.split_contents()
#     # form = tokens.pop(1)

#     # helper = None

#     # try:
#     #     helper = tokens.pop(1)
#     # except IndexError:
#     #     pass

#     # if helper is not None:
#     #     template = helper
#     tag_name, to_do = token.split_contents()
#     name = FormTabNode(to_do)
#     return to_do

@keep_lazy(str)
def remove_spaces(value):
    html = re.sub(r">\s{3,}<", "> <", force_str(value))
    return re.sub(r"/><", r"/> <", force_str(html))

class SpecialSpacelessNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return remove_spaces(self.nodelist.render(context).strip())


@register.tag
def specialspaceless(parser, token):
    """
    Removes whitespace between HTML tags, and introduces a whitespace
    after buttons an inputs, necessary for Bootstrap to place them
    correctly in the layout.
    """
    nodelist = parser.parse(("endspecialspaceless",))
    parser.delete_first_token()

    return SpecialSpacelessNode(nodelist)