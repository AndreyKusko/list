
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *
User = get_user_model()


def home(request):
    if request.user.is_authenticated:
        library, created = Library.objects.get_or_create(user=request.user)
        notebooks = Notebook.objects.filter(library=library)
        context = {
            "library": library,
            "notebooks": notebooks,
        }
        return render(request, "base.html", context)
    context = {}
    return render(request, "base.html", context)


def notebook(request, notebook_id):
    context = {
        'notebook': Notebook.objects.get(id=notebook_id),
    }
    return render(request, "notebook.html", context)


class NotebookApiView(viewsets.ModelViewSet):
    model = Notebook
    permission_classes = [IsAuthenticated]
    allowed_methods = ['PUT', 'PATCH', 'GET', 'DELETE']
    serializer_class = NotebookSerializer
    queryset = Notebook.objects.all()

    def list(self, request):
        queryset = self.queryset.filter(user=request.user, is_deleted=False)
        notebook_id = request.query_params.get('id', None)
        if notebook_id:
            queryset = get_object_or_404(self.model, id=request.query_params['id'])
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
        # return queryset

    def put(self, request):
        user = request.user
        library_id = request.data.get('library_id', None)
        if library_id:
            notebooks_qty = self.model.objects.filter(library_id=library_id).count()
            queryset = self.model.objects.create(
                user=user,
                library_id=library_id,
                title=notebooks_qty+1,
                ordering_number=notebooks_qty+1
            )
            serializer = self.serializer_class(queryset, many=False)
            return Response(serializer.data)

    def patch(self, request):
        model_id = request.data.get('id', None)
        if model_id:
            model = get_object_or_404(self.model, id=model_id, user=request.user)
            title = request.data.get('title', None)
            model.is_deleted = False
            if title:
                model.title = title

            model.save()
            serializer = self.serializer_class(model, many=False)
            return Response(serializer.data)
        else:
            raise ValueError('Notebook id required')

    def destroy(self, request, *args, **kwargs):
        model_id = kwargs.get('pk')
        model = get_object_or_404(self.model, id=model_id, user=request.user)
        model.is_deleted = True
        model.save(update_fields=['is_deleted'])

        serializer = self.serializer_class(model, many=False)
        return Response(serializer.data)


class NoteApiView(viewsets.ModelViewSet):
    model = Note
    permission_classes = [IsAuthenticated]
    allowed_methods = ['PUT', 'PATCH', 'GET', 'DELETE']
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def list(self, request):
        notebook_id = request.query_params.get('notebook_id', None)

        if notebook_id:
            queryset = self.model.objects.filter(notebook_id=notebook_id, user=request.user)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        else:
            raise ValueError('notebook id required')

    def put(self, request):
        user = request.user
        notebook_id = request.data.get('notebook_id', None)
        if notebook_id:
            model = self.model()
            model.user = user
            model.notebook = get_object_or_404(Notebook, id=notebook_id, user=request.user)

            is_list = request.data.get('is_list', False)
            is_note = request.data.get('is_note', False)
            if is_list:
                model.is_list = is_list
            if is_note:
                model.is_note = is_note

            title = request.data.get('title', '')
            # ck_text = request.data.get('ck_text', '')
            text = request.data.get('text', '')
            if title and is_list and not is_note:
                model.title = title
            elif not text and not is_list and is_note:
                raise ValueError('text required for note')
            elif not title and text and not is_list and is_note:
                model.title = text.split()[0]
            else:
                raise ValueError('title required for creating a list')

            ordering_number = request.data.get('ordering_number', None)
            if ordering_number:
                model.ordering_number = ordering_number
            else:
                notes_qty = self.model.objects.filter(notebook_id=notebook_id).count()
                model.ordering_number = notes_qty+1

            model.save()
            serializer = self.serializer_class(model, many=False)
            return Response(serializer.data)
        else:
            raise ValueError('Notebook id required')

    def patch(self, request):
        model_id = request.data.get('id', None)
        if model_id:
            model = get_object_or_404(self.model, id=model_id, user=request.user)
            title = request.data.get('title', None)

            if title:
                model.title = title

            model.save()
            serializer = self.serializer_class(model, many=False)
            return Response(serializer.data)
        else:
            raise ValueError('Notebook id required')

    def delete(self, request):
        queryset = self.model.delete(id=self.request.query_params.get['id'])
        return queryset


class PointApiView(viewsets.ModelViewSet):
    model = Point
    permission_classes = [IsAuthenticated]
    allowed_methods = ['PUT', 'PATCH', 'GET', 'DELETE']
    serializer_class = PointSerializer
    queryset = Point.objects.all()

    @classmethod
    def get_extra_actions(cls):
        return []

    def list(self, request, *args, **kwargs):
        note_id = self.request.query_params.get('note_id', None)
        if note_id:
            queryset = self.model.objects.filter(is_deleted=False, note_id=note_id, user=self.request.user).order_by("is_crossed", "ordering_number", "title", "id")
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        else:
            raise ValueError('notebook id required')

    def put(self, request):
        user = request.user
        model = self.model(user=user)
        note_id = request.data.get('note_id', None)
        point_id = request.data.get('point_id', None)
        if note_id:
            model.note_id = note_id

        ordering_number = request.data.get('ordering_number', None)
        if ordering_number:
            model.ordering_number = ordering_number
        if not request.data.get('title', None):
            raise ValueError('title required')
        model.title = request.data.get('title')
        if point_id:
            model.parent_point = Point.objects.get(id=point_id)
        model.text = request.data.get('text', '')
        model.active = request.data.get('active', True)
        model.hidden_note = request.data.get('hidden_note', '')
        model.save()

        serializer = self.serializer_class(model, many=False)
        return Response(serializer.data)

    def patch(self, request):
        model_id = request.data.get('id', None)
        if model_id:
            model = get_object_or_404(self.model, id=model_id, user=request.user)

            # todo: strange construction with none and if make it siply
            title = request.data.get('title', None)
            if title:
                model.title = title

            note_id = request.data.get('note_id', None)

            if note_id:
                model.note_id = note_id
            if model.is_deleted:
                model.is_deleted = False

            if 'cross_out' in request.data:
                model.is_crossed = True if model.is_crossed is False else False

            model.save()
            serializer = self.serializer_class(model, many=False)
            return Response(serializer.data)
        else:
            raise ValueError('Notebook id required')

    def destroy(self, request, *args, **kwargs):
        model_id = kwargs.get('pk')
        model = get_object_or_404(self.model, id=model_id, user=request.user)
        model.is_deleted = True
        model.save(update_fields=['is_deleted'])
        serializer = self.serializer_class(model, many=False)
        return Response(serializer.data)
