from bs4 import BeautifulSoup as Soup
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import nltk
import numpy as np
from scipy import linalg
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

def parse_blog(file):
    blog_text = open(file, encoding='utf8').read()
    clean_blog_post = blog_text.replace('&lt;', '<').replace('&gt;', '>')
    soup = Soup(clean_blog_post, 'html5lib')
    blog = []
    all_content = []
    for entry in soup.findAll('entry'):
        if 'post-' in entry.find('id').getText():
            entry_content = entry.find('content')
            if entry_content.find('div'):
                entry_text_array = []
                for div in entry_content.findAll('div'):
                    entry_text_array.append(div.getText())
                entry_text = ' '.join(entry_text_array)
            else:
                entry_text = entry_content.getText()

            entry_tags = [category.attrs['term'] for category in entry.findAll('category')]
            blog_post = {
                'title': entry.find('title').getText(),
                'content': entry_text,
                'tags': entry_tags
            }
            all_content.append(entry_text)
            blog.append(blog_post)

    # print(blog[67].get('title'))
    # print(blog[67].get('content'))
    # print(blog[67].get('tags'))
    # print(len(blog))
    #
    # print("\n".join(allContent[:3]))

    return all_content


def fast_ai_nlp_svd(content):

    nltk.download('stopwords')
    stop_words = stopwords.words('russian')
    print(stop_words[45:60])
    vectorizer = CountVectorizer(stop_words=stop_words)  # , tokenizer=LemmaTokenizer())
    vectors = vectorizer.fit_transform(content).todense()  # (documents, vocab)
    print(vectors.shape)  # , vectors.nnz / vectors.shape[0], row_means.shape
    print(len(all_content), vectors.shape)
    vocab = np.array(vectorizer.get_feature_names())
    print(vocab.shape)
    print(vocab[8000:8020])

    U, s, Vh = linalg.svd(vectors, full_matrices=False)
    plt.plot(s[20:40])
    plt.show()
    print(U.shape, s.shape, Vh.shape)
    print(show_topics(Vh[:10], vocab))


def show_topics(a, vocabulary):
    num_top_words = 8
    top_words = lambda t: [vocabulary[i] for i in np.argsort(t)[:-num_top_words - 1:-1]]
    topic_words = ([top_words(t) for t in a])
    return [' '.join(t) for t in topic_words]


if __name__ == "__main__":
    all_content = parse_blog('blog-07-14-2019.xml')
    fast_ai_nlp_svd(all_content)
