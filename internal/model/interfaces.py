from abc import abstractmethod
from typing import Protocol, Any, Sequence

from internal.model import model


class INodeService(Protocol):
    # INSERT
    @abstractmethod
    async def nodes_ip(self) -> list[str]: pass

    @abstractmethod
    async def health_check(self, node_ip: str) -> int: pass

    @abstractmethod
    def connect_to_vpn(self, config_path: str): pass

    @abstractmethod
    def disconnect_from_vpn(self, config_path: str): pass

    @abstractmethod
    def check_speed(self) -> tuple[float, float]: pass

    @abstractmethod
    def check_ping(self, host) -> tuple[float, float]: pass

    @abstractmethod
    async def update_node_metrics(
            self,
            nodes_ip: list[str],
            ok_responses: list[int],
            failed_responses: list[int],
            package_losses: list[int],
            pings: list[int],
            download_speeds: list[int],
            upload_speeds: list[int]
    ): pass

    @abstractmethod
    async def delete_client_config(self, node_ip: str, client_address: str): pass


class IClientService(Protocol):
    @abstractmethod
    async def all_client_address(self) -> list[str]: pass

    @abstractmethod
    async def get_client(self, client_address: str) -> model.Client: pass


class IContractVPN(Protocol):
    @abstractmethod
    async def nodes_ip(self) -> list[str]: pass

    @abstractmethod
    async def update_node_metrics(
            self,
            nodes_ip: list[str],
            ok_responses: list[int],
            failed_responses: list[int],
            package_losses: list[int],
            pings: list[int],
            download_speeds: list[int],
            upload_speeds: list[int]
    ): pass

    @abstractmethod
    async def all_client_address(self) -> list[str]: pass

    @abstractmethod
    async def get_client(self, client_address: str) -> model.Client: pass


class DBInterface(Protocol):
    @abstractmethod
    async def insert(self, query: str, query_params: dict) -> int: pass

    @abstractmethod
    async def delete(self, query: str, query_params: dict) -> None: pass

    @abstractmethod
    async def update(self, query: str, query_params: dict) -> None: pass

    @abstractmethod
    async def select(self, query: str, query_params: dict) -> Sequence[Any]: pass

    @abstractmethod
    async def multi_query(self, queries: list[str]) -> None: pass


class INodeClient(Protocol):
    @abstractmethod
    async def health_check(self, node_ip: str): pass

    @abstractmethod
    async def delete_client_config(self, node_ip: str, client_address: str): pass
