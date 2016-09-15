#!/usr/bin/python
"""Check for invalid data in Metastock database.

Usage:
    mscheck.py <folder>    Check Metastock database located at <folder>

By Carl Christerson, 2016
    https://github.com/carlcnx/mscheck
Based on pyms by David Shipman
    https://github.com/dshipman/pyms

GPL Licensed : Please read the enclosed license in COPYING"""

import sys
import os.path
import pyms

def CheckStock(stock):
	"""Check Metastock stock
	Args:
		stock: Stock to check
	"""
# Read stock data
	close1 = 0
	for bar in stock:
		try:
			date = bar['date']
			open = bar['open']
			high = bar['high']
			low = bar['low']
			close = bar['close']
			volume = bar['volume']
			unadj = bar['unadj']

# Check for OHLC inconsistency
			if open == 0:
				ok = low <= high and low <= close and high >= close
				if not ok:
					print(' {0} {1} Invalid HLC: H={2:.2f} L={3:.2f} C={4:.2f}'.format(stock.symbol, date, high, low, close))
			else:
				ok = low <= open and low <= high and low <= close and high >= open and high >= close
				if not ok:
					print(' {0} {1} Invalid OHLC: O={2:.2f} H={3:.2f} L={4:.2f} C={5:.2f}'.format(stock.symbol, date, open, high, low, close))

# Check for unadjusted splits
			if close1 > 0 and close > close1 and close / close1 > 3:
				print(' {0} {1} Abnormal gain: C={2:.2f} C[1]={3:.2f}'.format(stock.symbol, date, close, close1))
			if close > 0 and close < close1 and close1 / close > 3:
				print(' {0} {1} Abnormal loss: C={2:.2f} C[1]={3:.2f}'.format(stock.symbol, date, close, close1))
			close1 = close

		except Exception as e:
			print('{0} {1}: {2} {3}'.format(stock.symbol, date, type(e).__name__, e))


def CheckDir(msdir):
	"""Check Metastock folder
	Args:
		msdir: Folder to check
	"""
	print('Checking {0}'.format(msdir))

# Check all stocks in directory
	for stock in msdir:
		try:
			if stock != None:
				CheckStock(stock)
		except Exception as e:
			print('{0} {1}: {2}'.format(stock.symbol, type(e).__name__, e))


def main(argv):
	"""Check Metastock folder in specified folder and subfolders
	Args:
		argv: Metastock root folder
	"""
	if argv == None or len(argv) < 2:
		print(__doc__)
		return

	msroot = argv[1]
	if not os.path.isdir(msroot):
		print('Can not find folder: {0}'.format(msroot))
		return

	for folder, subs, files in os.walk(msroot):
		try:
			msdir = pyms.MSDirectory(folder)
			CheckDir(msdir)
		except IOError as e:
			pass
		except Exception as e:
			print('{0}: {1}'.format(type(e).__name__, e))


if __name__ == "__main__":
	main(sys.argv)
