from argparse import Namespace
from locust import runners
import locustfile


options = Namespace()
options.host = "http://localhost:8000"
options.num_clients = 50
options.reset_stats = False
options.hatch_rate = options.num_clients
options.num_requests = options.num_clients * 20


runners.locust_runner = runners.LocalLocustRunner([locustfile.WebsiteUser], options=options)
runners.locust_runner.start_hatching(locust_count=10, hatch_rate=2)
runners.locust_runner.greenlet.join()

for name, value in runners.locust_runner.stats.entries.items():
    print(name, value.__dict__)


