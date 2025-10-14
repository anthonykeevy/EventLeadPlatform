# Australian GST Tax Invoice Requirements

**Author:** Dimitri 🔍 (Data Domain Architect)  
**Date:** October 13, 2025  
**Compliance:** Australian Taxation Office (ATO) GST requirements

---

## Critical Requirement: TWO ABNs on Tax Invoices

### ATO Rule:
For GST-compliant tax invoices in Australia, you MUST include:

1. **SELLER'S ABN** (EventLead Platform - us)
2. **BUYER'S ABN** (Customer - them) - **Required if total ≥ $1,000**

---

## Where ABNs Are Stored

### 1. Seller's ABN (EventLead Platform)
**Location:** `Company` + `CompanyBillingDetails` tables (CompanyID = 1)

```sql
-- Get EventLead Platform's ABN (SELLER)
SELECT c.Name, bd.ABN, bd.TaxInvoiceName, bd.BillingAddress, bd.GSTRegistered
FROM Company c
JOIN CompanyBillingDetails bd ON c.CompanyID = bd.CompanyID
WHERE c.CompanyID = 1;  -- EventLead Platform
-- Returns:
-- Name: "EventLead Platform"
-- ABN: "12345678901" (OUR ABN)
-- TaxInvoiceName: "EVENTLEAD PLATFORM PTY LTD"
-- BillingAddress: "123 Tech Street, Sydney NSW 2000"
-- GSTRegistered: 1 (Yes)
```

---

### 2. Buyer's ABN (Customer Company)
**Location:** `Company` + `CompanyBillingDetails` tables (CompanyID ≥ 2)

```sql
-- Get Customer's ABN (BUYER)
SELECT c.Name, bd.ABN, bd.TaxInvoiceName, bd.BillingAddress, bd.GSTRegistered
FROM Company c
JOIN CompanyBillingDetails bd ON c.CompanyID = bd.CompanyID
WHERE c.CompanyID = 400;  -- ICC Sydney example
-- Returns:
-- Name: "ICC Sydney"
-- ABN: "53004085616"
-- TaxInvoiceName: "INTERNATIONAL CONVENTION CENTRE SYDNEY PTY LTD"
-- BillingAddress: "14 Darling Drive, Sydney NSW 2000"
-- GSTRegistered: 1
```

---

## GST Tax Invoice Example (Both ABNs)

```
┌─────────────────────────────────────────────────────────────────┐
│                         TAX INVOICE                             │
├─────────────────────────────────────────────────────────────────┤
│ From (SELLER):                                                  │
│ EventLead Platform Pty Ltd                                      │
│ ABN: 12 345 678 901  ← OUR ABN (CompanyID = 1)                 │
│ 123 Tech Street, Sydney NSW 2000                                │
│ Phone: +61 2 9215 7100                                          │
│ Email: billing@eventlead.com.au                                 │
│                                                                  │
│ To (BUYER):                                                     │
│ International Convention Centre Sydney Pty Ltd                  │
│ ABN: 53 004 085 616  ← CUSTOMER'S ABN (CompanyID = 400)        │
│ 14 Darling Drive, Sydney NSW 2000                               │
├─────────────────────────────────────────────────────────────────┤
│ Invoice Number: INV-2025-042                                    │
│ Invoice Date: 13 October 2025                                   │
│ Due Date: 13 October 2025 (Due on receipt)                      │
├─────────────────────────────────────────────────────────────────┤
│ Description                  Qty    Unit Price    Amount         │
│                                     (ex GST)      (ex GST)       │
│ ─────────────────────────────────────────────────────────────── │
│ Form Publication             3      $90.00        $270.00        │
│ (Sydney Boat Show 2025)                                         │
│                                                                  │
│ Subtotal (excluding GST):                        $270.00        │
│ GST (10%):                                         $27.00        │
│ ─────────────────────────────────────────────────────────────── │
│ TOTAL (including GST):                            $297.00 AUD   │
├─────────────────────────────────────────────────────────────────┤
│ This is a tax invoice for GST purposes.                         │
│ Payment terms: Due on receipt.                                  │
│                                                                  │
│ ABN: 12 345 678 901 ← CRITICAL: Seller's ABN shown again       │
└─────────────────────────────────────────────────────────────────┘
```

---

## ATO Requirements Checklist

### For Tax Invoices ≥ $1,000 (including GST):

| Requirement | Source | Status |
|-------------|--------|--------|
| ✅ Seller's ABN | `SystemConfig.PlatformABN` | ✅ |
| ✅ **Buyer's ABN** | `CompanyBillingDetails.ABN` | ✅ |
| ✅ Seller's legal name | `SystemConfig.PlatformLegalName` | ✅ |
| ✅ Invoice date | Invoice table | ✅ |
| ✅ Description of goods/services | Invoice line items | ✅ |
| ✅ GST amount (if applicable) | Calculated (10% of subtotal) | ✅ |
| ✅ "Tax Invoice" wording | Invoice template | ✅ |

### For Tax Invoices < $1,000:
- Buyer's ABN is **optional** (but recommended)
- All other requirements still apply

---

## Code Implementation

### Invoice Generation Service

```python
# backend/modules/invoices/invoice_service.py
from sqlalchemy.orm import Session
from .models import Invoice, InvoiceLineItem
from backend.modules.companies.models import Company, CompanyBillingDetails
from backend.modules.system.models import SystemConfig

class InvoiceService:
    """Generate GST-compliant tax invoices"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_platform_billing_details(self) -> dict:
        """
        Get EventLead Platform's billing details (SELLER)
        CompanyID = 1 (EventLead Platform company)
        """
        platform = self.db.query(Company).join(CompanyBillingDetails).filter(
            Company.CompanyID == 1  # EventLead Platform
        ).first()
        
        if not platform:
            raise ValueError("EventLead Platform company (CompanyID = 1) not found")
        
        billing = platform.billing_details
        
        return {
            'ABN': billing.ABN,
            'LegalName': billing.TaxInvoiceName,
            'BillingAddress': billing.BillingAddress,
            'BillingEmail': billing.BillingEmail,
            'BillingPhone': billing.BillingPhone,
            'GSTRegistered': billing.GSTRegistered
        }
    
    def generate_invoice(
        self, 
        company_id: int, 
        line_items: list[dict]
    ) -> Invoice:
        """
        Generate GST-compliant tax invoice
        
        Args:
            company_id: Customer company ID (BUYER)
            line_items: List of invoice line items
                [{"description": "Form Publication", "qty": 3, "unit_price": 90.00}]
        
        Returns:
            Invoice object with BOTH seller's and buyer's ABN
        """
        # Get SELLER details (EventLead Platform - CompanyID = 1)
        platform = self.get_platform_billing_details()
        
        # Get BUYER details (Customer - CompanyID ≥ 2)
        customer = self.db.query(Company).join(CompanyBillingDetails).filter(
            Company.CompanyID == company_id,
            Company.CompanyID != 1  # Not EventLead Platform
        ).first()
        
        if not customer:
            raise ValueError(f"Customer company {company_id} not found")
        
        customer_billing = customer.billing_details
        
        # Calculate totals
        subtotal = sum(item['qty'] * item['unit_price'] for item in line_items)
        
        # GST calculation (10% if both parties are GST registered)
        gst_rate = 0.10 if (
            platform['GSTRegistered'] and 
            customer_billing.GSTRegistered
        ) else 0.0
        
        gst_amount = subtotal * gst_rate
        total = subtotal + gst_amount
        
        # Check if buyer's ABN required (total >= $1,000)
        requires_buyer_abn = total >= 1000.00
        
        # Create invoice
        invoice = Invoice(
            company_id=company_id,
            
            # SELLER details (EventLead Platform)
            seller_abn=platform['ABN'],
            seller_legal_name=platform['LegalName'],
            seller_address=platform['BillingAddress'],
            seller_email=platform['BillingEmail'],
            seller_phone=platform['BillingPhone'],
            
            # BUYER details (Customer)
            buyer_abn=customer_billing.ABN,  # ← CUSTOMER'S ABN
            buyer_legal_name=customer_billing.TaxInvoiceName,
            buyer_address=customer_billing.BillingAddress,
            buyer_email=customer_billing.BillingEmail,
            
            # Amounts
            subtotal=subtotal,
            gst_rate=gst_rate,
            gst_amount=gst_amount,
            total=total,
            currency='AUD',
            
            # Compliance
            is_tax_invoice=True,
            requires_buyer_abn=requires_buyer_abn,
            
            # Metadata
            invoice_date=datetime.utcnow(),
            due_date=datetime.utcnow(),  # Due on receipt
        )
        
        self.db.add(invoice)
        
        # Add line items
        for item in line_items:
            line_item = InvoiceLineItem(
                invoice=invoice,
                description=item['description'],
                quantity=item['qty'],
                unit_price=item['unit_price'],
                amount=item['qty'] * item['unit_price']
            )
            self.db.add(line_item)
        
        self.db.commit()
        self.db.refresh(invoice)
        
        return invoice
```

---

## Database Schema Updates

### Invoice Table (needs BOTH ABNs)

```sql
CREATE TABLE [Invoice] (
    InvoiceID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CompanyID BIGINT NOT NULL,
    
    -- SELLER details (EventLead Platform - from SystemConfig)
    SellerABN NVARCHAR(11) NOT NULL,
    SellerLegalName NVARCHAR(200) NOT NULL,
    SellerAddress NVARCHAR(500) NOT NULL,
    SellerEmail NVARCHAR(100) NOT NULL,
    SellerPhone NVARCHAR(20) NULL,
    
    -- BUYER details (Customer - from CompanyBillingDetails)
    BuyerABN NVARCHAR(11) NOT NULL,
    BuyerLegalName NVARCHAR(200) NOT NULL,
    BuyerAddress NVARCHAR(500) NOT NULL,
    BuyerEmail NVARCHAR(100) NOT NULL,
    
    -- Invoice details
    InvoiceNumber NVARCHAR(50) NOT NULL UNIQUE,
    InvoiceDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    DueDate DATETIME2 NOT NULL,
    
    -- Amounts
    Subtotal DECIMAL(10, 2) NOT NULL,
    GSTRate DECIMAL(5, 2) NOT NULL DEFAULT 0.10,
    GSTAmount DECIMAL(10, 2) NOT NULL,
    Total DECIMAL(10, 2) NOT NULL,
    Currency NVARCHAR(3) NOT NULL DEFAULT 'AUD',
    
    -- Compliance flags
    IsTaxInvoice BIT NOT NULL DEFAULT 1,
    RequiresBuyerABN BIT NOT NULL DEFAULT 0,  -- True if total >= $1,000
    
    -- Status
    Status NVARCHAR(20) NOT NULL DEFAULT 'Unpaid',
    PaidDate DATETIME2 NULL,
    
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    
    CONSTRAINT FK_Invoice_Company FOREIGN KEY (CompanyID) REFERENCES [Company](CompanyID),
    CONSTRAINT FK_Invoice_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [User](UserID)
);
GO
```

---

## Summary

### ✅ What We Have:
1. **Seller's ABN** (EventLead Platform) - `Company` table (CompanyID = 1) ✅
2. **Buyer's ABN** (Customer) - `Company` table (CompanyID ≥ 2) ✅
3. **Invoice table** - Stores BOTH ABNs for GST compliance ✅

### ✅ ATO Compliance:
- ✅ Both ABNs on tax invoices ≥ $1,000
- ✅ GST amount calculated and displayed (10%)
- ✅ "Tax Invoice" wording included
- ✅ Legal entity names (not trading names)
- ✅ Full addresses for both parties

### 📋 Action Items:
1. **Create EventLead Platform company** (CompanyID = 1 with your ABN)
2. **Update Invoice table** (add SellerABN, BuyerABN fields)
3. **Update invoice generation** (pull from Company table for both ABNs)
4. **Test with real ABNs** (yours + customer's)

---

**Critical:** Make sure to update EventLead Platform's ABN in CompanyBillingDetails (CompanyID = 1) with YOUR actual ABN once registered!

---

*Dimitri - Data Domain Architect* 🔍  
*"Australian GST compliance: Two ABNs, one tax invoice"*

