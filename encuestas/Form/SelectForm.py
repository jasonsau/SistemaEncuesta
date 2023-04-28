from .ITypeForm import ITypeForm


class SelectForm(ITypeForm):

    def return_html(self, options) -> str:
        print(options)
        string = "<select name = ''>"

        for data in options:
            string = string + "<option value = '"+data.value_question_options + "' name = '" + data.name_question_options + "'>" + data.label_question_options + "</option>"

        string = string + "</select>"
        return string