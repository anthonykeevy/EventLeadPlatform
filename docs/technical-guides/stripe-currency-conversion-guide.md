# Stripe Currency Conversion Guide

**Author:** Dimitri 🔍 (Data Domain Architect)  
**Date:** October 13, 2025  
**Question:** "Will Stripe convert to local currency?"

---

## Quick Answer

**YES**, Stripe supports multi-currency payments and can handle currency conversion automatically. However, there are **two approaches** with different trade-offs:

1. **Presentment Currency** (Recommended for EventLead)
2. **Settlement Currency** (Stripe auto-converts)

---

## Approach 1: Presentment Currency (Recommended)

### How It Works:
- You charge customers in **their local currency** (AUD for AU, USD for US, GBP for UK)
- Stripe processes payment in **that currency**
- Stripe settles to your bank account in **your preferred currency** (e.g., AUD)

### Example Flow:
```
1. Australian customer → Invoice $99.00 AUD → Stripe charges $99.00 AUD
   → Stripe deposits $99.00 AUD to your AU bank account

2. US customer (future) → Invoice $75.00 USD → Stripe charges $75.00 USD
   → Stripe converts USD to AUD at daily rate (~$110 AUD)
   → Stripe deposits $110 AUD to your AU bank account
```

### Benefits:
- ✅ **Transparent pricing:** Customer sees price in their currency
- ✅ **No customer confusion:** US customer pays $75 USD (not $99 AUD converted)
- ✅ **Lower card fees:** Customer's bank doesn't charge foreign transaction fee (~3%)
- ✅ **Better conversion rates:** Customer experience is native currency

### Stripe Conversion Fee:
- **1% conversion fee** on top of Stripe's standard fees
- Example: US customer pays $75 USD → Stripe converts to ~$110 AUD → You receive $110 AUD minus 1% conversion fee (~$1.10) = **$108.90 AUD**

### Setup in Stripe:
```python
# Create Price in customer's currency
stripe.Price.create(
    product='prod_FormPublication',
    unit_amount=9900,  # $99.00
    currency='aud',  # Australian customer
)

stripe.Price.create(
    product='prod_FormPublication',
    unit_amount=7500,  # $75.00
    currency='usd',  # US customer (future)
)

# Create PaymentIntent in customer's currency
stripe.PaymentIntent.create(
    amount=9900,
    currency='aud',  # Matches customer's country
    customer=customer_id,
)
```

---

## Approach 2: Settlement Currency (Stripe Auto-Converts)

### How It Works:
- You charge customers in **one fixed currency** (e.g., AUD only)
- Customer's bank converts to their local currency at time of payment
- Stripe settles to your bank account in **AUD**

### Example Flow:
```
1. Australian customer → Invoice $99.00 AUD → Stripe charges $99.00 AUD
   → Stripe deposits $99.00 AUD to your AU bank account

2. US customer (future) → Invoice $99.00 AUD → Customer's bank converts AUD to USD (~$68 USD)
   → Customer pays ~$68 USD + 3% foreign transaction fee (~$2) = $70 USD charged
   → Stripe deposits $99.00 AUD to your AU bank account
```

### Benefits:
- ✅ **Simple setup:** One price, one currency (AUD)
- ✅ **Predictable revenue:** You always receive AUD

### Drawbacks:
- ❌ **Poor customer experience:** US customer sees "$99 AUD" which is confusing
- ❌ **Foreign transaction fees:** Customer's bank charges 2-3% extra fee
- ❌ **Abandoned carts:** Customers don't like seeing foreign currency prices
- ❌ **Competitive disadvantage:** Competitors show prices in local currency

---

## Recommendation for EventLead Platform

### **Use Presentment Currency (Approach 1)**

**Why:**
1. **Better customer experience:** US customers see "$75 USD" not "$99 AUD"
2. **Lower customer costs:** No foreign transaction fees (2-3% saving)
3. **Competitive advantage:** Match Eventbrite, Typeform (multi-currency pricing)
4. **Scalable:** Add new currencies easily (EUR, GBP, NZD)

**Implementation:**
```python
# backend/modules/payments/stripe_service.py

def get_price_for_country(country_code: str) -> dict:
    """
    Get form publication price in customer's local currency
    """
    pricing = {
        'AU': {'amount': 9900, 'currency': 'aud', 'display': '$99.00 AUD'},
        'US': {'amount': 7500, 'currency': 'usd', 'display': '$75.00 USD'},
        'GB': {'amount': 6500, 'currency': 'gbp', 'display': '£65.00 GBP'},
        'NZ': {'amount': 10500, 'currency': 'nzd', 'display': '$105.00 NZD'},
        # ... more countries
    }
    return pricing.get(country_code, pricing['AU'])  # Default to AUD


# Create PaymentIntent with customer's currency
def create_payment_intent(company_id: int, amount: int, currency: str):
    """Create Stripe PaymentIntent in customer's currency"""
    
    # Get company's country
    company = db.query(Company).join(CompanyBillingDetails).filter(
        Company.CompanyID == company_id
    ).first()
    
    country_code = company.billing_details.country  # 'AU', 'US', etc.
    pricing = get_price_for_country(country_code)
    
    # Create PaymentIntent in customer's currency
    intent = stripe.PaymentIntent.create(
        amount=pricing['amount'],
        currency=pricing['currency'],
        customer=company.stripe_customer_id,
        metadata={
            'company_id': company_id,
            'country': country_code,
        }
    )
    
    return intent
```

---

## Currency Conversion Details

### Stripe's Conversion Process:
1. **Daily exchange rates:** Stripe updates FX rates daily (based on interbank rates)
2. **Conversion fee:** 1% on top of standard Stripe fees
3. **Settlement:** Converted to your settlement currency (AUD)
4. **Payout timing:** 2-7 business days (depends on bank)

### Total Fees Example:
```
US customer pays $75.00 USD for form publication

Stripe standard fee (2.9% + 30¢):
  - $75.00 × 2.9% = $2.18
  - Fixed fee: $0.30
  - Total Stripe fee: $2.48 USD

Conversion (USD → AUD):
  - $75.00 USD × 1.47 exchange rate = $110.25 AUD
  - Conversion fee (1%): $110.25 × 1% = $1.10 AUD
  - Net after conversion: $109.15 AUD

Stripe standard fee (converted):
  - $2.48 USD × 1.47 = $3.65 AUD

You receive:
  - $110.25 AUD (gross)
  - Minus $3.65 AUD (Stripe fee)
  - Minus $1.10 AUD (conversion fee)
  - Net: $105.50 AUD

Effective fee: 4.3% (2.9% Stripe + 1% conversion + 0.4% rounding)
```

### Comparison to Fixed AUD Pricing:
```
If you charged $99 AUD to US customer (Approach 2):

Customer sees on their statement:
  - $99.00 AUD × 0.68 (bank rate) = $67.32 USD
  - Foreign transaction fee (3%): $2.02 USD
  - Total charged: $69.34 USD

Your revenue:
  - $99.00 AUD (gross)
  - Minus Stripe fee (2.9% + 30¢): $3.17 AUD
  - Net: $95.83 AUD

Effective fee: 3.2% (but customer paid extra 3% to their bank!)
```

**Conclusion:** Presentment currency costs you 1% more in fees, but customer saves 3% in foreign transaction fees = **better customer experience**.

---

## Implementation Checklist

### Phase 1: MVP (Australia Only)
- [x] Single currency (AUD)
- [x] Single price ($99 AUD)
- [x] No conversion needed

### Phase 2: Multi-Currency (Future)
- [ ] Add Country table (ISO codes, currency mappings)
- [ ] Define prices per currency (USD, GBP, EUR, NZD)
- [ ] Update payment flow to use customer's currency
- [ ] Enable Stripe multi-currency support (Dashboard → Settings → Payment methods)
- [ ] Test with Stripe test cards in different currencies

### Stripe Dashboard Setup:
1. Navigate to **Settings → Payment methods**
2. Enable **Multi-currency support**
3. Select **Settlement currency**: AUD (your bank account currency)
4. Add **Presentment currencies**: USD, GBP, EUR, NZD
5. Save changes

### Code Changes:
```python
# 1. Add currency to CompanyBillingDetails
class CompanyBillingDetails(Base):
    company_id = Column(BigInteger, primary_key=True)
    country = Column(String(2), ForeignKey('Country.CountryCode'))  # FK to Country table
    currency = Column(String(3), nullable=False)  # AUD, USD, GBP (from Country table)
    
    # Relationship
    country_details = relationship('Country')


# 2. Payment service uses customer's currency
class PaymentService:
    def create_payment_for_form_publication(self, company_id: int):
        company = self.db.query(Company).filter(
            Company.CompanyID == company_id
        ).first()
        
        # Get pricing for customer's country
        pricing = self.get_pricing(company.billing_details.country)
        
        # Create Stripe PaymentIntent in customer's currency
        intent = stripe.PaymentIntent.create(
            amount=pricing['amount'],
            currency=pricing['currency'],
            customer=company.stripe_customer_id,
        )
        
        return intent


# 3. Invoice shows customer's currency
def generate_invoice_pdf(invoice: Invoice):
    billing = invoice.company.billing_details
    
    # Format amount in customer's currency
    if billing.currency == 'AUD':
        amount_display = f"${invoice.total:.2f} AUD"
    elif billing.currency == 'USD':
        amount_display = f"${invoice.total:.2f} USD"
    elif billing.currency == 'GBP':
        amount_display = f"£{invoice.total:.2f} GBP"
    # ... etc
    
    return generate_pdf(amount_display, billing)
```

---

## Pricing Strategy Recommendations

### Option A: Maintain Price Parity (Recommended for MVP)
Convert $99 AUD to equivalent in other currencies:
- **AU:** $99 AUD
- **US:** $75 USD (99 AUD × 0.68 + rounding)
- **UK:** £65 GBP (99 AUD × 0.55 + rounding)
- **NZ:** $105 NZD (99 AUD × 1.06 + rounding)

**Benefit:** Fair pricing, maintains margins across countries

### Option B: Market-Based Pricing
Set prices based on market willingness to pay (not just FX conversion):
- **AU:** $99 AUD (baseline)
- **US:** $79 USD (higher than parity - US market can pay more)
- **UK:** £59 GBP (competitive with UK SaaS pricing)
- **NZ:** $99 NZD (lower than parity - smaller market)

**Benefit:** Optimize revenue per market, competitive positioning

### Recommendation:
Start with **Option A** (price parity) for simplicity. Monitor conversion rates, adjust to **Option B** (market-based) in Year 2.

---

## Key Takeaways

✅ **Stripe DOES support multi-currency** (presentment currency)  
✅ **Currency aligns with Country** (Country table has CurrencyCode field)  
✅ **Stripe converts to AUD** (your settlement currency)  
✅ **1% conversion fee** (small cost for better customer experience)  
✅ **MVP: AUD only** (no conversion needed yet)  
✅ **Future: Add currencies** when entering new markets (USD, GBP, EUR, NZD)

### Stripe Documentation:
- Multi-currency: https://stripe.com/docs/currencies
- Presentment currency: https://stripe.com/docs/currencies/presentment-currencies
- Conversion rates: https://stripe.com/docs/currencies/conversions

---

**Ready to implement?** Let me know if you have questions about Stripe setup!

---

*Dimitri - Data Domain Architect* 🔍  
*"Currency is just another domain - design it right once"*

