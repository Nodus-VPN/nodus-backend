import time
import requests

from internal import model

config_path = "/etc/wireguard/wg3.conf"


async def NewMetricsAgent(
        node_service: model.INodeService
):
    while True:
        ok_responses = []
        failed_responses = []
        package_losses = []
        pings = []
        download_speeds = []
        upload_speeds = []

        nodes_ip = await node_service.nodes_ip()
        for node_ip in nodes_ip:
            config_url = f"http://{node_ip}:7000/wg/client/config/0xBb35CB00d1e54A98b6a44E4F42faBedD43660293"

            response = requests.get(config_url, json={"client_secret_key": "admin"})
            with open(config_path, "wb") as file:
                file.write(response.content)

            # UPTIME
            health = await node_service.health_check(node_ip)
            if health:
                ok_responses.append(1)
                failed_responses.append(0)
            else:
                ok_responses.append(0)
                failed_responses.append(1)

            node_service.connect_to_vpn("wg3")

            package_loss, avg_ping = node_service.check_ping(node_ip)
            package_losses.append(int(package_loss * 100))
            pings.append(int(avg_ping * 100))

            download_speed, upload_speed = node_service.check_speed()
            download_speeds.append(int(download_speed * 100))
            upload_speeds.append(int(upload_speed * 100))

            node_service.disconnect_from_vpn("wg3")

        await node_service.update_node_metrics(
            nodes_ip,
            ok_responses,
            failed_responses,
            package_losses,
            pings,
            download_speeds,
            upload_speeds,
        )
        time.sleep(20)
