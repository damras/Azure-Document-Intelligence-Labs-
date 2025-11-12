# Azure Document Intelligence Service Setup Guide

This guide walks you through creating an Azure Document Intelligence resource in the Azure Portal. **Complete this setup before starting Lab 1.**

---

## 📋 Prerequisites

Before you begin, ensure you have:
- ✅ An active **Azure subscription**
- ✅ Appropriate permissions to create resources in Azure
- ✅ Access to the [Azure Portal](https://portal.azure.com)

---

## 🚀 Step-by-Step Setup Instructions

### Step 1: Navigate to Azure Document Intelligence

1. Go to the [Azure Portal](https://portal.azure.com)
2. In the search bar at the top, type: **"Document Intelligence"** or **"AI Foundry | Document Intelligence"**
3. Click on **"AI Foundry | Document Intelligence"** from the search results

### Step 2: Create New Document Intelligence Resource

1. Click the **"+ Create"** or **"Create Document Intelligence"** button
2. You'll see the "Create Document Intelligence" page with multiple tabs

---

## ⚙️ Configuration Settings

### Tab 1: Basics

Fill in the following details:

#### Project Details

| Field | Value | Description |
|-------|-------|-------------|
| **Subscription** | Select your subscription | Choose the Azure subscription you want to use |
| **Resource group** | Create new or select existing | Example: `user8-rg` |



#### Instance Details

| Field | Value | Description |
|-------|-------|-------------|
| **Region** | Select your region | Example: `Sweden Central` |
| **Name** | Enter a unique name | Example: `user8-di-001`,  |
| **Pricing tier** | Select pricing tier | **Standard S0** (recommended for production)<br>**Free F0** (good for testing, limited calls) |

**Pricing Tier Options:**
- **Free F0**: 500 pages per month (great for testing and learning)
- **Standard S0**: Pay-as-you-go ($1 per 1,000 pages for most models)

> **Note:** For this workshop, you can use either Free F0 (if available) or Standard S0. The Free tier is sufficient for all workshop exercises.

**Important Notes:**
- The **Name** must be globally unique across Azure
- Choose a **Region** close to your location for better performance
- You may see a notification about subscription registration for Cognitive Services - this is normal

#### Screenshot Reference:
```
┌─────────────────────────────────────────────────────┐
│ Project Details                                     │
│ Subscription: ME-MngEnvMCAP969215-sarmadraza-1     │
│ Resource group: (New) user8-rg                     │
│                                                     │
│ Instance Details                                    │
│ Region: Sweden Central                             │
│ Name: user8-di-001                                 │
│ Pricing tier: Standard S0                          │
└─────────────────────────────────────────────────────┘
```

### Tab 2: Network

Configure network security for your resource:

**Type:** (Choose one of the following options)

✅ **Recommended for Workshop: "All networks, including the internet, can access this resource"**
- Select this option for easy access during the workshop
- No additional configuration needed

**Other Options:**
- **Selected networks**: Configure specific network security (advanced)
- **Disabled**: Private endpoint only (advanced)

> **For Production:** Consider using "Selected networks" or "Disabled" with private endpoints for enhanced security.

#### Screenshot Reference:
```
┌─────────────────────────────────────────────────────┐
│ Network                                             │
│                                                     │
│ Type:                                              │
│ ◉ All networks, including the internet, can       │
│   access this resource.                            │
│                                                     │
│ ○ Selected networks, configure network security   │
│   for your Azure AI services resource.             │
│                                                     │
│ ○ Disabled, no networks can access this resource.  │
│   You could configure private endpoint             │
│   connections after resource creation.             │
└─────────────────────────────────────────────────────┘
```

### Tab 3: Identity

Configure managed identities for secure access to other Azure resources:

**System assigned managed identity**
- **Status**: Leave as **Off** (not required for this workshop)
- This feature is used for advanced scenarios where Document Intelligence needs to access other Azure resources

**User assigned managed identity**
- Leave empty (not required for this workshop)

> **What is Managed Identity?** It's a security feature that allows Azure services to authenticate to other services without storing credentials in code. Not needed for basic workshop scenarios.

#### Screenshot Reference:
```
┌─────────────────────────────────────────────────────┐
│ Identity                                            │
│                                                     │
│ System assigned managed identity                   │
│ Status: ◉ Off  ○ On                               │
│                                                     │
│ User assigned managed identity                      │
│ [No user assigned managed identities assigned]     │
└─────────────────────────────────────────────────────┘
```

### Tab 4: Tags (Optional)

Add tags to organize and track resources (optional but recommended):

**Example Tags:**

| Name | Value |
|------|-------|
| Environment | Workshop |
| Project | DocumentIntelligence |
| Owner | YourName |
| CostCenter | Training |

> **Why use tags?** Tags help you organize resources, track costs, and manage resources across teams. Useful for production environments.

### Tab 5: Review + create

1. Review all your settings
2. Azure will validate your configuration
3. If validation passes, click **"Create"** button
4. Wait for deployment to complete (usually 1-2 minutes)

---

## ✅ Deployment Complete

After successful deployment, you'll see:

```
✓ Your deployment is complete

Deployment name: FormRecognizerCreate-20251111203933
Subscription: ME-MngEnvMCAP969215-sarmadraza-1
Resource group: user8-rg
```

**Next Steps:** Click **"Go to resource"** button

---

## 🔑 Get Your Credentials

After deployment, you need to retrieve your **Endpoint** and **API Key** for the workshop:

### Step 1: Navigate to Your Resource

1. Click **"Go to resource"** from the deployment page, OR
2. Go to Azure Portal → Resource Groups → Your Resource Group → Your Document Intelligence resource

### Step 2: Get Endpoint and Keys

1. In the left sidebar, click **"Keys and Endpoint"**
2. You'll see:
   - **Endpoint**: A URL like `https://user8-di-001.cognitiveservices.azure.com/`
   - **KEY 1**: A long alphanumeric string
   - **KEY 2**: An alternative key (backup)

3. **Copy these values** - you'll need them for the workshop!

#### Screenshot Example:
```
┌─────────────────────────────────────────────────────┐
│ Keys and Endpoint                                   │
│                                                     │
│ Endpoint                                           │
│ https://user8-di-001.cognitiveservices.azure.com/ │
│ [Copy]                                             │
│                                                     │
│ KEY 1                                              │
│ a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6                  │
│ [Show] [Copy] [Regenerate]                        │
│                                                     │
│ KEY 2                                              │
│ z9y8x7w6v5u4t3s2r1q0p9o8n7m6l5k4                  │
│ [Show] [Copy] [Regenerate]                        │
└─────────────────────────────────────────────────────┘
```

### Step 3: Save Your Credentials

Create a `.env` file in the `Labs` folder with your credentials:

```env
AZ_DOCINT_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
AZ_DOCINT_KEY=your-api-key-here
```

**Replace:**
- `your-resource-name` with your actual resource name (e.g., `user8-di-001`)
- `your-api-key-here` with your KEY 1 value

> ⚠️ **Security Warning:** Never commit your `.env` file to Git! It contains sensitive credentials. The `.gitignore` file in this repository is already configured to exclude it.

---

## 📊 Verify Your Setup

To confirm everything is working:

1. ✅ Resource deployed successfully
2. ✅ Endpoint copied (starts with `https://` and ends with `.cognitiveservices.azure.com/`)
3. ✅ API Key copied (long alphanumeric string)
4. ✅ `.env` file created in the `Labs` folder with both values

---

## 💰 Cost Management

### Free Tier (F0)
- **500 pages per month** across all models
- Perfect for this workshop
- No charges unless you exceed the limit

### Standard Tier (S0)
- **Pay-as-you-go** pricing
- Approximately **$1-10 per 1,000 pages** depending on the model
- This workshop uses approximately **50-100 pages total** across all labs

**Estimated Workshop Cost (Standard S0):** Less than $1 USD

### Cost-Saving Tips
1. Use the **Free tier (F0)** if available in your region
2. Delete the resource after completing the workshop
3. Set up **cost alerts** in Azure Cost Management
4. Monitor usage in Azure Portal → Your Resource → Metrics

---

## 🧹 Cleanup (After Workshop)

When you're done with the workshop:

### Option 1: Delete the Resource (Recommended)
1. Go to Azure Portal
2. Navigate to your Document Intelligence resource
3. Click **"Delete"**
4. Confirm deletion
5. Type the resource name to confirm

### Option 2: Delete the Entire Resource Group
1. Go to Azure Portal → Resource Groups
2. Select your resource group (e.g., `user8-rg`)
3. Click **"Delete resource group"**
4. Type the resource group name to confirm
5. This deletes ALL resources in the group

> **Warning:** Deleting a resource is permanent and cannot be undone. Make sure you've saved any important data before deletion.

---

## ❓ Troubleshooting

### Issue: "Subscription not registered for Cognitive Services"

**Solution:**
1. Go to Azure Portal → Subscriptions → Your Subscription
2. Click "Resource providers" in the left menu
3. Search for `Microsoft.CognitiveServices`
4. Click "Register" if it shows "Not Registered"
5. Wait 2-3 minutes for registration to complete
6. Try creating the resource again

### Issue: "Resource name already exists"

**Solution:**
- Resource names must be globally unique
- Try adding numbers or your initials: `qnb-di-001`, `user123-docint`
- Use a different region if needed

### Issue: "Region not available"

**Solution:**
- Try a different region (Sweden Central, East US, West Europe are usually available)
- Check [Azure Products by Region](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/?products=cognitive-services) for availability

### Issue: "Free tier not available"

**Solution:**
- Free tier (F0) is limited to 1 resource per subscription
- If you already have a free Document Intelligence resource, delete it first, OR
- Use Standard S0 tier (costs are minimal for this workshop)

### Issue: "Quota exceeded"

**Solution:**
- Free tier: Wait until next month, OR upgrade to Standard S0
- Standard tier: Check your quota limits in Azure Portal

---

## 📚 Additional Resources

- [Azure Document Intelligence Documentation](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/)
- [Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
- [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio) - Visual testing tool
- [Azure Free Account](https://azure.microsoft.com/en-us/free/) - Get $200 credit for 30 days

---

## ✅ Ready to Start!

Once you have:
- ✅ Azure Document Intelligence resource created
- ✅ Endpoint and API Key copied
- ✅ `.env` file configured

You're ready to begin **[Lab 1 - Read API](lab-1-read/README.md)**!

---

**Questions or Issues?** Refer to the troubleshooting section above or consult the [official documentation](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/).

**Happy Learning! 🎉**
