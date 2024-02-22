import os
import lxml.etree as ET
import jinja2
import re


class ObjectToXml():

    def make_xml(self, save):
        for x in self.br_input:
            templateLoader = jinja2.FileSystemLoader(searchpath="./")
            templateEnv = jinja2.Environment(loader=templateLoader)
            template_file = self.template_path
            template = templateEnv.get_template(template_file)
            # templateLoader = jinja2.PackageLoader(
            #     "acdh_baserow_utils", "templates"
            # )
            # templateEnv = jinja2.Environment(loader=templateLoader, trim_blocks=True, lstrip_blocks=True)
            # template = templateEnv.get_template('./tei.xml')
            xml = template.render({"objects": [x]})
            xml = re.sub(r'\s+$', '', xml, flags=re.MULTILINE)
            xml = ET.fromstring(xml)
            if save:
                filename = f"{x[self.filename]}.xml"
                os.makedirs(self.save_dir, exist_ok=True)
                with open(os.path.join(self.save_dir, filename), 'wb') as f:
                    f.write(ET.tostring(xml, pretty_print=True, encoding="utf-8"))
            yield ET.tostring(xml, pretty_print=True, encoding="utf-8")

    def make_xml_single(self, save):
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template_file = self.template_path
        template = templateEnv.get_template(template_file)
        xml = template.render({"objects": self.br_input})
        xml = re.sub(r'\s+$', '', xml, flags=re.MULTILINE)
        xml = xml.replace("&", "&amp;")
        xml = ET.fromstring(xml)
        if save:
            filename = f"{self.filename}.xml"
            os.makedirs(self.save_dir, exist_ok=True)
            with open(os.path.join(self.save_dir, filename), 'wb') as f:
                f.write(ET.tostring(xml, pretty_print=True, encoding="utf-8"))
        return ET.tostring(xml, pretty_print=True, encoding="utf-8")

    def __init__(
        self,
        br_input=None,
        save_dir=None,
        filename=None,
        template_path=None
    ):
        if br_input is None:
            print("please provide baserow input by using BaseRowClient().yield_rows() generator.")
        else:
            self.br_input = br_input
        if save_dir is None:
            self.save_dir = "out"
        else:
            self.save_dir = save_dir
        if template_path is None:
            self.template_path = "templates/tei.xml"
        else:
            self.template_path = template_path
        if filename is None:
            self.filename = "filename"
        else:
            self.filename = filename
