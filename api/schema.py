import graphene
from graphene_django import DjangoObjectType
from .models import Book, Author
from django.db.models.expressions import Expression


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author


class BookType(DjangoObjectType):
    class Meta:
        model = Book


class AutherInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()


class BookInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    author = graphene.Int()
    year_published = graphene.String()
    review = graphene.Int()


class CreateBook(graphene.Mutation):
    class Arguments:
        book_data = BookInput(required=True)

    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, book_data=None):
        try:
            book_instance = Book(
                title=book_data.title,
                author=Author.objects.get(id=book_data.author),
                year_published=book_data.year_published,
                review=book_data.review
            )
            book_instance.save()
            return CreateBook(book=book_instance)
        except Author.DoesNotExist:
            return CreateBook(book=None)


class UpdateBook(graphene.Mutation):
    class Arguments:
        book_data = BookInput(required=True)

    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, book_data=None):
        try:
            book_instance = Book.objects.get(pk=book_data.id)
            print()
            if book_instance:
                try:
                    book_instance.title = book_data.title
                    book_instance.author = Author.objects.get(id=book_data.author)
                    book_instance.year_published = book_data.year_published
                    book_instance.review = book_data.review
                    book_instance.save()
                    return UpdateBook(book=book_instance)
                except Author.DoesNotExist:
                    return UpdateBook(book=None)
        except Book.DoesNotExist:
            return UpdateBook(book=None)


class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, id):
        try:
            book_instance = Book.objects.get(pk=id)
            book_instance.delete()
        except Book.DoesNotExist:
            return None
        return None


class CreateAuthor(graphene.Mutation):
    class Arguments:
        author_data = AutherInput(required=True)

    author = graphene.Field(AuthorType)

    @staticmethod
    def mutate(root, info, author_data=None):
        try:
            author_instance = Author(
                title=author_data.title,
            )
            author_instance.save()
            return CreateAuthor(author=author_instance)
        except Author.DoesNotExist:
            return CreateAuthor(author=None)


class UpdateAuthor(graphene.Mutation):
    class Arguments:
        author_data = AutherInput(required=True)

    author = graphene.Field(AuthorType)

    @staticmethod
    def mutate(root, info, author_data=None):
        try:
            author_instance = Author.objects.get(pk=author_data.id)
            if author_instance:
                author_instance.title = author_data.title
                author_instance.save()
                return UpdateAuthor(author=author_instance)
        except Author.DoesNotExist:
            return UpdateAuthor(author=None)


class DeleteAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    author = graphene.Field(AuthorType)

    @staticmethod
    def mutate(root, info, id):
        try:
            book_instance = Author.objects.get(pk=id)
            book_instance.delete()
            return None
        except Author.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()
    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()
    delete_author = DeleteAuthor.Field()


class Query(graphene.ObjectType):
    all_author = graphene.List(AuthorType)
    author = graphene.Field(AuthorType, author_id=graphene.Int())
    all_books = graphene.List(BookType)
    book = graphene.Field(BookType, book_id=graphene.Int())
    author_books = graphene.List(BookType, author_id=graphene.Int())

    def resolve_all_author(self, info, **kwargs):
        print(info.context.user)
        try:
            return Author.objects.all()
        except Expression:
            return None

    def resolve_author(self, info, author_id):
        try:
            return Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return None

    def resolve_all_books(self, info, **kwargs):
        try:
            return Book.objects.all()
        except Expression:
            return None

    def resolve_book(self, info, book_id):
        try:
            return Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return None

    def resolve_author_books(self, info, author_id):
        try:
            return Book.objects.filter(author__id=author_id)
        except Book.DoesNotExist:
            return None
