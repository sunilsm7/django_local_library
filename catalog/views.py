from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.


def index(request):
    """
        View function for home page os site.
    """
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (Status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.all().count()
    booktitle_startswith_the = Book.objects.filter(title__istartswith='t').count()

    # Nymber of visits to this, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    # Render the  HTML template index.html with the data in the contex variables
    context = {'num_books': num_books, 'num_instances': num_instances,
               'num_instances_available': num_instances_available, 'num_authors': num_authors, 'num_genres': num_genres,
               'booktitle_startswith_the': booktitle_startswith_the, 'num_visits': num_visits}
    return render(request, 'index.html', context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    queryset = Book.objects.all()
    template_name = 'catlog/book_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['books_count'] = Book.objects.all().count()
        return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    queryset = Author.objects.all()
    template_name = 'catlog/author_list.html'
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    context_object_name = 'bookinstance_list'
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanBooksAllListView(PermissionRequiredMixin, generic.ListView):
	"""
	Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission.
	"""
	model = BookInstance
	context_object_name = 'bookinstance_list'
	permission_required = 'catalog.can_mark_returned'
	template_name = 'catalog/bookinstance_list_borrowed_all.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(status__exact = 'o').order_by('due_back')





