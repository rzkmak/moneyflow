# Sanitized Sample Files

This directory contains sanitized sample CSV files for testing purposes. These files use mock data and do not contain any real personal or financial information.

## Files

### paypay-sample.csv
- Format: UTF-8 encoded
- Source structure: PayPay Balance export format
- Contains: 10 mock transactions with various payment and top-up scenarios
- Purpose: Testing PayPay parser functionality

### smbc-sample.csv
- Format: Shift-JIS (CP932) encoded
- Source structure: SMBC Credit Card export format
- Contains: 4 mock transactions with Japanese merchant names
- Purpose: Testing SMBC parser with Japanese encoding support

## Usage

These files can be used to test the CSV import functionality without using real personal financial data.

## Original Data

The original sample files containing real transaction data are not included in the repository for privacy reasons. See:
- `sample-input-paypay/` - Contains real PayPay transactions (not committed)
- `sample-input-smbc/` - Contains real SMBC transactions (not committed)

The sanitized versions maintain the same CSV structure and data format while using completely fictional data.