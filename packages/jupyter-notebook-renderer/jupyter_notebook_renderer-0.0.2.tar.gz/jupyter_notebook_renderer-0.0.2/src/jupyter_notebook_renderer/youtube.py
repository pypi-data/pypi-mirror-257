from IPython.display import display, HTML
from ensure import ensure_annotations
from jupyter_notebook_renderer.custom_exception import InvalidURLException
from jupyter_notebook_renderer.logger import logger
from py_youtube import Data


@ensure_annotations
def get_time_info(url: str) -> int:
    def _verify_vid_id_len(vid_id, _expected_len=11):
        vid_id_len = len(vid_id)
        if vid_id_len != _expected_len:
            raise InvalidURLException(
                f"Invalid video id with length :{vid_id_len}, expected: {_expected_len}"
            )

    try:
        split_val = url.split("=")
        if len(split_val) >= 4:
            raise InvalidURLException
        if "watch" in url:
            if "&t" in url:
                vid_id, time = split_val[-2][:-2], int(split_val[-1][:-1])
                _verify_vid_id_len(vid_id)
                logger.info(f"video starts at {time}")
                return time
            else:
                vid_id, time = split_val[-1], 0
                _verify_vid_id_len(vid_id)
                logger.info(f"video starts at {time}")
                return time
        else:
            if "=" in url and "&t" in url:
                vid_id, time = split_val[0].split("/")[-1].split("?")[0], int(
                    split_val[-1]
                )

                _verify_vid_id_len(vid_id)
                logger.info(f"video starts at {time}")
                return time
            else:
                vid_id, time = url.split("/")[-1].split("?")[0], 0
                _verify_vid_id_len(vid_id)
                logger.info(f"video starts at {time}")
                return time
    except Exception:
        raise InvalidURLException


@ensure_annotations
def render_youtube_video(url: str, width: int = 780, height: int = 600) -> str:
    try:
        if url is None:
            raise InvalidURLException("URL can not be empty")
        data = Data(url).data()
        if data["publishdate"] is not None:
            time = get_time_info(url)
            vid_ID = data["id"]
            embeded_url = f"https://www.youtube.com/embed/{vid_ID}?start={time}"
            logger.info(f"embed url : {embeded_url}")

            iframe = f"""<iframe
            width="{width}" height="{height}"
            src="{embeded_url}"
            title="YouTube video player"
            frameborder="0"
            allow="accelerometer;
            autoplay; clipboard-write;
            encrypted-media; gyroscope;
            picture-in-picture; web-share" allowfullscreen>
            </iframe>
            """
            display(HTML(iframe))
            return "success"
        else:
            raise InvalidURLException
    except Exception as e:
        raise e
