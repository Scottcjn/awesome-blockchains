import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_blockchain_module():
    spec = importlib.util.spec_from_file_location(
        "basic_blockchain",
        ROOT / "blockchain.py" / "blockchain.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_first_block_uses_genesis_defaults():
    module = load_blockchain_module()

    block = module.Block.first()

    assert block.index == 0
    assert block.data == "Genesis"
    assert block.previous_hash == "0"
    assert len(block.hash) == 64


def test_first_block_accepts_custom_genesis_data():
    module = load_blockchain_module()

    block = module.Block.first("Custom genesis")

    assert block.index == 0
    assert block.data == "Custom genesis"
    assert block.previous_hash == "0"


def test_next_block_links_to_previous_hash():
    module = load_blockchain_module()
    first = module.Block.first("Root")

    second = module.Block.next(first, "Transfer")

    assert second.index == first.index + 1
    assert second.data == "Transfer"
    assert second.previous_hash == first.hash
    assert second.hash != first.hash


def test_hash_changes_when_block_data_changes():
    module = load_blockchain_module()

    first = module.Block(1, "payload-a", "previous")
    second = module.Block(1, "payload-b", "previous")

    assert first.hash != second.hash


def test_sample_chain_preserves_order_and_links():
    module = load_blockchain_module()

    chain = module.build_sample_chain()

    assert [block.index for block in chain] == [0, 1, 2, 3]
    assert chain[0].previous_hash == "0"
    assert all(chain[i].previous_hash == chain[i - 1].hash for i in range(1, len(chain)))
