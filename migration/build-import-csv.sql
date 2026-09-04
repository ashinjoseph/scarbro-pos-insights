SET NOCOUNT ON;
WITH sold AS (SELECT DISTINCT ip.ProductID AS PID FROM Invoice_Product ip),
mig AS (SELECT p.PID FROM Product p WHERE p.AddedDate >= '2026-04-15'
        UNION SELECT p.PID FROM Product p JOIN sold s ON s.PID = p.PID),
base AS (
  SELECT
    p.PID,
    RTRIM(p.Barcode)                                        AS Barcode,
    LEFT(LTRIM(RTRIM(p.ProductName)), 40)                   AS PName,
    LEFT(COALESCE(NULLIF(LTRIM(RTRIM(p.Description)), ''),
                  LTRIM(RTRIM(p.ProductName))), 128)        AS PDesc,
    CAST(ISNULL(p.PurchaseCost, 0) AS decimal(12,2))        AS CostPrice,
    CAST(ISNULL(p.SalesCost, 0)    AS decimal(12,2))        AS NetPrice,
    CASE WHEN RTRIM(c.TaxApplicable) = 'No' THEN CAST(0 AS decimal(9,3))
         ELSE ISNULL(tm.Percentage, 0) END                  AS TaxPct,
    LEFT(LTRIM(RTRIM(p.Category)), 40)                      AS CatName
  FROM Product p
  JOIN mig m       ON m.PID = p.PID
  JOIN Category c  ON RTRIM(c.CategoryName) = RTRIM(p.Category)
  LEFT JOIN TaxMaster tm ON RTRIM(tm.TaxName) = RTRIM(c.TaxnameX)
)
SELECT
  '"' + REPLACE(PName, '"', '""') + '","'
      + REPLACE(PDesc, '"', '""') + '",'
  + CONVERT(varchar(20), CostPrice) + ','
  + CONVERT(varchar(20), CAST(ROUND(NetPrice * (1 + TaxPct / 100.0), 2) AS decimal(12,2))) + ','
  + CONVERT(varchar(20), CAST(TaxPct AS decimal(9,2))) + ',"'
  + REPLACE(CatName, '"', '""') + '"'
FROM base
ORDER BY CatName, PName;
