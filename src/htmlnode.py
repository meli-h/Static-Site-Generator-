


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def props_to_html(self):
        if not self.props:
            return ""
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        if value is None :
            raise ValueError("LeafNode must have a value")

        
        
        
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode has no value!")

        if not self.tag:
            return str(self.value)
        

        attrs = self.props_to_html()
        attr_part = f" {attrs}" if attrs else ""

        return f"<{self.tag}{attr_part}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode requires at least one child node")


        children_html = ""


        for child in self.children:
            child_html = child.to_html()  
            children_html = children_html + child_html
        
        if not self.props:
            return f"<{self.tag}>{children_html}</{self.tag}>"  
        else:
            props_html = self.props_to_html()
            return f"<{self.tag} {props_html}>{children_html}</{self.tag}>"

       