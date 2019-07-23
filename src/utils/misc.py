import mimetypes
import os

from django.utils.text import slugify
from django.conf import settings
from django.http import Http404, FileResponse

def create_slug(model_cls, instance=None, attribute=None, text=None, new_slug=None):
    """Creates a slug for the instance of model_cls out of either attribute (if not None),
    otherwise out of text"""

    if new_slug is not None:
        slug = new_slug
    else:
        if attribute is None:
            if text is None:
                raise Exception('create_slug: need to either pass attribute or text')
            attr = text
        else:
            # if instance is None: raise..
            attr = getattr(instance, attribute)
        slug = slugify(attr)
    qs = model_cls.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(model_cls, instance, attribute=attribute, text=text, new_slug=new_slug)
    return slug


def chunks(list_, chunk_size):
    # if chunk_size < 1 ... raise
    return [list_[i:i+chunk_size] for i in range(0, len(list_), chunk_size)]




# def check_for_media_file(media_path):
#     print('base_dir ', settings.BASE_DIR)
#     print('media_root', settings.MEDIA_ROOT)
#     print('media_path ', media_path)
#     fpath = os.path.join(settings.BASE_DIR, media_path)
#     print('check for media file with media path: ', fpath)
#     print('found: ', os.path.isfile(fpath))
#     return os.path.isfile(fpath)
    # try:
    #     fpath = os.path.join(settings.MEDIA_ROOT, media_path)
    #     print('check for media file with media path: ', media_path)
    #     #mimetype = mimetypes.guess_type(fpath)

    #     return True
    #     #return FileResponse(open(fpath, 'rb'), content_type=mimetype)
    # except: #IOError or FileNotFoundError
    #     return False