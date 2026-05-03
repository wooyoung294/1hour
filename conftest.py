import glob
import os
import platform
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from playwright.sync_api import Playwright
import pytest

from common.env_parser import load_env_vars
from common.make_pytest_conf import playwright_config_base, playwright_tear_down_base
from common.step_context import clear_current_step, set_current_step
from pages.login_page import LoginPage

HEADLESS = False
PAGE_URL = None

pytest_plugins = [
    f'steps.{Path(f).stem}'
    for f in glob.glob('steps/*.py')
    if not f.endswith('__init__.py')
]


def pytest_addoption(parser):
    parser.addoption('--env', action='store', default='qa', help='Target environment (e.g. qa, stage)')


def pytest_configure(config):
    env = config.getoption('--env')
    os.environ['ENV'] = env

    env_file = Path(f'.env.{env}')
    if env_file.exists():
        load_dotenv(env_file, verbose=True, override=True)
    else:
        load_dotenv(verbose=True)

    global PAGE_URL
    PAGE_URL = os.getenv('PAGE_URL')

    config._env_vars = load_env_vars(env)


@pytest.fixture(scope='session')
def env_name(request):
    return request.config.getoption('--env')


@pytest.fixture(scope='session')
def env_vars(request):
    return request.config._env_vars


@pytest.fixture(scope='session')
def worker_id(request):
    if hasattr(request.config, 'workerinput'):
        return request.config.workerinput['workerid']
    return 'master'


@pytest.fixture(scope='session')
def browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=HEADLESS, channel='chrome')
    yield browser
    browser.close()


@pytest.fixture
def data_store():
    return {}


@pytest.fixture(scope='session')
def web_session_driver(playwright: Playwright, worker_id):
    cookie_path = f'cookie_{worker_id}.json'

    browser = playwright.chromium.launch(headless=HEADLESS, channel='chrome')
    context = browser.new_context(locale='ko-KR', timezone_id='Asia/Seoul')
    page = context.new_page()

    page.goto(PAGE_URL, wait_until='domcontentloaded')
    login_page = LoginPage(page)
    login_page.fill_id_from_env()
    login_page.fill_password_from_env()
    login_page.click_login_btn()
    page.wait_for_url(lambda url: '/login' not in url, timeout=30000)

    context.storage_state(path=cookie_path)
    context.close()
    browser.close()
    return cookie_path


@pytest.fixture
def web_function_driver(browser, playwright: Playwright, request, web_session_driver, data_store):
    no_cookie = request.node.get_closest_marker('no_cookie')
    storage = None if no_cookie else web_session_driver

    request.node._rp_teardown_done = False

    page, context, browser = playwright_config_base(playwright, PAGE_URL, browser, storage, headless=HEADLESS)
    request.node._rp_page = page
    request.node._rp_context = context

    def capture_auth_token(req):
        if 'api-v1-b.1hour.ai' in req.url:
            auth = req.headers.get('authorization')
            if auth:
                data_store['auth_token'] = auth

    def capture_lesson_response(response):
        if 'api-v1-b.1hour.ai/video/video/' in response.url and response.request.method == 'POST':
            try:
                data = response.json()
                if data.get('id'):
                    data_store['lesson_id'] = data['id']
                    logger.info(f'lessonId 캡처됨: {data["id"]}')
            except Exception:
                pass

    page.on('request', capture_auth_token)
    page.on('response', capture_lesson_response)

    try:
        yield page
    finally:
        if not getattr(request.node, '_rp_teardown_done', False):
            playwright_tear_down_base(request, context, page)
            request.node._rp_teardown_done = True


def pytest_bdd_before_step(request, feature, scenario, step, step_func):
    set_current_step(f'{step.keyword} {step.name}', step_func)


def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    clear_current_step()


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    logger.error(f'Scenario: {scenario.name}')
    logger.error(f'Feature: {feature.name}')


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    import allure

    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        page = item.funcargs.get('web_function_driver')
        if not page:
            return

        console_errors = getattr(page, '_console_errors', [])
        if console_errors:
            allure.attach('\n'.join(console_errors), name='Console Errors', attachment_type=allure.attachment_type.TEXT)

        network_errors = getattr(page, '_network_errors', [])
        if network_errors:
            allure.attach('\n'.join(network_errors), name='Network Errors', attachment_type=allure.attachment_type.TEXT)


def pytest_collection_modifyitems(items):
    for item in items:
        if item.get_closest_marker('gw0'):
            item.add_marker(pytest.mark.xdist_group(name='gw0_group'))


def pytest_sessionfinish():
    os.makedirs('allure-results', exist_ok=True)
    with open('allure-results/environment.properties', 'w', encoding='utf-8') as f:
        f.write(f'OS={platform.platform()}\n')
        f.write(f'ENV={os.getenv("ENV", "PROD")}\n')
