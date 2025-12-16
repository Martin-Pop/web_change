import time
from .downloader import get_page_hash
from .endpoints_dao import EndpointDAO


class EndpointMonitor:

    def __init__(self):
        self.dao = EndpointDAO()
        self.running = False

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

    def process_endpoint(self, page, current_time):
        url = page['url']
        page_id = page['id']
        old_hash = page['hash']
        interval = page['check_interval']

        print(f"Checking {url}...")

        new_hash = get_page_hash(url)

        if new_hash:
            if old_hash and new_hash != old_hash:
                print(f"!!! CHANGE DETECTED: {url} !!!")
                # notify other

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