import requests
from bs4 import BeautifulSoup, Tag

from app import format_table_for_shop


class Parser:
    __EXCLUDED_PARAMETERS = ["Faktura:"]
    __paired_parameters = {}

    """
    Parses product properties for given allegro link
    :returns: parameters as map
    """

    def parse_product_parameter(self, link):
        product_html = requests.get(link)
        paired_parameters = self.__parse(product_html)
        filtered_parameters = self.__filter_excluded_parameters(paired_parameters)
        return filtered_parameters

    def __filter_excluded_parameters(self, paired_parameters):
        filtered = {param_name: v for (param_name, v) in paired_parameters.items() if
                    param_name not in self.__EXCLUDED_PARAMETERS}
        return filtered

    def __can_proceed(self, element):
        return isinstance(element, Tag) and (len(element.contents) > 1)

    def __map_parameter_table(self, children):
        for element in children:
            if self.__can_proceed(element):
                self.__map_parameter_table(element.contents)
            elif len(element.contents) != 0:
                values = element.contents[0].contents
                if len(values) > 1:
                    self.__paired_parameters.update({values[0].string: values[1].string})
                else:
                    self.__paired_parameters.update(
                        {values[0].contents[0].contents[0].string: values[0].contents[0].contents[1].string})
        return self.__paired_parameters

    def __parse(self, html):
        webpage_entity = BeautifulSoup(html.text)
        parameter_table_parent = webpage_entity.find(attrs={"data-prototype-id": "allegro.showoffer.parameters"})
        parameter_table: BeautifulSoup = parameter_table_parent.contents[1].contents[0]
        return self.__map_parameter_table(parameter_table.contents)


parser = Parser()
dupa = parser.parse_product_parameter("https://allegro.pl/monnari-torebka-listonoszka-worek-2018-hit-i7156430954.html")
__formattedHtml = format_table_for_shop(dupa)
print(__formattedHtml)
