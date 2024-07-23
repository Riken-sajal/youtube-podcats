from feedgen.feed import FeedGenerator

def create_rss_feed(audio_files, base_url):
    fg = FeedGenerator()
    fg.load_extension('podcast')

    fg.title('YouTube Audio Feed')
    fg.link(href=base_url, rel='self')
    fg.description('A feed of audio files downloaded from YouTube')
    fg.language('en')

    for audio_file in audio_files:
        fe = fg.add_entry()
        fe.id(base_url + audio_file.file.url)
        fe.title(audio_file.title)
        fe.description(f'Audio file: {audio_file.title}')
        fe.enclosure(base_url + audio_file.file.url, 0, 'audio/mpeg')
        fe.pubDate(audio_file.uploaded_at)
        fe.link(href=base_url + audio_file.file.url)

    fg.podcast.itunes_category('Technology', 'Podcasting')
    fg.podcast.itunes_image(base_url + '/path/to/your/podcast/image.jpg')
    fg.podcast.itunes_summary('A summary of your podcast.')
    fg.podcast.itunes_author('Your Name')
    fg.podcast.itunes_explicit('no')

    return fg.rss_str(pretty=True)
