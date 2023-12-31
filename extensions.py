from maltego_trx.decorator_registry import TransformRegistry, TransformSet

registry = TransformRegistry(
    owner="HawkEyes",
    author="Hawk Dev",
    host_url="https://hawk-eyes.com",
    version="0.1.0",
    seed_ids=["demo"]
)

WalletExplorer_set = TransformSet("WalletExplorer", "WalletExplorer Transforms")
