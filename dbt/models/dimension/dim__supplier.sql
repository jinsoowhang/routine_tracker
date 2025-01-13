{{ config(materialized='table') }}

WITH dining_out AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%7-eleven%' THEN '7-Eleven'
			WHEN LOWER(supplier) LIKE '%85c bakery%' THEN '85C Bakery Cafe'
			WHEN LOWER(supplier) LIKE '%angelos burgers%' THEN 'Angelos Burgers'
			WHEN LOWER(supplier) LIKE '%boudin sf%' THEN 'Boudin SF'
			WHEN LOWER(supplier) LIKE '%cava%' THEN 'Cava'
			WHEN LOWER(supplier) LIKE '%chick-fil-a%' OR LOWER(supplier) LIKE '%chick fil a%' THEN 'Chick-fil-A'
			WHEN LOWER(supplier) LIKE '%chipotle%' THEN 'Chipotle'
			WHEN LOWER(supplier) LIKE '%daveshotchicken%' OR LOWER(supplier) LIKE '%daves hot%' THEN 'Daves Hot Chicken'
			WHEN LOWER(supplier) LIKE '%denny%' THEN 'Dennys'
			WHEN LOWER(supplier) LIKE '%el pollo loco%' THEN 'El Pollo Loco'
			WHEN LOWER(supplier) LIKE '%mcdonald%' THEN 'McDonalds'
			WHEN LOWER(supplier) LIKE '%panda express%' THEN 'Panda Express'
			WHEN LOWER(supplier) LIKE '%sees candy%' OR LOWER(supplier) LIKE '%seecandy%' THEN 'Sees Candy'
			WHEN LOWER(supplier) LIKE '%starbucks%' THEN 'Starbucks'
			WHEN LOWER(supplier) LIKE '%subway%' THEN 'Subway'
		ELSE NULL END AS parent_supplier,
		'Dining Out' AS spend_category
	FROM {{ ref('stg__finance') }}
),

entertainment AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%amc%' THEN 'AMC'
			WHEN LOWER(supplier) LIKE '%crypto.com%' THEN 'Crypto.com'
			WHEN LOWER(supplier) LIKE '%indian wells%' THEN 'Indian Wells' 
			WHEN LOWER(supplier) LIKE '%oc fair%' THEN 'OC Fair'
			WHEN LOWER(supplier) LIKE '%stubhub%' THEN 'Stubhub'
		ELSE NULL END AS parent_supplier,
		'Entertainment' AS spend_category
	FROM {{ ref('stg__finance') }}
),

gifts_donations AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%home church%' THEN 'Home Church'
		ELSE NULL END AS parent_supplier,
		'Gifts and Donations' AS spend_category
	FROM {{ ref('stg__finance') }}
),

grocery AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%costco%' AND LOWER(supplier) NOT LIKE '%costcosta%' THEN 'Costco'
			WHEN LOWER(supplier) LIKE '%northgate market%' THEN 'Northgate Market'
			WHEN LOWER(supplier) LIKE '%stater bros%' OR LOWER(supplier) LIKE '%staterbros%' THEN 'Stater Bros'
			WHEN LOWER(supplier) LIKE '%target%' THEN 'Target'
			WHEN LOWER(supplier) LIKE '%trader joe%' THEN 'Trader Joes'
			WHEN LOWER(supplier) LIKE '%walmart%' OR LOWER(supplier) LIKE '%wal-mart%' THEN ''
		ELSE NULL END AS parent_supplier,
		'Grocery' AS spend_category
	FROM {{ ref('stg__finance') }}
),

health_wellness AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%24 hour fitness%' THEN '24 Hour Fitness'
			WHEN LOWER(supplier) LIKE '%classpass%' THEN 'ClassPass'
			WHEN LOWER(supplier) LIKE '%cvs%' THEN 'CVS Pharmacy'
			WHEN LOWER(supplier) LIKE '%kaiser%' THEN 'Kaiser Permanente'
			WHEN LOWER(supplier) LIKE '%hospital%' THEN 'Others - Hospital'
			WHEN LOWER(supplier) LIKE '%pharmacy%' THEN 'Others - Pharmacy'
			WHEN LOWER(supplier) LIKE '%walgreens%' THEN 'Walgreens'
		ELSE NULL END AS parent_supplier,
		'Health and Wellness' AS spend_category
	FROM {{ ref('stg__finance') }}
),

home AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%home depot%' THEN 'Home Depot'
		ELSE NULL END AS parent_supplier,
		'Home' AS spend_category
	FROM {{ ref('stg__finance') }}
),

insurance AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%geico%' THEN 'Geico'
		ELSE NULL END AS parent_supplier,
		'Insurance' AS spend_category
	FROM {{ ref('stg__finance') }}
),

payments AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%payment%' THEN 'Payment'
			WHEN LOWER(supplier) LIKE '%purchase interest%' THEN 'Purchase Interest'
		ELSE NULL END AS parent_supplier,
		'Payments' AS spend_category
	FROM {{ ref('stg__finance') }}
),

rent_mortgage AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%hoa fees%' THEN 'HOA Fees'
		ELSE NULL END AS parent_supplier,
		'Rent and Mortgage' AS spend_category
	FROM {{ ref('stg__finance') }}
),

shopping AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%99-cents-only%' THEN '99 Cents Only'
			WHEN LOWER(supplier) LIKE '%amzn%' OR LOWER(supplier) LIKE '%amazon%' THEN 'Amazon'
			WHEN LOWER(supplier) LIKE '%bloomingdales%' THEN 'Bloomingdales'
			WHEN LOWER(supplier) LIKE '%ebay%' THEN 'eBay'
			WHEN LOWER(supplier) LIKE '%forever 21%' THEN 'Forever 21'
			WHEN LOWER(supplier) LIKE '%ross%' THEN 'Ross Stores'
		ELSE NULL END AS parent_supplier,
		'Shopping' AS spend_category
	FROM {{ ref('stg__finance') }}
),

subscriptions AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%aaa%' THEN 'AAA'
			WHEN LOWER(supplier) LIKE '%annual fee%' THEN 'Annual Fee'
			WHEN LOWER(supplier) LIKE '%annual membership fee%' THEN 'Annual Membership Fee'
			WHEN LOWER(supplier) LIKE '%dmv%' THEN 'DMV'
		ELSE NULL END AS parent_supplier,
		'Subscriptions' AS spend_category
	FROM {{ ref('stg__finance') }}
),

transportation AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%arco%' THEN 'Arco'
			WHEN LOWER(supplier) LIKE '%circle k%' THEN 'Circle K'
			WHEN LOWER(supplier) LIKE '%clipper services%' OR LOWER(supplier) LIKE '%clipper systems%' THEN 'Clipper'
			WHEN LOWER(supplier) LIKE '%express lanes%' THEN 'Express Lanes'
			WHEN LOWER(supplier) LIKE '%lyft%' THEN 'Lyft'
			WHEN LOWER(supplier) LIKE '%uber%' THEN 'Uber'
		ELSE NULL END AS parent_supplier,
		'Transportation' AS spend_category
	FROM {{ ref('stg__finance') }}
),

travel AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%jetblue%' THEN 'Jet Blue'
			WHEN LOWER(supplier) LIKE '%john wayne airport%' THEN 'John Wayne Airport'
			WHEN LOWER(supplier) LIKE '%marriott%' THEN 'Marriott Hotel'
			WHEN LOWER(supplier) LIKE '%southwes%' THEN 'Southwest Airlines'
		ELSE NULL END AS parent_supplier,
		'Travel' AS spend_category
	FROM {{ ref('stg__finance') }}
),

-- utilities AS (
-- 	SELECT DISTINCT
-- 		supplier,
-- 		CASE
-- 			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
-- 			WHEN LOWER(supplier) LIKE '%%' THEN ''
-- 		ELSE NULL END AS parent_supplier,
-- 		'' AS spend_category
-- FROM public.stg__finance
-- )

results AS (
	SELECT * FROM dining_out WHERE parent_supplier IS NOT NULL
	UNION 
	SELECT * FROM entertainment WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM gifts_donations WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM grocery WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM health_wellness WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM home WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM insurance WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM payments WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM rent_mortgage WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM shopping WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM subscriptions WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM transportation WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM travel WHERE parent_supplier IS NOT NULL
)

SELECT *
FROM results