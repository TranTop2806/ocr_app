import requests
from dataclasses import dataclass


@dataclass
class Agent:
    ip : str
    username : str
    password : str
    port : int

class Proxies:
    def __init__(self, agents : list[Agent]):
        self.agents = agents
        self.proxies = self.create_proxies()

    def get_proxies(self, idx : int):
        link = self.proxies[idx % len(self.proxies)]
        return {
            "http": link,
            "https": link
        }

    def create_proxy(self, agent : Agent):
        return f"http://{agent.username}:{agent.password}@{agent.ip}:{agent.port}"
    
    def create_proxies(self):
        proxies = []
        for agent in self.agents:
            proxies.append(self.create_proxy(agent))
        return proxies

    def test_proxies(self):
        for agent in self.agents:
            proxy = self.create_proxy(agent)
            try:
                response = requests.get("http://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5)
                if response.ok:
                    print(f"Proxy {proxy} is working. Your IP: {response.json()['origin']}")
                else:
                    print(f"Proxy {proxy} returned status code {response.status_code}")
            except Exception as e:
                print(f"Error occurred while testing proxy {proxy}: {e}")
            
if __name__ == "__main__":

    agents = [
        Agent(ip='198.23.239.134', port=6540, username='qqxnuqlx', password='h4eapuuligg9'),
        Agent(ip='207.244.217.165', port=6712, username='qqxnuqlx', password='h4eapuuligg9'),
        Agent(ip='107.172.163.27', port=6543, username='qqxnuqlx', password='h4eapuuligg9'),
        Agent(ip='64.137.42.112', port=5157, username='qqxnuqlx', password='h4eapuuligg9'),
        Agent(ip='173.211.0.148', port=6641, username='qqxnuqlx', password='h4eapuuligg9'),
        Agent(ip='161.123.152.115', port=6360, username='qqxnuqlx', password='h4eapuuligg9'),
        Agent(ip='167.160.180.203', port=6754, username='qqxnuqlx', password='h4eapuuligg9'),
        Agent(ip='154.36.110.199', port=6853, username='qqxnuqlx', password='h4eapuuligg9'),
        Agent(ip='173.0.9.70', port=5653, username='qqxnuqlx', password='h4eapuuligg9'),
        Agent(ip='173.0.9.209', port=5792, username='qqxnuqlx', password='h4eapuuligg9')
    ]

    proxies = Proxies(agents)
    proxies.test_proxies()

    print(proxies.get_proxies(0))


