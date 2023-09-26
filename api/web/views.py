import json
from datetime import datetime
from typing import Any

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
from libs.utils.db_client import StealMangaDb, get_manga_config
from libs.utils.interface import UpdateMangaConfigData


def health():
    return HttpResponse()


def home():
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
    # pprint({
    #     "code": code,
    #     "state": state,
    #     "scope": scope,
    #     "request.GET": request.GET,
    # })

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
        # pprint({
        #     "data": request.POST,
        #     "types": types
        # })
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
        body: dict = json.loads(request.body)
        cartoon_name: Any = body.get('cartoon_name')
        cartoon_id: Any = body.get('cartoon_id')
        latest_chapter: Any = body.get('latest_chapter')
        max_chapter: Any = body.get('max_chapter')
        disabled: Any = body.get('disabled')
        downloaded: Any = body.get('downloaded')
        project_name: Any = body.get('project_name')

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


def download_cartoon_by_id(request: WSGIRequest, cartoon_id: str):
    print(f'cartoon_id: {cartoon_id}')
    if request.method == 'POST':
        steal_manga_db = StealMangaDb()
        manga_config = steal_manga_db.get_manga_config(cartoon_id)

        if manga_config is None:
            return HttpResponse(status_code=404)

        print(f'download: ${manga_config.cartoon_name}')
        res = download_manga_manual(manga_config, auto_update_config=False)
        return JsonResponse({
            "status":  200 if res else 400
        })

    return HttpResponse(status_code=404)


def manga_updated(request: WSGIRequest):
    if request.method == 'POST':
        body: dict = json.loads(request.body)
        cartoon_name: Any = body.get('cartoon_name')
        cartoon_id: Any = body.get('cartoon_id')
        latest_chapter: Any = body.get('latest_chapter')
        max_chapter: Any = body.get('max_chapter')
        disabled: Any = body.get('disabled')
        downloaded: Any = body.get('downloaded')
        project_name: Any = body.get('project_name')

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

    # print(f'latest_update: {latest_update}')

    results_viewed_sorted, results_yet_view_sorted = get_manga_updated(
        latest_update=latest_update)

    man_mirror_cartoons = get_manga_config(ManMirror.project_name)
    my_novel_cartoons = get_manga_config(MyNovel.project_name)

    return JsonResponse({
        "updated": datetime.now().isoformat(sep='T', timespec='auto'),
        "man_mirror_cartoons":  [d.to_json() for d in man_mirror_cartoons],
        "my_novel_cartoons":  [d.to_json() for d in my_novel_cartoons],
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
