import json
from datetime import datetime
from pprint import pprint
from typing import Any, List

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from download_script import execute_download
from libs.action.download_manga_manual import download_manga_manual
from libs.action.update_manga_config import update_manga_config
from libs.man_mirror import ManMirror
from libs.my_novel import MyNovel
from libs.upload_google_drive import generate_drive_manga_exists
from libs.upload_google_drive.google_auth import (
    get_google_creds,
    get_google_flow,
    write_google_token,
)
from libs.upload_google_drive.manga_result import get_manga_updated
from libs.utils.constants import WEB_URL
from libs.utils.db_client import get_manga_config
from libs.utils.interface import UpdateMangaConfigData


def health(request: HttpRequest):
    return HttpResponse()


def home(request: HttpRequest):
    return HttpResponse()


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
    """ google auth callback """
    code = request.GET['code']
    state = request.GET['state']
    scope = request.GET['scope']
    pprint({
        "code": code,
        "state": state,
        "scope": scope,
        "request.GET": request.GET,
    })

    flow = get_google_flow()
    flow.fetch_token(code=code)

    # You can use flow.credentials, or you can just get a requests session
    # using flow.authorized_session.
    # session = flow.authorized_session()
    # print(session.get('https://www.googleapis.com/userinfo/v2/me').json())
    # flow.fetch_token(
    #     authorization_response=authorization_response,
    # )
    creds = flow.credentials
    write_google_token(creds)
    return redirect(WEB_URL)


def download_manga(request: WSGIRequest):
    if request.method == "POST":
        enable_download_mam_mirror = False
        enable_download_mam_mirror_manual = False
        enable_download_my_novel = False
        body = json.loads(request.body)
        types = body['types'] or request.POST.getlist('types', [])
        pprint({
            "data": request.POST,
            "types": types
        })
        if 'man-mirror' in types:
            enable_download_mam_mirror = True
        if 'man-mirror-manual' in types:
            enable_download_mam_mirror_manual = True
        if 'my-novel' in types:
            enable_download_my_novel = True

        execute_download(
            enable_download_mam_mirror=enable_download_mam_mirror,
            enable_download_mam_mirror_manual=enable_download_mam_mirror_manual,
            enable_download_my_novel=enable_download_my_novel,
        )
    return redirect("/")


def download_manga_one(request: WSGIRequest):
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
        res = download_manga_manual(d)
        return JsonResponse({
            "status":  200 if res else 400
        })

    return JsonResponse({
        "status":  200
    })


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

    results_viewed_sorted, results_yet_view_sorted, count_manga_downloaded_hash = get_manga_updated(
        latest_update=latest_update)

    man_mirror_cartoons = get_manga_config(ManMirror.project_name)
    # with open(os.path.join(MANGE_ROOT_DIR, 'man-mirror.json'), encoding='utf-8') as f:
    #     man_mirror_cartoons = json.load(f)

    my_novel_cartoons = get_manga_config(MyNovel.project_name)

    # with open(os.path.join(MANGE_ROOT_DIR, 'my-novel.json'), encoding='utf-8') as f:
    #     my_novel_cartoons = json.load(f)

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

    # for project_name, project_json in manga_exists_json.items():
    #     # print(f'project: {project}')
    #     manga_list: List[Any] = [{
    #         "manga_name": manga_name,
    #         "total":  manga_json['total'] or 0
    #     } for manga_name, manga_json in project_json['sub_dirs'].items()]
    #     manga_exists.append({
    #         "project_name": project_name,
    #         "manga_list": manga_list
    #     })

    # if 'man-mirror' in manga_exists_json and manga_exists_json['man-mirror'] is not None:
    #     man_mirror_downloaded = manga_exists_json['man-mirror']['sub_dirs']

    man_mirror_cartoons = [{
        "cartoon_name": d.cartoon_name,
        "cartoon_id": d.cartoon_id,
        "latest_chapter": d.latest_chapter,
        "max_chapter": d.max_chapter,
        "disabled": d.disabled or False,
        "downloaded": count_manga_downloaded_hash.get(d.cartoon_id, 0),
    } for d in man_mirror_cartoons]

    # if 'my-novel' in manga_exists_json and manga_exists_json['my-novel'] is not None:
    #     my_novel_downloaded = manga_exists_json['my-novel']['sub_dirs']
    my_novel_cartoons = [{
        "cartoon_name": d.cartoon_name,
        "cartoon_id": d.cartoon_id,
        "latest_chapter": d.latest_chapter,
        "max_chapter": d.max_chapter,
        "disabled": d.disabled or False,
        "downloaded": count_manga_downloaded_hash.get(d.cartoon_id, 0),
    } for d in my_novel_cartoons]

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


def fetch_manga_updated(request: WSGIRequest):
    """ fetch manga updated """

    if request.method == 'POST':
        generate_drive_manga_exists()

    return JsonResponse({
        "success": True
    })
