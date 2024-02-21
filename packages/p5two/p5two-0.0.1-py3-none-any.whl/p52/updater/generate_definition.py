import black
import bs4


def generate_definition_file(data):
    print("Generating definition file")
    items = []
    for item in data["classitems"]:
        if (
            ("name" in item)
            and (item["class"] == "p5")
            and ("addons" not in item["file"])
            and (item["module"] not in ["Foundation"])
            and (not "deprecated" in item)
        ):
            items.append(item)

    def generateItem(item):
        name = item["name"]
        if "description" in item:
            docstring = bs4.BeautifulSoup(
                item["description"].replace("<p>", "").replace("</p>", ""), features="lxml"
            ).text
        else:
            docstring = ""
        if item["itemtype"] == "method":
            # it is a function
            if "overloads" in item:
                params = ["*args", "**kwargs"]
            else:
                try:
                    params = [x["name"] for x in item["params"]]
                except:
                    params = []

            params = ", ".join(params)

            return f'''
    def {name}({params}):
        """
        {docstring}
        """
        return window.{name}({params})
    '''
        elif item["itemtype"] == "property":
            if "final" not in item:
                return f'''
    @property
    def {name}():
        """
        {docstring}
        """
        return window.{name}
    '''
            else:
                return f"""{name} = window.{name}"""

    def generateItem2(item):
        name = item["name"]
        docstring = ""
        if "description" in item:
            docstring = bs4.BeautifulSoup(
                item["description"].replace("<p>", "").replace("</p>", ""), features="lxml"
            ).text

        if item["itemtype"] == "method":
            # it is a function
            try:
                params = [x["name"] for x in item["params"]]
            except:
                params = ["*args", "**kwargs"]

            params = ", ".join(params)

            return f'''def {name}({params}):\n    """{docstring}"""\n    pass'''
        elif item["itemtype"] == "property":
            return f"""{name} = None"""

    with open("../static/p5definition.py", "w") as output:
        output.write("# type: ignore\n\n")
        methods = [i for i in items if i["itemtype"] == "method"]
        props = [i for i in items if i["itemtype"] == "property"]

        for method in methods:
            s = generateItem2(method)
            s = black.format_str(s, mode=black.Mode())
            output.write(s)
            output.write("\n\n")

        for prop in props:
            s = generateItem2(prop)
            s = black.format_str(s, mode=black.Mode())
            output.write(s)

    print("Done!")
