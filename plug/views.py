
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view,parser_classes
from .plagiarism_check import PlagiarismChecker 
from .bangla_nltk import BanglaNltk
from .pdf_converter import PdfConverter
from .multi_file_to_array_text import MultiFile


@api_view(["POST"])
@parser_classes([MultiPartParser,FormParser,JSONParser])
def twoTextPlagiarismCheck(request):
    
    if (request.method == 'POST'):
        plagiarism_obj = PlagiarismChecker()
        b_nltk = BanglaNltk()
        doc1 = request.data['doc1']
        doc2 = request.data['doc2']
        text1 = b_nltk.sentence_tokenizer(doc1)
        text2 = b_nltk.sentence_tokenizer(doc2)
        
        arrayOfResult = plagiarism_obj.plugCheckFromTextArray(text1, text2)

        return Response(arrayOfResult, status=200)


@api_view(["POST"])
@parser_classes([MultiPartParser,FormParser,JSONParser])
def twoPdfPlagiarismCheck(request):
    
    if (request.method == 'POST'):
        file1 = request.FILES["file1"]
        file2 = request.FILES["file2"]
        
        pdf_text1 = PdfConverter.converter(request.FILES["file1"])
        pdf_text2 = PdfConverter.converter(request.FILES["file2"])
        plagiarism_obj = PlagiarismChecker()
        similarText = plagiarism_obj.sentenceSimilarity(pdf_text1, pdf_text2)
        percentage = plagiarism_obj.percentageOfText(pdf_text1, pdf_text2)
        dic = {'between':file1.name + " " + file2.name,'text':similarText, 'percent': percentage}
        return JsonResponse(dic, safe=False)


@api_view(["POST"])
@parser_classes([MultiPartParser,FormParser,JSONParser])
def multiplePdfPlagiarismCheck(request):
    
    if (request.method == 'POST'):
        files = request.data.getlist('files')

        multi_file_instance = MultiFile(files)
        res = multi_file_instance.multiFilePlugCheck()
        
        return Response(res, status=200)

@api_view(["POST"])
@parser_classes([MultiPartParser,FormParser,JSONParser])
def oneToManyPdfPlagiarismCheck(request):
    
    if (request.method == 'POST'):
        file = request.data.getlist('file')
        files = request.data.getlist('files')
        single_pdf_text = PdfConverter.converter(file)
        multiple_file_instance = MultiFile(files)
        plag_result = multiple_file_instance.single_file_to_multifile_plug_check(single_pdf_text, file.name) 
        
        return Response(plag_result, status=200)