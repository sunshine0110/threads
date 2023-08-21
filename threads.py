import threading
import requests
import time

user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
)

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1

    def get_value(self):
        with self.lock:
            return self.value

def fetch_url(url, duration, stop_event, success_counter, failure_counter):
    start_time = time.time()
    
    while not stop_event.is_set() and time.time() - start_time < duration:
        try:
            headers = {
                'User-Agent': user_agent,
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.google.com/',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                success_counter.increment()
            else:
                failure_counter.increment()
        except requests.RequestException as e:
            failure_counter.increment()
            pass
        
        time.sleep(1)  # Tunggu 1 detik sebelum permintaan berikutnya

def main(url, num_threads, duration):
    stop_event = threading.Event()
    success_counter = Counter()
    failure_counter = Counter()
    thread_list = []
    
    for i in range(num_threads):
        thread = threading.Thread(target=fetch_url, args=(url, duration, stop_event, success_counter, failure_counter), name=f"Thread-{i}")
        thread_list.append(thread)
        thread.start()

    time.sleep(duration)
    stop_event.set()
    
    for thread in thread_list:
        thread.join()

    print("Total Successful Requests:", success_counter.get_value())
    print("Total Failed Requests:", failure_counter.get_value())

if __name__ == "__main__":
    url = input("Masukkan URL: ")
    num_threads = int(input("Masukkan jumlah thread: "))
    duration = int(input("Masukkan durasi maksimum (dalam detik): "))

    main(url, num_threads, duration)
