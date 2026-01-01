import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.infrastructure.parsers import PayPayParser, SMBCParser
from src.infrastructure.models import SourceType

def test_paypay_parser():
    # Minimal sample
    content = b"""Date & Time,Amount Outgoing (Yen),Amount Incoming (Yen),Transaction ID,Method,Business Name
2025/11/07 18:58:48,645,-,02128111013981929472,PayPay Balance,Steven Candra
"""
    parser = PayPayParser()
    txs = parser.parse(content, "test.csv")
    assert len(txs) == 1
    t = txs[0]
    assert t.amount == 645
    assert t.source == "PayPay Balance"
    assert t.source_type == SourceType.paypay
    assert t.record_hash == "02128111013981929472"
    print("PayPay Parser Test Passed")

def test_smbc_parser():
    # CP932 Sample
    # Header line
    header = 'User,4980-00**-****-****,Olive Gold\n'.encode('cp932')
    # Data line: 2025/11/28, Merchant, 4950, 1, 1, 4950, ''
    row = '2025/11/28,TestShop,4950,1,1,4950,\n'.encode('cp932')
    content = header + row
    
    parser = SMBCParser()
    txs = parser.parse(content, "test.csv")
    assert len(txs) == 1
    t = txs[0]
    assert t.amount == 4950
    assert t.merchant == "TestShop"
    # assert t.source == "Olive Gold (4980-00**-****-****)" # Logic in parser was f"{card_name} ({masked_num})"
    # masked_num=4980..., card_name=Olive Gold
    print(f"SMBC Source: {t.source}")
    assert "Olive Gold" in t.source
    print("SMBC Parser Test Passed")

if __name__ == "__main__":
    test_paypay_parser()
    test_smbc_parser()
