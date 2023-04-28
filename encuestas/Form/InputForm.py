from .ITypeForm import ITypeForm


class InputForm(ITypeForm):

    def return_html(self, options) -> str:
        print(options)
        string = ""
        for data in options:
            string = "<input value = '" + data.value_question_options + "' name = '" + data.name_question_options + "' id = '" + data.id_question_options + "'/>"
        return string
