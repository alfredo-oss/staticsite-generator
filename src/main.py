from service.nodes.textnode import TextNode
from service.utils.functions import copy_resources_recursively
from service.utils.functions import generate_pages_recursive
import sys

def main():
    base_path = sys.argv[1] if sys.argv[1] else "/"
    source_path = "static"
    destination_path = "docs"
    copy_resources_recursively(source_path, destination_path)
    generate_pages_recursive('content', 'template.html', destination_path, base_path)




if __name__ == "__main__":
    main()
