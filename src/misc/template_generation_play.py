from service.utils.functions import generate_page
from service.utils.functions import generate_pages_recursive

generate_pages_recursive('content', 'template.html', 'public')
"""
generate_page('content/index.md', 'template.html', 'public/index.html')
generate_page('content/blog/glorfindel/index.md', 'template.html', 'public/blog/glorfindel/index.html')
generate_page('content/blog/tom/index.md', 'template.html', 'public/blog/tom/index.html')
generate_page('content/blog/majesty/index.md', 'template.html', 'public/blog/majesty/index.html')
generate_page('content/contact/index.md', 'template.html', 'public/contact/index.html')
"""