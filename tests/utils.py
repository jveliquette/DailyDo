from html.parser import HTMLParser


class Data:
    def __init__(self, content):
        self.content = content

    def inner_text(self):
        return self.content

    def to_html(self, level):
        return "  " * level + self.content + "\n"


class Tag:
    def __init__(self, name, attrs):
        self.name = name
        self.attrs = dict(attrs or {})
        self.missing_close = False
        self.children = []

    def add_data(self, data):
        self.children.append(Data(data))

    def add_child(self, tag):
        self.children.append(tag)

    def has_direct_child(self, name):
        for child in self.children:
            if hasattr(child, "name") and child.name == name:
                return True
        return False

    def get_direct_child(self, name):
        for child in self.children:
            if hasattr(child, "name") and child.name == name:
                return child
        return None

    def get_all_children(self, name, result=None):
        if result is None:
            result = []
        for child in self.children:
            if hasattr(child, "name") and child.name == name:
                result.append(child)
            if hasattr(child, "get_all_children"):
                child.get_all_children(name, result)
        return result

    def inner_text(self):
        content = ""
        for child in self.children:
            content += child.inner_text()
        return content

    def to_html(self, level):
        if self.name:
            start = "  " * level + f"<{self.name} {self.attrs}>"
            content = ""
            end = "\n"
            if self.name not in Document.empty_tags:
                start += "\n"
                content = ""
                for child in self.children:
                    content += child.to_html(level + 1)
                end = "  " * level + f"</{self.name}>\n"
            return start + content + end
        elif len(self.children) == 1:
            return self.children[0].to_html(0)

    def __str__(self):
        return self.name


class Document(HTMLParser):
    empty_tags = [
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    ]

    def __init__(self):
        super().__init__()
        self.root = Tag("", None)
        self.decl = None
        self.tag_stack = [self.root]
        self.errors = []

    def handle_decl(self, declaration):
        self.decl = declaration.lower()
        self.decl = self.decl.replace("doctype", "").strip()

    def handle_starttag(self, tag_name, attrs):
        tag = Tag(tag_name, attrs)
        if len(self.tag_stack) > 0:
            self.tag_stack[-1].add_child(tag)
        if tag_name not in self.empty_tags:
            self.tag_stack.append(tag)

    def handle_data(self, data):
        if len(self.tag_stack) > 0 and len(data.strip()) > 0:
            self.tag_stack[-1].add_data(data.strip())
        elif len(data.strip()) > 0:
            self.errors.append("Content outside the root tag")

    def handle_endtag(self, tag):
        if len(self.tag_stack) > 0:
            if tag != self.tag_stack[-1].name:
                self.errors.append(f"Unmatched close tag: {tag}")
            else:
                self.tag_stack.pop()
        else:
            self.errors.append(f"Unmatched close tag: {tag}")

    def has_fundamental_five(self):
        if len(self.root.children) == 0:
            return False

        html = self.root.get_direct_child("html")
        return (
            self.decl == "html"
            and html.name == "html"
            and html.has_direct_child("head")
            and html.has_direct_child("body")
            and html.get_direct_child("head").has_direct_child("title")
        )

    def select(self, *selectors):
        tag = self.root
        for selector in selectors:
            tag = tag.get_direct_child(selector)
            if tag is None:
                break
        return tag

    def __str__(self):
        return f"""<!doctype {self.decl}>
{self.root.to_html(0)}
"""
