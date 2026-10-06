# Tableau Public Dashboard Implementation Guide
## Executive Sales & Financial Performance Dashboard

This guide walks you step-by-step through building, styling, and publishing the **Executive Sales & Financial Performance Dashboard** in **Tableau Desktop** or **Tableau Public** (100% free tool).

---

## 1. Connecting Data Source in Tableau

1. Launch **Tableau Desktop** or **Tableau Public** (downloadable free from [public.tableau.com](https://public.tableau.com)).
2. Under **Connect** &rarr; **To a File**, select **Text File**.
3. Navigate to this repository and select:
   ```
   data/sales_financial_dataset.csv
   ```
4. Verify the data preview pane:
   - Ensure `Order Date` and `Ship Date` are recognized as **Date** data types (calendar icon).
   - Ensure `Sales`, `Profit`, `Cost`, `Target Sales` are recognized as **Number (decimal)**.
   - Ensure `Quantity`, `Year`, `Postal Code` are recognized appropriately.
5. Click on **Sheet 1** to open the Tableau visualization canvas.

---

## 2. Creating Key Calculated Fields

In the left Data pane, click the small down arrow next to the Search bar and select **Create Calculated Field**. Create the following 4 formulas:

### A. Profit Margin %
* **Field Name:** `Profit Margin %`
* **Formula:**
  ```tableau
  SUM([Profit]) / SUM([Sales])
  ```
* **Format:** Right-click the newly created field in the Data pane &rarr; **Default Properties** &rarr; **Number Format** &rarr; **Percentage** (1 decimal place).

### B. Profit Status (Conditional Color Logic)
* **Field Name:** `Profit Status`
* **Formula:**
  ```tableau
  IF SUM([Profit]) >= 0 THEN "Profitable" ELSE "Unprofitable" END
  ```

### C. Target Sales Variance %
* **Field Name:** `Target Variance %`
* **Formula:**
  ```tableau
  (SUM([Sales]) - SUM([Target Sales])) / SUM([Target Sales])
  ```
* **Format:** Set default number format to **Percentage** with `+` and `-` prefix formatting.

### D. Regional Fixed LOD Benchmark
* **Field Name:** `Region Sales Benchmark (LOD)`
* **Formula:**
  ```tableau
  { FIXED [Region] : SUM([Sales]) }
  ```
* **Purpose:** Computes the total region sales regardless of sub-category filtering, allowing percentage-of-region comparisons.

---

## 3. Building Individual Worksheets

### Worksheet 1: `KPI_Scorecards` (BANs)
1. Drag `Measure Values` to the **Text** card on the Marks shelf.
2. In the `Measure Values` shelf, keep only: `SUM(Sales)`, `SUM(Profit)`, `[Profit Margin %]`, and `CNTD(Order ID)`.
3. Drag `Measure Names` to **Columns**.
4. Change view from *Standard* to *Fit Width*.
5. Format fonts: Size 20pt Bold for numbers, 10pt Semi-Bold for titles.

### Worksheet 2: `Monthly_Sales_Profit_Trend` (Dual-Axis Time-Series)
1. Drag `Order Date` to **Columns** &rarr; Right-click and choose continuous **Month** (e.g., *May 2023*).
2. Drag `Sales` to **Rows**.
3. Drag `Profit` to **Rows** (right next to `Sales`).
4. Right-click the second pill `SUM(Profit)` on the Rows shelf &rarr; select **Dual Axis**.
5. Right-click the right-hand profit axis &rarr; select **Synchronize Axis** (or leave independent with clear color labeling).
6. On the **Marks Shelf**:
   - For `SUM(Sales)`: Set mark type to **Line** &rarr; Color: Royal Blue (`#2563EB`) &rarr; Size: Medium.
   - For `SUM(Profit)`: Set mark type to **Bar** or **Line** &rarr; Color: Emerald Green (`#10B981`) &rarr; Opacity: 60%.

### Worksheet 3: `Regional_Performance` (Bar & Margin Breakdown)
1. Drag `Region` to **Columns**.
2. Drag `Sales` to **Rows**.
3. Sort `Region` descending by `SUM(Sales)`.
4. Drag `[Profit Margin %]` to the **Color** mark.
5. Set palette to Diverging (Red-Green or Orange-Blue) centered at 0.10 (10% target).
6. Enable Mark Labels &rarr; Show Mark Labels.

### Worksheet 4: `SubCategory_Profit_Matrix` (Profitability Ranking)
1. Drag `Sub-Category` to **Rows**.
2. Drag `Profit` to **Columns**.
3. Sort descending by `SUM(Profit)`.
4. Drag `[Profit Status]` to **Color** card:
   - Profitable: Emerald Green (`#10B981`)
   - Unprofitable: Crimson Red (`#EF4444`)
5. Add a reference line on the X-axis at constant value `0` (Dark Gray dashed line).

### Worksheet 5: `Customer_Segment_Share` (Donut / Pie)
1. Change Mark type to **Pie**.
2. Drag `Segment` to **Color**.
3. Drag `Sales` to **Angle** and **Size**.
4. Drag `Segment` and `Sales` (Quick Table Calculation &rarr; *Percent of Total*) to **Label**.
5. *(Optional Donut Center):* Create a dual-axis with a dummy calculated field `MIN(1)`, color the second mark white, and display total sales in the donut hole.

---

## 4. Assembling the Executive Dashboard

1. Click the **New Dashboard** icon at the bottom.
2. Under **Size** (left panel), change from *Fixed* to **Automatic** (or 1440 x 900 px widescreen).
3. Drag a **Vertical Layout Container** onto the canvas.
4. **Header Zone:**
   - Add a **Text Object** at the top:
     - Title: `Executive Sales & Financial Performance Dashboard` (20pt Bold, Dark Navy `#0F172A`).
     - Subtitle: `Data Analyst Internship Task 4 | Interactive Business Analytics` (10pt Muted `#64748B`).
5. **Filters & Slicers Zone:**
   - Place a horizontal layout container directly below the header.
   - From any worksheet, right-click and enable Quick Filters for:
     - `Region` (Multiple values dropdown)
     - `Category` (Multiple values dropdown)
     - `Segment` (Multiple values dropdown)
     - `Order Date` (Relative date / Year slider)
   - Apply each filter to: **Apply to Worksheets** &rarr; **All Using This Data Source**.
6. **KPI Row:** Place `KPI_Scorecards` in a horizontal container.
7. **Charts Grid:**
   - Row 1: `Monthly_Sales_Profit_Trend` (spanning 65% width) and `Customer_Segment_Share` (spanning 35% width).
   - Row 2: `Regional_Performance` (spanning 50% width) and `SubCategory_Profit_Matrix` (spanning 50% width).

---

## 5. Adding Interactivity (Dashboard Actions)

1. In the top menu, go to **Dashboard** &rarr; **Actions...**
2. Click **Add Action** &rarr; **Filter...**
   - **Name:** `Filter by Region`
   - **Source Sheet:** `Regional_Performance`
   - **Run action on:** `Select`
   - **Target Sheets:** All other sheets.
   - **Clearing the selection will:** `Show all values`.
3. Now, clicking any region (e.g. "West") automatically cross-filters all time series, KPI cards, and sub-category charts!

---

## 6. Publishing to Tableau Public (Free Online Link)

1. In Tableau, navigate to **Server** &rarr; **Tableau Public** &rarr; **Save to Tableau Public As...**
2. Sign in with your free Tableau Public account (create one at [public.tableau.com](https://public.tableau.com) if you haven't yet).
3. Name your workbook:
   ```
   Executive Sales and Financial Performance Dashboard - Task 4
   ```
4. Once published, your browser will open the live interactive dashboard URL.
5. Copy this URL — you can paste it directly into your GitHub README and final internship submission link!

---
