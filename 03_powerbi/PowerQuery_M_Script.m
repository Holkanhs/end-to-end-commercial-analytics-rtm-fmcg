// =============================================================
// RTM Mexico FMCG — Power Query (M) script
//
// Star-schema load. Four CSV files (the dbt Gold marts) are loaded
// directly; no derivations in M. All business logic above the load —
// calculated columns, calculated tables, DAX measures — lives inside
// the .pbix as DAX (see Data_Dictionary.md sections 2–4).
//
// To use:
//   1. Paste each `let ... in ...` block into a new blank query
//      (Home > Transform data > New Source > Blank Query >
//       Advanced Editor).
//   2. Change `pDataFolder` to the absolute path of your data/ folder.
//   3. Refresh.
// =============================================================


// -------------------------------------------------------------
// 1) PARAMETER: data folder  (change once, reuse everywhere)
// -------------------------------------------------------------
// Query name: pDataFolder
let
    pDataFolder = "C:\path\to\DBT-MEXICO-FMCG-RTM-PROJECT\03_powerbi\data"
in
    pDataFolder


// -------------------------------------------------------------
// 2) FACT: fct_sales  (100,000 invoice lines)
// -------------------------------------------------------------
// Query name: fct_sales
let
    Source = Csv.Document(
        File.Contents(pDataFolder & "\fct_sales.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"customers_key",     type text},
        {"product_key",       type text},
        {"location_key",      type text},
        {"invoice_id",        Int64.Type},
        {"invoice_date",      type date},
        {"units",             Int64.Type},
        {"revenue",           type number},
        {"cost",              type number},
        {"margin",            type number},
        {"margin_pct",        type number},
        {"avg_ticket_price",  type number},
        {"profit_segment",    type text},
        {"payment_mode",      type text}
    })
in
    Typed


// -------------------------------------------------------------
// 3) DIM: dim_customers  (288 customer-profile rows)
// -------------------------------------------------------------
// Query name: dim_customers
let
    Source = Csv.Document(
        File.Contents(pDataFolder & "\dim_customers.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"customers_key",   type text},
        {"customer_age",    Int64.Type},
        {"customer_gender", type text},
        {"loyalty_status",  type text}
    })
in
    Typed


// -------------------------------------------------------------
// 4) DIM: dim_products  (64 brand × category rows)
// -------------------------------------------------------------
// Query name: dim_products
let
    Source = Csv.Document(
        File.Contents(pDataFolder & "\dim_products.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"product_key",     type text},
        {"brand",           type text},
        {"category",        type text},
        {"cost_price",      type number},
        {"selling_price",   type number},
        {"stock_on_hand",   Int64.Type},
        {"reorder_level",   Int64.Type},
        {"lead_time_days",  type number}
    })
in
    Typed


// -------------------------------------------------------------
// 5) DIM: dim_locations  (72 route rows)
// -------------------------------------------------------------
// Query name: dim_locations
let
    Source = Csv.Document(
        File.Contents(pDataFolder & "\dim_locations.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"location_key",  type text},
        {"city",          type text},
        {"channel",       type text},
        {"store_format",  type text}
    })
in
    Typed


// =============================================================
// AFTER LOADING — in Power BI Desktop:
//
// Relationships (set in Model view):
//   fct_sales[customers_key] --> dim_customers[customers_key]  (*:1)
//   fct_sales[product_key]   --> dim_products[product_key]     (*:1)
//   fct_sales[location_key]  --> dim_locations[location_key]   (*:1)
//   fct_sales[invoice_date]  --> Dim_Date[Date]                (*:1)
//
// Dim_Date is a DAX calculated table, NOT loaded from M.
// Create it with: CALENDAR(DATE(2024,1,1), DATE(2024,12,31))
// then add Year, Quarter, MonthNo, MonthName, YearMonth, DayOfWeek.
// Mark it as a Date Table (Modeling > Mark as date table > Date).
//
// Calculated columns and measures live in the .pbix —
// see Data_Dictionary.md sections 3 and 4.
// =============================================================
