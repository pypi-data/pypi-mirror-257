# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
import requests, json, os
from xyz_util.crawlutils import extract_between
from xyz_util.datautils import dict2str, access
from django.conf import settings
import logging

log = logging.getLogger('django')
from instaloader.instaloader import *

PICTURE_SAVE_DIR = os.environ.get('INSTAGRAM_PICTURE_SAVE_DIR', settings.MEDIA_ROOT)


class MyLoader(Instaloader):
    on_pic_downloaded = None
    catch_url = None

    def download_pic(self, filename: str, url: str, mtime: datetime,
                     filename_suffix: Optional[str] = None, _attempt: int = 1) -> bool:
        if callable(self.catch_url):
            self.catch_url(url)

        rs = super(MyLoader, self).download_pic(filename, url, mtime, filename_suffix=filename_suffix,
                                                _attempt=_attempt)
        if callable(self.on_pic_downloaded):
            self.on_pic_downloaded(filename + '_' + filename_suffix + '.jpg')
            return rs
        return True


def search_user_post_pictures(username, dir=PICTURE_SAVE_DIR, options={}, **kwargs):
    loader = MyLoader(
        quiet=True,
        dirname_pattern=f'{dir}/{{target}}',
        post_metadata_txt_pattern='',
        storyitem_metadata_txt_pattern='',
        iphone_support=False,
        save_metadata=False,
        compress_json=False,
        download_videos=False,
        **options
    )
    rs = []
    print(username)
    loader.catch_url = rs.append
    from instaloader.__main__ import _main
    _main(loader, [username], download_profile_pic=False, download_posts=False, **kwargs)
    return rs
