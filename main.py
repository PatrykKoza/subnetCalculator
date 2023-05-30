import ipcalc
import yaml
import logging

config_file = "config.yaml"

# Logging configuration
logging.basicConfig(
    level=logging.DEBUG,  # Ustawienie poziomu logowania na DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format wiadomości logowania
    filename='app.logs',  # Nazwa pliku, do którego zapisywane są logi
    filemode='a'  # Tryb zapisu logów (w - zastępowanie pliku, a - dopisywanie do pliku)
)


class NetworkCalculator:
    def __init__(self, network):
        self.network = network
        self.subnets = set()

    def addSubnet(self, subnet):
        if ipcalc.Network(subnet) in ipcalc.Network(self.network):
            self.subnets.add(subnet)
            return True
        else:
            return False

    def ipInSubnet(self, ip_address):
        ip = ipcalc.IP(ip_address)
        if ip in ipcalc.Network(self.network):
            for subnet in self.subnets:
                if ip in ipcalc.Network(subnet):
                    return subnet  # IP in subnet
                else:
                    return True  # IP in network
        else:
            return False  # IP not in network+

    def getNetwork(self):
        return self.network

    def __repr__(self):
        return f"Network: {self.network}\nSubnets: {self.subnets}"


if __name__ == '__main__':

    toCalculate = set()

    # Load networks $ subnets
    with open(f'{config_file}', 'r', ) as f:
        config = yaml.safe_load(f)
        networks = set(config['networks'].split())
        subnets = set(config['subnets'].split())

        print(networks)

        print(subnets)

        for network in networks:
            toCalculate.add(NetworkCalculator(network))

        for subnet in subnets:
            for c in toCalculate:
                if not c.addSubnet(subnet):
                    logging.debug(f"Subnet {subnet} not in network {c.getNetwork()}")

    for t in toCalculate:
        print(t)
