
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from requests import post
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.generic import UpdateView, DeleteView

# get list post all


class PostListView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm()
        context = {'post_list': posts, 'form': form}
        return render(request, 'blogs/post_list.html', context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
        context = {'post_list': posts, 'form': form}
        return render(request, 'blogs/post_list.html', context)

# detail about post


'''
post(id)==>primary_key
# Khóa ngoại của bảng này là khóa chính của bảng kia
'''


class PostDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk) # get primary_key
        form = CommentForm()
        context = {'post': post, 'from': form}
        return render(request, 'blogs/post_detail.html', context=context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'blogs/post_detail.html', context)

# class PostDetailView(View):
#     def get(self, request, pk, *args, **kwargs):
#         post = Post.objects.get(pk=pk)
#         form = CommentForm()

#         context = {
#             'post': post,
#             'form': form,
#         }

#         return render(request, 'blogs/post_detail.html', context)

#     def post(self, request, pk, *args, **kwargs):
#         post = Post.objects.get(pk=pk)
#         form = CommentForm(request.POST)

#         if form.is_valid():
#             new_comment = form.save(commit=False)
#             new_comment.author = request.user
#             new_comment.post = post
#             new_comment.save()

#         comments = Comment.objects.filter(post=post).order_by('-created_on')

#         context = {
#             'post': post,
#             'form': form,
#             'comments': comments,
#         }

#         return render(request, 'blogs/post_detail.html', context)

# edit your post


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'blogs/post_edit.html'

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blogs/post_delete.html'
    success_url = reverse_lazy('post')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blogs/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs.get('post_pk')
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
