# tidyX
![GitHub stars](https://img.shields.io/github/stars/lgomezt/tidyX?style=social)
![Downloads](https://pepy.tech/badge/tidyX)

![Before and After tidyX](https://github.com/lgomezt/tidyX/raw/main/docs/source/tutorials/before_after_tidyX.png)

`tidyX` is a Python package designed for cleaning and preprocessing text for machine learning applications, **especially for text written in Spanish and originating from social networks.** This library provides a complete pipeline to remove unwanted characters, normalize text, group similar terms, etc. to facilitate NLP applications.

**To deep dive in the package visit our [website](https://tidyx.readthedocs.io/en/latest/)**

## Installation

Install the package using pip:

```bash
pip install tidyX
```

Make sure you have the necessary dependencies installed. If you plan on lemmatizing, you'll need `spaCy` along with the appropriate language models. For Spanish lemmatization, we recommend downloading the `es_core_news_sm` model:

```bash
python -m spacy download es_core_news_sm 
```

For English lemmatization, we suggest the `en_core_web_sm` model:

```bash
python -m spacy download en_core_web_sm 
```

To see a full list of available models for different languages, visit [Spacy's documentation](https://spacy.io/models/).


## Features

- [**Standardize Text Pipeline**](https://tidyx.readthedocs.io/en/latest/usage/standardize_text_pipeline.html): The [`preprocess()`](https://tidyx.readthedocs.io/en/latest/user_documentation/TextPreprocessor.html#tidyX.text_preprocessor.TextPreprocessor.preprocess) method provides an all-encompassing solution for quickly and effectively standardizing input strings, with a particular focus on tweets. It transforms the input to lowercase, strips accents (and emojis, if specified), and removes URLs, hashtags, and certain special characters. Additionally, it offers the option to delete stopwords in a specified language, trims extra spaces, extracts mentions, and removes 'RT' prefixes from retweets.

```python
from tidyX import TextPreprocessor as tp

# Raw tweet example
raw_tweet = "RT @user: Check out this link: https://example.com 🌍 #example 😃"

# Applying the preprocess method
cleaned_text = tp.preprocess(raw_tweet)

# Printing the cleaned text
print("Cleaned Text:", cleaned_text)
```

**Output**:
```
Cleaned Text: check out this link
```

To remove English stopwords, simply add the parameters `remove_stopwords=True` and `language_stopwords="english"`:

```python
from tidyX import TextPreprocessor as tp

# Raw tweet example
raw_tweet = "RT @user: Check out this link: https://example.com 🌍 #example 😃"

# Applying the preprocess method with additional parameters
cleaned_text = tp.preprocess(raw_tweet, remove_stopwords=True, language_stopwords="english")

# Printing the cleaned text
print("Cleaned Text:", cleaned_text)
```

**Output**:
```
Cleaned Text: check link
```

For a more detailed explanation of the customizable steps of the function, visit the official [preprocess() documentation](https://tidyx.readthedocs.io/en/latest/api/TextPreprocessor.html#tidyX.text_preprocessor.TextPreprocessor.preprocess).


- [**Stemming and Lemmatizing**](https://tidyx.readthedocs.io/en/latest/usage/stemming_and_lemmatizing.html): One of the foundational steps in preparing text for NLP applications is bringing words to a common base or root. This library provides both [`stemmer()`](https://tidyx.readthedocs.io/en/latest/user_documentation/TextNormalization.html#tidyX.text_normalization.TextNormalization.stemmer) and [`lemmatizer()`](https://tidyx.readthedocs.io/en/latest/user_documentation/TextNormalization.html#tidyX.text_normalization.TextNormalization.lemmatizer) functions to perform this task across various languages. 
- [**Group similar terms**](https://tidyx.readthedocs.io/en/latest/usage/group_similar_terms.html): When working with a corpus sourced from social networks, it's common to encounter texts with grammatical errors or words that aren't formally included in dictionaries. These irregularities can pose challenges when creating Term Frequency matrices for NLP algorithms. To address this, we developed the [`create_bol()`]([https://tidyx.readthedocs.io/en/latest/examples/tutorial.html#create-bol](https://tidyx.readthedocs.io/en/latest/user_documentation/TextPreprocessor.html#tidyX.text_preprocessor.TextPreprocessor.create_bol)) function, which allows you to create specific bags of terms to cluster related terms.
- [**Remove unwanted elements**](https://tidyx.readthedocs.io/en/latest/usage/remove_unwanted_elements.html): such as [special characters](https://tidyx.readthedocs.io/en/latest/user_documentation/TextPreprocessor.html#tidyX.text_preprocessor.TextPreprocessor.remove_special_characters), [extra spaces](https://tidyx.readthedocs.io/en/latest/user_documentation/TextPreprocessor.html#tidyX.text_preprocessor.TextPreprocessor.remove_extra_spaces), [accents](https://tidyx.readthedocs.io/en/latest/user_documentation/TextPreprocessor.html#tidyX.text_preprocessor.TextPreprocessor.remove_accents), [emojis](https://tidyx.readthedocs.io/en/latest/user_documentation/TextPreprocessor.html#tidyX.text_preprocessor.TextPreprocessor.remove_accents), [urls](https://tidyx.readthedocs.io/en/latest/user_documentation/TextPreprocessor.html#tidyX.text_preprocessor.TextPreprocessor.remove_urls), tweeter [mentions](https://tidyx.readthedocs.io/en/latest/user_documentation/TextPreprocessor.html#tidyX.text_preprocessor.TextPreprocessor.remove_mentions), among others.
- [**Dependency Parsing Visualization**](https://tidyx.readthedocs.io/en/latest/usage/dependency_parsing_visualization.html): Incorporates visualization tools that enable the display of dependency parses, facilitating linguistic analysis and feature engineering.
- **Much more!**

## Tutorials
- [Stemming and Lemmatizing Texts Efficiently](https://tidyx.readthedocs.io/en/latest/tutorials/stemming_and_lemmatizing_efficiently.html)
- [Word Cloud](https://tidyx.readthedocs.io/en/latest/tutorials/word_cloud.html)
- [Topic Modelling](https://tidyx.readthedocs.io/en/latest/tutorials/topic_modelling.html)

## Contributing

Contributions to enhance `tidyX` are welcome! Feel free to open issues for bug reports, feature requests, or submit pull requests. If this package has been helpful, please give us a star :D
