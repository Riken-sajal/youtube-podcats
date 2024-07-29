from feedgen.feed import FeedGenerator
import os
from mutagen.mp3 import MP3
import datetime


def create_rss_feed(audio_files, base_url):
    fg = FeedGenerator()

    # Add the necessary namespaces
    fg.rss_str(pretty=True)
    fg.load_extension('podcast')
    fg.load_extension('atom')
    fg.load_extension('content')

    fg.title('YouTube Audio Feed')
    fg.link(href=base_url, rel='self')
    fg.description('A feed of audio files downloaded from YouTube')
    fg.language('en')
    fg.podcast.itunes_category('Technology', 'Podcasting')
    fg.podcast.itunes_explicit('no')

    fg.podcast.itunes_author('Your Name')
    fg.podcast.itunes_image(base_url + '/media/cover_imgs/csvvc.jpg')
    fg.podcast.itunes_summary('A summary of your podcast.')
    fg.podcast.itunes_subtitle('Your podcast subtitle')
    fg.podcast.itunes_owner(name='Riken', email='Riken@sajaltech.com')
    fg.podcast.itunes_new_feed_url(base_url + '/podcast/rss-feed/')

    for audio_file in audio_files:
        audio_file_path = base_url + '/' + audio_file.media_path
        fe = fg.add_entry()

        fe.link(href=audio_file_path)
        fe.title(audio_file.title)
        fe.description(audio_file.description)

        # Ensure URL has a valid file extension
        file_url_with_extension = audio_file_path if audio_file_path.endswith('.mp3') else audio_file_path + '.mp3'

        fe.enclosure(url=file_url_with_extension, length=str(os.path.getsize(audio_file.file.path)), type="audio/mpeg")

        audio = MP3(audio_file.file.path)
        duration_in_seconds = int(audio.info.length)
        duration_str = str(datetime.timedelta(seconds=duration_in_seconds))

        fe.podcast.itunes_duration(duration_str)
        fe.pubDate(audio_file.uploaded_at.strftime("%a, %d %b %Y %H:%M:%S %z"))
        fe.podcast.itunes_image(base_url + '/media/cover_imgs/csvvc.jpg')

    rss_feed_content = fg.rss_str(pretty=True)
    return rss_feed_content
