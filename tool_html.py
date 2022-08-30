import os
import jinja2

class Jinja2():
    def __init__(self):
        self.template_loc =  os.getcwd() #腳本路徑

    def render_jinja_html(self, file_name, **context):
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_loc+'/')
        ).get_template(file_name).render(context)
