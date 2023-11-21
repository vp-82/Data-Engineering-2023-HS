CREATE OR REPLACE TABLE `adventureworks.dwh_product_with_reviews` AS
WITH
  -- CTE for joined product details
  product_details AS (
    SELECT
      p.productid,
      p.name AS product_name,
      p.productnumber,
      p.makeflag,
      p.finishedgoodsflag,
      p.color,
      p.safetystocklevel,
      p.reorderpoint,
      p.standardcost,
      p.listprice,
      p.size,
      p.sizeunitmeasurecode,
      p.weightunitmeasurecode,
      p.weight,
      p.daystomanufacture,
      p.productline,
      p.class,
      p.style,
      p.productsubcategoryid,
      p.productmodelid,
      p.sellstartdate,
      p.sellenddate,
      p.discontinueddate,
      sc.name AS subcategory_name,
      c.name AS category_name
    FROM
      `adventureworks.product` p
    LEFT JOIN `adventureworks.productsubcategory` sc ON p.productsubcategoryid = sc.productsubcategoryid
    LEFT JOIN `adventureworks.productcategory` c ON sc.productcategoryid = c.productcategoryid
  ),
  -- CTE for aggregated product reviews
  product_reviews AS (
    SELECT
      productid,
      ARRAY_AGG(STRUCT(productreviewid, reviewername, reviewdate, emailaddress, rating, comments)) AS reviews
    FROM
      `adventureworks.productreview`
    GROUP BY
      productid
  )
-- Final SELECT with join of CTEs
SELECT
  pd.*,
  pr.reviews
FROM
  product_details pd
LEFT JOIN product_reviews pr ON pd.productid = pr.productid;
