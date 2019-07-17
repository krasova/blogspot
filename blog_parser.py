from bs4 import BeautifulSoup as Soup


def parse_blog(file):
    blog_text = open(file, encoding='utf8').read()
    clean_blog_post = blog_text.replace('&lt;', '<').replace('&gt;', '>')
    soup = Soup(clean_blog_post, 'html5lib')
    blog = []
    for entry in soup.findAll('entry'):
        entry_content = entry.find('content')
        if entry_content.find('div'):
            entry_text = ''
            for div in entry_content.findAll('div'):
                entry_text += div.getText()
        else:
            entry_text = entry_content.getText()

        entry_tags = [category.attrs['term'] for category in entry.findAll('category')]
        blog_post = {
            'title': entry.find('title').getText(),
            'content': entry_text,
            'tags': entry_tags
        }

        blog.append(blog_post)

    print(blog[67].get('title'))
    print(blog[67].get('content'))
    print(blog[67].get('tags'))


if __name__ == "__main__":
    parse_blog('blog-07-17-2019.xml')
