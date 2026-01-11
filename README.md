# 🤖 Autonomous Portfolio Competition Tracker

**Fully automated portfolio tracking system with 5 competing strategies:**
- 👤 **Your Buy & Hold Portfolio** (from TradingView)
- 💡 **AI-Assisted Portfolio** (Claude recommends, you approve)
- 🐢 **Conservative Bot** (-10% sell threshold)
- 🏃 **Moderate Bot** (-7% sell threshold)
- 🚀 **Aggressive Bot** (-5% sell threshold)

**Updates automatically daily at 4:05 PM EST via GitHub Actions!**

---

## 🚀 One-Time Setup (15 minutes)

### Step 1: Create GitHub Account
1. Go to https://github.com
2. Click "Sign up" (if you don't have an account)
3. Follow the signup process

### Step 2: Create New Repository
1. Click the **"+"** in top right → **"New repository"**
2. Name it: `portfolio-tracker`
3. Set to **Public** (required for free GitHub Pages)
4. ✅ Check "Add a README file"
5. Click **"Create repository"**

### Step 3: Upload Files
1. In your new repository, click **"Add file"** → **"Upload files"**
2. **Drag and drop ALL these files:**
   - `portfolio_tracker.py`
   - `requirements.txt`
   - `.github/workflows/update_portfolio.yml` (create folder structure first)
3. Click **"Commit changes"**

**Important:** The `.github/workflows/` folder structure must be exact!

### Step 4: Enable GitHub Actions
1. Go to **"Settings"** tab in your repository
2. Click **"Actions"** → **"General"** (left sidebar)
3. Under **"Workflow permissions"**, select:
   - ✅ **"Read and write permissions"**
4. Click **"Save"**

### Step 5: Enable GitHub Pages
1. Still in **"Settings"**, click **"Pages"** (left sidebar)
2. Under **"Source"**, select:
   - Branch: **main**
   - Folder: **/ (root)**
3. Click **"Save"**
4. **Your URL will appear!** (e.g., `https://yourusername.github.io/portfolio-tracker/`)
5. **Bookmark this URL!** 🔖

### Step 6: Run First Update Manually
1. Go to **"Actions"** tab
2. Click **"Update Portfolio Dashboard"** (left sidebar)
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait ~30 seconds for green checkmark ✅
5. Visit your GitHub Pages URL → Dashboard appears!

---

## ✅ That's It! Fully Automated!

### What Happens Now:
- **Every day at 4:05 PM EST:** GitHub Actions runs automatically
- **Fetches closing prices** from Yahoo Finance
- **Bots check thresholds** and trade autonomously if triggered
- **Updates your webpage** with latest portfolio values
- **You just visit the URL** anytime to see current standings!

### Your Workflow:
1. **Bookmark your GitHub Pages URL**
2. **Check it whenever you want** (daily, weekly, monthly)
3. **That's it!** Everything else is automatic

---

## 📊 Portfolio Details

### 👤 Your Buy & Hold Portfolio
**Strategy:** Hold until quarterly rebalance (April 9, 2026)

**Holdings (from TradingView):**
- AVGO: 28.86 shares @ $346.35
- NVDA: 53.8 shares @ $185.89
- WMT: 87 shares @ $114.94
- IBKR: 142.4 shares @ $70.21
- ORCL: 50.04 shares @ $199.78
- UNH: 28.93 shares @ $345.57
- NEM: 92.08 shares @ $108.58
- TGT: 94.95 shares @ $105.30
- PYPL: 173.94 shares @ $57.50
- MO: 174.27 shares @ $57.38

**Started:** January 3, 2026  
**Initial Value:** $100,000

### 💡 AI-Assisted Portfolio
**Strategy:** Claude makes recommendations, you approve changes

**Holdings:** Same as your portfolio initially  
**Started:** January 10, 2026  
**Initial Value:** $100,000

### 🐢 Conservative Bot
**Strategy:** Sell when stock drops -10% or more  
**Philosophy:** "Patience wins - give stocks room to breathe"  
**Expected Trades:** 1-3 per month  
**Initial Value:** $100,000

### 🏃 Moderate Bot
**Strategy:** Sell when stock drops -7% or more  
**Philosophy:** "Active management with discipline"  
**Expected Trades:** 3-6 per month  
**Initial Value:** $100,000

### 🚀 Aggressive Bot
**Strategy:** Sell when stock drops -5% or more  
**Philosophy:** "Quick exits, protect capital"  
**Expected Trades:** 8-15 per month  
**Initial Value:** $100,000

---

## 🔧 Troubleshooting

### Dashboard not updating?
1. Go to **Actions** tab
2. Check if workflow is running (green checkmark = success)
3. If red X → Click on it to see error
4. Usually means: GitHub Actions not enabled or permissions issue

### Can't see GitHub Pages?
1. Wait 2-3 minutes after first run
2. Make sure repository is **Public**
3. Check Settings → Pages is enabled

### Want to force an update NOW?
1. Go to **Actions** tab
2. Click **"Update Portfolio Dashboard"**
3. Click **"Run workflow"** → **"Run workflow"**
4. Refresh your dashboard URL after 30 seconds

---

## 🎯 Competition Goals

**After 12 months (January 2027), we'll know:**
- Did your buy-and-hold strategy beat the bots?
- Which bot strategy performed best?
- Did Conservative's patience win?
- Did Aggressive's quick exits win?
- Was Moderate the sweet spot?

**Success Criteria for Trusting AI with Real Money:**
- Bot survives 12 months without blowing up in last 6 months
- Win rate >65%
- Beats S&P 500
- Demonstrates consistent learning/improvement

---

## 📅 What This Tracks

**Every day at 4:05 PM EST, the system:**
1. ✅ Fetches closing prices for all stocks
2. ✅ Calculates current portfolio values
3. ✅ Checks if any bot should trade:
   - Conservative: Any stock down -10%+? → SELL & BUY alternative
   - Moderate: Any stock down -7%+? → SELL & BUY alternative
   - Aggressive: Any stock down -5%+? → SELL & BUY alternative
4. ✅ Logs all trades with timestamps
5. ✅ Updates beautiful HTML dashboard
6. ✅ Commits changes to GitHub
7. ✅ Your webpage updates automatically!

**You do:** Nothing! Just visit the URL to check standings.

---

## 🌐 Your Dashboard Features

**Leaderboard:**
- Current rankings (who's #1?)
- Portfolio values
- Gains/losses in $ and %

**Individual Portfolio Cards:**
- Current value
- Performance metrics
- For bots: Win rate, total trades, recent activity

**Trade History:**
- Every autonomous trade logged
- Date, time, stocks involved
- Reason for trade
- Profit/loss

**Fully Responsive:**
- Works on phone, tablet, desktop
- Beautiful design
- Real-time data (updates daily)

---

## 💡 Tips

### Check Your Dashboard:
- **Daily:** See if any bots traded today
- **Weekly:** Track performance trends
- **Monthly:** Compare strategies

### Bookmark These:
- 🌐 Your dashboard URL
- ⚙️ Your GitHub repository (to check Actions)

### Share Your Dashboard:
Your GitHub Pages URL is public! Share it with:
- Friends interested in AI trading
- Financial discussion groups
- Anyone who wants to follow the experiment

---

## 🎊 That's It!

**Set it up once → Runs automatically forever → Just watch the competition unfold!**

The bots are now learning from real market data, making autonomous decisions, and competing against your strategy!

Visit your dashboard URL anytime to see who's winning! 🏆

---

**Questions?** Check the Actions tab in your repository to see the automation running!
