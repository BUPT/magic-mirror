"""
File: lecture_generate_service.py
Author: Duan-JM
Email: vincent.duan95@outlook.com
Github: https://github.com/Duan-JM
Description:
    Test for lecture_generate_service
"""
from .utils import init_logger
from ..service.lecture_generate_service import LectureGenerateService


def record_test(Service, logger):
    """
    test for record
    """
    pass


def video_parse_test(Service, logger):
    """
    test for video_parse_test
    """
    pass


def generate_video_test(Service, logger):
    """
    test for generate_video_test
    """
    pass


def clean_up_test(Service, logger):
    """
    test for clean up test
    """
    pass


def test_whole():
    """
    whole test
    """
    logger = init_logger()

    logger.info("Init Service")
    test_service = LectureGenerateService(
        video_dev='/dev/video0',
        screen_dev='/dev/video1',
        audio_dev='/dev/xxx',
        cache_dir='/tmp/lecutre_cache_file',
        output_dir='./',
        merge_config='./merge_config.json')

    logger.info("Record test")
    record_test(test_service, logger)

    logger.info("Video parse test")
    video_parse_test(test_service, logger)

    logger.info("generate_video test")
    video_parse_test(test_service, logger)

    logger.info("Cleanup test")
    clean_up_test(test_service, logger)
