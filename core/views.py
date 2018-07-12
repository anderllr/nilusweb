from django.shortcuts import render
# Create your views here.


def signin(request):
    return render(request,'signin.html')




# class PDFTemplateResponse(TemplateResponse):
#
#     def generate_pdf(self, retval):
#
#         html = self.content
#
#         result = StringIO.StringIO()
#         rendering = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
#
#         if rendering.err:
#             return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
#         else:
#             self.content = result.getvalue()
#
#     def __init__(self, *args, **kwargs):
#         super(PDFTemplateResponse, self).__init__(*args, mimetype='application/pdf', **kwargs)
#         self.add_post_render_callback(self.generate_pdf)
#
#
# class PDFTemplateView(TemplateView):
#     response_class = PDFTemplateResponse