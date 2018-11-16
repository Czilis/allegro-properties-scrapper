
"""
Formats given paired parameters for paste ready html
"""
def format_table_for_shop(paired_parameters):
    formatted_html_for_paste = "<table class=\"properties_table\">"

    for index, key in enumerate(paired_parameters):
        if index % 2 == 0:
            formatted_html_for_paste += "<tr>"

        formatted_html_for_paste += ("<td class=\"label\">" + key + "</td>") + (
                "<td>" + paired_parameters[key] + "</td>")

        if index % 2 != 0:
            formatted_html_for_paste += "</tr>"

    formatted_html_for_paste += "</table>"
    return formatted_html_for_paste
