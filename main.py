from pysui import SyncClient, SuiConfig, handle_result, ObjectID, SuiAddress
from pysui.abstracts import SignatureScheme
from pysui.sui.sui_txn import SyncTransaction

from utils import logger
from utils.file_manager import str_to_file


def file_to_list(
        filename: str
):
    with open(filename, 'r+') as f:
        return list(filter(bool, f.read().splitlines()))


def send_tx(private_key: str):
    txer = SyncTransaction(client=SyncClient(SuiConfig.user_config(
        rpc_url="https://suifrens-rpc.mainnet.sui.io/",
        prv_keys=[
            {
                'wallet_key': private_key,
                'key_scheme': SignatureScheme.ED25519
            }
        ]
    )))

    txer.move_call(
        target="0x03e88d43a310633152deef7d164dd4273eb2ce8b0ffc0d1ff597ab49fd88908d::quest::mint",
        arguments=[
            ObjectID("0x109bf36609bef3f02452445d34f515a5e8a7bc6e4cb6336cbdd9be83ae62b1c3"),
            SuiAddress("0x01baaf89af9309444d63d6fbb4faba8bf5232e5286a92ddb22e899027f90b13b"),
            ObjectID("0x0000000000000000000000000000000000000000000000000000000000000006"),
        ]
    )

    exec_result = handle_result(txer.execute(gas_budget="10000000"))

    logger.debug(f"Result: {exec_result.to_json()}")


def main():
    print("Main <crypto/> moves: https://t.me/+tdC-PXRzhnczNDli\n")

    keys = file_to_list("keys.txt")

    for key in keys:
        try:
            send_tx(key)
            logger.info(f"Sent tx for: {key}")
        except Exception as e:
            logger.error(e)
            str_to_file("logs/error.txt", key)

    logger.info("Done")


if __name__ == "__main__":
    main()
