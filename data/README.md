# Data Directory

## How to Get the Dataset

### Option 1: Download from Kaggle (Recommended)

1. **Visit Kaggle Dataset**
   - Go to: https://www.kaggle.com/mlg-ulb/creditcardfraud
   - Sign in (create free account if needed)

2. **Download the File**
   - Click "Download" button
   - This downloads `creditcard.zip` (~65 MB)

3. **Extract to This Directory**
   ```bash
   unzip creditcard.zip -d .
   ```
   - This creates `creditcard.csv` (143 MB) in this folder

### Option 2: Use Kaggle API

```bash
# Install Kaggle CLI
pip install kaggle

# Set up API credentials (see Kaggle account settings)
# Create ~/.kaggle/kaggle.json with your API token

# Download dataset
kaggle datasets download -d mlg-ulb/creditcardfraud

# Extract
unzip creditcardfraud.zip
```

### Option 3: Using Python

```python
# Install kaggle-api
pip install kaggle

# Download in Python
import kaggle
kaggle.api.dataset_download_files('mlg-ulb/creditcardfraud', unzip=True)
```

---

## Dataset Information

**File:** `creditcard.csv`
**Size:** ~143 MB
**Format:** CSV with headers

**Columns:**
- `Time` (int): Seconds elapsed from first transaction
- `V1-V28` (float): PCA-transformed features (confidential)
- `Amount` (float): Transaction amount in EUR
- `Class` (int): 0 = Legitimate, 1 = Fraudulent

**Statistics:**
- **Rows:** 284,807 transactions
- **Fraud Rate:** 0.172% (492 fraudulent)
- **Time Period:** 2 days (September 2013)
- **Currency:** EUR (€)

---

## Verification

Once downloaded, verify the file:

```python
import pandas as pd

df = pd.read_csv('creditcard.csv')
print(df.shape)  # Should print (284807, 31)
print(df.isnull().sum().sum())  # Should print 0
print(df['Class'].value_counts())  # Should show 284315 legitimate, 492 fraudulent
```

---

## Directory Structure After Download

```
data/
├── creditcard.csv         (143 MB - main dataset)
└── README.md             (this file)
```

---

## Notes

- ⚠️ **Privacy:** Features are PCA-transformed to protect sensitive information
- ✅ **No Missing Data:** The dataset is clean with no missing values
- 📊 **Imbalanced:** Heavy class imbalance (0.17% fraud) - use stratified sampling
- 📅 **Time Range:** Only 2 days - not suitable for temporal analysis alone

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| File too large for download | Use command line or kaggle-api |
| Kaggle auth error | Verify `~/.kaggle/kaggle.json` exists |
| CSV won't open | File is 143 MB - use pandas, not Excel |
| Different file size | Confirm you downloaded `.zip` not other files |

---

**Last Updated:** March 2026
