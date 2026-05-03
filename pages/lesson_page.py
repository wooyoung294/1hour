import time

from loguru import logger

from common.base import Base


class LessonPage(Base):
    DELETE_URL = 'https://api-v1-b.1hour.ai/video/editvideo/{id}/'
    CONTENT_STATE_URL = 'https://api-v1-b.1hour.ai/video/{id}/content_state/'

    def verify_video_title(self, title: str):
        self.expect_visible(self.page.get_by_text(title).first)

    def wait_for_class_finished(self, lesson_id, auth_token: str, timeout: int = 120, interval: int = 2):
        assert lesson_id, 'lessonId 없음'

        url = self.CONTENT_STATE_URL.format(id=lesson_id)
        headers = {'Authorization': auth_token} if auth_token else {}

        deadline = time.time() + timeout
        last_code = None
        while time.time() < deadline:
            response = self.page.context.request.patch(url, headers=headers)
            if response.ok:
                data = response.json()
                last_code = data.get('data', {}).get('status', {}).get('code')
                if last_code == 'FINISHED':
                    logger.info(f'수업 생성 완료: {lesson_id}')
                    return
            time.sleep(interval)

        raise TimeoutError(f'수업 생성 완료 대기 타임아웃 ({timeout}s) - lessonId={lesson_id}, last_code={last_code}')

    def delete_lesson(self, lesson_id, auth_token: str):
        if not lesson_id:
            logger.info('lessonId 없음 - 스킵')
            return

        url = self.DELETE_URL.format(id=lesson_id)
        headers = {'Authorization': auth_token} if auth_token else {}
        response = self.page.context.request.delete(url, headers=headers)
        assert response.ok, f'수업 삭제 실패: {response.status}'
        logger.info(f'수업 삭제 완료: {lesson_id}')
