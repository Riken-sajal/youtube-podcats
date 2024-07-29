from feedgen.feed import FeedGenerator
import os
from mutagen.mp3 import MP3
import datetime

def create_rss_feed(audio_files, base_url):
    
    fg = FeedGenerator()
    fg.load_extension('podcast')
    
    fg.title('YouTube Audio Feed')
    fg.description('A feed of audio files downloaded from YouTube')
    fg.language('en')
    fg.podcast.itunes_category('Technology', 'Podcasting')
    fg.podcast.itunes_explicit('no')
    
    fg.link(href=base_url, rel='self')

    fg.podcast.itunes_author('Your Name')
    fg.podcast.itunes_image(base_url +'/'+ os.path.join('media','cover_imgs',"csvvc.jpg"))
    fg.podcast.itunes_summary('A summary of your podcast.')
    fg.podcast.itunes_subtitle('Your podcast subtitle')
    fg.podcast.itunes_owner(name='Riken', email='Riken@sajaltech.com')
    fg.podcast.itunes_new_feed_url(base_url + '/podcast/rss-feed/')
    fg.podcast.itunes_new_feed_url(base_url + '/podcast/rss-feed/')
    for audio_file in audio_files:
        audio_file_path = base_url + '/' +audio_file.media_path
        fe = fg.add_entry()
        breakpoint()
        
        fe.link(href=audio_file_path)
        fe.title(audio_file.title)
        fe.description(audio_file.description)
        fe.enclosure(url=base_url + audio_file.file.url,length=audio_file.length_in_seconds,type="audio/mpeg")
        audio = MP3(audio_file.file.path)
        duration_in_seconds = int(audio.info.length)
        duration_str = str(datetime.timedelta(seconds=duration_in_seconds))
        fe.podcast.itunes_duration(duration_str)
        fe.pubDate(audio_file.uploaded_at.strftime("%a, %d %b %Y %H:%M:%S %z"))
        fe.podcast.itunes_image(base_url +'/'+ os.path.join('media','cover_imgs',"csvvc.jpg"))
        
        
        
    rss_feed_content = fg.rss_str(pretty=True)
    return rss_feed_content
