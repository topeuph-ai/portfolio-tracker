#!/usr/bin/env python3
"""
🤖 AUTONOMOUS PORTFOLIO TRACKER
Runs daily at 4:05 PM EST via GitHub Actions
Tracks 5 competing portfolios with real-time market data
"""

import yfinance as yf
import json
import datetime
import os
from pathlib import Path

# Portfolio data file
DATA_FILE = 'portfolio_data.json'

# Initialize portfolios
def initialize_portfolios():
    """Initialize or load portfolio data"""
    
    # Your actual TradingView positions
    portfolios = {
        'ceri': {
            'name': 'CERI (Buy & Hold)',
            'emoji': '👤',
            'initial': 100000,
            'startDate': '2026-01-03',
            'strategy': 'Quarterly rebalance only',
            'holdings': [
                {'ticker': 'AVGO', 'entry': 346.35, 'shares': 28.86},
                {'ticker': 'NVDA', 'entry': 185.89, 'shares': 53.8},
                {'ticker': 'WMT', 'entry': 114.94, 'shares': 87},
                {'ticker': 'IBKR', 'entry': 70.21, 'shares': 142.4},
                {'ticker': 'ORCL', 'entry': 199.78, 'shares': 50.04},
                {'ticker': 'UNH', 'entry': 345.57, 'shares': 28.93},
                {'ticker': 'NEM', 'entry': 108.58, 'shares': 92.08},
                {'ticker': 'TGT', 'entry': 105.30, 'shares': 94.95},
                {'ticker': 'PYPL', 'entry': 57.50, 'shares': 173.94},
                {'ticker': 'MO', 'entry': 57.38, 'shares': 174.27}
            ]
        },
        'assisted': {
            'name': 'AI-Assisted',
            'emoji': '💡',
            'initial': 100000,
            'startDate': '2026-01-10',
            'strategy': 'Claude recommends, you decide',
            'holdings': [
                {'ticker': 'AVGO', 'entry': 346.35, 'shares': 28.86},
                {'ticker': 'NVDA', 'entry': 185.89, 'shares': 53.8},
                {'ticker': 'WMT', 'entry': 114.94, 'shares': 87},
                {'ticker': 'IBKR', 'entry': 70.21, 'shares': 142.4},
                {'ticker': 'ORCL', 'entry': 199.78, 'shares': 50.04},
                {'ticker': 'UNH', 'entry': 345.57, 'shares': 28.93},
                {'ticker': 'NEM', 'entry': 108.58, 'shares': 92.08},
                {'ticker': 'TGT', 'entry': 105.30, 'shares': 94.95},
                {'ticker': 'PYPL', 'entry': 57.50, 'shares': 173.94},
                {'ticker': 'MO', 'entry': 57.38, 'shares': 174.27}
            ]
        }
    }
    
    # Load existing data or create new bot portfolios
    if os.path.exists(DATA_FILE):
        print("📂 Loading existing portfolio data...")
        with open(DATA_FILE, 'r') as f:
            saved = json.load(f)
            portfolios.update(saved)
    else:
        print("🆕 First run - initializing bot portfolios...")
        # Bots will be initialized with current prices below
        portfolios['conservative'] = None
        portfolios['moderate'] = None
        portfolios['aggressive'] = None
    
    return portfolios

def fetch_current_prices(tickers):
    """Fetch current closing prices for all stocks"""
    print(f"\n💰 Fetching closing prices for {len(tickers)} stocks...")
    prices = {}
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period='2d')  # Get last 2 days to ensure data
            if not hist.empty:
                price = round(hist['Close'].iloc[-1], 2)
                prices[ticker] = price
                print(f"  ✓ {ticker}: ${price}")
            else:
                print(f"  ✗ {ticker}: No data available")
                prices[ticker] = None
        except Exception as e:
            print(f"  ✗ {ticker}: Error - {str(e)}")
            prices[ticker] = None
    
    return prices

def initialize_bot_portfolio(bot_name, sell_threshold, current_prices):
    """Initialize a bot portfolio with current market prices"""
    bot_tickers = ['AVGO', 'PM', 'JPM', 'WFC', 'NVDA', 'COP', 'PFE', 'TGT', 'MO', 'BAC']
    holdings = []
    
    for ticker in bot_tickers:
        price = current_prices.get(ticker)
        if price and price > 0:
            shares = int(10000 / price)  # ~$10k per position
            holdings.append({
                'ticker': ticker,
                'entry': price,
                'shares': shares
            })
    
    emoji = '🐢' if 'conservative' in bot_name.lower() else '🏃' if 'moderate' in bot_name.lower() else '🚀'
    
    return {
        'name': bot_name,
        'emoji': emoji,
        'initial': 100000,
        'startDate': datetime.datetime.now().strftime('%Y-%m-%d'),
        'sellThreshold': sell_threshold,
        'strategy': f'Sell at {sell_threshold}%',
        'holdings': holdings,
        'trades': [],
        'wins': 0,
        'losses': 0,
        'resets': 0
    }

def calculate_portfolio_value(portfolio, current_prices):
    """Calculate current value of a portfolio"""
    total = 0
    for holding in portfolio['holdings']:
        price = current_prices.get(holding['ticker'], holding['entry'])
        if price:
            total += price * holding['shares']
    return total

def check_bot_trades(portfolios, current_prices):
    """Check if any bot should make autonomous trades"""
    alternatives = ['MSFT', 'AAPL', 'GOOGL', 'AMZN', 'META']
    trades_made = []
    
    for bot_key in ['conservative', 'moderate', 'aggressive']:
        if not portfolios[bot_key]:
            continue
            
        bot = portfolios[bot_key]
        
        for i, holding in enumerate(bot['holdings']):
            current_price = current_prices.get(holding['ticker'])
            if not current_price:
                continue
            
            change_percent = ((current_price - holding['entry']) / holding['entry']) * 100
            
            # Check if sell threshold hit
            if change_percent <= bot['sellThreshold']:
                sell_value = current_price * holding['shares']
                loss = sell_value - (holding['entry'] * holding['shares'])
                
                # Pick alternative with valid price
                import random
                valid_alts = [t for t in alternatives if current_prices.get(t)]
                if not valid_alts:
                    continue
                
                new_ticker = random.choice(valid_alts)
                new_price = current_prices[new_ticker]
                new_shares = int(sell_value / new_price)
                
                # Log trade
                trade = {
                    'date': datetime.datetime.now().isoformat(),
                    'dateString': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'action': 'AUTONOMOUS TRADE',
                    'soldTicker': holding['ticker'],
                    'soldPrice': round(current_price, 2),
                    'soldShares': holding['shares'],
                    'boughtTicker': new_ticker,
                    'boughtPrice': round(new_price, 2),
                    'boughtShares': new_shares,
                    'reason': f"{holding['ticker']} down {change_percent:.2f}% (trigger: {bot['sellThreshold']}%)",
                    'profitLoss': round(loss, 2)
                }
                
                bot['trades'].append(trade)
                trades_made.append((bot_key, trade))
                
                # Update holdings
                bot['holdings'][i] = {
                    'ticker': new_ticker,
                    'entry': new_price,
                    'shares': new_shares
                }
                
                # Update stats
                if loss >= 0:
                    bot['wins'] += 1
                else:
                    bot['losses'] += 1
                
                print(f"\n🤖 {bot['name']}: AUTONOMOUS TRADE!")
                print(f"   SOLD {trade['soldTicker']} ({trade['soldShares']} @ ${trade['soldPrice']})")
                print(f"   BOUGHT {trade['boughtTicker']} ({trade['boughtShares']} @ ${trade['boughtPrice']})")
                print(f"   Reason: {trade['reason']}")
                print(f"   P/L: ${trade['profitLoss']}")
                
                break  # One trade per bot per day
    
    return trades_made

def generate_html(portfolios, current_prices):
    """Generate beautiful HTML dashboard"""
    
    # Calculate all values
    values = {}
    for key in portfolios:
        if portfolios[key]:
            values[key] = calculate_portfolio_value(portfolios[key], current_prices)
    
    # Create standings
    standings = [
        {'key': k, 'name': portfolios[k]['emoji'] + ' ' + portfolios[k]['name'], 'value': v}
        for k, v in values.items()
    ]
    standings.sort(key=lambda x: x['value'], reverse=True)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏆 Portfolio Competition - Live Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{
            max-width: 1800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .subtitle {{ font-size: 1.2em; opacity: 0.9; margin-top: 5px; }}
        .update-badge {{
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 20px;
            margin-top: 15px;
            display: inline-block;
            font-size: 0.9em;
        }}
        .auto-badge {{
            background: #51cf66;
            color: white;
            padding: 8px 15px;
            border-radius: 15px;
            margin: 10px;
            display: inline-block;
            font-weight: bold;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
        }}
        .leaderboard {{
            background: #f8f9fa;
            padding: 30px;
        }}
        .leaderboard h2 {{
            text-align: center;
            color: #667eea;
            margin-bottom: 20px;
            font-size: 2em;
        }}
        .leader-row {{
            background: white;
            padding: 20px;
            margin: 10px 0;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .leader-row.first {{
            background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
            font-weight: bold;
            font-size: 1.1em;
        }}
        .rank {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
            width: 40px;
        }}
        .positive {{ color: #28a745; }}
        .negative {{ color: #dc3545; }}
        .bot-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            padding: 30px;
        }}
        .bot-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 3px solid #667eea;
        }}
        .bot-card.winning {{
            border-color: #51cf66;
            background: #f0fff4;
        }}
        .bot-header {{
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 15px;
            margin-bottom: 15px;
        }}
        .bot-title {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }}
        .bot-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .bot-stats {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }}
        .stat-row {{
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
            font-size: 0.95em;
        }}
        .trade-log {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            max-height: 250px;
            overflow-y: auto;
        }}
        .trade-entry {{
            background: white;
            padding: 10px;
            margin: 8px 0;
            border-radius: 5px;
            border-left: 4px solid #667eea;
            font-size: 0.85em;
        }}
        .footer {{
            background: #333;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        @media (max-width: 1200px) {{
            .bot-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 5-WAY PORTFOLIO COMPETITION</h1>
            <div class="subtitle">Autonomous AI Trading Lab • Real Market Data</div>
            <div class="auto-badge">🤖 FULLY AUTONOMOUS</div>
            <div class="update-badge">
                📊 Last Updated: {datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p EST')}
            </div>
            <p style="margin-top: 15px; font-size: 0.9em;">Updates automatically daily at 4:05 PM EST</p>
        </div>
        
        <div class="leaderboard">
            <h2>🏆 CURRENT STANDINGS</h2>
"""
    
    # Add leaderboard rows
    for idx, s in enumerate(standings):
        port = portfolios[s['key']]
        change = s['value'] - port['initial']
        change_pct = (change / port['initial']) * 100
        
        html += f"""
            <div class="leader-row {'first' if idx == 0 else ''}">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div class="rank">{idx + 1}.</div>
                    <div>{s['name']} {'🏆' if idx == 0 else ''}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.5em; font-weight: bold;">${s['value']:,.0f}</div>
                    <div class="{'positive' if change >= 0 else 'negative'}" style="font-size: 1.1em;">
                        {'+' if change >= 0 else ''}${change:,.0f} ({change_pct:+.2f}%)
                    </div>
                </div>
            </div>
"""
    
    html += """
        </div>
        
        <div class="bot-grid">
"""
    
    # Add portfolio cards
    for key in ['ceri', 'assisted', 'conservative', 'moderate', 'aggressive']:
        if not portfolios[key]:
            continue
            
        port = portfolios[key]
        value = values[key]
        change = value - port['initial']
        change_pct = (change / port['initial']) * 100
        is_winning = key == standings[0]['key']
        
        # Bot-specific stats
        if key in ['conservative', 'moderate', 'aggressive']:
            total_trades = len([t for t in port.get('trades', []) if t['action'] == 'AUTONOMOUS TRADE'])
            win_rate = (port['wins'] / total_trades * 100) if total_trades > 0 else 0
            
            stats_html = f"""
                <div class="bot-stats">
                    <div class="stat-row">
                        <span>Win Rate:</span>
                        <span><strong>{win_rate:.0f}% ({port['wins']}/{total_trades})</strong></span>
                    </div>
                    <div class="stat-row">
                        <span>Total Trades:</span>
                        <span><strong>{total_trades}</strong></span>
                    </div>
                    <div class="stat-row">
                        <span>Strategy:</span>
                        <span><strong>{port['strategy']}</strong></span>
                    </div>
                </div>
            """
            
            # Recent trades
            recent_trades = port.get('trades', [])[-5:][::-1]
            if recent_trades:
                trades_html = '<div class="trade-log"><div style="font-weight: bold; margin-bottom: 10px;">Recent Trades:</div>'
                for trade in recent_trades:
                    trades_html += f"""
                        <div class="trade-entry">
                            <div style="color: #6c757d; font-size: 0.85em;">{trade['dateString']}</div>
                            <div style="margin-top: 5px;"><strong>SOLD:</strong> {trade['soldTicker']} ({trade['soldShares']} @ ${trade['soldPrice']})</div>
                            <div><strong>BOUGHT:</strong> {trade['boughtTicker']} ({trade['boughtShares']} @ ${trade['boughtPrice']})</div>
                            <div style="margin-top: 5px; color: #6c757d;">{trade['reason']}</div>
                            <div class="{'positive' if trade['profitLoss'] >= 0 else 'negative'}" style="margin-top: 5px;">
                                P/L: {'+' if trade['profitLoss'] >= 0 else ''}${trade['profitLoss']}
                            </div>
                        </div>
                    """
                trades_html += '</div>'
            else:
                trades_html = '<div class="trade-log" style="text-align: center; color: #6c757d; padding: 20px;">No trades yet • Bot monitoring markets daily</div>'
        else:
            stats_html = f"""
                <div class="bot-stats">
                    <div class="stat-row">
                        <span>Started:</span>
                        <span><strong>{port['startDate']}</strong></span>
                    </div>
                    <div class="stat-row">
                        <span>Holdings:</span>
                        <span><strong>{len(port['holdings'])} stocks</strong></span>
                    </div>
                    <div class="stat-row">
                        <span>Strategy:</span>
                        <span><strong>{port['strategy']}</strong></span>
                    </div>
                </div>
            """
            trades_html = ''
        
        html += f"""
            <div class="bot-card {'winning' if is_winning else ''}">
                <div class="bot-header">
                    <div class="bot-title">{port['emoji']} {port['name']}</div>
                </div>
                <div class="bot-value">${value:,.0f}</div>
                <div style="font-size: 1.3em; font-weight: bold; margin-bottom: 15px;" class="{'positive' if change >= 0 else 'negative'}">
                    {'+' if change >= 0 else ''}${change:,.0f} ({change_pct:+.2f}%)
                </div>
                {stats_html}
                {trades_html}
            </div>
"""
    
    html += f"""
        </div>
        
        <div class="footer">
            <p><strong>🤖 Fully Autonomous Trading Lab</strong></p>
            <p style="margin-top: 10px;">Updates automatically daily at 4:05 PM EST via GitHub Actions</p>
            <p style="margin-top: 5px; font-size: 0.9em;">Competition started January 2026 • Ends January 2027</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

def main():
    """Main execution"""
    print("="*80)
    print("🤖 AUTONOMOUS PORTFOLIO TRACKER")
    print("="*80)
    print(f"⏰ Running at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}")
    print()
    
    # Load portfolios
    portfolios = initialize_portfolios()
    
    # Get all unique tickers
    all_tickers = set()
    for key, port in portfolios.items():
        if port and 'holdings' in port:
            for h in port['holdings']:
                all_tickers.add(h['ticker'])
    
    # Add alternatives
    all_tickers.update(['MSFT', 'AAPL', 'GOOGL', 'AMZN', 'META', 'PM', 'JPM', 'WFC', 'COP', 'PFE', 'BAC'])
    
    # Fetch current prices
    current_prices = fetch_current_prices(sorted(all_tickers))
    
    # Initialize bots on first run
    if not portfolios['conservative']:
        print("\n🤖 Initializing bot portfolios with current prices...")
        portfolios['conservative'] = initialize_bot_portfolio('Conservative Bot', -10, current_prices)
        portfolios['moderate'] = initialize_bot_portfolio('Moderate Bot', -7, current_prices)
        portfolios['aggressive'] = initialize_bot_portfolio('Aggressive Bot', -5, current_prices)
        print("✅ Bots initialized!")
    
    # Check for autonomous trades
    print("\n🔍 Checking bots for trading opportunities...")
    trades = check_bot_trades(portfolios, current_prices)
    
    if not trades:
        print("  ℹ️  No trades triggered today - all bots holding positions")
    
    # Save data
    print("\n💾 Saving portfolio data...")
    with open(DATA_FILE, 'w') as f:
        json.dump(portfolios, f, indent=2)
    print("✅ Data saved!")
    
    # Generate HTML
    print("\n🎨 Generating HTML dashboard...")
    html = generate_html(portfolios, current_prices)
    
    with open('index.html', 'w') as f:
        f.write(html)
    print("✅ Dashboard created: index.html")
    
    # Show summary
    print("\n" + "="*80)
    print("📊 PORTFOLIO SUMMARY")
    print("="*80)
    for key in ['ceri', 'assisted', 'conservative', 'moderate', 'aggressive']:
        if portfolios[key]:
            value = calculate_portfolio_value(portfolios[key], current_prices)
            change = value - portfolios[key]['initial']
            change_pct = (change / portfolios[key]['initial']) * 100
            print(f"{portfolios[key]['emoji']} {portfolios[key]['name']:20s} ${value:>10,.0f} ({change_pct:>+7.2f}%)")
    
    print("\n✅ Run complete! Dashboard updated at GitHub Pages URL")
    print("="*80)

if __name__ == '__main__':
    main()
