import glob
import json
import os
from datetime import datetime
from pprint import pprint
from typing import Any, List

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from download_script import execute_download
from libs.action.update_manga_config import update_manga_config
from libs.upload_google_drive.google_auth import (
    get_google_creds,
    get_google_flow,
    write_google_token,
)
from libs.upload_google_drive.manga_result import get_manga_updated
from libs.utils.constants import MANGE_ROOT_DIR
from libs.utils.interface import UpdateMangaConfigData


@csrf_protect
def home(request: HttpRequest):
    projects = []
    creds = get_google_creds()

    manga_exists_json, results_viewed_sorted, results_yet_view_sorted = get_manga_updated()

    man_mirror_cartoons = []
    with open(os.path.join(MANGE_ROOT_DIR, 'man-mirror.json'), encoding='utf-8') as f:
        man_mirror_cartoons = json.load(f)

    my_novel_cartoons = []
    with open(os.path.join(MANGE_ROOT_DIR, 'my-novel.json'), encoding='utf-8') as f:
        my_novel_cartoons = json.load(f)

    # for project_dir in os.listdir(f'{CARTOON_DIR}'):
    #     if not os.path.isdir(os.path.join(CARTOON_DIR, project_dir)):
    #         continue
    #     # for name in files:
    #     #     print(os.path.join(root, name))
    #     title = project_dir

    #     sub_dirs = []

    #     for sub_project_cartoon_dir in os.listdir(os.path.join(CARTOON_DIR, project_dir)):
    #         # print(f'{sub_project_cartoon_dir}')
    #         image_pdf_list = glob.glob(os.path.join(
    #             CARTOON_DIR, project_dir, sub_project_cartoon_dir, '*.pdf'))
    #         sub_dirs.append({
    #             "title": sub_project_cartoon_dir,
    #             "image_pdf_list": image_pdf_list
    #         })

    #     projects.append({
    #         "title": project_dir,
    #         "sub_dirs": sub_dirs
    #     })

        # for name in dirs:
        # print(os.path.join(root, name))

    manga_exists = []

    for project_name, project_json in manga_exists_json.items():
        # print(f'project: {project}')
        manga_list: List[Any] = [{
            "manga_name": manga_name,
            "total":  manga_json['total'] or 0
        } for manga_name, manga_json in project_json['sub_dirs'].items()]
        manga_exists.append({
            "project_name": project_name,
            "manga_list": manga_list
        })

    man_mirror_downloaded = manga_exists_json['man-mirror']['sub_dirs']
    my_novel_downloaded = manga_exists_json['my-novel']['sub_dirs']
    # print(projects)
    man_mirror_cartoons = [{
        "cartoon_name": cartoon_name,
        "cartoon_id": cartoon_id,
        "latest_chapter": latest_chapter,
        "max_chapter": max_chapter,
        "disabled": disabled or False,
        "downloaded": man_mirror_downloaded[cartoon_name]['total'] or 0 if man_mirror_downloaded[cartoon_name] is not None else 0,
    } for cartoon_name, cartoon_id, latest_chapter, max_chapter, disabled in man_mirror_cartoons]

    my_novel_cartoons = [{
        "cartoon_name": cartoon_name,
        "cartoon_id": cartoon_id,
        "latest_chapter": latest_chapter,
        "max_chapter": '',
        "disabled": disabled or False,
        "downloaded": my_novel_downloaded[cartoon_name]['total'] or 0 if my_novel_downloaded[cartoon_name] is not None else 0,
    } for cartoon_name, cartoon_id, latest_chapter, disabled in my_novel_cartoons]
    # pprint({
    #     "man_mirror_cartoons": man_mirror_cartoons,
    #     "my_novel_cartoons": my_novel_cartoons,
    # })
    context = {
        # "projects": projects,
        "manga_exists": manga_exists,
        "man_mirror_cartoons": man_mirror_cartoons,
        "my_novel_cartoons": my_novel_cartoons or [],
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
    return redirect("http://localhost:8001/")


def download_manga(request: WSGIRequest):
    if request.method == "POST":
        enable_download_mam_mirror = False
        enable_download_mam_mirror_manual = False
        enable_download_my_novel = False
        body = json.loads(request.body)
        type = body['type'] or request.POST['type']
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


def manga_updated(request: WSGIRequest):
    if request.method == 'POST':
        body = json.loads(request.body)
        cartoon_name = body['cartoon_name']
        cartoon_id = body['cartoon_id']
        latest_chapter = body['latest_chapter']
        max_chapter = body['max_chapter']
        disabled = body['disabled']
        downloaded = body['downloaded']
        project_name = body['project_name']

        pprint({
            "cartoon_name": cartoon_name,
            "cartoon_id": cartoon_id,
            "latest_chapter": latest_chapter,
            "max_chapter": max_chapter,
            "disabled": disabled,
            "downloaded": downloaded,
            "project_name": project_name,
        })

        d = UpdateMangaConfigData(
            cartoon_name=cartoon_name,
            cartoon_id=cartoon_id,
            latest_chapter=latest_chapter,
            max_chapter=max_chapter,
            disabled=disabled,
            downloaded=downloaded,
            project_name=project_name,
        )
        res = update_manga_config(d)
        return JsonResponse({
            "status":  200 if res else 400
        })

    latest_update = request.GET.get("latest_update")

    print(f'latest_update: {latest_update}')

    manga_exists_json, results_viewed_sorted, results_yet_view_sorted = get_manga_updated(
        latest_update=latest_update)

    man_mirror_cartoons = []
    with open(os.path.join(MANGE_ROOT_DIR, 'man-mirror.json'), encoding='utf-8') as f:
        man_mirror_cartoons = json.load(f)

    my_novel_cartoons = []
    with open(os.path.join(MANGE_ROOT_DIR, 'my-novel.json'), encoding='utf-8') as f:
        my_novel_cartoons = json.load(f)

    # for project_dir in os.listdir(f'{CARTOON_DIR}'):
    #     if not os.path.isdir(os.path.join(CARTOON_DIR, project_dir)):
    #         continue
    #     # for name in files:
    #     #     print(os.path.join(root, name))
    #     title = project_dir

    #     sub_dirs = []

    #     for sub_project_cartoon_dir in os.listdir(os.path.join(CARTOON_DIR, project_dir)):
    #         # print(f'{sub_project_cartoon_dir}')
    #         image_pdf_list = glob.glob(os.path.join(
    #             CARTOON_DIR, project_dir, sub_project_cartoon_dir, '*.pdf'))
    #         sub_dirs.append({
    #             "title": sub_project_cartoon_dir,
    #             "image_pdf_list": image_pdf_list
    #         })

    #     projects.append({
    #         "title": project_dir,
    #         "sub_dirs": sub_dirs
    #     })

        # for name in dirs:
        # print(os.path.join(root, name))

    manga_exists = []

    for project_name, project_json in manga_exists_json.items():
        # print(f'project: {project}')
        manga_list: List[Any] = [{
            "manga_name": manga_name,
            "total":  manga_json['total'] or 0
        } for manga_name, manga_json in project_json['sub_dirs'].items()]
        manga_exists.append({
            "project_name": project_name,
            "manga_list": manga_list
        })

    man_mirror_downloaded = manga_exists_json['man-mirror']['sub_dirs']
    my_novel_downloaded = manga_exists_json['my-novel']['sub_dirs']
    # print(projects)
    man_mirror_cartoons = [{
        "cartoon_name": cartoon_name,
        "cartoon_id": cartoon_id,
        "latest_chapter": latest_chapter,
        "max_chapter": max_chapter,
        "disabled": disabled or False,
        "downloaded": man_mirror_downloaded[cartoon_name]['total'] or 0 if man_mirror_downloaded[cartoon_name] is not None else 0,
    } for cartoon_name, cartoon_id, latest_chapter, max_chapter, disabled in man_mirror_cartoons]

    my_novel_cartoons = [{
        "cartoon_name": cartoon_name,
        "cartoon_id": cartoon_id,
        "latest_chapter": latest_chapter,
        "max_chapter": '',
        "disabled": disabled or False,
        "downloaded": my_novel_downloaded[cartoon_name]['total'] or 0 if my_novel_downloaded[cartoon_name] is not None else 0,
    } for cartoon_name, cartoon_id, latest_chapter, disabled in my_novel_cartoons]

    return JsonResponse({
        "updated": datetime.now().isoformat(sep='T', timespec='auto'),
        "manga_exists": manga_exists or [],
        "man_mirror_cartoons": man_mirror_cartoons or [],
        "my_novel_cartoons": my_novel_cartoons or [],
        "results_viewed_sorted": results_viewed_sorted or [],
        "results_yet_view_sorted": results_yet_view_sorted or []
    })


def auth_google_drive(request: HttpRequest):
    creds = get_google_creds()

    if request.method == 'POST':
        # body = json.loads(request.body)
        # redirect_uri = body['redirect_uri']
        flow = get_google_flow()
        auth_data = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            # access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            # include_granted_scopes='true'
        )
        authorization_url, _ = auth_data

        return JsonResponse({
            "authorization_url": authorization_url
        })

    return JsonResponse({
        "google_authen_status": creds is not None and creds.valid and not creds.expired,
    })
