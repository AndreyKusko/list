from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app2_notebooks import (
    models as a2_m,
    serializers as a2_s,
)

User = get_user_model()


def home(request):
    context = {}
    if not request.user.is_authenticated:
        return render(request, "base.html", context)
    library, created = a2_m.Library.objects.get_or_create(user=request.user)
    context['library'] = library
    context['notebooks'] = a2_m.Notebook.objects.filter(library=library)
    return render(request, "base.html", context)


def notebook(request, notebook_id):
    context = {'notebook': a2_m.Notebook.objects.get(id=notebook_id), }
    return render(request, "notebook.html", context)


class NotebookApiView(viewsets.ModelViewSet):
    model = a2_m.Notebook
    permission_classes = [IsAuthenticated]
    allowed_methods = ['PUT', 'PATCH', 'GET', 'DELETE']
    serializer_class = a2_s.NotebookSerializer
    queryset = a2_m.Notebook.objects.all()

    def list(self, request):

        queryset = self.queryset.filter(user=request.user, is_deleted=False)
        if request.query_params.get('id'):
            queryset = get_object_or_404(self.model, id=request.query_params['id'])
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        library_id = request.data.get('library_id')
        if not library_id:
            return
        notebooks_qty = self.model.objects.filter(library_id=library_id).count()
        queryset = self.model.objects.create(
            user=user,
            library_id=library_id,
            title=notebooks_qty + 1,
            ordering_number=notebooks_qty + 1
        )
        serializer = self.serializer_class(queryset, many=False)
        return Response(serializer.data)

    def patch(self, request):
        model_id = request.data.get('id')
        if not model_id:
            raise ValueError('Notebook id required')
        model = get_object_or_404(self.model, id=model_id, user=request.user)
        model.is_deleted = False
        model.title = request.data.get('title') or model.title

        model.save()
        serializer = self.serializer_class(model, many=False)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):

        model = get_object_or_404(self.model, id=kwargs.get('pk'), user=request.user)
        model.is_deleted = True
        model.save(update_fields=['is_deleted'])

        serializer = self.serializer_class(model, many=False)
        return Response(serializer.data)


class NoteApiView(viewsets.ModelViewSet):
    model = a2_m.Note
    permission_classes = [IsAuthenticated]
    allowed_methods = ['PUT', 'PATCH', 'GET', 'DELETE']
    serializer_class = a2_s.NoteSerializer
    queryset = a2_m.Note.objects.all()

    def list(self, request):
        notebook_id = request.query_params.get('notebook_id')

        if not notebook_id:
            raise ValueError('notebook id required')
        queryset = self.model.objects.filter(notebook_id=notebook_id, user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        notebook_id = request.data.get('notebook_id')
        if not notebook_id:
            raise ValueError('Notebook id required')
        model = self.model()
        model.user = user
        model.notebook = get_object_or_404(a2_m.Notebook, id=notebook_id, user=request.user)

        is_list = request.data.get('is_list', False)
        is_note = request.data.get('is_note', False)
        if is_list:
            model.is_list = is_list
        if is_note:
            model.is_note = is_note

        title = request.data.get('title', '')
        text = request.data.get('text', '')
        if title and is_list and not is_note:
            model.title = title
        elif not text and not is_list and is_note:
            raise ValueError('text required for note')
        elif not title and text and not is_list and is_note:
            model.title = text.split()[0]
        else:
            raise ValueError('title required for creating a list')

        model.ordering_number = request.data.get('ordering_number') or self.model.objects.filter(
            notebook_id=notebook_id).count() + 1

        model.save()
        serializer = self.serializer_class(model, many=False)
        return Response(serializer.data)

    def patch(self, request):
        model_id = request.data.get('id')

        if not model_id:
            raise ValueError('Notebook id required')
        model = get_object_or_404(self.model, id=model_id, user=request.user)

        model.title = request.data.get('title') or model.title

        model.save()
        serializer = self.serializer_class(model, many=False)
        return Response(serializer.data)

    def delete(self, request):
        queryset = self.model.delete(id=self.request.query_params.get['id'])
        return queryset


class PointApiView(viewsets.ModelViewSet):
    model = a2_m.Point
    permission_classes = [IsAuthenticated]
    allowed_methods = ['PUT', 'PATCH', 'GET', 'DELETE']
    serializer_class = a2_s.PointSerializer
    queryset = a2_m.Point.objects.all()

    @classmethod
    def get_extra_actions(cls):
        return []

    def list(self, request, *args, **kwargs):
        note_id = self.request.query_params.get('note_id')

        if not note_id:
            raise ValueError('notebook id required')
        queryset = self.model.objects.filter(
            is_deleted=False, note_id=note_id, user=self.request.user
        ).order_by("is_crossed", "ordering_number", "title", "id")
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        model = self.model(user=user)
        model.note_id = request.data.get('note_id') or model.note_id

        model.ordering_number = request.data.get('ordering_number') or model.ordering_number
        if not request.data.get('title'):
            raise ValueError('title required')
        model.title = request.data.get('title')
        model.parent_point = a2_m.Point.objects.get(id=request.data.get('point_id')) or model.parent_point
        model.text = request.data.get('text', '')
        model.active = request.data.get('active')
        model.hidden_note = request.data.get('hidden_note', '')
        model.save()

        serializer = self.serializer_class(model, many=False)
        return Response(serializer.data)

    def patch(self, request):
        model_id = request.data.get('id')
        if not model_id:
            raise ValueError('Notebook id required')
        model = get_object_or_404(self.model, id=model_id, user=request.user)

        # todo: strange construction with none and if make it siply
        model.title = request.data.get('title') or model.title

        note_id = request.data.get('note_id')

        model.note_id = note_id or model.note_id
        if model.is_deleted:
            model.is_deleted = False

        if 'cross_out' in request.data:
            model.is_crossed = True if model.is_crossed is False else False

        model.save()
        serializer = self.serializer_class(model, many=False)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        model_id = kwargs.get('pk')
        model = get_object_or_404(self.model, id=model_id, user=request.user)
        model.is_deleted = True
        model.save(update_fields=['is_deleted'])
        serializer = self.serializer_class(model, many=False)
        return Response(serializer.data)
