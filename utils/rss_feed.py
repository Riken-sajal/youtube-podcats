from feedgen.feed import FeedGenerator
import os
from mutagen.mp3 import MP3
import datetime
import urllib.parse


def create_rss_feed(audio_files, base_url):
    fg = FeedGenerator()

    # Set required channel elements first
    fg.title('YouTube Audio Feed')
    fg.link(href=base_url, rel='self')
    fg.description('A feed of audio files downloaded from YouTube')
    fg.language('en')

    # Load the podcast extension
    fg.load_extension('podcast')

    # Add iTunes specific tags
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
        encoded_audio_file_path = urllib.parse.quote(audio_file_path, safe=':/')

        fe = fg.add_entry()
        fe.guid(encoded_audio_file_path)
        fe.link(href=encoded_audio_file_path)
        fe.title(audio_file.title)
        fe.description(audio_file.description)

        # Ensure URL has a valid file extension
        file_url_with_extension = encoded_audio_file_path if encoded_audio_file_path.endswith(
            '.mp3') else encoded_audio_file_path + '.mp3'

        fe.enclosure(url=file_url_with_extension, length=str(os.path.getsize(audio_file.file.path)), type="audio/mpeg")

        audio = MP3(audio_file.file.path)
        duration_in_seconds = int(audio.info.length)
        duration_str = str(datetime.timedelta(seconds=duration_in_seconds))

        fe.podcast.itunes_duration(duration_str)
        fe.pubDate(audio_file.uploaded_at.strftime("%a, %d %b %Y %H:%M:%S %z"))
        fe.podcast.itunes_image(base_url + '/media/cover_imgs/csvvc.jpg')

    rss_feed_content = fg.rss_str(pretty=True)
    return rss_feed_content
