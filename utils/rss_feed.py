from feedgen.feed import FeedGenerator
import os


def create_rss_feed(audio_files, base_url):
    fg = FeedGenerator()
    fg.load_extension('podcast')

    fg.title('YouTube Audio Feed')
    fg.link(href=base_url, rel='self')
    fg.description('A feed of audio files downloaded from YouTube')
    fg.language('en')

    fg.podcast.itunes_author('Your Name')
    fg.podcast.itunes_category('Technology', 'Podcasting')
    fg.podcast.itunes_image(base_url + '/path/to/your/podcast/image.jpg')
    fg.podcast.itunes_summary('A summary of your podcast.')
    fg.podcast.itunes_explicit('no')
    fg.podcast.itunes_subtitle('Your podcast subtitle')
    fg.podcast.itunes_owner(name='Your Name', email='your.email@example.com')
    fg.podcast.itunes_new_feed_url(base_url + '/podcast/rss-feed/')

    for audio_file in audio_files:
        fe = fg.add_entry()
        fe.id(base_url + audio_file.file.url)
        fe.title(audio_file.title)
        fe.description(audio_file.description)
        audio_file_path = base_url + audio_file.file.url
        file_size = os.path.getsize(audio_file.file.path)
        fe.enclosure(audio_file_path, str(file_size), 'audio/mpeg')
        fe.pubDate(audio_file.uploaded_at.strftime("%a, %d %b %Y %H:%M:%S %z"))
        fe.link(href=audio_file_path)
        fe.guid(base_url + audio_file.file.url, permalink=False)

    rss_feed_content = fg.rss_str(pretty=True)
    return rss_feed_content
