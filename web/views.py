import glob
import io
import os
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas

from libs.utils.constants import CARTOON_DIR


def home(request):
    projects = []

    for project_dir in os.listdir(f'{CARTOON_DIR}'):
        # for name in files:
        #     print(os.path.join(root, name))
        title = project_dir

        sub_dirs = []

        for sub_project_cartoon_dir in os.listdir(os.path.join(CARTOON_DIR, project_dir)):
            print(f'{sub_project_cartoon_dir}')
            image_pdf_list = glob.glob(os.path.join(
                CARTOON_DIR, project_dir, sub_project_cartoon_dir, '*.pdf'))
            sub_dirs.append({
                "title": sub_project_cartoon_dir,
                "image_pdf_list": image_pdf_list
            })

        projects.append({
            "title": title,
            "sub_dirs": sub_dirs
        })

        # for name in dirs:
        # print(os.path.join(root, name))

    # print(projects)

    context = {
        "projects": projects
    }
    return render(request, template_name='home/index.html', context=context)


def pdf_view(request):
    pdf_path = request.GET.get("pdf_path", None)  # default None if not present
    print(f'pdf_path {pdf_path}')
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    # p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=pdf_path)


def pdf_view_v2(request):
    pdf_path = request.GET.get("pdf_path", None)  # default None if not present
    return HttpResponse(f'<h1>{pdf_path}</h1>')
