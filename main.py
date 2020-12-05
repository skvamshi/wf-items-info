import time
import logging
import sys
from detect_text import process_image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            path_string = str(event.src_path)
            event_file_name = path_string[path_string.rfind('\\') + 1:]
            if event_file_name.startswith('Warframe'):
                result_json = process_image(path_string)
                print(f'event type: {event.event_type}  path : {event.src_path} result: {result_json}')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
