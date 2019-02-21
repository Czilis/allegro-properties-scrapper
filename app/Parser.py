import requests
from bs4 import BeautifulSoup


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

    def __map_parameter_table(self, parameter_table: BeautifulSoup):
        result = parameter_table.find_all("div", class_="_18da3096")
        for element in result:
            if len(element.contents) == 2:
                self.__paired_parameters.update({element.contents[0].string: element.contents[1].string})

        return self.__paired_parameters

    def __parse(self, html):
        webpage_entity = BeautifulSoup(html.text)
        parameter_table_parent = webpage_entity.find(attrs={"data-prototype-id": "allegro.showoffer.parameters"})
        parameter_table: BeautifulSoup = parameter_table_parent.contents[1].contents[0]
        return self.__map_parameter_table(parameter_table)
