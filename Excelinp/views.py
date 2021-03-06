from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django import forms
from django.template import RequestContext
import django_excel as excel
from Excelinp.models import Question, Choice, Item
from Excelinp.forms import searchForm
import pyexcel.ext.xls
from django.db.models import Q
from django.http import Http404
from .forms import customHaystackSearchForm
from haystack.query import SearchQuerySet
# import pyexcel.ext.xlsx
# import pyexcel.ext.ods3

# Create your views here.


class UploadFileForm(forms.Form):
    file = forms.FileField()


# Create your views here.
def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv", file_name="download")
    else:
        form = UploadFileForm()
    return render_to_response(
        'upload_form.html',
        {
            'form': form,
            'title': 'Excel file upload and download example',
            'header': 'Please choose any excel file from your cloned repository:'
        },
        context_instance=RequestContext(request))


def download(request, file_type):
    sheet = excel.pe.Sheet(data)
    return excel.make_response(sheet, file_type)

    
def download_as_attachment(request, file_type, file_name):
    return excel.make_response_from_array(data, file_type, file_name=file_name)


def export_data(request, atype):
    if atype == "sheet":
        return excel.make_response_from_a_table(
            Question, 'xls', file_name="sheet")
    elif atype == "book":
        return excel.make_response_from_tables(
            [Question, Choice], 'xls', file_name="book")
    elif atype == "custom":
        question = Question.objects.get(slug='ide')
        query_sets = Choice.objects.filter(question=question)
        column_names = ['choice_text', 'id', 'votes']
        return excel.make_response_from_query_sets(
            query_sets,
            column_names,
            'xls',
            file_name="custom"
        )
    else:
        return HttpResponseBadRequest("Bad request. please put one of these in your url suffix: sheet, book or custom")

def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row
        if form.is_valid():
            request.FILES['file'].save_book_to_database(
                models=[
                # Question, Choice,
                 Item],
                initializers=[
                # None, choice_func,
                None],
                mapdicts=[
                    # ['question_text', 'pub_date', 'slug'],
                    # ['question', 'choice_text', 'votes'],
                    ['ID','Code','Description','Unit','Price3']]
            )
            return HttpResponse("OK", status=200)
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render_to_response(
        'upload_form.html',
        {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        },
        context_instance=RequestContext(request))


def import_sheet(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            request.FILES['file'].save_to_database(
                name_columns_by_row=2,
                model=Question,
                mapdict=['question_text', 'pub_date', 'slug'])
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render_to_response('upload_form.html',
                              {'form': form},
                              context_instance=RequestContext(request))


def exchange(request, file_type):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        filehandle = request.FILES['file']
        return excel.make_response(filehandle.get_sheet(), file_type)
    else:
        return HttpResponseBadRequest()


def parse(request, data_struct_type):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        filehandle = request.FILES['file']
        if data_struct_type == "array":
            return JsonResponse({"result": filehandle.get_array()})
        elif data_struct_type == "dict":
            return JsonResponse(filehandle.get_dict())
        elif data_struct_type == "records": 
            return JsonResponse({"result": filehandle.get_records()})
        elif data_struct_type == "book":
            return JsonResponse(filehandle.get_book().to_dict())
        elif data_struct_type == "book_dict":
            return JsonResponse(filehandle.get_book_dict())
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

def search(request):
    # form_class = searchForm
    # if request.method == "POST":
    #     form = form_class(data=request.POST)
    #     if form.is_valid():
    #         return HttpResponse('WORKING!!!',status=200)
    #     # else:
    #     #     return HttpResponseBadRequest()    
    # return render_to_response('upload_form.html',
    #                           {'form': form_class},
    #                           context_instance=RequestContext(request))
    
    # form = customHaystackSearchForm(request.GET)
    # searchresults = form.search()
    # return render(request, 'search2.html', {'form' : form})
    form = customHaystackSearchForm(request.GET)
    searchresults = form.search()
    try:
        sTerm = request.GET['code']
    except:
        return render(request, 'search2.html', {'form' : form})
    results = SearchQuerySet().auto_query(sTerm)
    items = []
    for r in results:
        items.append(r.object)
    if(items==[]):
        val=0
    else:
        val=1        
    return render(request, 'search2.html', {'form' : form, 'items': items, 'value': val})


def itemDescription(request,pk):
    try:
        item = Item.objects.get(ID=pk)
    except:
        raise Http404("Item does not exist")    
    context = {'item':item}
    # print(item.Description)
    return render(request, 'result.html', context)

