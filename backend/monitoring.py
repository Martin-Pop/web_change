import time, threading
from .downloader import get_page_hash
from .endpoints_dao import EndpointDAO


class EndpointMonitor:

    def __init__(self, ws_client, notify_stat_update):
        self.dao = EndpointDAO()
        self.running = False
        self.ws = ws_client
        self.notify = notify_stat_update

    def start(self):
        threading.Thread(target=self.run, daemon=True).start()

    def add_to_monitor(self, url, interval=60):
        current_time = int(time.time())
        self.dao.insert_endpoint(url, interval, current_time)

    def remove_from_monitor(self, id):
        self.dao.delete_endpoint(id)

    def get_all_endpoints(self):
        return self.dao.get_all_endpoints()

    def update_check_interval(self, page_id, interval):
        self.dao.update_interval(page_id, interval)
        self.dao.reschedule_check(page_id, 0)

    def get_statistics(self, page_id):
        #changes = self.dao.get_changes(page_id)
        return self.dao.get_changes(page_id)

    def process_endpoint(self, page, current_time):
        url = page['url']
        page_id = page['id']
        old_hash = page['hash']
        interval = page['check_interval']

        print(f"Checking {url}...")
        resp = self.ws.send_message(f'checking this url: {url}', 1, 'Info')
        new_hash = get_page_hash(url)
        if new_hash:
            changed = (old_hash and new_hash != old_hash) or old_hash is None
            if changed:
                self.dao.add_change_record(page_id, 1, current_time)
                print(f"!!! CHANGE DETECTED: {url} !!!")
            else:
                self.dao.add_change_record(page_id, 0, current_time)
                print(f"!!! CHANGE NOT DETECTED: {url} !!!")

            self.notify(page_id, {'date': current_time, 'change_detected': changed})

            next_check = current_time + interval
            self.dao.update_check_result(page_id, new_hash, next_check)
        else:
            print(f"Failed to fetch {url}, retrying shortly")
            retry_time = current_time + 60
            self.dao.reschedule_check(page_id, retry_time)

    def run(self):
        self.running = True
        print("Monitor started...")

        while self.running:
            current_time = int(time.time())
            pending_pages = self.dao.get_due_endpoints(current_time)

            for page in pending_pages:
                self.process_endpoint(page, current_time)

            time.sleep(1)

    def stop(self):
        self.running = False