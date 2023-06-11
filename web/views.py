import glob
import os
from pprint import pprint

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

from download_script import execute_download
from libs.upload_google_drive.google_auth import (
    get_google_creds,
    get_google_flow,
    write_google_token,
)
from libs.upload_google_drive.manga_result import get_manga_updated
from libs.utils.constants import CARTOON_DIR


@csrf_protect
def home(request: HttpRequest):
    projects = []
    creds = get_google_creds()
    results_viewed_sorted, results_yet_view_sorted = get_manga_updated()

    for project_dir in os.listdir(f'{CARTOON_DIR}'):
        if not os.path.isdir(os.path.join(CARTOON_DIR, project_dir)):
            continue
        # for name in files:
        #     print(os.path.join(root, name))
        title = project_dir

        sub_dirs = []

        for sub_project_cartoon_dir in os.listdir(os.path.join(CARTOON_DIR, project_dir)):
            # print(f'{sub_project_cartoon_dir}')
            image_pdf_list = glob.glob(os.path.join(
                CARTOON_DIR, project_dir, sub_project_cartoon_dir, '*.pdf'))
            sub_dirs.append({
                "title": sub_project_cartoon_dir,
                "image_pdf_list": image_pdf_list
            })

        projects.append({
            "title": project_dir,
            "sub_dirs": sub_dirs
        })

        # for name in dirs:
        # print(os.path.join(root, name))

    # print(projects)

    context = {
        "projects": projects,
        "google_auth_ok": creds is not None and creds.valid and not creds.expired,
        "results_viewed_sorted": results_viewed_sorted,
        "results_yet_view_sorted": results_yet_view_sorted
    }
    return render(request, template_name='home/index.html', context=context)


@csrf_protect
def google_auth(request: HttpRequest):
    flow = get_google_flow()
    auth_data = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        # access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        # include_granted_scopes='true'
    )
    authorization_url, _ = auth_data

    return render(request, template_name='google_auth/index.html', context={
        "google_auth_link": authorization_url
    })


def google_callback(request: WSGIRequest):
    code = request.GET['code']
    pprint({
        "code": code,
        "request.GET": request.GET,
    })

    flow = get_google_flow()
    flow.fetch_token(code=code)

    # You can use flow.credentials, or you can just get a requests session
    # using flow.authorized_session.
    session = flow.authorized_session()
    print(session.get('https://www.googleapis.com/userinfo/v2/me').json())
    # flow.fetch_token(
    #     authorization_response=authorization_response,
    # )
    creds = flow.credentials
    write_google_token(creds)
    return redirect("/")


def download_manga(request: WSGIRequest):
    if request.method == "POST":
        enable_download_mam_mirror = False
        enable_download_mam_mirror_manual = False
        enable_download_my_novel = False

        type = request.POST['type']
        pprint({
            "data": request.POST,
            "type": type
        })
        if type == 'man-mirror':
            enable_download_mam_mirror = True
        if type == 'man-mirror-manual':
            enable_download_mam_mirror_manual = True
        if type == 'my-novel':
            enable_download_my_novel = True

        execute_download(
            enable_download_mam_mirror=enable_download_mam_mirror,
            enable_download_mam_mirror_manual=enable_download_mam_mirror_manual,
            enable_download_my_novel=enable_download_my_novel,
        )
    return redirect("/")
