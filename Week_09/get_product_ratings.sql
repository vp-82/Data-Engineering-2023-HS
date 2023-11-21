SELECT
  product_name,
  AVG(review.rating) as average_rating,
  MIN(review.rating) as min_rating,
  MAX(review.rating) as max_rating,
  COUNT(review.rating) as rating_count
FROM
  `adventureworks.dwh_product_with_reviews`,
  UNNEST(reviews) as review
GROUP BY
  product_name
ORDER BY
  average_rating DESC
LIMIT 10;

