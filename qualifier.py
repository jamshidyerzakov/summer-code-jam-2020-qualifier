import datetime
import re
import typing


def sort_list_of_tuple(arr: typing.List, content: str) -> None:
    """
    Sorting list of tuple, where tuple -> (word, word's frequency)
    by the word's appearance index in the content.
    """
    n = len(arr)

    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if (arr[j])[1] == (arr[j + 1])[1] and content.find((arr[j])[0]) > content.find((arr[j + 1])[0]):
                (arr[j]), (arr[j + 1]) = (arr[j + 1]), (arr[j])


class ArticleField:
    """The `ArticleField` class for the Advanced Requirements."""

    def __init__(self, field_type: typing.Type[typing.Any]):
        self.field_type = field_type

    def __set__(self, instance, value) -> None:
        instance.val = value
        if not isinstance(instance.val, self.field_type):
            raise TypeError("expected an instance of type '{expected}' for attribute '{attr}', got '{unexpected}' "
                            "instead".format(
                                expected=self.field_type.__name__,
                                unexpected=type(instance.val).__name__,
                                attr=self.name
                            )
            )

    def __get__(self, instance, owner) -> object:
        return instance.val

    def __set_name__(self, owner, name) -> None:
        """Setting name of an attribute."""
        self.name = name


class Article:
    """The `Article` class you need to write for the qualifier."""
    ID = -1
    attr = ArticleField(field_type=int)

    def __init__(self, title: str, author: str, publication_date: datetime.datetime, content: str):
        type(self).ID += 1
        self.id = self.ID
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.content = content
        self.last_edited = None

    def short_introduction(self, n_characters: int):
        """Short introduction based on n_characters."""
        short_content = self.content[:n_characters + 1]
        last_space_index = short_content.rfind(" ")
        last_newline_index = short_content.rfind("\n")
        index = last_space_index if last_space_index > last_newline_index else last_newline_index
        return short_content[:index]

    def most_common_words(self, n_word: int):
        """Most common words in the article."""

        # retrieving words only consisting ascii characters
        content = re.findall(r'\b[a-z]{1,100}\b', self.content.lower())
        unordered_words_count = {}

        # saving as {word : frequency} ( unordered )
        for word in content:
            if word in unordered_words_count:
                unordered_words_count[word] += 1
            else:
                unordered_words_count[word] = 1

        ordered_list_words = [(word, freq)  # reverse ordered list of tuples
                              for word, freq in sorted(unordered_words_count.items(), key=lambda item: item[1])]

        ordered_list_words.reverse()
        # sorting words by their appearance index in the content
        sort_list_of_tuple(ordered_list_words, self.content)

        return {word: freq for word, freq in ordered_list_words[:n_word]}

    def __repr__(self):
        """String representation of a class."""
        return "<{class_name} title=\"{title}\" author='{author}' publication_date='{pub_date}'>".format(
            class_name=__class__.__name__,
            title=self.title,
            author=self.author,
            pub_date=self.publication_date.isoformat()
        )

    def __len__(self):
        """Length of the content of an article."""
        return len(self.content)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

        if key == 'content':
            self.last_edited = datetime.datetime.now()

    def __gt__(self, other):
        return self.publication_date > other.publication_date

    def __lt__(self, other):
        return self.publication_date < other.publication_date
