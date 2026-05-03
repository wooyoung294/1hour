"""Playwright 생명주기 - context 생성, teardown, tracing, video."""

import os
import shutil
from typing import Optional

import allure
from dotenv import load_dotenv
from loguru import logger
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, ViewportSize

load_dotenv(verbose=True)
URL = os.getenv('URL')
PAGE_URL = os.getenv('PAGE_URL')

TRACE_PATH = 'traces/'
VIDEO_PATH = 'videos/'


def safe_remove(target: str):
    if target == 'videos':
        path = VIDEO_PATH
    else:
        path = TRACE_PATH
    if os.path.exists(path):
        shutil.rmtree(path)


def playwright_config_base(
    playwright: Playwright,
    target_url: str,
    browser: Browser | None = None,
    storage_state: str | None = None,
    headless: bool = False,
    permissions: Optional[list[str]] = None,
) -> tuple[Page, BrowserContext, Browser]:
    """Playwright 세션을 생성하고 target_url로 진입한다.

    :return: tuple[Page, BrowserContext, Browser]
    """
    if browser is None:
        browser = playwright.chromium.launch(headless=headless, channel='chrome')
    vp: ViewportSize = {'width': 1600, 'height': 800}
    context = browser.new_context(
        viewport=vp,
        storage_state=storage_state,
        record_video_dir=VIDEO_PATH,
        record_video_size=vp,
        permissions=permissions,
        locale='ko-KR',
        timezone_id='Asia/Seoul',
    )

    # context.tracing.start(screenshots=True, snapshots=True, sources=False)

    page = context.new_page()

    page._console_errors = []
    page._network_errors = []
    page._api_logs = []

    def on_console(msg):
        if msg.type == 'error':
            page._console_errors.append(f'[{msg.type}] {msg.text}')

    def on_request_failed(request):
        page._network_errors.append(f'{request.method} {request.url} - {request.failure}')

    def on_response(response):
        if response.status >= 400:
            page._network_errors.append(f'{response.status} {response.request.method} {response.url}')

        # API 응답 전체 수집 (정적 리소스 제외)
        url = response.url
        content_type = response.headers.get('content-type', '')
        if 'json' in content_type or 'api' in url:
            try:
                body = response.json()
            except Exception:
                body = None
            page._api_logs.append({
                'method': response.request.method,
                'url': url,
                'status': response.status,
                'body': body,
            })

    page.on('console', on_console)
    page.on('requestfailed', on_request_failed)
    page.on('response', on_response)

    page.goto(target_url, wait_until='domcontentloaded')
    page.wait_for_url(target_url)
    page.wait_for_load_state('domcontentloaded')

    return page, context, browser


def playwright_tear_down_base(request, context: BrowserContext, page: Page):
    """tracing 저장, video 첨부, context 정리."""
    try:
        # trace_name = f'{request.node.name.split("[")[0]}_trace.zip'
        # trace_path = f'{TRACE_PATH}/{trace_name}'
        # context.tracing.stop(path=trace_path)

        # with open(trace_path, 'rb') as trace_file:
        #     trace_data = trace_file.read()
        #     allure.attach(
        #         'npx playwright show-trace <ZIP 파일 이름>.zip',
        #         name='Trace 실행방법',
        #         attachment_type=allure.attachment_type.TEXT,
        #     )
        #     allure.attach(trace_data, name=trace_name, attachment_type='application/zip')

        context.close()

        video_path = page.video.path()
        video_name = f'web_{request.node.name}_video.webm'
        with open(video_path, 'rb') as f:
            video_data = f.read()
            allure.attach(video_data, name=video_name, attachment_type=allure.attachment_type.WEBM)

    except Exception as e:
        logger.error(f'[teardown] failed: {e!r}')
